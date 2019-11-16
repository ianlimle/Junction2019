import requests

files = {'file': open('../model_faces/female_face.jpg','rb')}
values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

# URL = "https://lionellloh-ndls.localhost.run/upload/"
URL = "http://127.0.0.1:5000/upload/"

r = requests.post(URL, files=files)
# r = requests.get("http://127.0.0.1:5000", verify = False)


print(r.text)