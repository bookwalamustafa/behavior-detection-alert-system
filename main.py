import cv2
import time
import mediapipe as mp
from utils.face_detection import FaceDetector
from utils.hand_tracking import HandTracker
from utils.alert_system import AlertSystem

def is_hand_in_red_zone(hand_landmarks, face_coords):
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    
    height, width, _ = frame.shape
    finger_x = int(index_finger_tip.x * width)
    finger_y = int(index_finger_tip.y * height)
    
    for (x, y, w, h) in face_coords:
        if x < finger_x < x + w and y < finger_y < y + h:
            return True
    return False

cap = cv2.VideoCapture(0)
face_detector = FaceDetector()
hand_tracker = HandTracker()
alert_system = AlertSystem()

hand_in_red_zone = False
start_time = None
alert_threshold = 3

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector.detect_face(gray_frame)
    hand_results = hand_tracker.track_hands(rgb_frame)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            hand_tracker.mp_draw.draw_landmarks(
                frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
            )

            if is_hand_in_red_zone(hand_landmarks, faces):
                if not hand_in_red_zone:
                    hand_in_red_zone = True
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > alert_threshold:
                        alert_system.trigger_alert()
            else:
                hand_in_red_zone = False
                start_time = None

    cv2.imshow('Behavioral Detection Alert System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()