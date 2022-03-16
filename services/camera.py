import cv2
from keras.preprocessing.image import img_to_array
import numpy as np

from .behaviors import load_trained_model, load_face_haar_cascade
from .constants import emotions


# Import cascade file for facial recognition
face_haar_cascade = load_face_haar_cascade()
# Load pre-trained model
model = load_trained_model()

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.counter = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while True:
            success, image = self.video.read()
            if self.counter%30 == 0:

                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_haar_cascade.detectMultiScale(
                    gray_image,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30,30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    roi = gray_image[y:y+h, x:x+w]
                    roi = cv2.resize(roi, (64, 64))
                    roi = roi.astype("float") / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    # Predict the emotion
                    prediction = model.predict(roi)[0]

                    # Show result
                    maxindex = int(np.argmax(prediction))
                    cv2.putText(image, emotions[maxindex], (int(x)+10, int(y)-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                #image = cv2.flip(image, 1)
                ret, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()
            self.counter += 1