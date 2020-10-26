from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer, MDToolbar
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.screen import Screen
from kivymd.uix.button import Button, MDFlatButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.switch import Switch
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.popup import Popup
from functools import partial
import paho.mqtt.client as mqtt
from time import time

Config.set('graphics', 'resizable', True)


# Variables
username = "root_system0"
password = "random.random()"


class cardButton(MDCard, Button):
    pass


class AcFeatures(MDGridLayout):
    pass
        


class Room(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Main screen layout
        screen_layout = MDGridLayout()
        screen_layout.cols = 2
        screen_layout.md_bg_color = [0, 1, 1, 1]

        # AC region
        self.timer = 0
        new_layout = MDFloatLayout()
        self.new_card = MDCard(
            orientation='vertical',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        self.new_card.md_bg_color = app.off_red
        ac_image = Image(
            source='static/ac1.png',
        )
        ac_image.size_hint_y = 0.9
        
        ac_image.pos_hint = {'top': 1.0, 'center_x' : 0.5}
        self.new_card.radius = [4] * 4

        # ac_button.bind(active=callback)
        self.new_card.add_widget(ac_image)
        self.new_card.on_press = self.ac_touch_down
        self.new_card.on_release = self.ac_touch_up
        temp = MDLabel(text='18ºC')
        temp.font_size = 10
        temp.size = (0.25, 1)
        temp.color = [1, 1, 1, 1]
        new_layout.add_widget(self.new_card)
        screen_layout.add_widget(new_layout)

        
        self.ac_popup = Popup(
            title = 'AC settings',
            content=AcFeatures(),
            size_hint = (0.75, 0.75)
        )
        self.ac_popup.background_color = [i / 255 for i in [137, 205, 211]] + [1]
        #self.ac_popup.on_open = self.faltu

        #--------------------------------------------------------------#


        # Light setup
        new_layout = MDFloatLayout()
        self.light_card = MDCard(
            orientation='horizontal',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        self.light_card.md_bg_color = app.dark_color
        light_image = Image(
            source='static/light1.png',
            size_hint=(1, 1),
        )
        self.light_card.on_press = self.light_change
        self.light_card.add_widget(light_image)
        new_layout.add_widget(self.light_card)
        screen_layout.add_widget(new_layout)



        screen_layout.add_widget(Button(text='TODO'))
        screen_layout.add_widget(Button(text='TODO'))
        screen_layout.add_widget(Button(text='TODO'))
        screen_layout.add_widget(Button(text='TODO'))
        screen_layout.add_widget(Button(text='TODO'))
        screen_layout.add_widget(Button(text='TODO'))
        self.add_widget(screen_layout)

    def faltu(self, *args):
        self.image_box.md_bg_color = self.new_card.md_bg_color

    def ac_touch_down(self, *args):
        self.timer = time()
        
    
    def ac_touch_up(self, *args):
        if (time() - self.timer > 0.5):
            self.ac_popup.open()
        else:
            app.switch(0, 'ac', 1)
            self.new_card.md_bg_color = app.on_green if self.new_card.md_bg_color == app.off_red else app.off_red 
        self.timer = 0

    def button_change(self, btn, *args):
        if btn.background_color == [0, 0, 0, 1]:
            btn.background_color = [1, 1, 1, 1]
            btn.color = [0, 0, 0, 1]
        else:
            btn.background_color = [0, 0, 0, 1]
            btn.color = [1, 1, 1, 1]
    
    def light_change(self, *args):
        if self.light_card.md_bg_color == app.dark_color:
            self.light_card.md_bg_color = app.light_color
        else:
            self.light_card.md_bg_color = app.dark_color
        app.switch(0, 'light')

    def button_behaviour(self, button, state):
        pass

# Main box layout inside which everthing is present
class MainScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        # Standard requirements
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Main code inside build
        self.build()

    # Main code
    def build(self):

        # Starting toolbar for navigation
        self.toolbar = MDToolbar(pos_hint={'top': 1}, elevation=10)
        self.toolbar.title = self.sm.current
        self.add_widget(self.toolbar)

        # Navigation layout start
        #nav_layout = NavigationLayout()

        # Screens for each and every room
        sm = ScreenManager()

        # My room (room 0)
        screen = Screen(name='0')
        screen.add_widget(Room())
        sm.add_widget(screen)


class RoomApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.equipments_dict = {
            'light' : '12',
            'fan' : '13',
            'extra' : '14',
            'ac' : '4'
        }
    def build(self):
        self.theme_cls.primary_palette = 'Green'

        # Colors
        self.dark_color = [i / 255 for i in [50] * 3] + [1]
        self.light_color = [i / 255 for i in [240, 240, 240]] + [1]
        self.on_green = [i / 255 for i in [46, 139, 87]] + [1]
        self.off_red = [i / 255 for i in [220, 20, 60]] + [0.99]


        # Connection to home server
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)

        self.client.connect('192.168.29.148', 1883, 60)
        self.client.publish('test', '1, 1')
        
        


        # Way to lithargic to create everything here
        return Room()
        # ---------------------------------------------------------------- #

    def switch(self, room, equipment, ac_code=None):
        self.client.publish('room' + str(room) + '/' + self.equipments_dict[equipment], ac_code)



if __name__ == "__main__":
    app = RoomApp()
    app.run()
