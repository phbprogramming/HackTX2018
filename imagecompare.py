from skimage.measure import compare_ssim as ssim
import numpy as np
import cv2
import dhash
from PIL import Image
import urllib
import io
#import face

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compareImages(imageA, imageB):
    # compute the mean squared error and structural similarity
	# index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    return (m, s)

    print("MSE: " + str(m))
    print("SSIM: " + str(s))

# photo1 has to be local and photo2 has to be a link
def doComparison(photo1loc, photo2loc):
    original = cv2.imread(photo1loc)
    contrast = url_to_image(photo2loc)
    contrast = cv2.resize(contrast, (original.shape[1], original.shape[0]))

    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    MSE, SSIM = compareImages(original, contrast)

    image1 = Image.open(photo1loc)
    row1, col1 = dhash.dhash_row_col(image1)
    # print(dhash.format_hex(row1, col1))

    newfile = io.BytesIO(urllib.request.urlopen(photo2loc).read())

    image2 = Image.open(newfile)
    row2, col2 = dhash.dhash_row_col(image2)
    # print(dhash.format_hex(row2, col2))

    num_bits_different = dhash.get_num_bits_different(dhash.dhash_int(image1), dhash.dhash_int(image2))
    # print(num_bits_different)

    #faceCompare = face.beginImageRec(photo1loc, photo2loc)

    faceCompare = 0.3

    return (MSE, SSIM, num_bits_different, faceCompare)
