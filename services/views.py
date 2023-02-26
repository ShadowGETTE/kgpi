from aiortc import RTCSessionDescription, RTCPeerConnection, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaBlackhole, MediaRelay
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from ninja import NinjaAPI

from .transform_track import VideoTransformTrack
from .utils import predict, gen
from .camera import VideoCamera

import json

def wrapped_default(self, obj):
    return getattr(obj.__class__, '__json__', wrapped_default.default)(obj)
wrapped_default.default = json.JSONEncoder().default

json.JSONEncoder.original_default = json.JSONEncoder.default
json.JSONEncoder.default = wrapped_default


def home(request):
    return render(request, 'home.html')


def image_process(request):
    return render(request, 'image.html')


def stream_process(request):
    return render(request, 'stream.html')


@gzip.gzip_page
def predict_stream(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("aborted")


def test(request):
    return render(request, 'index.html')


pcs = set()
api = NinjaAPI()

@csrf_exempt
@api.post("offer/")
async def offer(request):
    json_data = json.loads(request.body)
    rtc_session_description = RTCSessionDescription(sdp=json_data['sdp'], type=json_data['type'])

    pc = RTCPeerConnection(
        configuration=RTCConfiguration(
            iceServers=[
                RTCIceServer(
                    urls='turn:135.181.237.91:3478?transport=udp'
                )
            ]
        )
    )

    pcs.add(pc)
    recorder = MediaBlackhole()

    relay = MediaRelay()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(relay.subscribe(track))
            )

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle rtc_session_description
    await pc.setRemoteDescription(rtc_session_description)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    # await pc.setRemoteDescription(rtc_session_description)
    await pc.setLocalDescription(answer)

    return JsonResponse({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})


@csrf_exempt
@require_POST
def predict_image(request):
    image = request.FILES.get('image')
    data, statistic = predict(image)
    response = {
        "image": data,
        "title": image.name,
        "statistic": statistic,
    }
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')
