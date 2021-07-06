import 'package:flutter/material.dart';
import 'equipments.dart';
import 'globals.dart' as globals;

class Room extends StatefulWidget {
  final int roomNumber;

  Room({this.roomNumber});

  @override
  _RoomState createState() => _RoomState();
}

class _RoomState extends State<Room> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueAccent.shade200,
      appBar: AppBar(
        title: Text(globals.rooms[widget.roomNumber]),
      ),
      body: GridView.count(
        mainAxisSpacing: 25,
        crossAxisSpacing: 25,
        crossAxisCount: 2,
        padding: EdgeInsets.all(25),
        children: [
          BinaryButton(
            equipment: 'Light',
            roomNumber: widget.roomNumber,
          ),
          BinaryButton(
            equipment: 'Fan',
            roomNumber: widget.roomNumber,
          ),
          AC(widget.roomNumber),
        ],
      ),
    );
  }
}
