#!/usr/bin/ python3
# import rospy
# from geometry_msgs.msg import Twist
# from geometry_msgs.msg import Pose
# from geometry_msgs.msg import Pose2D
# from logcart_follow.msg import LeaderTrack
# from nav_msgs.msg import Odometry
# from sensor_msgs.msg import Joy
# from sensor_msgs.msg import LaserScan
# from std_msgs.msg import String

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
#from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.clock import CyClockBase, mainthread, Clock
from kivy.config import Config
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import urllib.request as urllib2
import base64
#import PIL.Image as Image1
import io

from kivy.graphics.texture import Texture

import numpy as np
import math  
import serial
import time
import requests
import threading
import cv2
Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'borderless', '1')
Config.set('graphics','show_cursor', '1') # TODO: Set show_cursor to '0' for deployment

Builder.load_file("UI_backup.kv")
is_captured = '1'
id = '0'
url = 'http://192.168.43.252:5000/'
#######################################################################################
################################### Window Manager ####################################
#######################################################################################

class WindowManager(ScreenManager):
    # Global variable shared across screens
    global is_captured 
    is_captured = '1'
    global id
    id = '0'
    global url
    url = 'http://192.168.43.252:5000/'
#######################################################################################
###################################### Main Window ####################################
#######################################################################################
class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, timeout = 1.0/20)
    
            #break thread when leave main screen

    def upload_face(self, UPLOAD_FILEPATH = '/home/waihong/Desktop/pic.jpg', URL = "%simage/upload"%(url)):
        descriptor = open(UPLOAD_FILEPATH,'rb')
        #print(descriptor)
        image_id = time.strftime("%Y%m%d")+time.strftime("%H%M%S")
        files = {'image': ("male-lol", descriptor, 'multipart/form-data', {'Expires': '0'})}
        
        r = requests.post(URL, files=files, data=dict(unique_id = image_id))
        if r.status_code > 202:
            print('status code: ' + str(r.status_code) + ', image_id: %s failed to update' % image_id)
        else:
            print('status code: ' + str(r.status_code) + ', image_id: %s updated successfully' % image_id)
        
        return image_id

    def update(self, dt):
        lower = np.array([0, 5, 90], dtype = "uint8")
        upper = np.array([80, 255, 255], dtype = "uint8")
        
        # Change box!
        upper_bound_x = 220
        lower_bound_x = 420
        upper_bound_y = 130
        lower_bound_y = 370
        
        face_cascade = cv2.CascadeClassifier("/home/waihong/catkin_ws/src/logcart_UI/model/face.xml")
        scar_cascade = cv2.CascadeClassifier("/home/waihong/catkin_ws/src/logcart_UI/model/scar.xml")
        pigment_cascade = cv2.CascadeClassifier("/home/waihong/catkin_ws/src/logcart_UI/model/pigmentation.xml")
        
        ret, frame = self.capture.read()
        if ret:
            
            #denoising by using a gaussian blur
            #frame = cv2.GaussianBlur(frame, (3,3), 0)
            # Skin
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            skinMask = cv2.inRange(hsv, lower, upper)
            # apply a series of erosions and dilations to the mask
        	# using an elliptical kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            skinMask = cv2.erode(skinMask, kernel, iterations = 2)
            skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
        	# blur the mask to help remove noise, then apply the
        	# mask to the frame
            skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
            skin = cv2.bitwise_and(frame, frame, mask = skinMask)
            
            cv2.rectangle(skin,(upper_bound_x,upper_bound_y),(lower_bound_x,lower_bound_y),(0,255,0),2)
            font = cv2. FONT_HERSHEY_SIMPLEX
            cv2.putText(skin, 'Place your Face Here', (upper_bound_x - 20,upper_bound_y - 20), font, 0.5,(11,255,255), 2, cv2.LINE_AA)
            
            gray = cv2.cvtColor(skin, cv2.COLOR_BGR2GRAY)
            gray_skin = gray[upper_bound_y:lower_bound_y, upper_bound_x:lower_bound_x]
            new_skin = skin[upper_bound_y:lower_bound_y, upper_bound_x:lower_bound_x]

            # faces = face_cascade.detectMultiScale(gray,1.3,2)
            scars = scar_cascade.detectMultiScale(gray_skin,1.4,300)
            pigments = pigment_cascade.detectMultiScale(gray_skin,1.4,300)
            
            mask = np.zeros(frame.shape, frame.dtype)
                        
            # for (x,y,w,h) in faces:
            #     cv2.rectangle(img=mask, pt1 = (x, y), pt2 = (x+w, y+h), color = (255, 255, 255), thickness = -1)
            #     face_crop = cv2.bitwise_and(frame, mask)     
            #     face_skin = face_crop[upper_bound_y:lower_bound_y, upper_bound_x:lower_bound_x]
            #     img_face_box = frame[upper_bound_y:lower_bound_y, upper_bound_x:lower_bound_x]
            #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
            #     cv2.rectangle(frame,(upper_bound_x,upper_bound_y),(lower_bound_x,lower_bound_y),(0,255,0),2)
            #     font = cv2. FONT_HERSHEY_SIMPLEX
            #     cv2.putText(frame, 'Place your Face Here', (upper_bound_x - 20,upper_bound_y - 20), font, 0.5,(11,255,255), 2, cv2.LINE_AA)

            for (x_scars, y_scars, w_scars, h_scars) in scars:
                cv2.rectangle(new_skin,(x_scars,y_scars),(x_scars+w_scars,y_scars+h_scars),(255,11,255),2)
        
            for (x_pig, y_pig, w_pig, h_pig) in pigments:
                cv2.rectangle(new_skin,(x_pig,y_pig),(x_pig+w_pig,y_pig+h_pig),(255,0,0),2)
        
            
            
            # convert it to texture
            face_crop = cv2.flip(skin, 0)
            buf = face_crop.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            global is_captured 
            if is_captured == '2' :
                write_name = '/home/waihong/Desktop/pic.jpg'
                cv2.imwrite(write_name, frame)
                global id
                id = self.upload_face()
                is_captured = '3'
                
            
            # display image from the texture
            


class WebcamWindow(Screen, KivyCamera):
    def __init__(self, **kwargs):
        self.name = 'webcam'
        super(WebcamWindow, self).__init__(**kwargs)
        super(KivyCamera, self).__init__(**kwargs)
        

    def build(self):
        # self.capture = cv2.VideoCapture(1)
        self.my_camera = KivyCamera()
        return self.my_camera

    # def on_pre_leave(self):
    #     self.take_pic()
    def btn_pressed(self):
        if self.ids.va1.state ==  "normal":
           self.ids.va1.state =  "down" 
           print(self.ids.va1.state)
        elif self.ids.va1.state ==  "down":
            self.ids.va1.state =  "normal"
     
    @mainthread
    def on_enter(self):
        self.capture.open(0)
        self.ids.analyse_button.state = "down"
        global is_captured
        print(is_captured)
        # if is_captured == '3':
        #     print("haha")
        #     self.ids.analyse_button.state = "normal"
        #threading.Thread(target=lambda: self.getsavecallback()).start()
    

    def on_leave(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
        global is_captured
        is_captured = '1'
    
    def take_pic(self):
        global is_captured
        is_captured = '2'
        #app.root.current = "analyse"
    def getsavecallback(self):
        time_start = time.time()
        #timer countdown added to check message every 1 second
        while True:
            #print(self.is_at_application_window)
            if time.time() - time_start  >= 1 and self.manager.current == "webcam" :
                #print("runnn")
                global is_captured
                print(is_captured)
                if is_captured == '3':
                    print("haha")
                    global id 
                    id = self.upload_face()
                    self.ids.analyse_button.state = "normal"
                time_start = time.time()    
            #break thread when leave main screen
            elif self.manager.current != "webcam":
                #print("haha")
                break

class AnalyseWindow(Screen):
    def __init__(self, **kwargs):
        self.name = 'analyse'
        super(AnalyseWindow,self).__init__(**kwargs)
        #super(FacePlus,self).__init__(**kwargs)
        #self.face_plus = FacePlus()
        self.result = None
    
    @mainthread
    def on_pre_enter(self):
        self.ids.pic.reload()
        self.ids.condition_pic.source = '../resources/images/white.png'
        self.ids.condition.text = "skin condition:   \n  severity:     "
    @mainthread
    def on_enter(self):
        global id
        print(id)
        self.result = self.get_analysis(id)
        #self.result = self.face_plus.run()
        result1 = self.result
        #print(result1)
        if result1["gender"] == "Male" :
            if result1["severity"] == 1 :
                self.ids.condition_pic.source = '../resources/images/face_severe_man.jpg'
                self.ids.condition.text = "skin condition: ACNE \n severity: SEVERE"
            elif result1["severity"] == 0 :
                self.ids.condition_pic.source = '../resources/images/face_mild_man.jpg'
                self.ids.condition.text = "skin condition: ACNE \n severity: MILD"
        if result1["gender"] == "Female" :
            if result1["severity"] == 1 :
                self.ids.condition_pic.source = '../resources/images/face_severe_woman.jpg'
                self.ids.condition.text = "skin condition: ACNE \n severity: SEVERE"
            elif result1["severity"] == 0 :
                self.ids.condition_pic.source = '../resources/images/face_mild_woman.jpg'
                self.ids.condition.text = "skin condition: ACNE \n severity: MILD"
        # def create_scrollview(self):
        #     base = ["element {}".format(i) for i in range(3)]
        #     layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        #     layout.bind(minimum_height=layout.setter("height"))

        #     for element in base:
        #         layout.add_widget(Button(text=element, background_normal="../resources/images/capture_button_pressed.png", size=(50, 500), size_hint=(1, None),
        #                                 background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
        #     scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        #     scrollview.add_widget(layout)
        #     self.ids.view.add_widget(scrollview)

    def get_analysis(self,UNIQUE_ID):
        URL = "%simage/analyse/%s" %(url,UNIQUE_ID)

        try:
            r = requests.get(URL)

        except Exception as e:
            print(str(e))

        return r.json()
class RecommendWindow(Screen):
    def __init__(self, **kwargs):
        self.name = 'recommend'
        super(RecommendWindow,self).__init__(**kwargs)
        #super(FacePlus,self).__init__(**kwargs)
    
    @mainthread
    def on_enter(self):
        global id
        products = self.get_products(id)["data"]
        print(products)
        for i in range(len(products)):
            product = 'product_pic%d'%(i+1)
            self.ids[product].source = products[i]["picture"]
            name = 'product_name%d'%(i+1)
            self.ids[name].text = "%s \n \nPrice: $%s \n \nIngredients: %s"%(products[i]["name"],products[i]["price"],products[i]["ingredients"])

    def get_products(self,UNIQUE_ID):
        URL = "%simage/products/%s"%(url,UNIQUE_ID)

        try:
            r = requests.get(URL)

        except Exception as e:
            print(str(e))

        return r.json()
    
    def btn2_pressed(self):
        if self.ids.va2.state ==  "normal":
           self.ids.va2.state =  "down" 

        elif self.ids.va2.state ==  "down":
            self.ids.va2.state =  "normal"

class BeautifyWindow(Screen) :
    def __init__(self, **kwargs):
        self.name = 'beautify'
        super(BeautifyWindow,self).__init__(**kwargs)
    
    def build(self):
        carousel = Carousel(direction='right')
        image = AsyncImage(source='/home/waihong/Desktop/pic.jpg', allow_stretch=True)
        carousel.add_widget(image)
        return carousel
        
        
    def on_pre_enter(self):
        self.ids.pic1.reload()

    def retrieve_merged_face(self,IMAGE_ID, IMAGE_FILEPATH = "/home/waihong/Desktop/pic2.jpg"):
        r = requests.get("%simage/merge/%d"%(url,IMAGE_ID))
        #r.encoding = "utf-8"
        print(r.json())  
        decoded = base64.b64decode(r.json()["merged_image"])

        f = open(IMAGE_FILEPATH, 'wb')
        f.write(decoded)
        f.close()
        print("Image decoded and stored with filepath: "+IMAGE_FILEPATH)

    @mainthread
    def on_enter(self):
        #self.build()
        print(type(id))
        self.retrieve_merged_face(int(id))
        print("done")
        self.ids.pic2.source = '/home/waihong/Desktop/pic2.jpg'
        
class TestApp(App):  #Main Class
    def __init__(self):
        super(TestApp, self).__init__()
        #rospy.init_node('logcart_ui')

    def build(self):
        sm = WindowManager(transition=NoTransition())
        sm.current = 'webcam'
        # sm.current = 'application'
        #sm.current = 'map'
        
        return sm


  

class FacePlus():
    def __init__(self, **kwargs):
        self.acne = 0
    
    def analyse_face(self,filepath):
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
                    'return_attributes': 'skinstatus'
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
            acne_score = score['faces'][0]['attributes']['skinstatus']['acne']
            darkcircle_score = score['faces'][0]['attributes']['skinstatus']['dark_circle']
            stain_score = score['faces'][0]['attributes']['skinstatus']['stain']    
            final_score = int(round((acne_score + darkcircle_score + stain_score)/3))
            print("Final score", final_score)
            if final_score >= 20:
                return 0
            else:
                return 1
        except Exception as e:
            print("Error", e)
    
    def run(self):
        analyse_return = self.analyse_face(r'/home/waihong/Desktop/pic.jpg')
        acne_mod = self.acne_mod(analyse_return)
        self.acne = acne_mod
        return self.acne
        #print (self.acne)

if __name__ == "__main__":    
    TestApp().run()
