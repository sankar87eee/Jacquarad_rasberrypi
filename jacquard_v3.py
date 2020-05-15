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
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '450')

aio = Client('sankar87eee', 'aio_BcjL967yMztvxoZkHT1i5hdRrdsz')

kivy.require('1.11.1')

"""
    Run_view Image, getdata, based on the pick input and pick number the array value is computed and stored as image.
"""

print('something')

JACQUARD_DESIGN_TOTAL_PICK =0
JACQUARD_MERGE = 0
JACQUARD_BORDER_BODY = 1
JACQUARD_REVERSE_ROW = 0
JACQUARD_REVERSE_COLUMN = 0
JACQUARD_PICK = 0
JACQUARD_PICK_INC = 1
JACQUARD_REPEAT = 0
JACQUARD_TOP_BOT_HEIGHT = 300

if JACQUARD_PICK <1: JACQUARD_PICK =1
elif JACQUARD_PICK > 1000000: JACQUARD_PICK = 1000000


JACQUARD_REPEAT = 0
if JACQUARD_REPEAT <1: JACQUARD_REPEAT =1
elif JACQUARD_REPEAT > 1000000: JACQUARD_REPEAT = 1000000

CURRENT_PICK =200
IMAGE_DIVIDE_SIZE = 100


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
        print(_feed1_value)
        print(type(_feed1_value))

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
    CURRENT_REPEAT = ObjectProperty(None)
    pass


class PopUp(Popup):
    def __init__(self, source_value):
        super().__init__()
        self.ids.view_image.source = source_value
        self.size_hint = 0.8, 0.6


class  View_Pick_Inc_BoxLayout(BoxLayout):

    global JACQUARD_PICK_INC

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

    def pic_inc_value(self, x):
        global JACQUARD_PICK_INC
        JACQUARD_PICK_INC = x
        print(JACQUARD_PICK_INC)

    def pick_inc(self):
        global JACQUARD_PICK_INC
        global JACQUARD_PICK
        JACQUARD_PICK = JACQUARD_PICK + JACQUARD_PICK_INC

        App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK)      # this is access root id from other class
        App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class

    def pick_dec(self):
        global JACQUARD_PICK_INC
        global JACQUARD_PICK
        JACQUARD_PICK = JACQUARD_PICK - JACQUARD_PICK_INC
        if JACQUARD_PICK < 0:
            JACQUARD_PICK = 0
        elif JACQUARD_PICK > 100000:
            JACQUARD_PICK = 100000
        App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK) # this is access root id from other class
        App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK) # this is access root id from other class


class BotImage(Widget):

    bot_image = ObjectProperty(None)
    bot_texture_size = ListProperty((0, 0))
    bot_texture_pos = ListProperty((0, 0))

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)

    def bot_bottom_image(self, dt):

        global JACQUARD_PICK
        global JACQUARD_TOP_BOT_HEIGHT
        global CURRENT_PICK
        global IMAGE_DIVIDE_SIZE
        img1 = cv2.imread('JACQUARD_DESIGN.bmp', 1)
        img = cv2.flip(img1, 0)
        # img = np.flipud(img)
        from kivy.core.window import Window
        img_height, img_width = img.shape[0], img.shape[1]
        window_width = Window.width
        window_height = Window.height
        if JACQUARD_PICK < img_height:
            if img_height - JACQUARD_PICK - JACQUARD_TOP_BOT_HEIGHT < 0:
                bot_image_start = 0
            else:
                bot_image_start = img_height - JACQUARD_PICK - JACQUARD_TOP_BOT_HEIGHT

            bot = img[bot_image_start: img_height - JACQUARD_PICK]
            bot_img = bot.tostring()
            bot_texture = Texture.create(size=(bot.shape[1], bot.shape[0]), colorfmt='rgb')
            bot_texture.blit_buffer(bot_img, colorfmt='rgb', bufferfmt='ubyte', size=(bot.shape[1], bot.shape[0]))
            self.bot_image = bot_texture
            self.bot_texture_size = (bot.shape[1]*window_width/800*1,bot.shape[0]*window_height/800*1)
            self.bot_texture_pos = (self.pos[0], 240-self.bot_texture_size[1]+self.pos[1])

            print('PPPPPPPPPPPPPOOOOOOOOOOSSSSSSSSSSSS', self.height,self.size,'texture size',self.bot_texture_size,'type',type(self.pos[0]))
        else:
            JACQUARD_PICK =0
            App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK)  # this is access root id from other class
            App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK)  # this is access root id from other class


class TopImage(Widget):

    top_image = ObjectProperty(None)
    bot_image = ObjectProperty(None)
    top_texture_size = ListProperty((0,0))
    top_texture_pos = ListProperty((0,0))
    def __init__(self,**kwargs):
        Widget.__init__(self, **kwargs)

    def top_bottom_image(self, dt):
        global JACQUARD_PICK
        global JACQUARD_TOP_BOT_HEIGHT
        print('top image clock')
        global CURRENT_PICK
        global IMAGE_DIVIDE_SIZE
        img1 = cv2.imread('JACQUARD_DESIGN.bmp', 1)
        img = cv2.flip(img1, 0)
        #img = np.flipud(img)
        from kivy.core.window import Window
        img_height, img_width = img.shape[0], img.shape[1]
        window_width = Window.width
        window_height = Window.height

        if JACQUARD_PICK <= img_height:
            top = img[img_height-JACQUARD_PICK: img_height -JACQUARD_PICK + JACQUARD_TOP_BOT_HEIGHT]
            top_img = top.tostring()
            top_texture = Texture.create(size=(top.shape[1], top.shape[0]), colorfmt='rgb')
            top_texture.blit_buffer(top_img, colorfmt='rgb', bufferfmt='ubyte',size=(top.shape[1], top.shape[0]))
            self.top_image = top_texture
            self.top_texture_size = (top.shape[1]*window_width/800*1, top.shape[0]*window_height/480*1)
        else:
            JACQUARD_PICK =0
            App.get_running_app().root.ids.pick_text.text = str(JACQUARD_PICK)  # this is access root id from other class
            App.get_running_app().root.ids.pick_slider.value = int(JACQUARD_PICK)  # this is access root id from other class
            ##############


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
        global JACQUARD_DESIGN_BODY
        global JACQUARD_DESIGN_BODY_BORDER_MERGE
        global JACQUARD_DESIGN_MERGE
        global JACQUARD_DESIGN
        global JACQUARD_DESIGN_TOTAL_PICK
        try:
            JACQUARD_SETTING = {'JACQUARD_TYPE': 'MERGE', 'JACQUARD_INVERT': 'OFF',
                                'JACQUARD_REVERSE_ROW': 'OFF', 'JACQUARD_REVERSE_COL': 'OFF', 'JACQUARD_REPEAT': 0}
            JACQUARD_DESIGN_BODY = cv2.imread("JACQUARD_DESIGN_BODY.bmp")  # Importing the jacquard design
            JACQUARD_DESIGN_BODY_BORDER_MERGE = cv2.imread(
                "JACQUARD_DESIGN_BODY_BORDER_MERGE.bmp")  # Importing the jacquard design
            JACQUARD_DESIGN_MERGE = cv2.imread("JACQUARD_DESIGN_MERGE.bmp")  # Importing the jacquard design
            JACQUARD_DESIGN = cv2.imread("JACQUARD_DESIGN_MERGE.bmp")  # Importing the jacquard design
            JACQUARD_DESIGN_TOTAL_PICK = JACQUARD_DESIGN.shape[0]
        except Exception:
            print('Error')

        with open("JACQUARD_SETTING.txt", 'r') as f:
            JACQUARD_SETTING = eval(f.read())
            # f.write(str(JACQUARD_SETTING))
            f.close()

    def on_start(self):
        global JACQUARD_SETTING
        global JACQUARD_REPEAT
        global JACQUARD_DESIGN_TOTAL_PICK
        self.initialization()
        # Home Screen Update and initialization
        #read JACQUARD_DESIGN, find hight and width display in home page
        self.root.ids.total_repeat.text= str(JACQUARD_SETTING['JACQUARD_REPEAT'])
        self.root.ids.total_pick.text = str(JACQUARD_DESIGN_TOTAL_PICK)
        # Menu screen update and initialization
        JACQUARD_REPEAT = JACQUARD_SETTING['JACQUARD_REPEAT']
        self.root.ids.repeat_text.text = str(JACQUARD_REPEAT)
        self.root.ids.repeat_slider.value = int(JACQUARD_REPEAT)
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "MERGE":
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.merge_file.background_color = (0.4, 1, 0.4, 1)
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.merge_file.background_color = (1, 0.4, 0.4, 1)

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

    def on_press_start(self,  status_bar, status_label):
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "stop":
            JACQUARD_START_STOP = "start"
            self.event1 = Clock.schedule_interval(self.root.ids.topimage.top_bottom_image, 1/10)
            self.event2 = Clock.schedule_interval(self.root.ids.botimage.bot_bottom_image, 1/10)
            status_bar.canvas_status = [0, 0.5, 0, 1]
            status_label.text = "STATUS: ON"

    def on_press_stop(self, status_bar, status_label):
        global JACQUARD_START_STOP
        if JACQUARD_START_STOP == "start":
            JACQUARD_START_STOP = "stop"
            self.event1.cancel()
            self.event2.cancel()
            status_bar.canvas_status = [0.5, 0, 0, 1]
            status_label.text = "STATUS: OFF"

        #############################################

    def on_press_bodyborderfile(self):
        global JACQUARD_BORDER_BODY
        global JACQUARD_MERGE
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "MERGE":
            JACQUARD_SETTING['JACQUARD_TYPE'] = "BODY_BORDER"
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.merge_file.background_color = (1, 0.4, 0.4, 1)
        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            self.root.ids.body_border_file.background_color = (0.4, 1, 0.4, 1)
            self.root.ids.merge_file.background_color = (1, 0.4, 0.4, 1)

    def on_press_mergefile(self):

        global JACQUARD_SETTING

        if JACQUARD_SETTING['JACQUARD_TYPE'] == "BODY_BORDER":
            JACQUARD_SETTING['JACQUARD_TYPE'] = "MERGE"
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.merge_file.background_color = (0.4, 1, 0.4, 1)
        elif JACQUARD_SETTING['JACQUARD_TYPE'] == "MERGE":
            self.root.ids.body_border_file.background_color = (1, 0.4, 0.4, 1)
            self.root.ids.merge_file.background_color = (0.4, 1, 0.4, 1)

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

    def on_touch_down(self):
        pass
    
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
                print('select .bmp file')
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
        JACQUARD_SETTING['JACQUARD_REPEAT'] = int(self.root.ids.repeat_slider.value)
        self.root.ids.repeat_text.text = str(JACQUARD_SETTING['JACQUARD_REPEAT'])
        if JACQUARD_SETTING['JACQUARD_REPEAT'] == 0:
            self.root.ids.repeat_text.text = 'Super Loop'

    def checkfun(self):
        global JACQUARD_PICK_INC
        print('checkfun',JACQUARD_PICK_INC)

    def repeat_inc(self):
        global JACQUARD_PICK_INC
        global JACQUARD_REPEAT

        JACQUARD_SETTING['JACQUARD_REPEAT'] = JACQUARD_SETTING['JACQUARD_REPEAT'] + int(JACQUARD_PICK_INC)
        self.root.ids.repeat_text.text = str(JACQUARD_SETTING['JACQUARD_REPEAT'] )
        self.root.ids.repeat_slider.value = int(JACQUARD_SETTING['JACQUARD_REPEAT'] )

    def repeat_dec(self):
        global JACQUARD_PICK_INC
        global JACQUARD_REPEAT
        global JACQUARD_SETTING
        JACQUARD_SETTING['JACQUARD_REPEAT'] = JACQUARD_SETTING['JACQUARD_REPEAT'] - JACQUARD_PICK_INC
        if JACQUARD_SETTING['JACQUARD_REPEAT'] < 0:
            JACQUARD_SETTING['JACQUARD_REPEAT'] = 0
        elif JACQUARD_SETTING['JACQUARD_REPEAT'] > 1000:
            JACQUARD_SETTING['JACQUARD_REPEAT'] = 1000

        self.root.ids.repeat_text.text = str(JACQUARD_SETTING['JACQUARD_REPEAT'])
        self.root.ids.repeat_slider.value = int(JACQUARD_SETTING['JACQUARD_REPEAT'])
        if JACQUARD_SETTING['JACQUARD_REPEAT'] ==0:
            self.root.ids.repeat_text.text = 'Super Loop'


    def pick_slider(self):
        global JACQUARD_PICK
        JACQUARD_PICK = int(self.root.ids.pick_slider.value)
        self.root.ids.pick_text.text = str(JACQUARD_PICK)


    def select_body_file(self, path, filename):
        try:
            print('{path}'.format(path = filename[0]))
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('JACQUARD_DESIGN_BODY.bmp')
        except Exception:
            print("select File")

    def select_border_file(self, path, filename):
        try:
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('JACQUARD_DESIGN_BOARDER.bmp')
        except Exception:
            print("select File")


    def select_merge_file(self, path, filename):
        try:
            print('{path}'.format(path = filename[0]))
            image_file = PILImage.open(filename[0])  #change it to the selected file path
            image_file = image_file.convert('L')  # convert image to monochrome - this works
            image_file = image_file.convert('1')  # convert image to black and white
            image_file.save('JACQUARD_DESIGN_MERGE.bmp')
        except Exception:
            print("select File")

    def update_settings(self):
        global JACQUARD_SETTING
        global JACQUARD_REPEAT
        JACQUARD_REPEAT = JACQUARD_SETTING['JACQUARD_REPEAT']
        with open("JACQUARD_SETTING.txt", 'w') as f:
            f.write(str(JACQUARD_SETTING))
            f.close()
        print(JACQUARD_SETTING)
        self.on_start()

def app_thread():
    Jacquaredgui().run()




_IoT_thread = threading.Thread(target=IoT_thread)

_App_thread = threading.Thread(target=app_thread)


#_IoT_thread.start()
_App_thread.start()