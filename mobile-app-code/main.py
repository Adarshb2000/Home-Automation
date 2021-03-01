from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.stacklayout import MDStackLayout
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
from kivy.clock import Clock
from functools import partial
import paho.mqtt.client as mqtt
from time import time

Config.set('graphics', 'resizable', True)


# Variables
username = "username"
password = "password"


class AcCard(MDCard):
    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '5dp'
        self.pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        self.size_hint = size
        self.radius = [4] * 4
        self.md_bg_color = app.off_red

        self.build()

    def build(self):
        self.add_widget(Image(source='static/ac1.png'))


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
        self.new_card = AcCard((0.75, 0.75))

        # Details
        details_box = MDGridLayout(size_hint_y = 0.25)
        details_box.cols = 1
        self.temperature_label = MDLabel(text='18°C', pos_hint={'center_x' : 0.5})
        self.temperature_label.font_size = 20
        self.temperature_label.size = (0.25, 1)
        self.temperature_label.color = [1, 1, 1, 1]
        details_box.add_widget(self.temperature_label)
        self.new_card.add_widget(details_box)

        self.new_card.on_press = self.ac_touch_down
        self.new_card.on_release = self.ac_touch_up
        new_layout.add_widget(self.new_card)
        screen_layout.add_widget(new_layout)

        # AC POPUP
        #--------------------------------#
        popup_layout = MDGridLayout()
        popup_layout.cols = 1

        
        self.image_box = AcCard((0.5, 0.5))
        popup_layout.add_widget(self.image_box)


        # all the features for ac
        features_layout = MDGridLayout()
        features_layout.cols = 2

        # Temp incease, decrease
        new_box_layout = MDFloatLayout()
        dec_button = MDCard(
            orientation='vertical',
            padding='5dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        dec_button.id = 'temp-'
        dec_button.md_bg_color = [i / 255 for i in [136, 199, 220]] + [1]
        dec_button.add_widget(MDLabel(text='Temp-'))
        new_box_layout.add_widget(dec_button)
        dec_button.on_press = partial(self.ac_features_send, dec_button)
        features_layout.add_widget(new_box_layout)
        
        new_box_layout = MDFloatLayout()
        inc_button = MDCard(
            orientation='vertical',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        inc_button.md_bg_color = [i / 255 for i in [246, 205, 139]] + [1]
        inc_button.add_widget(MDLabel(text='Temp+'))
        inc_button.id = 'temp+'
        inc_button.on_press = partial(self.ac_features_send, inc_button)
        new_box_layout.add_widget(inc_button)
        features_layout.add_widget(new_box_layout)

        #-----------------#
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        features_layout.add_widget(Button(text='TODO'))
        
        popup_layout.add_widget(features_layout)
        self.ac_popup = Popup(
            title = 'AC settings',
            size_hint = (.75, .75)
        )
        self.ac_popup.content = popup_layout
        self.ac_popup.background_color = [i / 255 for i in [137, 205, 211]] + [1]

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

    def ac_touch_down(self, *args):
        self.timer = time()
        
    
    def ac_touch_up(self, popup = False, *args):
        if (time() - self.timer > 0.5) and not popup:
            self.ac_popup.open()
        else:
            color = self.new_card.md_bg_color
            if color == app.off_red:
                app.switch(0, 'ac', 1)
                self.new_card.md_bg_color = self.image_box.md_bg_color = app.on_green
            else:
                app.switch(0, 'ac', 0)
                self.new_card.md_bg_color = self.image_box.md_bg_color = app.off_red
        self.timer = 0

    def button_change(self, btn, *args):
        if btn.background_color == [0, 0, 0, 1]:
            btn.background_color = [1, 1, 1, 1]
            btn.color = [0, 0, 0, 1]
        else:
            btn.background_color = [0, 0, 0, 1]
            btn.color = [1, 1, 1, 1]
    
    def ac_features_send(self, feature):
        self.button_behaviour(feature, feature.md_bg_color, 0)
        if feature.id.startswith('temp'):
            app.switch(0, 'ac', feature.id[-1])
    
    def light_change(self, *args):
        if self.light_card.md_bg_color == app.dark_color:
            self.light_card.md_bg_color = app.light_color
        else:
            self.light_card.md_bg_color = app.dark_color
        app.switch(0, 'light')

    def button_behaviour(self, button, color, state, time=None):
        temp = color.copy()
        if not state:
            Clock.schedule_once(partial(self.button_behaviour, button, temp, 1), 0.05)
            button.md_bg_color = [0.5, 0.5, 0.5, 1]
        else:
            button.md_bg_color = color

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
