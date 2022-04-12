from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip

from .utils import predict, gen
from .camera import VideoCamera

from asgiref.sync import async_to_sync

from transform_track import VideoTransformTrack


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


@async_to_sync
async def offer(request):
    rtc_session_description = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
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
                VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
            )

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle rtc_session_description
    await pc.setRemoteDescription(rtc_session_description)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(rtc_session_description)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


@csrf_exempt
@require_POST
def predict_image(request):
    image = request.FILES.get('image')
    result = predict(image)
    return HttpResponse(result, content_type='image/jpeg')
