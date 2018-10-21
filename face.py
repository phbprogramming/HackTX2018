import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import cognitive_face as CF
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from collections import OrderedDict


# # Replace <Subscription Key> with your valid subscription key.
subscription_key = "b7f4fdc9ebcb487097a805a095f31601"
assert subscription_key
# CF.Key.set(subscription_key)

# # You mus   t use the same region in your REST call as you used to get your
# # subscription keys. For example, if you got your subscription keys from
# # westus, replace "westcentralus" in the URI below with "westus".
# #
# # Free trial subscription keys are generated in the westcentralus region.
# # If you use a free trial subscription key, you shouldn't need to change
# # this region.
# face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
# CF.BaseUrl.set(face_api_url)

# # Set image_url to the URL of an image that you want to analyze.
# image_url = 'https://how-old.net/Images/faces2/main007.jpg'
# faces = CF.face.detect(image_url)
# print(faces)

# filepath = ___________INSERTVARHERE

def beginImageRec(filePath, imageToCheck){
    headers = {
        # Request headers
        'Content-Type': 'application/octet-steam',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # image_url = 'https://how-old.net/Images/faces2/main007.jpg'
    face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    # data = {'url': image_url}
    data = open(filePath).read()
    response = requests.post(face_api_url, params=params, headers=headers, octet-stream=data)
    face1 = response.json()
    # print(face1);
    #################

    # jdata = faces

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    # body = "{'url':'https://how-old.net/Images/faces2/main007.jpg'}"

    image_url = imageToCheck
    # image_url = 'https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?cs=srgb&dl=adult-attractive-beautiful-415829.jpg&fm=jpg'
    # face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    })
    data = {'url': image_url}
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    face2 = response.json()
    # print(face2);

    faceIdArray = []
    faceIdArray.append(face2[0]["faceId"])

    dataJ = {}
    dataJ['faceId'] = face1[0]["faceId"]
    dataJ['faceIds'] = faceIdArray
    dataJ['maxNumOfCandidatesReturned'] = 1000
    dataJ['mode'] = "matchFace"

    # dataTest = str.encode(json.dumps(dataJ))

    # print(dataTest)

    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars"

    params = urllib.parse.urlencode({
    })

    data  = {
            'faceId': face1[0]["faceId"],
            'faceIds': faceIdArray,
            'maxNumOfCandidatesReturned': 1000,
            'mode': "matchFace"
            }
    print(data)
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    returnedValue = response.json()

    print(returnedValue)
}


# try:
#     conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
#     conn.request("POST", "/face/v1.0/faceindsimilars?%s" % params, data, headers)
#     response = conn.getresponse()
#     data = response.read()
#     print(data)
#     conn.close()
# except Exception as e:
#     print("[Errno {0}] {1}".format(e.errno, e.strerror))
