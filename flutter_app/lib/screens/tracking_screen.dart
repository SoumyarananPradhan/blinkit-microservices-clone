import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'home_screen.dart';

class TrackingScreen extends StatefulWidget {
  final String orderId;
  const TrackingScreen({super.key, required this.orderId});

  @override
  State<TrackingScreen> createState() => _TrackingScreenState();
}

class _TrackingScreenState extends State<TrackingScreen> {
  String _status = "Loading...";
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _fetchStatus();
    // Poll the backend every 3 seconds
    _timer = Timer.periodic(
      const Duration(seconds: 3),
      (timer) => _fetchStatus(),
    );
  }

  @override
  void dispose() {
    _timer?.cancel(); // Stop polling when we leave the screen
    super.dispose();
  }

  Future<void> _fetchStatus() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8004/track/${widget.orderId}'),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _status = data['status'];
        });
      }
    } catch (e) {
      print("Tracking Error: $e");
    }
  }

  // Simple UI helper for the timeline
  Widget _buildTimelineStep(String stepName, bool isComplete) {
    return Row(
      children: [
        Icon(
          isComplete ? Icons.check_circle : Icons.radio_button_unchecked,
          color: isComplete ? Colors.green : Colors.grey,
          size: 30,
        ),
        const SizedBox(width: 15),
        Text(
          stepName,
          style: TextStyle(
            fontSize: 18,
            fontWeight: isComplete ? FontWeight.bold : FontWeight.normal,
            color: isComplete ? Colors.black : Colors.grey,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    // Determine which steps are complete based on current status
    int statusLevel = 0;
    if (_status == "PLACED") statusLevel = 1;
    if (_status == "PACKED") statusLevel = 2;
    if (_status == "OUT_FOR_DELIVERY") statusLevel = 3;
    if (_status == "DELIVERED") statusLevel = 4;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Track Order"),
        backgroundColor: Colors.yellow[700],
        leading: IconButton(
          icon: const Icon(Icons.home),
          onPressed: () => Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(builder: (context) => const HomeScreen()),
            (route) => false,
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Order ID:", style: TextStyle(color: Colors.grey[600])),
            Text(
              widget.orderId,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 40),

            _buildTimelineStep("Order Placed", statusLevel >= 1),
            Container(
              height: 30,
              width: 2,
              color: statusLevel >= 2 ? Colors.green : Colors.grey,
              margin: const EdgeInsets.only(left: 14),
            ),

            _buildTimelineStep("Packed", statusLevel >= 2),
            Container(
              height: 30,
              width: 2,
              color: statusLevel >= 3 ? Colors.green : Colors.grey,
              margin: const EdgeInsets.only(left: 14),
            ),

            _buildTimelineStep("Out for Delivery", statusLevel >= 3),
            Container(
              height: 30,
              width: 2,
              color: statusLevel >= 4 ? Colors.green : Colors.grey,
              margin: const EdgeInsets.only(left: 14),
            ),

            _buildTimelineStep("Delivered", statusLevel >= 4),
          ],
        ),
      ),
    );
  }
}
