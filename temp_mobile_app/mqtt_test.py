import paho.mqtt.client as mqtt
from random import randint as rint

def on_message(client, userdata, message):
    print(message.topic, str(message.payload))

client = mqtt.Client()

client.username_pw_set('test', '123')

client.connect('192.168.29.148')
client.on_message = on_message

client.subscribe('test/#')

client.loop_forever()