import cv2
import mediapipe as mp
import time
# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# Flags
watering_active = False
current_tray = None
'''-------------------------------------------------------------------------------------------------------------'''
# Functions for each tray
def water_all_trays():
    print("💧 Watering ALL trays!")
def water_tray_1():
    print("💧 Watering Tray 1")
def water_tray_2():
    print("💧 Watering Tray 2")
def water_tray_3():
    print("💧 Watering Tray 3")
def stop_watering():
    print("🛑 Stopping all watering")
'''-----------------------------------------------------------------------------------------------------------------------'''
# Detect which fingers are up
def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    status = []
    status.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    for tip_id in tips_ids[1:]:
        status.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)
    return status  # [Thumb, Index, Middle, Ring, Pinky]
'''--------------------------------------------------------------------------------------------------------------------------'''
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
                # Stop (Fist) → All fingers down
                if not any(finger_status):
                    cv2.putText(frame, "Fist: Stop Watering", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if watering_active:
                        stop_watering()
                        watering_active = False
                        current_tray = None
'''------------------------------------------------------------------------------------------------------------------------'''
                # Open palm (All fingers up)
                elif all(finger_status):
                    cv2.putText(frame, "Open Palm: Water All Trays", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    if not watering_active or current_tray != 'all':
                        water_all_trays()
                        watering_active = True
                        current_tray = 'all'
'''-------------------------------------------------------------------------------------------------------------------------'''
                # Only Index finger (Tray 1)
                elif finger_status[1] and not any(finger_status[2:]):
                    cv2.putText(frame, "Index Finger: Water Tray 1", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    if not watering_active or current_tray != 'tray1':
                        water_tray_1()
                        watering_active = True
                        current_tray = 'tray1'
                # Index + Middle (Tray 2)
                elif finger_status[1] and finger_status[2] and not any(finger_status[3:]):
                    cv2.putText(frame, "2 Fingers: Water Tray 2", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 0), 2)
                    if not watering_active or current_tray != 'tray2':
                        water_tray_2()
                        watering_active = True
                        current_tray = 'tray2'
                # Index + Middle + Ring (Tray 3)
                elif finger_status[1] and finger_status[2] and finger_status[3] and not finger_status[4]:
                    cv2.putText(frame, "3 Fingers: Water Tray 3", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    if not watering_active or current_tray != 'tray3':
                        water_tray_3()
                        watering_active = True
                        current_tray = 'tray3'
                else:
                    cv2.putText(frame, "Gesture Not Recognized", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Show your hand...", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
        cv2.imshow("Gesture Controlled Watering", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
