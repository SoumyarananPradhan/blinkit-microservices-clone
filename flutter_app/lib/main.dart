import 'package:flutter/material.dart';
import 'screens/home_screen.dart'; // <-- CHANGED THIS LINE

void main() {
  runApp(const BlinkitCloneApp());
}

class BlinkitCloneApp extends StatelessWidget {
  const BlinkitCloneApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Blinkit Clone',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: Colors.grey[50],
      ),
      home: const HomeScreen(), // <-- CHANGED THIS LINE
    );
  }
}
