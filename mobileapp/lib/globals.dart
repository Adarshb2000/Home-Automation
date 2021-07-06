import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';

MqttServerClient client;

final builder = MqttClientPayloadBuilder();

final Color onColor = Colors.green.shade600;

final Color offColor = Colors.grey.shade400;

Map<String, int> equipmentCode = {
  'Light': 12, // D6
  'Fan': 13,
  'Bulb': 14, // D5
  'Extra': 5,
  'AC': 4
};

Map<int, List<IconData>> equipments = {
  12: [MdiIcons.lightbulbOff, MdiIcons.lightbulbOn],
  13: [MdiIcons.fromString('fan_off'), MdiIcons.fromString('fan')],
};

Map<int, String> rooms = {
  0: 'Adarsh',
  1: 'Mummy Papa',
  2: 'Shubhi Di',
  3: 'Hall',
  4: 'Extras',
};

int boolToInt(bool boolean) {
  return (boolean) ? 0 : 1;
}

final String host = '192.168.29.202';
final String username = 'root';
final String password = 'Python.random.random';
final String identifier = 'My Android';
