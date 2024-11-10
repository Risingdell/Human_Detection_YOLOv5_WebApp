import torch
import cv2
import sqlite3
import time

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

conn = sqlite3.connect('human_detection.db')
cursor = conn.cursor()

def store_human_count(count):
    cursor.execute("INSERT INTO human_count (count) VALUES (?)", (count,))
    conn.commit()

def store_max_human_count(max_count):
    cursor.execute("INSERT INTO total_count (total_count) VALUES (?)", (max_count,))
    conn.commit()

cap = cv2.VideoCapture(0)

start_time = time.time()
max_distinct_person_count = 0

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
threshold_line = frame_height // 2

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    results = model(frame)

    persons = results.xyxy[0]
    current_person_ids = set()

    for det in persons:
        class_id = int(det[5])
        if class_id == 0:
            x1, y1, x2, y2 = map(int, det[:4])
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            if center_y > threshold_line:
                person_id = (center_x, center_y)
                current_person_ids.add(person_id)

    max_distinct_person_count = max(max_distinct_person_count, len(current_person_ids))

    store_human_count(len(current_person_ids))

    cv2.putText(frame, f"Humans detected: {len(current_person_ids)}", (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Human Detection', frame)

    if time.time() - start_time >= 60:

        print(f"Max number of humans detected in 1 minute: {max_distinct_person_count}")

        store_max_human_count(max_distinct_person_count)

        max_distinct_person_count = 0
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
conn.close()
