import base64
import urllib.request as urllib2
import json
import glob
import requests

class FacePlus():
    def __init__(self, **kwargs):        
        self.file = ""
    
    def analyse_face(self, filepath):
        http_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
        key = "Kn1HpBcqh8NC5oVqvkjqkf2nlXyjkQrE"
        secret = "9JgTtVTaZNY-uLW3KACwqjcQm5mT2yMn"
        with open(filepath,'rb') as fr:
            img64 = base64.b64encode(fr.read())
            img64 = img64.decode('utf-8')
            payload = {
                        'api_key': key,
                        'api_secret': secret,
                        'image_base64':img64,
                        'return_attributes': 'skinstatus'
                        }

        try:
            res = requests.post(http_url, data=payload)
            return res
        except Exception as e:
            print('Error:')
            print(e)

    def analyse_gender(self, filepath):
        http_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
        key = "Kn1HpBcqh8NC5oVqvkjqkf2nlXyjkQrE"
        secret = "9JgTtVTaZNY-uLW3KACwqjcQm5mT2yMn"
        fr = open(filepath,'rb')
        img64 = base64.b64encode(fr.read())
        img64 = img64.decode('utf-8')
        payload = {
                    'api_key': key, 
                    'api_secret': secret, 
                    'image_base64':img64,
                    'return_attributes': 'gender'
                    }
        fr.close()
        try:
            res = requests.post(http_url, data=payload)
            return res
        except Exception as e:
            print('Error:')
            print(e)
    
    def acne_mod(self, score):
        try:
            score = score.json()
            print(score)

            bb_top = score['faces'][0]['face_rectangle']['top']
            bb_left = score['faces'][0]['face_rectangle']['left']
            bb_width = score['faces'][0]['face_rectangle']['width']            
            bb_height = score['faces'][0]['face_rectangle']['height']
            bounding_box_coordinates = bb_top, bb_left, bb_width, bb_height
            # print("bounding box coordinates", bounding_box_coordinates)

            acne_score = score['faces'][0]['attributes']['skinstatus']['acne']
            darkcircle_score = score['faces'][0]['attributes']['skinstatus']['dark_circle']
            stain_score = score['faces'][0]['attributes']['skinstatus']['stain']    
            final_score = int(round((acne_score + darkcircle_score + stain_score)/3))
            print("Final score", final_score)
            # print("acne score", acne_score)
            # print("darkcircle score", darkcircle_score)
            # print("stain score", stain_score)

            if final_score >= 20:
                return 1, bounding_box_coordinates
            else:
                return 0, bounding_box_coordinates
        except Exception as e:
            print("Error", str(e))
    
    def run(self):
        analyse_return = self.analyse_face(r"{}".format(self.file))
        acne_mod = self.acne_mod(analyse_return)

        gender_return = self.analyse_gender(r"{}".format(self.file))
        gender_return = gender_return.json()
        gender = gender_return['faces'][0]['attributes']['gender']['value']
       
        return acne_mod, gender




class MergeFace():
    def __init__(self, **kwargs):
        self.template_path = ""
        self.merge_path = ""
        self.template_rectangle = ""
    
    def analyse_face(self, template_path, merge_path, template_rectangle):
        http_url = 'https://api-us.faceplusplus.com/imagepp/v1/mergeface'
        key = "Kn1HpBcqh8NC5oVqvkjqkf2nlXyjkQrE"
        secret = "9JgTtVTaZNY-uLW3KACwqjcQm5mT2yMn"

        fr = open(self.template_path,'rb')
        template_path = base64.b64encode(fr.read())
        template_base64 = template_path.decode('utf-8')

        fr = open(self.merge_path,'rb')
        merge_path = base64.b64encode(fr.read())
        merge_base64 = merge_path.decode('utf-8')

        payload = {
                    'api_key': key, 
                    'api_secret': secret,         
                    'template_rectangle': template_rectangle,            
                    'template_base64': template_base64,
                    'merge_base64': merge_base64,
                    'merge_rate': 0               
                    }
        fr.close()
        try:
            res = requests.post(http_url, data=payload)
            #get response
            qrcont = res.json()
            # print(qrcont['result'])
            text_file = open("Output.txt", "w")
            text_file.write(qrcont['result'])
            text_file.close()    
            return qrcont
 
        except Exception as e:
            print('Error:')
            print(e)
    
    def run(self):
        analyse_return = self.analyse_face(
            template_path = self.template_path,
            merge_path = self.merge_path,
            template_rectangle =  self.template_rectangle)

# Analyse from single image
if __name__ == "__main__":

    hello = FacePlus()
    # CHANGE PATH: Input acne face
    template_image = "/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/Faceplus/nov_test/acne_14.jpg"
    hello.file = template_image
    hello_return = hello.run()
    rectangle_box = hello_return[0][1]
    gender = hello_return[1]
    print(gender)


    merge = MergeFace()
    merge.template_path = r"{}".format(template_image)
    if gender == 'Female':
        # CHANGE PATH: Female model
        merge.merge_path = r"/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/images/hass/makeup3.jpg"
    else:
        # CHANGE PATH: Male model
        merge.merge_path = r"/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/Faceplus/test2/male_face.jpg"
    merge.template_rectangle = "{}, {}, {}, {}".format(rectangle_box[0], rectangle_box[1], rectangle_box[2],
                                                       rectangle_box[3])
    print(merge.template_rectangle)
    merge.run()