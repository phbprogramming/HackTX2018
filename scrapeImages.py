import itertools
import pynder
import robobrowser
import re
import time
import requests
import json
import imagecompare

MOBILE_USER_AGENT = r"Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://m.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

#FBTOKEN = get_access_token("holycisthelanguageofgod@gmail.com", "ISeeG0dInCode!")
#rint(FBTOKEN)
#FBID = "100029456320936"
#session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)

# DEPRECATED #
# FROM NOW ON USE THE PHONE NUMBER AUTHENTICATION #

CODE_REQUEST_URL = "https://graph.accountkit.com/v1.2/start_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=fr_FR&phone_number=#placeholder&response_type=token&sdk=ios"
CODE_VALIDATE_URL = "https://graph.accountkit.com/v1.2/confirm_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&confirmation_code=#confirmation_code&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=fr_FR&login_request_code=#request_code&phone_number=#phone_number&response_type=token&sdk=ios"
TOKEN_URL = "https://api.gotinder.com/v2/auth/login/accountkit"

HEADERS = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0'}


def get_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    f = s.get_form()
    if f.submit_fields.get('__CONFIRM__'):
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    else:
        raise Exception("Couldn't find the continue button. Maybe you supplied the wrong login credentials? Or maybe Facebook is asking a security question?")
    access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
    return access_token

def sendCode(number):
    URL = CODE_REQUEST_URL.replace("#placeholder", number)
    r = requests.post(URL, headers=HEADERS, verify=False)
    print(r.url)
    response = r.json()
    if(response.get("login_request_code") == None):
        return False
    else:
        return response["login_request_code"]

def getToken(number, code, req_code):
    VALIDATE_URL = CODE_VALIDATE_URL.replace("#confirmation_code", code)
    VALIDATE_URL = VALIDATE_URL.replace("#phone_number", number)
    VALIDATE_URL = VALIDATE_URL.replace("#request_code", req_code)
    r_validate = requests.post(VALIDATE_URL, headers=HEADERS, verify=False)
    validate_response = r_validate.json()
    print(validate_response)
    access_token = validate_response["access_token"]
    access_id = validate_response["id"]
    GetToken_content = json.dumps({'token':access_token, 'id':access_id, "client_version":"9.0.1"})
    GetToken_headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0', 'Content-Type':'application/json'}
    r_GetToken = requests.post(TOKEN_URL, data=GetToken_content, headers=GetToken_headers, verify=False)
    token_response = r_GetToken.json()
    if(token_response["data"].get("api_token") == None):
        return token_response
    else:
        return token_response["data"]["api_token"]

def record_profile(name, age, distance, insta, photos):
	f.write("Name: " + name)
	f.write("age: " + age)
	f.write("distance from search origin: " + distance + "km")

	f.write("instagram profile: " + insta)
	f.write("Photos:")

	num = 1
	for photo in photos:
		f.write("Photo " + num + ":")
		f.write("	url: " + photo[0])
		f.write("	MSE: " + photo[1])
		f.write("	SSIM: " + photo[2])
		f.write("	bits of difference: " + photo[3])
		f.write("")
		num += 1

	f.write("------------------------------------------------------------------------------")
	f.flush()

# {'name': 'ok', 'ageRange': ['ok', 'ok'], 'fileName': ['02ee45ff-58ed-4aaf-9c2f-1262c95c7f60.mp4', '079e640b-0c52-4741-a2
# d1-59d80e285cca.mp4', '149f92b8-9a12-4404-b043-e1f27fcabcde.mp4', '1d4daa86-5f5b-47a9-858f-47f9e4c81dcf.mp4', '20180324_
# 181309.jpg', '20180324_181313.jpg', '20180324_194808.jpg', '20180324_203922_001.jpg', '25139427-6f74-402d-9558-5dfd11d35
# 4a6.mp4', '39b9e8e2-510b-436d-8e42-73eb32e0c70a.mp4', '68f15f8c-1faa-46d4-80d3-889c7f2a4198.mp4', '6a68cf29-9e75-46e8-af
# 11-2b9b8ff4cddd.mp4', '743795fc-8631-4a57-b933-a60e6cf5db07.mp4', '78affe4e-e0d1-4e38-a6df-6b61b3942a03.mp4', '7a4164f0-
# 203c-443b-8965-fef33c7fd0a2.mp4', '80953031-8d12-47c0-be0e-6a247f6f5f92.mp4', '8a06183a-f46e-4242-8822-7999e9cdb46c.mp4'
# , '8b274c6f-4ef8-4d2e-9ab0-6cb11c39b1a1.mp4', '9e610140-6027-4595-8907-578299a50a91.mp4', '9fef73b3-1d69-44a1-ab46-5e75e
# ded112f.mp4', 'a51d9672-3ba2-4f4e-be44-64a05bc1039c.mp4', 'ab5fa593-aff4-4429-951d-7ed8576fbcf4.mp4', 'abaf7c78-65ae-404
# e-acd6-501b939acd59.mp4', 'b4ae9a03-be3d-4459-8383-eae954ee6a5e.mp4', 'bc93be95-df61-4db6-96b4-609cd205f01b.mp4', 'c4458
# ff8-afe3-455e-9259-1c54dbf65c13.mp4', 'c4eeddc8-44f1-4fa5-80fe-fb6d9c4e0027.mp4', 'e24d6c30-4147-4a89-a061-2aba51ad2353.
# mp4', 'ea62d7df-dc8c-42d6-bb6d-db3e8a9d5ca0.mp4', 'eb5b96ea-3814-4a09-ac90-fe708cf913ce.mp4', 'ee05c35b-606a-4fc5-9220-8
# 5dd67da6506.mp4'], 'location': [30.5, -97.9], 'radius': 'ok'}

def run(guiInput):
    result = imagecompare.doComparison("somephoto.JPG", "https://animals.sandiegozoo.org/sites/default/files/2016-11/animals_hero_lizards.jpg")
    print(result[1])
    # phone_number = "15125228879"
    # log_code = sendCode(phone_number)
    # sms_code = input("Please enter the code you've received by sms")
    #
    # myToken = str(getToken(phone_number, sms_code, log_code))
    #
    # print("Here is your Tinder token :" + myToken)
    #
    # session = pynder.Session(XAuthToken=myToken)
    # session.update_location(guiInput['location'][0], guiInput['location'][1])
    # users = session.nearby_users(guiInput['radius'])
    #
    # i = 1
    #
    # #itertools.islice(users, 10):
    # #needs to stop using relative path, is only geting the first one
    # basephoto = guiInput["fileName"][0]
    #
    # f = open("logfile.txt", "a")
    #
    # for user in users:
    #     match = False
    #     time.sleep(1)
    #     print(" ")
    #     print(i)
    #     i+=1
    #     print("Name: " + user.name)
    #     print("Insta: " + str(user.instagram_username))
    #     print("Age: " + str(user.age))
    #     for url in user.photos:
    #         result = imagecompare.doComparison(basephoto, url)
    #         if (result[0] < 3000 or result[1] > 0.4 or result[2] < 30):
    #             match = True
    #     if(match):
    #         record_profile(user.name, str(user.age), str(user.distance_km), str(user.instagram_username), photos)
