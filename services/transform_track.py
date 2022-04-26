import cv2
from aiortc import MediaStreamTrack

from av.video import VideoFrame
from keras_preprocessing.image import img_to_array
import numpy as np

from .behaviors import load_face_haar_cascade, load_trained_model
from .constants import emotions

face_haar_cascade = load_face_haar_cascade()

model = load_trained_model()


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        # perform edge detection
        img = frame.to_ndarray(format="bgr24")
        #gray_image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        gray_image = np.dot(img[...,::-1], [0.299, 0.587, 0.114]).astype(np.uint8)
        # faces = face_haar_cascade.detectMultiScale(
        #     gray_image,
        #     #img,
        #     scaleFactor=1.3,
        #     minNeighbors=5,
        #     minSize=(30, 30),
        #     flags=cv2.CASCADE_SCALE_IMAGE
        # )
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     roi = gray_image[y:y + h, x:x + w]
        #     #roi = img[y:y + h, x:x + w]
        #     roi = cv2.resize(roi, (64, 64))
        #     roi = roi.astype("float") / 255.0
        #     roi = img_to_array(roi)
        #     roi = np.expand_dims(roi, axis=0)
        #
        #     prediction = model.predict(roi)[0]
        #     print(prediction(roi))
        #
        #     maxindex = int(np.argmax(prediction))
        #     print(maxindex)
        #     cv2.putText(img, emotions[maxindex], (int(x) + 10, int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        #                 (0, 0, 255), 2)

        # rebuild a VideoFrame, preserving timing information
        # new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame = VideoFrame.from_ndarray(gray_image, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame