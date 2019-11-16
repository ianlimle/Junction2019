import requests

def upload_face(UPLOAD_FILEPATH, UNIQUE_ID, URL = "http://lionellloh-ndls.localhost.run/upload"):
    descriptor = open(UPLOAD_FILEPATH,'rb')
    print(descriptor)
    # files = {'file': descriptor, 'Content-Type': 'image/jpeg'}
    files = {'image': ("male-lol", descriptor, 'multipart/form-data', {'Expires': '0'})}
    r = requests.post(URL, files=files, data=dict(unique_id = UNIQUE_ID))

    return r


if __name__ == "__main__":
    r = upload_face("/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/model_faces/male_face.jpg", "testinglol6")
    print(r.status_code)
    print(r.text)


