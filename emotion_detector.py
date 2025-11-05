import cv2
from fer import FER

def detect_emotion():
    detector = FER()
    cam = cv2.VideoCapture(0)  # 0 = default webcam
    emotion_result = None

    print("Press 'q' to capture your emotion from webcam")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow('Emotion Capture - Press q', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to capture
            emotions = detector.detect_emotions(frame)
            if emotions:
                # Take the emotion with the highest confidence
                emotion_result = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
            break

    cam.release()
    cv2.destroyAllWindows()
    return emotion_result

# Standalone test
if __name__ == "__main__":
    emotion = detect_emotion()
    if emotion:
        print("Detected Emotion:", emotion)
    else:
        print("No face detected!")
