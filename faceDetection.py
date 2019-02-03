import face_recognition
import numpy as np
import cv2
import urllib
import io


def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image

def compareFaces(base_photo, target_photo):

    bse_image = face_recognition.load_image_file(base_photo)

    try:
        bse_encoding = face_recognition.face_encodings(bse_image)[0]
        tgt_encoding = face_recognition.face_encodings(url_to_image(target_photo))[0]
    except:
        return (-1)

    known_encodings = [bse_encoding]

    face_distances = face_recognition.face_distance(known_encodings, tgt_encoding)

    return face_distances[0]

