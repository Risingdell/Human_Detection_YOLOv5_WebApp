# Human_Detection_YOLOv5_WebApp
This project uses the YOLOv5 model for real-time human detection via a webcam. It tracks and counts distinct human entries, stores detection data in an SQLite database, and is set up to enable data display on a webpage.

The application captures video from a webcam and leverages the YOLOv5 model to detect people in real-time. The system counts and stores individual and maximum distinct human entries detected per minute in a local SQLite database. This stored data can be further used to display statistics on a web interface.


Real-Time Detection: Uses YOLOv5 to detect people in webcam feed.
  Tracking and Counting: Tracks and counts the distinct human entries per frame.
  Database Storage: Stores data (total count per minute) in an SQLite database.
  Data for Web Display: Enables real-time and historical human count data for web-based monitoring.

1. Python 3.7+: Ensure Python is installed.
2. Required Libraries: Install necessary libraries with the following command:
   ```bash
   pip install torch opencv-python sqlite3
