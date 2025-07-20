import cv2
import mediapipe as mp
import time
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# status
watering_active = False
current_tray = None
status_message = "Show a gesture to start watering."
def log_water_time(message):
    with open("watering_log.txt", "a") as file:
        file.write(f"{time.ctime()}: {message}\n")
'''---------------------------------------------------------'''
# Tray functions
def water_tray(tray_number):
    global watering_active, current_tray, status_message
    watering_active = True
    current_tray = f"tray{tray_number}"
    status_message = f"Watering Tray {tray_number}... Show Fist to Stop."
    log_water_time(f"Watered Tray {tray_number}")
#water all trays
def water_all_trays():
    global watering_active, current_tray, status_message
    watering_active = True
    current_tray = "all"
    status_message = "Watering ALL trays... Show Fist to Stop."
    log_water_time("Watered All Trays")
#stop watering
def stop_watering():
    global watering_active, current_tray, status_message
    watering_active = False
    status_message = "Watering Stopped. Show Gesture to Start Again."
    current_tray = None
    log_water_time("Watering stopped")
# Finger detection
def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    status = []
    status.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    for tip_id in tips_ids[1:]:
        status.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)
    return status  
# Webcam
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_status = fingers_up(hand_landmarks)
                # Fist to stop
                if not any(finger_status):
                    if watering_active:
                        stop_watering()
                # water all trays
                elif all(finger_status):
                    if not watering_active or current_tray != 'all':
                        water_all_trays()
                # Tray 1
                elif finger_status[1] and not any(finger_status[2:]):
                    if not watering_active or current_tray != 'tray1':
                        water_tray(1)
                # Tray 2
                elif finger_status[1] and finger_status[2] and not any(finger_status[3:]):
                    if not watering_active or current_tray != 'tray2':
                        water_tray(2)
                # Tray 3
                elif finger_status[1] and finger_status[2] and finger_status[3] and not finger_status[4]:
                    if not watering_active or current_tray != 'tray3':
                        water_tray(3)
        # Always display current status
        cv2.putText(frame, status_message, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)
        cv2.imshow("Gesture Controlled Watering", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
