import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Status
watering_active = False
current_tray = None
status_message = "Show a gesture to start watering."
last_action_time = 0
cooldown = 1  # seconds

gesture_buffer = []
buffer_size = 5

def log_water_time(message):
    with open("watering_log.txt", "a") as file:
        file.write(f"{time.ctime()}: {message}\n")

# Tray functions
def water_tray(tray_number):
    global watering_active, current_tray, status_message
    watering_active = True
    current_tray = f"tray{tray_number}"
    status_message = f"Watering Tray {tray_number}... Show Fist to Stop."
    log_water_time(f"Watered Tray {tray_number}")

def water_all_trays():
    global watering_active, current_tray, status_message
    watering_active = True
    current_tray = "all"
    status_message = "Watering ALL trays... Show Fist to Stop."
    log_water_time("Watered All Trays")

def stop_watering():
    global watering_active, current_tray, status_message
    watering_active = False
    current_tray = None
    status_message = "Watering Stopped. Show Gesture to Start Again."
    log_water_time("Watering stopped")

# Better hand detection
def fingers_up(hand_landmarks):
    fingers = []
    tips_ids = [4, 8, 12, 16, 20]

    # Thumb
    fingers.append(int(hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x))
    # Index to pinky
    for id in range(1, 5):
        fingers.append(int(hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y))

    return tuple(fingers)

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        gesture_detected = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = fingers_up(hand_landmarks)
                gesture_buffer.append(fingers)
                if len(gesture_buffer) > buffer_size:
                    gesture_buffer.pop(0)

                if all(g == gesture_buffer[0] for g in gesture_buffer):
                    gesture_detected = gesture_buffer[0]

        # Cooldown check
        if gesture_detected and time.time() - last_action_time > cooldown:
            if gesture_detected == (0, 0, 0, 0, 0):
                if watering_active:
                    stop_watering()
            elif gesture_detected == (1, 1, 1, 1, 1):
                if not watering_active or current_tray != 'all':
                    water_all_trays()
            elif gesture_detected == (0, 1, 0, 0, 0):
                if not watering_active or current_tray != 'tray1':
                    water_tray(1)
            elif gesture_detected == (0, 1, 1, 0, 0):
                if not watering_active or current_tray != 'tray2':
                    water_tray(2)
            elif gesture_detected == (0, 1, 1, 1, 0):
                if not watering_active or current_tray != 'tray3':
                    water_tray(3)
            last_action_time = time.time()

        cv2.putText(frame, status_message, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)

        cv2.imshow("Gesture Controlled Watering", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
