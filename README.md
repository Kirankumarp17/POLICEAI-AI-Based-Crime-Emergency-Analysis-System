# 🚔 POLICEAI — AI-Based Crime & Emergency Analysis System

POLICEAI is an AI-powered crime and emergency analysis system developed as an academic project using Python, Machine Learning, Computer Vision, Data Analytics, and Streamlit.

The system provides a unified dashboard for crime risk prediction, complaint classification, incident management, crime analytics, hotspot visualization, CCTV object detection, and emergency alert management.

---

## 🎯 Project Objective

The main objective of POLICEAI is to develop an intelligent decision-support prototype that can help analyze crime-related information and organize emergency incidents through a single interactive platform.

The system combines Machine Learning, Computer Vision, Natural Language Processing techniques, Data Visualization, and Database Management.

---

## ✨ Key Features

### 🤖 1. Crime Risk Prediction

- Uses a Random Forest Regression model.
- Predicts crime risk based on multiple factors.
- Considers:
  - Latitude
  - Longitude
  - Hour
  - Day
  - Month
  - Crime Type
  - Weather
  - Population Density
  - Area
- Displays a risk score and risk level.
- Shows Random Forest feature importance.
- Displays saved model performance metrics.

---

### 📝 2. AI Complaint Analysis

- Accepts complaints written in natural language.
- Classifies complaints into different crime categories.
- Provides:
  - Detected crime
  - Confidence score
  - Priority level
- Stores analyzed incidents in the SQLite database.
- Supports human review of AI-generated results.

---

### 🗄️ 3. Incident Management

- Stores police incidents using SQLite.
- Displays registered incidents.
- Allows officers/users to update incident status.
- Supported statuses include:
  - Pending
  - Under Investigation
  - Resolved
  - Closed

---

### 📊 4. Crime Analytics

Provides visual analysis of crime data including:

- Crime type distribution
- Area-wise crime distribution
- Crime distribution by hour
- Monthly crime distribution
- Most common crime
- Highest crime area

---

### 🗺️ 5. Crime Hotspot Map

- Interactive geographical crime visualization.
- Uses Folium and HeatMap.
- Displays crime hotspots based on latitude and longitude.
- Allows filtering by:
  - Crime Type
  - Area
- Helps visualize geographical crime patterns.

---

### 📹 6. CCTV AI Monitoring

- Uses YOLO and OpenCV for real-time object detection.
- Uses a webcam/CCTV feed.
- Detects objects such as:
  - Person
  - Car
  - Motorcycle
  - Bus
  - Truck
- Displays bounding boxes and object counts.
- Provides real-time monitoring information.

> CCTV detection is intended for object/event analysis and does not identify people as criminals.

---

### 🚨 7. Emergency Alert System

Allows users to create emergency alerts for:

- Accident
- Fire
- Medical Emergency
- Suspicious Activity
- Missing Person

Each emergency is assigned a priority level such as:

- MEDIUM
- HIGH
- CRITICAL

Emergency alerts are stored in the database for further management.

---

### 🚨 8. Emergency Management

- Displays saved emergency alerts.
- Shows:
  - Emergency type
  - Location
  - Description
  - Priority
  - Status
  - Created time
- Allows emergency status updates.
- Supported statuses:
  - Active
  - Under Investigation
  - Resolved
  - Closed

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| Pandas | Data processing |
| Scikit-learn | Machine Learning |
| Random Forest | Crime risk prediction |
| YOLO | Object detection |
| OpenCV | CCTV/video processing |
| Folium | Interactive maps |
| SQLite | Database management |
| Joblib | ML model storage |
| NumPy | Numerical processing |

---

## 🧠 Machine Learning

POLICEAI uses a Random Forest Regression model for crime risk prediction.

### Input Features

```text
Latitude
Longitude
Hour
Day
Month
Crime Type
Weather
Population Density
Area
