# Blinkit Clone - Microservices E-Commerce Application 🛒

A full-stack, containerized e-commerce application built to demonstrate a modern **Microservices Architecture**. This project features a cross-platform frontend communicating with multiple independent Python backend services, all orchestrated via Docker.

## 🚀 System Architecture

The backend is completely decoupled into four independent RESTful microservices, each handling a specific domain of the e-commerce flow, connected to a MongoDB database.

* **User Service (Port 8001):** Manages user profiles and authentication.
* **Product Service (Port 8002):** Manages the grocery catalog, inventory, and database seeding.
* **Cart & Order Service (Port 8003):** Processes checkout logic, calculates totals, and persists order data.
* **Delivery Service (Port 8004):** Provides real-time order tracking and status updates via API polling.

## 🛠️ Tech Stack

**Frontend:**
* Flutter (Dart)
* Flutter Web (HTML Renderer)
* `http` package for REST API communication

**Backend:**
* Python 3
* FastAPI (High-performance async web framework)
* Motor (Asynchronous Python driver for MongoDB)
* Uvicorn (ASGI web server)

**Database & DevOps:**
* MongoDB
* Docker & Docker Compose
* CORS Middleware integration for secure cross-origin resource sharing

## ✨ Key Features

* **Microservice Communication:** Seamless data flow between a Flutter frontend and multiple separate FastAPI backends.
* **Dynamic Product Catalog:** Fetches and displays inventory directly from the Product Service database.
* **Cart Management:** Calculates order totals and formats complex nested JSON payloads for the backend.
* **Real-Time Order Tracking:** Implements an automated polling mechanism in Flutter to continuously fetch live delivery updates (Placed -> Packed -> Out for Delivery -> Delivered) from the Delivery Service.
* **Fully Containerized:** One-command setup using `docker-compose` to spin up the database and all backend APIs simultaneously.

## 🚦 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.

### 1. Start the Backend Microservices
Open your terminal in the root directory of the project and run:
```bash
docker-compose up --build
This will pull the MongoDB image and build the 4 FastAPI services. Wait until the terminal shows Application startup complete for all ports.

2. Seed the Database
To populate the app with sample grocery items, open your browser and navigate to:

Plaintext
http://localhost:8002/seed
3. Run the Flutter Frontend
Open a new terminal, navigate to the flutter_app directory, and launch the web app:

Bash
cd flutter_app
flutter run -d chrome --web-renderer html
🧪 Testing the Real-Time Tracking
To see the live order tracking in action:

Add items to your cart and complete the checkout in the Flutter app.

The app will navigate to the Tracking Screen and display your Order ID.

Open a terminal and run the following command (replace YOUR_ORDER_ID with the actual ID) to simulate a delivery update:

Windows (PowerShell):

PowerShell
Invoke-RestMethod -Uri "http://localhost:8004/update-status/YOUR_ORDER_ID" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"status":"OUT_FOR_DELIVERY"}'
Mac/Linux (cURL):

Bash
curl -X POST "http://localhost:8004/update-status/YOUR_ORDER_ID" -H "Content-Type: application/json" -d '{"status":"OUT_FOR_DELIVERY"}'
Watch the Flutter UI automatically update the tracking timeline!

🧠 Technical Challenges Overcome
CORS Management: Configured FastAPI CORSMiddleware across all microservices to safely accept preflight requests from the local Flutter Web client.

State Management & Polling: Designed a lifecycle-aware Dart Timer to poll the Delivery API every 3 seconds, ensuring the UI stays synced with the database without memory leaks.
