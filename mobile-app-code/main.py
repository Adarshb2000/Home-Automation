from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer, MDToolbar
from kivymd.uix.card import MDCard
from kivy.uix.switch import Switch
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import Button, MDFlatButton, MDFloatingActionButton, MDIconButton
from kivy.uix.image import Image
from kivymd.uix.slider import MDSlider
from kivymd.toast import toast
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivy.config import Config
from functools import partial
import paho.mqtt.client as mqtt

Config.set('graphics', 'resizable', True)


# Variables
username = "root_system0"
password = "random.random()"


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
        new_layout = MDFloatLayout()
        new_card = MDCard(
            orientation='horizontal',
            padding='10dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.75, 0.75),
        )
        new_card.md_bg_color = [i / 255 for i in [220, 20, 60]] + [1]
        ac_image = Image(
            source='static/ac1.png',
            size_hint=(0.9, 0.9),
        )
        ac_image.pos_hint = {'top': 1.0}
        new_card.radius = [5] * 4

        # ac_button.bind(active=callback)
        new_card.add_widget(ac_image)
        new_layout.add_widget(new_card)
        screen_layout.add_widget(new_layout)

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
        self.light_card.on_touch_down = self.light_change
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

    def timer_popup(self, *args):
        pass

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


        # Connection to home server
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)

        self.client.connect('192.168.29.148', 1883, 60)
        self.client.publish('test', 'test')
        
        


        # Way to lithargic to create everything here
        return Room()
        # ---------------------------------------------------------------- #

    def switch(self, room, equipment, ac_code=None):
        self.client.publish('room' + str(room) + '/' + self.equipments_dict[equipment], ac_code)



if __name__ == "__main__":
    app = RoomApp()
    app.run()
