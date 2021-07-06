import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/MQTTconnection.dart';

class BootScreen extends StatelessWidget {
  final Function connected;
  BootScreen(this.connected) {
    final client = MyMqttClient(
      callbackfunction: connected,
    );
    client.connect();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(
              height: 20,
            ),
            Text(
              "Connecting to the Server...",
              style: TextStyle(fontSize: 20),
            ),
            // ElevatedButton(
            //   child: Text('Hello World'),
            //   onPressed: () {
            //     Navigator.pop(context);
            //     Navigator.pushNamed(context, '/');
            //     Navigator.pop(context);
            //   },
            // ),
          ],
        ),
      ),
    );
  }
}
