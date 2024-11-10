import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        
    def track_hands(self, rgb_frame):
        results = self.hands.process(rgb_frame)
        return results