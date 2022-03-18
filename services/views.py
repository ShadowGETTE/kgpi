from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip

from .utils import predict, gen
from .camera import VideoCamera


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


@csrf_exempt
@require_POST
def predict_image(request):
	image = request.FILES.get('image')
	result = predict(image)
	return HttpResponse(result, content_type='image/jpeg')