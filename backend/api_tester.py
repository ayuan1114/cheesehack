import requests

base_url = "http://127.0.0.1:8000"
admin_token = "QBP7-4OEE-PIP5-C37L"

cred1 = {"username": "lebronjames", "password":"gyatt"}
cred2 = {"username": "ayuan1114", "password":"pw123"}
cred3 = {"username": "alsa", "password":"pw321"}

response = requests.post(base_url + "/create-user", json=cred1)
token1 = response.json()["access_token"]
print(response.content)
response = requests.post(base_url + "/create-user", json=cred2)
token2 = response.json()["access_token"]
print(response.content)
response = requests.post(base_url + "/create-user", json=cred3)
token3 = response.json()["access_token"]
print(response.content)

print(token1, token2, token3)

response = requests.post(base_url + "/upload-vid", json={"access_token": token1, "video_ref": "test_vid1.mp4"})
print(response.content)

response = requests.post(base_url + "/upload-vid", json={"access_token": token2, "video_ref": "test_vid2.mp4"})
print(response.content)

response = requests.post(base_url + "/upload-vid", json={"access_token": token3, "video_ref": "test_vid3.mp4"})
print(response.content)

response = requests.post(base_url + "/all-videos", json={"access_token": admin_token})
print(response.content)
