from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.button import Button as btn
from kivy.clock import Clock
from functools import partial

colors = {
    'off_red': [i / 255 for i in [220, 20, 60]] + [0.99],
    'on_green': [i / 255 for i in [46, 139, 87]] + [1],
    'light_color': [i / 255 for i in [240, 240, 240]] + [1],
    'dark_color': [i / 255 for i in [50] * 3] + [1],
    'warm_color': [i / 255 for i in [246, 205, 139]] + [1],
    'cold_color': [i / 255 for i in [136, 199, 220]] + [1]
}


class AcCard(MDCard):
    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        # Setup
        self.orientation = 'vertical'
        self.padding = '5dp'
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size_hint = size
        self.radius = [4] * 4

        self.build()

    # Build
    def build(self):
        # Image
        ac_image = Image(source='static/ac1.png')
        ac_image.size_hint = (1.25, 1.5)
        ac_image.pos_hint = {'center_x': 0.5}
        self.add_widget(ac_image)

        # Details
        details_box = MDBoxLayout(orientation='horizontal', size_hint_y=0.5)
        self.temprature = MDLabel(text='18°C')
        self.temprature.color = [1] * 4
        self.fan_speed = MDLabel(text='Fan: 2')
        self.fan_speed.color = [1] * 4
        details_box.add_widget(self.temprature)
        details_box.add_widget(self.fan_speed)
        self.add_widget(details_box)

    def temperature_change(self, change):
        self.temprature.text = str(
            int(str(self.temprature.text).split('°')[0]) + (-1) ** (~change)) + '°C'
        print(self.temprature.text)


class Buttonn(MDCard):
    def __init__(self, text, color, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '5dp'
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size_hint = (0.75, 0.75)
        self.md_bg_color = color

        self.add_widget(MDLabel(text=text))


class AcPopup(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.build()

    def build(self):

        # AC Card
        self.ac_card = AcCard((0.5, 0.5))
        self.add_widget(self.ac_card)

        # all the features for ac
        features_layout = MDGridLayout()
        features_layout.cols = 2

        # Temp incease, decrease
        new_box_layout = MDFloatLayout()
        dec_button = Buttonn('temp-', colors['cold_color'])
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
        inc_button.md_bg_color = ['warm_color']
        inc_button.add_widget(MDLabel(text='Temp+'))
        inc_button.id = 'temp+'
        inc_button.on_press = partial(self.ac_features_send, inc_button)
        new_box_layout.add_widget(inc_button)
        features_layout.add_widget(new_box_layout)

        features_layout.add_widget(btn(text='TODO'))
        features_layout.add_widget(btn(text='TODO'))
        features_layout.add_widget(btn(text='TODO'))
        features_layout.add_widget(btn(text='TODO'))

        self.add_widget(features_layout)

    def ac_features_send(self, feature):
        self.button_behaviour(feature, feature.md_bg_color, 0)
        if feature.id.startswith('temp'):
            from main import RoomApp
            app = RoomApp()
            app.switch(0, 'ac', feature.id[-1])

    def button_behaviour(self, button, color, state, time=None):
        temp = color.copy()
        if not state:
            Clock.schedule_once(
                partial(self.button_behaviour, button, temp, 1), 0.05)
            button.md_bg_color = [0.5, 0.5, 0.5, 1]
        else:
            button.md_bg_color = color
