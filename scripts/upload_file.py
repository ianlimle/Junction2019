import requests
import time

def upload_face(UPLOAD_FILEPATH, UNIQUE_ID, URL = "http://127.0.0.1:5000/image/upload"):
    descriptor = open(UPLOAD_FILEPATH,'rb')
    print(descriptor)
    # files = {'file': descriptor, 'Content-Type': 'image/jpeg'}
    files = {'image': ("male-lol", descriptor, 'multipart/form-data', {'Expires': '0'})}
    r = requests.post(URL, files=files, data=dict(unique_id = UNIQUE_ID))

    return r


def get_analysis(UNIQUE_ID):
    URL = f"http://127.0.0.1:5000/image/analyse/{UNIQUE_ID}"

    try:
        r = requests.get(URL)

    except Exception as e:
        print(str(e))

    return r.text

def get_products(UNIQUE_ID):
    URL = f"http://127.0.0.1:5000/image/products/{UNIQUE_ID}"

    try:
        r = requests.get(URL)

    except Exception as e:
        print(str(e))

    return r.text



if __name__ == "__main__":
    import time
    FILE_PATH = "/Users/lionellloh/Desktop/acne.jpg"
    # r = upload_face(FILE_PATH, "".join(str(time.time()).split(".")))
    # print(r.status_code)
    # print(r.text)

    unique_id = 1234
    print(upload_face(FILE_PATH, unique_id))
    # time.sleep(1)
    print(get_analysis(unique_id))

