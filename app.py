import cv2
import mediapipe as mp
from flask import Flask, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1,
                      min_detection_confidence=0.7,
                      min_tracking_confidence=0.7)

currentGesture = "NONE"


def detectGesture(handLandmarks):

    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if handLandmarks.landmark[tips[0]].x < handLandmarks.landmark[tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1,5):
        if handLandmarks.landmark[tips[i]].y < handLandmarks.landmark[tips[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total = fingers.count(1)

    if total == 5:
        return "LIGHT_ON"

    elif total == 0:
        return "LIGHT_OFF"

    elif total == 1:
        return "WATER"

    elif total == 2:
        return "MEDICINE"

    elif total >= 3:
        return "EMERGENCY"

    return "NONE"


def cameraLoop():

    global currentGesture

    cap = cv2.VideoCapture(0)

    while True:

        success, img = cap.read()

        if not success:
            continue

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        gesture = "NONE"

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                gesture = detectGesture(handLms)

        currentGesture = gesture


@app.route("/gesture")
def getGesture():

    return jsonify({
        "gesture": currentGesture
    })


if __name__ == "__main__":

    thread = threading.Thread(target=cameraLoop)
    thread.daemon = True
    thread.start()

    print("VisionCare Gesture Server Running")

    app.run(host="0.0.0.0", port=5000)
