from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

def on_message(*args):
    global reed, thermal, thermal_active
    topic = args[2].topic
    message = str(args[2].payload)

    if topic == 'test/0':
        reed = int(message[-2])
    elif topic == 'test/1':
        thermal = int(message[-2])
    else:
        thermal_active = int(message[-2])


app = Flask(__name__)
client = mqtt.Client()
client.username_pw_set('test', '123')
client.connect('192.168.29.148')
client.subscribe('test/#')
client.on_message = on_message
client.loop_start()

app.templates_auto_reload = True

reed = True
thermal = False
thermal_active = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_info')
def update_info():
    global reed, thermal, thermal_active
    return jsonify(reed=reed, thermal=thermal, thermal_active=thermal_active)


if __name__ == "__main__":
    app.run(host='192.168.29.148', debug=True)