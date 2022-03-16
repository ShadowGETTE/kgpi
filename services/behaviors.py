import cv2
from keras.models import model_from_json, load_model

from .constants import model_json_path, model_weights_path, cascade_xml_path


def load_trained_model():
	model = load_model('files/model.66.hdf5', compile=False)
	return model


def load_face_haar_cascade():
	return cv2.CascadeClassifier(cascade_xml_path)
