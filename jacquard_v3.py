import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from PIL import Image as PILImage
from kivy.uix.popup import Popup
import shutil
import os
import cv2
import numpy as np
from Adafruit_IO import Client
import threading
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
import RPi.GPIO as GPIO
import time
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '450')
Config.set('graphics', 'borderless', 'True')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fullscreen', 1)
aio = Client('sankar87eee', 'aio_BcjL967yMztvxoZkHT1i5hdRrdsz')

kivy.require('1.11.1')

"""
    Run_view Image, getdata, based on the pick input and pick number the array value is computed and stored as image.
"""

#GPIO.setwarnings(False)         #disable warnings

GPIO.setmode(GPIO.BCM)        #set pin numbering system
GPIO.setup(19,GPIO.OUT)

pi_pwm = GPIO.PWM(19,800)      #create PWM instance with frequency
pi_pwm.start(50)

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 1

print('something')

JACQUARD_NORMAL = 0
JACQUARD_BORDER_BODY = 1
JACQUARD_REVERSE_ROW = 0
JACQUARD_REVERSE_COLUMN = 0
JACQUARD_PICK = 10
JACQUARD_PICK_INC = 1
JACQUARD_REPEAT = 0
JACQUARD_TOP_BOT_HEIGHT = 300
BRIGHTNESS = 50

JACQUARD_SETTING = {'JACQUARD_TYPE': 'NORMAL', 'JACQUARD_INVERT': 'OFF',
                                'JACQUARD_REVERSE_ROW': 'OFF', 'JACQUARD_REVERSE_COL': 'OFF', 'JACQUARD_REPEAT': 0}
JACQUARD_RUNNING_STATUS= {'CURRENT_PICK': 0,'CURRENT_REPEAT':0}

#image declaration
BODY_IMAGE_HEIGHT = None
BODY_IMAGE_WIDTH = None
BODY_IMAGE = None
BORDER_IMAGE_HEIGHT = None
BORDER_IMAGE_WIDTH = None
BORDER_IMAGE = None
SOURCE_IMAGE_HEIGHT = None
SOURCE_IMAGE_WIDTH = None
SOURCE_IMAGE = None

if JACQUARD_PICK <1: JACQUARD_PICK =1
elif JACQUARD_PICK > 1000000: JACQUARD_PICK = 1000000

JACQUARD_REPEAT = 0
if JACQUARD_REPEAT <1: JACQUARD_REPEAT =1
elif JACQUARD_REPEAT > 1000000: JACQUARD_REPEAT = 1000000

CURRENT_PICK = 200
CURRENT_REPEAT = 1

def Jacquard_load_settings(): #called druing jacquard start
    pass

def Jacquard_save_settings(): #called during jacquard off
    pass

def Jacquard_Invert():
    pass

def Jacquard_Reverse_Row():
    pass

def Jacquard_Reverse_Column():
    pass

def Jacquard_desing_view():
    global RUN_VIEW_ARRAY
    pass

print(kivy.__version__)

_feed1_value = '50'

def IoT_thread():
    while True:
        global _feed1_value
        data = aio.receive('text')
        _feed1_value = data.value

class NewRoot:
    def myfun1(self):
        print("app function pressed")

class ManageFile:
    def __init__(self):
        self.destination = None
        self.source = None

    def copy_file(self, source):
        self.source = source
        print('copy function', self.destination, self.source)

    def paste_file(self, destination):
        try:
            self.destination =destination
            print('paste function', self.destination,self.source)
            shutil.copy(self.source, self.destination)
            self.source = []
        except Exception:
            print('unknown error while pasting')

    def delete_file(self, source):
        try:
            os.remove(source)
        except Exception:
            print("Unknown error delete_file")


class InfoHome(FloatLayout):
    pass


class PopUp(Popup):
    def __init__(self, source_value):
        super().__init__()
        self.ids.view_image.source = source_value
        self.size_hint = 0.8, 0.6

class ImageRead:
    def __init__(self):
        pass
    def jacquard_body_image(self):
        try:
            global BODY_IMAGE_HEIGHT
            global BODY_IMAGE_WIDTH
            global BODY_IMAGE
            img = cv2.imread('BODY_IMAGE.bmp', 1)
            BODY_IMAGE = cv2.flip(img, 0)           
            BODY_IMAGE_HEIGHT, BODY_IMAGE_WIDTH = BODY_IMAGE.shape[0], BODY_IMAGE.shape[1]
        except Exception:
            pass
        
    def jacquard_border_image(self):
        try:
            global BORDER_IMAGE_HEIGHT
            global BORDER_IMAGE_WIDTH
            global BORDER_IMAGE
            img = cv2.imread('BORDER_IMAGE.bmp', 1)
            BORDER_IMAGE = cv2.flip(img, 0) #fliped image here and fliped in texture          
            BORDER_IMAGE_HEIGHT, BORDER_IMAGE_WIDTH = BORDER_IMAGE.shape[0], BORDER_IMAGE.shape[1]
        except Exception:
            pass

    def jacquard_normal_image(self):
        try:
            global NORMAL_IMAGE_HEIGHT
            global NORMAL_IMAGE_WIDTH
            global NORMAL_IMAGE
            img = cv2.imread('NORMAL_IMAGE.bmp', 1)
            NORMAL_IMAGE = cv2.flip(img, 0) #fliped image here and fliped in texture           
            NORMAL_IMAGE_HEIGHT, NORMAL_IMAGE_WIDTH = NORMAL_IMAGE.shape[0], NORMAL_IMAGE.shape[1]
        except Exception:
            pass

    def jacquard_source_image(self):
        global SOURCE_IMAGE_HEIGHT
        global SOURCE_IMAGE_WIDTH
        global SOURCE_IMAGE
        try:
            img = cv2.imread('SOURCE_IMAGE.bmp', 1)
            SOURCE_IMAGE = cv2.flip(img, 0)            
            SOURCE_IMAGE_HEIGHT, SOURCE_IMAGE_WIDTH = SOURCE_IMAGE.shape[0], SOURCE_IMAGE.shape[1]
        except Exception:
            pass
        
def windowsize():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    from kivy.core.window import Window
    WINDOW_WIDTH = Window.width
    WINDOW_HEIGHT = Window.height
    
class BotImage(Widget):

    bot_image = ObjectProperty(None)
    bot_texture_size = ListProperty((0, 0))
    bot_texture_pos = ListProperty((0, 0))


    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)

    def top_bottom_image(self):
        global JACQUARD_PICK
        global JACQUARD_TOP_BOT_HEIGHT
        global WINDOW_WIDTH
        global WINDOW_HEIGHT   
        global SOURCE_IMAGE_HEIGHT
        global SOURCE_IMAGE_WIDTH
        global SOURCE_IMAGE
        if SOURCE_IMAGE_HEIGHT - JACQUARD_PICK - JACQUARD_TOP_BOT_HEIGHT < 0:
            bot_image_start = 0
        else:
            bot_image_start = SOURCE_IMAGE_HEIGHT - JACQUARD_PICK - JACQUARD_TOP_BOT_HEIGHT

        bot = SOURCE_IMAGE[bot_image_start: SOURCE_IMAGE_HEIGHT - JACQUARD_PICK]
        bot_img = bot.tostring()
        bot_texture = Texture.create(size=(bot.shape[1], bot.shape[0]), colorfmt='rgb')
        bot_texture.blit_buffer(bot_img, colorfmt='rgb', bufferfmt='ubyte', size=(bot.shape[1], bot.shape[0]))
        self.bot_image = bot_texture
        self.bot_texture_size = (bot.shape[1]*WINDOW_WIDTH/800*1,bot.shape[0]*WINDOW_HEIGHT/480*1)
        self.bot_texture_pos = (self.pos[0], 240-self.bot_texture_size[1]+self.pos[1])


    
class TopImage(Widget):

    top_image = ObjectProperty(None)
    bot_image = ObjectProperty(None)
    top_texture_size = ListProperty((0,0))
    top_texture_pos = ListProperty((0,0))
      
    def __init__(self,**kwargs):
        Widget.__init__(self, **kwargs)

    def top_bottom_image(self):
        global JACQUARD_PICK
        global JACQUARD_TOP_BOT_HEIGHT
        global WINDOW_WIDTH
        global WINDOW_HEIGHT                
        global SOURCE_IMAGE_HEIGHT
        global SOURCE_IMAGE_WIDTH
        global SOURCE_IMAGE

        top = SOURCE_IMAGE[SOURCE_IMAGE_HEIGHT-JACQUARD_PICK: SOURCE_IMAGE_HEIGHT -JACQUARD_PICK + JACQUARD_TOP_BOT_HEIGHT]
        top_img = top.tostring()
        top_texture = Texture.create(size=(top.shape[1], top.shape[0]), colorfmt='rgb')
        top_texture.blit_buffer(top_img, colorfmt='rgb', bufferfmt='ubyte',size=(top.shape[1], top.shape[0]))
        self.top_image = top_texture
        self.top_texture_size = (top.shape[1]*WINDOW_WIDTH/800*1, top.shape[0]*WINDOW_HEIGHT/480*1)

            ##############

class CallbackClock:
    def __init__(self):
        pass
    
    def callbackclock(df):
        global JACQUARD_PICK
        global JACQUARD_REPEAT
        global CURRENT_PICK
        global CURRENT_REPEAT
        global JACQUARD_TOP_BOT_HEIGHT
        global JACQUARD_REPEAT
        global JACQUARD_START_STOP
        global SOURCE_IMAGE_HEIGHT
        
        App.get_running_app().root.ids.topimage.top_bottom_image()
        App.get_running_app().root.ids.botimage.top_bottom_image()
        
        if  JACQUARD_START_STOP == "start":      
            if CURRENT_PICK >= SOURCE_IMAGE_HEIGHT:
                CURRENT_PICK =0
                CURRENT_REPEAT = CURRENT_REPEAT + 1
                if CURRENT_REPEAT > JACQUARD_REPEAT:
                    print("repeat over loom stop")
            JACQUARD_PICK = CURRENT_PICK
                    
        elif JACQUARD_START_STOP == "stop":
            if JACQUARD_PICK > SOURCE_IMAGE_HEIGHT:
                CURRENT_REPEAT = CURRENT_REPEAT + 1
                JACQUARD_PICK = 0
                
        App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK)      # this is access root id from other class
        App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class
               
        App.get_running_app().root.ids.total_repeat.text= str(JACQUARD_REPEAT)
        App.get_running_app().root.ids.total_pick.text = str(SOURCE_IMAGE_HEIGHT)
        App.get_running_app().root.ids.current_pick.text = str(CURRENT_PICK)  # this is access root id from other class
        App.get_running_app().root.ids.current_repeat.text = str(CURRENT_REPEAT)  # this is access root id from other class

              
        
class  View_Pick_Inc_BoxLayout(BoxLayout):


    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

    def pic_inc_value(self, x):
        global JACQUARD_PICK_INC
        JACQUARD_PICK_INC = x
        print(JACQUARD_PICK_INC)

    def pick_inc(self):
        global JACQUARD_PICK_INC
        global JACQUARD_PICK
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "stop":
            JACQUARD_PICK = JACQUARD_PICK + JACQUARD_PICK_INC
            App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK)      # this is access root id from other class
            App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class

    def pick_dec(self):
        global JACQUARD_PICK_INC
        global JACQUARD_PICK
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "stop":
            JACQUARD_PICK = JACQUARD_PICK - JACQUARD_PICK_INC
            if JACQUARD_PICK < 0:
                JACQUARD_PICK = 0
            elif JACQUARD_PICK > 50000:
                JACQUARD_PICK = 50000
            App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK) # this is access root id from other class
            App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class

class Jacquared(FloatLayout):

    def __init__(self, **kwargs):
        FloatLayout.__init__(self, **kwargs)
        self.Manage_file = ManageFile()
        print('object created')

    def file_paste(self, path, filename):
        self.Manage_file.paste_file(path)
        self.ids.filechooserSd._update_files()
        self.ids.filechooserUsb._update_files()

    def file_copy(self, path, filename):
        if filename == []:
            self.ids._My_file_hint.text = "Select BMP File"
            self.ids._Usb_file_hint.text = "Select BMP File"
        elif filename[0][-3:] != 'bmp':
            self.ids._My_file_hint.text = "Select BMP File"
            self.ids._Usb_file_hint.text = "Select BMP File"
        else:
            self.Manage_file.copy_file(filename[0])

    def file_delete(self, path, filename):
        if filename == []:
            self.ids._My_file_hint.text = "Select BMP File"
            self.ids._Usb_file_hint.text = "Select BMP File"
        elif filename[0][-3:] != 'bmp':
            self.ids._My_file_hint.text = "Select BMP File"
            self.ids._Usb_file_hint.text = "Select BMP File"
        else:
            self.Manage_file.delete_file(filename[0])
            self.ids.filechooserSd._update_files()
            self.ids.filechooserUsb._update_files()

JACQUARD_START_STOP = "stop"

class Jacquaredgui(App):

    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)


    bmpimage = ObjectProperty(None)
    designdata = None

    def build(self):
        return Jacquared()

    def initialization(self):
        
        global JACQUARD_SETTING
        global BODY_IMAGE
        global NORMAL_IMAGE
        global SOURCE_IMAGE
        global SOURCE_IMAGE_HEIGHT
        global JACQUARD_PICK  #in view jacquarad-pick and in home it is current_pick
        global JACQUARD_REPEAT
        global JACQUARD_RUNNING_STATUS
        global JACQUARD_SETTING
        global CURRENT_PICK
        ImageRead().jacquard_body_image()
        ImageRead().jacquard_border_image()
        ImageRead().jacquard_source_image()
        ImageRead().jacquard_normal_image()
        windowsize()           
        try:
            with open("JACQUARD_SETTING.txt", 'r') as f:
                JACQUARD_SETTING = eval(f.read())
                f.close()
                JACQUARD_REPEAT = JACQUARD_SETTING['JACQUARD_REPEAT']
        except Exception:
            pass
        
        try:
            with open("JACQUARD_RUNNING_STATUS.txt", 'r') as f:
                JACQUARD_RUNNING_STATUS= eval(f.read())
                f.close()
                CURRENT_PICK = JACQUARD_RUNNING_STATUS['CURRENT_PICK']                
                CURRENT_REPEAT = JACQUARD_RUNNING_STATUS['CURRENT_REPEAT']                
                JACQUARD_PICK = CURRENT_PICK
                
        except Exception:
            pass
        # Home Screen Update and initialization
        #read JACQUARD_DESIGN, find hight and width display in home page
        self.root.ids.total_repeat.text= str(JACQUARD_REPEAT)
        self.root.ids.total_pick.text = str(SOURCE_IMAGE_HEIGHT)
        # Menu screen update and initialization
        self.root.ids.repeat_text.text = str(JACQUARD_REPEAT)
        self.root.ids.repeat_slider.value = int(JACQUARD_REPEAT)
        
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "NORMAL":
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.normal_file.background_color = (0.4, 1, 0.4, 1)
        
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.normal_file.background_color = (1, 0.4, 0.4, 1)

        if JACQUARD_SETTING['JACQUARD_INVERT'] == "ON":
            self.root.ids.invert.text = 'INVERT ON'
            self.root.ids.invert.background_color= (0.4, 1, 0.4, 1)
        
        elif JACQUARD_SETTING['JACQUARD_INVERT'] == "OFF":
            self.root.ids.invert.text = 'INVERT OFF'
            self.root.ids.invert.background_color = (1, 0.4, 0.4, 1)

        if JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] =='ON':
            self.root.ids.reverse_row.text = 'REVERSE ROW ON'
            self.root.ids.reverse_row.background_color = (0.4, 1, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] == 'OFF':
            self.root.ids.reverse_row.text = 'REVERSE ROW OFF'
            self.root.ids.reverse_row.background_color = (1, 0.4, 0.4, 1)

        if JACQUARD_SETTING['JACQUARD_REVERSE_COL'] == 'ON':
            self.root.ids.reverse_column.text = 'REVERSE COL ON'
            self.root.ids.reverse_column.background_color = (0.4, 1, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_REVERSE_COL'] == 'OFF':
            self.root.ids.reverse_column.text = 'REVERSE COL OFF'
            self.root.ids.reverse_column.background_color = (1, 0.4, 0.4, 1)
        
        self.root.ids.pick_text.text = str(JACQUARD_PICK)      # this is access root id from other class
        self.root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class
        #self.event1 = Clock.schedule_interval(self.root.ids.topimage.top_bottom_image, 1/20)
        #self.event2 = Clock.schedule_interval(self.root.ids.botimage.top_bottom_image, 1/20)
        #self.event1 = Clock.schedule_interval(CallbackClock.callbackclock, 1/10)
        self.event2 = Clock.schedule_interval(CallbackClock.callbackclock, 1/10)                   

    def getserial(self):
      # Extract serial from cpuinfo file
      self.cpuserial = "0000000000000000"
      try:
        f = open('/proc/cpuinfo','r')
        for line in f:
          if line[0:6]=='Serial':
            self.cpuserial = line[10:26]
        f.close()
      except:
        self.cpuserial = "ERROR000000000"


    def on_start(self):
        
        global JACQUARD_SETTING
        global JACQUARD_REPEAT
        global SOURCE_IMAGE_HEIGHT
        mysystem = '0000000070de507b'
        self.getserial()
        if self.cpuserial != '0000000070de507b':
            from subprocess import call
            call("sudo shutdown -h now", shell=True) 
        
        self.initialization()
        GPIO.add_event_detect(26, GPIO.RISING,
                callback=self.power_cut_handler,
                bouncetime=200)
        
    def power_cut_handler(self):
        pass
    
    def on_press_start(self,  status_bar, status_label):
        global JACQUARD_START_STOP
        global JACQUARD_PICK
        global CURRENT_PICK
        JACQUARD_PICK = CURRENT_PICK
        self.root.ids.pick_text.text = str(JACQUARD_PICK)
        
        if JACQUARD_START_STOP == "stop":
            JACQUARD_START_STOP = "start"
            status_bar.canvas_status = [0, 0.5, 0, 1]
            status_label.text = "STATUS: ON"
        self.root.ids.update_button.disabled = True
        self.root.ids.body_border_file.disabled = True
        self.root.ids.normal_file.disabled = True
        self.root.ids.invert.disabled = True
        self.root.ids.reverse_row.disabled = True
        self.root.ids.reverse_column.disabled = True
        self.root.ids.repeat_dec_button.disabled = True
        self.root.ids.repeat_inc_button.disabled = True
                        
    def on_press_stop(self, status_bar, status_label):
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "start":
            JACQUARD_START_STOP = "stop"
            status_bar.canvas_status = [0.5, 0, 0, 1]
            status_label.text = "STATUS: OFF"
        self.root.ids.update_button.disabled = False
        self.root.ids.body_border_file.disabled = False
        self.root.ids.normal_file.disabled = False
        self.root.ids.invert.disabled = False
        self.root.ids.reverse_row.disabled = False
        self.root.ids.reverse_column.disabled = False
        self.root.ids.repeat_dec_button.disabled = False
        self.root.ids.repeat_inc_button.disabled = False        #############################################

    def on_press_bodyborderfile(self):
        global JACQUARD_BORDER_BODY
        global JACQUARD_NORMAL
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "NORMAL":
            JACQUARD_SETTING['JACQUARD_TYPE'] = "BODY_BORDER"
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.normal_file.background_color = (1, 0.4, 0.4, 1)
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.normal_file.background_color = (1, 0.4, 0.4, 1)

    def on_press_normalfile(self):

        global JACQUARD_SETTING

        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            JACQUARD_SETTING['JACQUARD_TYPE'] = "NORMAL"
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.normal_file.background_color = (0.4, 1, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_TYPE'] == "NORMAL":
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.normal_file.background_color = (0.4, 1, 0.4, 1)

    def on_press_invert(self):
        global JACQUARD_SETTING

        if JACQUARD_SETTING['JACQUARD_INVERT'] == "ON":
            JACQUARD_SETTING['JACQUARD_INVERT'] = "OFF"
            print(JACQUARD_SETTING['JACQUARD_INVERT'])
            self.root.ids.invert.text = 'INVERT OFF'
            self.root.ids.invert.background_color= (1, 0.4, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_INVERT'] == "OFF":
            JACQUARD_SETTING['JACQUARD_INVERT'] = "ON"
            print(JACQUARD_SETTING['JACQUARD_INVERT'])
            self.root.ids.invert.text = 'INVERT ON'
            self.root.ids.invert.background_color= (0.4, 1, 0.4, 1)

    
    def on_press_reverse_row(self):

        global JACQUARD_SETTING

        if JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] =='ON':
            JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] = 'OFF'
            self.root.ids.reverse_row.text = 'REVERSE ROW OFF'
            self.root.ids.reverse_row.background_color= (1, 0.4, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] == 'OFF':
            JACQUARD_SETTING['JACQUARD_REVERSE_ROW'] = 'ON'
            self.root.ids.reverse_row.text = 'REVERSE ROW ON'
            self.root.ids.reverse_row.background_color = (0.4, 1, 0.4, 1)

    def on_press_reverse_column(self):

        global JACQUARD_SETTING

        if JACQUARD_SETTING['JACQUARD_REVERSE_COL'] == 'ON':
            JACQUARD_SETTING['JACQUARD_REVERSE_COL'] = 'OFF'
            self.root.ids.reverse_column.text = 'REVERSE COL OFF'
            self.root.ids.reverse_column.background_color= (1, 0.4, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_REVERSE_COL'] == 'OFF':
            JACQUARD_SETTING['JACQUARD_REVERSE_COL'] = 'ON'
            self.root.ids.reverse_column.text = 'REVERSE COL ON'
            self.root.ids.reverse_column.background_color= (0.4, 1, 0.4, 1)

    def on_release_myfile_copy(self):
        self.root.ids.myfile_copy.size_hint = (1, 0.2)

    def on_press_myfile_copy(self):
        self.root.ids.myfile_copy.size_hint = (0.92, 0.18)

    def on_release_myfile_copy(self):
        self.root.ids.myfile_copy.size_hint = (1, 0.2)

    def on_press_myfile_paste(self):
        self.root.ids.myfile_paste.size_hint = (0.92, 0.18)

    def on_release_myfile_paste(self):
        self.root.ids.myfile_paste.size_hint = (1, 0.2)

    def on_press_myfile_view(self):
        self.root.ids.myfile_view.size_hint = (0.92, 0.18)

    def on_release_myfile_view(self):
        self.root.ids.myfile_view.size_hint = (1, 0.2)

    def on_press_myfile_delete(self):
        self.root.ids.myfile_delete.size_hint = (0.92, 0.18)

    def on_release_myfile_delete(self):
        self.root.ids.myfile_delete.size_hint = (1, 0.2)

    def on_press_usb_copy(self):
        self.root.ids.usb_copy.size_hint = (0.92, 0.18)

    def on_release_usb_copy(self):
        self.root.ids.usb_copy.size_hint = (1, 0.2)

    def on_press_usb_paste(self):
        self.root.ids.usb_paste.size_hint = (0.92, 0.18)
        
    def on_release_usb_paste(self):
        self.root.ids.usb_paste.size_hint = (1, 0.2)

    def on_press_usb_view(self):
        self.root.ids.usb_view.size_hint = (0.92, 0.18)
        
    def on_release_usb_view(self):
        self.root.ids.usb_view.size_hint = (1, 0.2)

    def on_press_usb_delete(self):
        self.root.ids.usb_delete.size_hint = (0.92, 0.18)

    def on_release_usb_delete(self):
        self.root.ids.usb_delete.size_hint = (1, 0.2)
                      #############################################

    def view_selected_file(self, path, filename):
        try:
            if filename == []:
                self.root.ids._My_file_name.text = "MyFile"
                self.root.ids._Usb_file_name.text = "USB"

                self.root.ids._My_file_hint.text = "Select BMP File"
                self.root.ids._Usb_file_hint.text = "Select BMP File"

            elif (filename[0][-3:] != 'bmp'):
                self.root.ids._My_file_hint.text = "Select BMP File"
                self.root.ids._Usb_file_hint.text = "Select BMP File"
            else:
                if self.root.ids._screen_manager.current == 'myfile_screen':
                    self.root.ids._My_file_name.text = filename[0]
                if self.root.ids._screen_manager.current == 'usb_screen':
                    self.root.ids._Usb_file_name.text = filename[0]

                with Image.open(os.path.join(path, filename[0])) as stream:
                    width, height = stream.size
                    if self.root.ids._screen_manager.current == 'myfile_screen':
                        self.root.ids._My_file_size.text = '{} x {}'.format(width, height)
                    if self.root.ids._screen_manager.current == 'usb_screen':
                        self.root.ids._Usb_file_size.text = '{} x {}'.format(width, height)
        except Exception:
            print('unknow error in view_selecected_file')

    def popup_view_file(self, path, filename):
        try:
            if filename == []:
                self.root.ids._My_file_name.text = "MyFile"
                self.root.ids._Usb_file_name.text = "USB"

                self.root.ids._My_file_hint.text = "Select BMP Design"
                self.root.ids._Usb_file_hint.text = "Select BMP Design"
                print('select file from folders')

            elif (filename[0][-3:] != 'bmp'):
                self.root.ids._My_file_hint.text = "Select BMP File"
                self.root.ids._Usb_file_hint.text = "Select BMP File"
            else:
                with PILImage.open(os.path.join(path, filename[0])) as stream:
                    width, height = stream.size
                    if self.root.ids._screen_manager.current == 'myfile_screen':
                        self.root.ids._My_file_size.text = '{} x {}'.format(width, height)
                    if self.root.ids._screen_manager.current == 'usb_screen':
                        self.root.ids._Usb_file_size.text = '{} x {}'.format(width, height)
                    PopUp(filename[0]).open()
        except Exception:
            print('Unknown Error popup_view_file')

    def meno_press_highlight_release(self):
        current_screen = self.root.ids._screen_manager.current
        if current_screen == "home_screen":
            self.root.ids._home_button.background_color = (0.97, 0.4, 0.7, 1.0)
        if current_screen == "meno_screen":
            self.root.ids._meno_button.text = _feed1_value
            self.root.ids._meno_button.background_color = (0.97, 0.4, 0.7, 1.0)
        if current_screen == "myfile_screen":
            self.root.ids._myfile_button.background_color = (0.97, 0.4, 0.7, 1.0)
        if current_screen == "usb_screen":
            self.root.ids._usb_button.background_color = (0.97, 0.4, 0.7, 1.0)
        if current_screen == "view_screen":
            self.root.ids._view_button.background_color = (0.97, 0.4, 0.7, 1.0)
        if current_screen == "contact_screen":
            self.root.ids._contact_button.background_color = (0.97, 0.4, 0.7, 1.0)

    def meno_press_highlight(self):
        current_screen = self.root.ids._screen_manager.current
        if current_screen == "home_screen":
            self.root.ids._home_button.background_color = (1.0, 0.0, 0.0, 1.0)
        if current_screen == "meno_screen":
            self.root.ids._meno_button.background_color = (1.0, 0.0, 0.0, 1.0)
        if current_screen == "myfile_screen":
            self.root.ids._myfile_button.background_color = (1.0, 0.0, 0.0, 1.0)
        if current_screen == "usb_screen":
            self.root.ids._usb_button.background_color = (1.0, 0.0, 0.0, 1.0)
        if current_screen == "view_screen":
            self.root.ids._view_button.background_color = (1.0, 0.0, 0.0, 1.0)
        if current_screen == "contact_screen":
            self.root.ids._contact_button.background_color = (1.0, 0.0, 0.0, 1.0)

    def repeat_slider(self):
        global JACQUARD_SETTING
        global JACQUARD_REPEAT
        JACQUARD_REPEAT = int(self.root.ids.repeat_slider.value)
        self.root.ids.repeat_text.text = str(JACQUARD_REPEAT)
        if JACQUARD_REPEAT == 0:
            self.root.ids.repeat_text.text = 'Super Loop'

    def repeat_inc(self):
        global JACQUARD_PICK_INC
        global JACQUARD_REPEAT

        JACQUARD_REPEAT = JACQUARD_REPEAT + int(JACQUARD_PICK_INC)
        self.root.ids.repeat_text.text = str(JACQUARD_REPEAT )
        self.root.ids.repeat_slider.value = int(JACQUARD_REPEAT )

    def repeat_dec(self):
        global JACQUARD_PICK_INC
        global JACQUARD_REPEAT
        global JACQUARD_SETTING
        JACQUARD_REPEAT = JACQUARD_REPEAT - JACQUARD_PICK_INC
        if JACQUARD_REPEAT < 0:
            JACQUARD_REPEAT = 0
        elif JACQUARD_REPEAT > 1000:
            JACQUARD_REPEAT = 1000

        self.root.ids.repeat_text.text = str(JACQUARD_REPEAT)
        self.root.ids.repeat_slider.value = int(JACQUARD_REPEAT)
        if JACQUARD_REPEAT ==0:
            self.root.ids.repeat_text.text = 'Super Loop'

    def pick_slider(self):
        global JACQUARD_PICK
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "stop":       
            JACQUARD_PICK = int(self.root.ids.pick_slider.value)
            self.root.ids.pick_text.text = str(JACQUARD_PICK)
        else:    
            self.root.ids.pick_slider.value = str(JACQUARD_PICK)
            self.root.ids.pick_text.text = str(JACQUARD_PICK)

    def select_body_file(self, path, filename):
        try:
            print('{path}'.format(path = filename[0]))
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('BODY_IMAGE.bmp')
        except Exception:
            print("select File")

    def select_border_file(self, path, filename):
        try:
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('BORDER_IMAGE.bmp')
        except Exception:
            print("select File")

    def select_normal_file(self, path, filename):
        try:
            print('{path}'.format(path = filename[0]))
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('NORMAL_IMAGE.bmp')
        except Exception:
            print("select File")
            
    def saveall(self):
        global JACQUARD_SETTING
        global JACQUARD_REPEAT
        global CURRENT_REPEAT
        global JACQUARD_RUNNING_STATUS
        global JACQUARD_PICK
        global CURRENT_PICK
        
        CURRENT_PICK = JACQUARD_PICK
        JACQUARD_SETTING['JACQUARD_REPEAT'] = JACQUARD_REPEAT
        JACQUARD_RUNNING_STATUS['CURRENT_REPEAT'] = CURRENT_REPEAT
        JACQUARD_RUNNING_STATUS['CURRENT_PICK'] = CURRENT_PICK
        
        with open("JACQUARD_SETTING.txt", 'w') as f:
            f.write(str(JACQUARD_SETTING))
            f.close()
        with open("JACQUARD_RUNNING_STATUS.txt", 'w') as f:
            f.write(str(JACQUARD_RUNNING_STATUS))
            f.close()
            
    def update_settings(self):
        self.saveall()               
        self.initialization()
        
        
    def brightness_slider(self,value):
        global BRIGHTNESS
        global pi_pwm 
        BRIGHTNESS = int(value)
        print(type(BRIGHTNESS),BRIGHTNESS)
        pi_pwm.start(BRIGHTNESS)
        
    def save_running_status(self):
        global JACQUARD_RUNNING_STATUS
        global JACQUARD_PICK
        JACQUARD_RUNNING_STATUS = {"CURRENT_PICK":CURRENT_PICK,"CURRENT_REPEAT":CURRENT_REPEAT}
        with open("JACQUARD_RUNNING_STATUS.txt", 'w') as f:
            f.write(str(JACQUARD_RUNNING_STATUS))
            f.close()
    
    def shutdown(self):
        from subprocess import call
        call("sudo shutdown -h now", shell=True)
        
    def on_stop(self):
        self.save_running_status()
        self.shutdown()
        
def app_thread():
    Jacquaredgui().run()

_IoT_thread = threading.Thread(target = IoT_thread)

_App_thread = threading.Thread(target = app_thread)

#_IoT_thread.start()

_App_thread.start()
