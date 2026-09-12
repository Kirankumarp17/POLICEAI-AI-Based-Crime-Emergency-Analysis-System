from ultralytics import YOLO
import cv2
from datetime import datetime


# ==========================================
# 🚔 POLICEAI - CCTV AI
# ==========================================

MODEL_PATH = "yolo11n.pt"

model = YOLO(MODEL_PATH)

# ==========================================
# Open Webcam
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("❌ Could not open camera")
    exit()


print("🚔 POLICEAI CCTV started")
print("Press Q to quit")


# ==========================================
# Main CCTV Loop
# ==========================================

while True:

    success, frame = cap.read()

    if not success:

        print("❌ Could not read camera")
        break


    # ======================================
    # YOLO Detection
    # ======================================

    results = model(
        frame,
        verbose=False
    )

    result = results[0]


    # ======================================
    # Draw Detection Boxes
    # ======================================

    annotated_frame = result.plot()


    # ======================================
    # Count Objects
    # ======================================

    object_counts = {}

    for box in result.boxes:

        class_id = int(
            box.cls[0]
        )

        class_name = model.names[
            class_id
        ]

        object_counts[class_name] = (
            object_counts.get(
                class_name,
                0
            ) + 1
        )


    # ======================================
    # Important Object Counts
    # ======================================

    person_count = object_counts.get(
        "person",
        0
    )

    car_count = object_counts.get(
        "car",
        0
    )

    motorcycle_count = object_counts.get(
        "motorcycle",
        0
    )

    bus_count = object_counts.get(
        "bus",
        0
    )

    truck_count = object_counts.get(
        "truck",
        0
    )


    # ======================================
    # Current Time
    # ======================================

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # ======================================
    # POLICEAI Header
    # ======================================

    cv2.putText(
        annotated_frame,
        "POLICEAI - CCTV AI",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )


    # ======================================
    # Detection Statistics
    # ======================================

    stats = [
        f"Persons: {person_count}",
        f"Cars: {car_count}",
        f"Motorcycles: {motorcycle_count}",
        f"Buses: {bus_count}",
        f"Trucks: {truck_count}"
    ]


    y_position = 80


    for text in stats:

        cv2.putText(
            annotated_frame,
            text,
            (20, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        y_position += 30


    # ======================================
    # Monitoring Status
    # ======================================

    if person_count > 0:

        status = "MONITORING"

    else:

        status = "NO PERSON DETECTED"


    cv2.putText(
        annotated_frame,
        f"Status: {status}",
        (20, y_position + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # ======================================
    # Timestamp
    # ======================================

    cv2.putText(
        annotated_frame,
        current_time,
        (20, y_position + 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )


    # ======================================
    # Display CCTV
    # ======================================

    cv2.imshow(
        "POLICEAI - CCTV AI",
        annotated_frame
    )


    # ======================================
    # Quit
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# Release Camera
# ==========================================

cap.release()

cv2.destroyAllWindows()

print("🚔 CCTV system stopped.")