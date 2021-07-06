import 'package:flutter/material.dart';
import 'package:mobileapp/boot_screen.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'room.dart';

void main() {
  final app = MyApp();
  runApp(app);
}

void toast(message) {
  Fluttertoast.showToast(msg: message);
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HelloWorld',
      themeMode: ThemeMode.dark,
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        accentColor: Colors.blueAccent,
      ),
      initialRoute: '/boot_screen',
      routes: {
        '/': (context) => MainScreen(),
        '/boot_screen': (context) => BootScreen(
              () => {
                Navigator.pop(context),
                // Navigator.pushNamed(context, '/room'),
              },
            ),
        '/room': (_) => Room(),
        '/room0': (_) => Room(
              roomNumber: 0,
            ),
      },
    );
  }
}

class MainScreen extends StatelessWidget {
  // final List<Room> rooms;
  // final ValueChanged<Room> onTapped;

  // MainScreen({this.rooms, this.onTapped});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Room"),
      ),
      body: ListView(
        children: [
          ListTile(
            title: Text('Adarsh'),
            onTap: () {
              Navigator.pushNamed(context, '/room0');
            },
          ),
          ListTile(
            title: Text('Room1'),
          ),
          ListTile(
            title: Text('Room2'),
          ),
        ],
      ),
    );
  }
}
