import base64
from math import ceil

import cv2
import numpy as np
from keras.preprocessing.image import img_to_array

from .behaviors import load_trained_model, load_face_haar_cascade
from .constants import emotions

from dataclasses import dataclass

prediction = None


@dataclass(frozen=True)
class EmojiStatistic:
    angry: float
    disgusted: float
    fearful: float
    happy: float
    sad: float
    surprised: float
    neutral: float

    def __json__(self):
        return self.__dict__


def predict(image):
    # Import cascade file for facial recognition
    face_haar_cascade = load_face_haar_cascade()
    # Load pre-trained model
    model = load_trained_model()

    # Read image
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detec faces
    faces = face_haar_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    statistic = None

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = gray_image[y:y + h, x:x + w]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        # Predict the emotion
        prediction = model.predict(roi)[0]

        statistic = EmojiStatistic(
            angry=float(ceil(prediction[0] * 100) / 100),
            disgusted=float(ceil(prediction[1] * 100) / 100),
            fearful=float(ceil(prediction[2] * 100) / 100),
            happy=float(ceil(prediction[3] * 100) / 100),
            sad=float(ceil(prediction[4] * 100) / 100),
            surprised=float(ceil(prediction[5] * 100) / 100),
            neutral=float(ceil(prediction[6] * 100) / 100)
        )

        # Show result
        maxindex = int(np.argmax(prediction))
        cv2.putText(image, emotions[maxindex], (int(x) + 10, int(y) + 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255),
                    2)

    retval, buffer = cv2.imencode('.jpg', image)
    data = base64.b64encode(buffer.tobytes())
    data = data.decode()
    return data, statistic


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
