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


class Room(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Main screen layout
        screen_layout = MDGridLayout()
        screen_layout.cols = 2
        screen_layout.md_bg_color = [0, 1, 1, 1]

        """trye = MDBoxLayout()
        trye.md_bg_color = [0, 1, 1, 1]
        trye.orientation = 'vertical'
        trye.padding = '50dp'
        ac_col = MDBoxLayout()
        ac_col.padding = '20dp'
        ac_col.pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        ac_col.orientation = 'vertical'
        def callback(instance, value):
            if value:
                ac_col.md_bg_color = [i / 255 for i in [46, 139, 87]] + [1]
            else:
                ac_col.md_bg_color = [i / 255 for i in [220, 20, 60]] + [0.99] 
        ac_logo_layout = MDGridLayout()
        ac_logo_layout.padding = 0, '1dp', '5dp', 0
        ac_logo_layout.cols = 1
        ac_logo_layout.size_hint_y = 0.5
        ac_image = Image(source='static/ac1.png')
        ac_logo_layout.add_widget(ac_image)
        ac_col.add_widget(ac_logo_layout)
        ac_col.md_bg_color = [i / 255 for i in [220, 20, 60]] + [1]
        ac_button_col = MDGridLayout()
        ac_button_col.pos_hint = {'center_x' : 0.5}
        ac_button_col.cols = 3
        ac_button_col.size_hint = (0.5, 0.1)
        ac_button_col.add_widget(MDLabel(text='OFF', pos_hint={'x' : 0.5}, text_size='5dp'))
        ac_button = MDSwitch(active=False)
        ac_button.bind(active=callback)
        ac_button.pos_hint = {'bottom' : 1, 'center_x' : 0.5}
        ac_button.size_hint_x = 1
        #ac_col.add_widget(ac_button)
        ac_button_col.add_widget(ac_button)
        ac_button_col.add_widget(MDLabel(text='    ON', pos_hint={'center_x' : 0.5}))
        ac_col.add_widget(ac_button_col)
        trye.add_widget(ac_col)
        screen_layout.add_widget(trye)
"""

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
            size_hint = (.75, .75)
        )
        self.ac_popup.background_color = [i / 255 for i in [137, 205, 211]] + [1]
        popup_layout = MDGridLayout()

        # AC image
        self.image_box = MDBoxLayout(orientation='vertical')
        popup_layout.cols = 1
        ac_image1 = Image(
            source='static/ac1.png',
            size_hint=(0.9, 0.9),
        )
        ac_image1.pos_hint = {'top' : 1}
        self.image_box.size_hint = (0.5, 0.5)
        self.image_box.add_widget(ac_image1)
        self.image_box.add_widget(MDLabel(text='18ºC'))
        popup_layout.add_widget(self.image_box)
        self.ac_popup.on_open = self.faltu


        # all the features for ac
        features_layout = MDGridLayout()
        features_layout.cols = 2

        # Temp incease, decrease
        new_box_layout = MDBoxLayout(orientation='vertical')
        inc_button = MDCard(
            orientation='horizontal',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        inc_button.md_bg_color = [i / 255 for i in [246, 205, 139]] + [1]
        inc_button.add_widget(MDLabel(text='Temp+'))
        dec_button = MDCard(
            orientation='horizontal',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        dec_button.md_bg_color = [i / 255 for i in [136, 199, 220]] + [1]
        dec_button.add_widget(MDLabel(text='Temp-'))
        features_layout.add_widget(inc_button)
        features_layout.add_widget(dec_button)


        #-----------------#
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        
        popup_layout.add_widget(features_layout)
        self.ac_popup.content = popup_layout

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
