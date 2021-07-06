import 'package:flutter/cupertino.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'globals.dart' as globals;

class MyMqttClient {
  String host = globals.host;
  String username = globals.username;
  String password = globals.password;
  String identifier = globals.identifier;
  Function callbackfunction;
  MqttConnectionState state = MqttConnectionState.disconnected;

  MyMqttClient({
    @required this.callbackfunction,
  }) {
    globals.client = MqttServerClient(host, identifier);
    globals.client.port = 1883;
    globals.client.keepAlivePeriod = 60;
    // globals.client.logging(on: false);
    // globals.client.secure = true;

    globals.client.onConnected = callbackfunction;
    globals.client.onDisconnected = onDisconnected;
  }

  void connect() async {
    assert(globals.client != null);
    try {
      await globals.client.connect(globals.username, globals.password);
    } catch (e) {
      print(e);
      state = MqttConnectionState.disconnected;
      globals.client.disconnect();
    }
  }

  void onDisconnected() {}
}
