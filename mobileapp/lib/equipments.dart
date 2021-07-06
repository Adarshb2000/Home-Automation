import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'globals.dart' as globals;

class BinaryButton extends StatefulWidget {
  final String equipment;
  final int roomNumber;
  BinaryButton({this.equipment, this.roomNumber});

  @override
  _BinaryButtonState createState() => _BinaryButtonState();
}

class _BinaryButtonState extends State<BinaryButton> {
  var color = globals.offColor;
  bool isOn = false;
  IconData icon;

  @override
  void initState() {
    super.initState();
    icon = globals.equipments[globals.equipmentCode[widget.equipment]]
        [globals.boolToInt(isOn)];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      width: 200,
      child: Card(
        color: color,
        child: InkWell(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                icon,
                size: 50,
              ),
              Text(
                widget.equipment,
              ),
            ],
          ),
          onTap: () => {
            isOn = !isOn,
            onTapFunction(),
          },
        ),
      ),
    );
  }

  void onTapFunction() {
    setState(() {
      color = (isOn) ? globals.onColor : globals.offColor;
      mqttTriger(globals.boolToInt(isOn));
      icon = globals.equipments[globals.equipmentCode[widget.equipment]]
          [globals.boolToInt(isOn)];
    });
  }

  void mqttTriger(int trigger) {
    int code = globals.equipmentCode[widget.equipment];
    String message = '';
    message = (code < 10) ? '0' + code.toString() : code.toString();
    globals.builder.addString(message + ' ' + trigger.toString());
    globals.client.publishMessage(
      'room' + widget.roomNumber.toString(),
      MqttQos.atMostOnce,
      globals.builder.payload,
    );
    globals.builder.clear();
  }
}

class AC extends StatefulWidget {
  final int roomNumber;
  AC(this.roomNumber);

  @override
  _ACState createState() => _ACState();
}

class _ACState extends State<AC> {
  bool isOn = false;
  Color tempInc = globals.offColor;
  Color tempDec = globals.offColor;
  Color acBackgroundColor = globals.offColor;
  int temperature = 0;

  final Map<int, Color> tempColor = {
    18: Colors.blue.shade100,
    19: Colors.blue.shade200,
    20: Colors.blue.shade400,
    21: Colors.green.shade100,
    22: Colors.green.shade200,
    23: Colors.yellow.shade400,
    24: Colors.yellow.shade800,
    25: Colors.orange.shade200,
    26: Colors.orange.shade300,
    27: Colors.orange.shade500,
    28: Colors.red.shade200,
    29: Colors.red.shade400,
    30: Colors.red.shade600,
    0: Colors.grey,
  };

  @override
  Widget build(BuildContext context) {
    return Card(
      color: acBackgroundColor,
      child: Column(
        children: [
          Expanded(
            flex: 8,
            child: Container(
              color: acBackgroundColor,
              padding: EdgeInsets.zero,
              width: 100000,
              child: Card(
                color: tempColor[temperature],
                child: InkWell(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        MdiIcons.airConditioner,
                        size: 35,
                        color: Colors.black,
                      ),
                      Text(
                        temperature.toString(),
                        style: TextStyle(
                          fontSize: 30,
                          color: Colors.black,
                        ),
                      ),
                    ],
                  ),
                  onTap: () => {
                    isOn = !isOn,
                    colorChange(),
                  },
                ),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.max,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Expanded(
                  flex: 1,
                  child: Container(
                    height: double.infinity,
                    child: Card(
                      color: tempDec,
                      child: InkWell(
                        child: Text(
                          'Temp-',
                          style: TextStyle(fontSize: 20),
                        ),
                        onTap: () => mqttTriger(a: '-'),
                      ),
                    ),
                  ),
                ),
                Expanded(
                  flex: 1,
                  child: Container(
                    height: double.infinity,
                    child: Card(
                      color: tempInc,
                      child: InkWell(
                        child: Container(
                          color: tempInc,
                          child: Text(
                            'Temp+',
                            style: TextStyle(fontSize: 20),
                          ),
                        ),
                        onTap: () =>
                            isOn ? mqttTriger(a: '+') : DoNothingAction(),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  void colorChange() {
    setState(() {
      if (isOn) {
        tempDec = Colors.blueAccent.shade400;
        tempInc = Colors.redAccent.shade400;
        acBackgroundColor = globals.onColor;
        mqttTriger(a: '1');
        temperature = 22;
      } else {
        acBackgroundColor = globals.offColor;
        tempDec = globals.offColor;
        tempInc = globals.offColor;
        mqttTriger(a: '0');
        temperature = 0;
      }
    });
  }

  void mqttTriger({String a, String b = ''}) {
    if (a == '+') {
      if (temperature < 30)
        setState(() {
          temperature += 1;
        });
    } else if (a == '-') {
      if (temperature > 18)
        setState(() {
          temperature -= 1;
        });
    }
    globals.builder.addString('04' + ' ' + a + ' ' + b);
    globals.client.publishMessage(
      'room' + widget.roomNumber.toString(),
      MqttQos.atMostOnce,
      globals.builder.payload,
    );
    globals.builder.clear();
  }
}
