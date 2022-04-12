from django.urls import path

from .views import (
    home,
    image_process,
    stream_process,
    predict_image,
    predict_stream,

    test,
    offer
)

urlpatterns = [
    path('', home, name='home'),
    path('image/', image_process, name='image_process'),
    path('stream/', stream_process, name='stream_process'),
    path('image/predict/', predict_image, name='predict_image'),
    path('stream/predict/', predict_stream, name='predict_stream'),

    path('test/', test, name='test'),
    path('offer/', offer, name='offer'),
]
