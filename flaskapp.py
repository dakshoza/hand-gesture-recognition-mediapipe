from flask import Flask, jsonify, render_template, Response
import cv2
import numpy as np
import time
import csv
import copy
import argparse
import itertools
import mediapipe as mp
from model import KeyPointClassifier
from create_vector_embeddings import GestureRecognizer

app = Flask(__name__)

check_sign_language = 'E'
status_message = ''

def generate_frames():
    # Argument parsing
    args = get_args()

    gesture_recognizer = GestureRecognizer()

    gesture_list = []

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    # Camera preparation
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Model load
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()

    # Read labels
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror display
        debug_image = copy.deepcopy(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_rgb.flags.writeable = False
        results = hands.process(frame_rgb)
        frame_rgb.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                gesture_list_len = len(gesture_list)
                which_hand_current, what_sign_current = handedness.classification[0].label[0:],keypoint_classifier_labels[hand_sign_id]

                if gesture_list_len == 0:
                    gesture_list.append([which_hand_current, what_sign_current])
                elif gesture_list_len ==1:
                    if gesture_list[gesture_list_len-1][0] != which_hand_current or gesture_list[gesture_list_len-1][1] != what_sign_current:
                        gesture_list.append([which_hand_current, what_sign_current])
                else:
                    if gesture_list[gesture_list_len-1][0] != which_hand_current or gesture_list[gesture_list_len-1][1] != what_sign_current:
                        if gesture_list[gesture_list_len-2][0] != which_hand_current or gesture_list[gesture_list_len-2][1] != what_sign_current:
                            gesture_list.append([which_hand_current, what_sign_current])
                
                if len(gesture_list) > len(check_sign_language) + 2:
                    print(gesture_list)
                    print("Incorrect Sequence")
                    update_status("Incorrect Sequence")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                else:
                    query_sequence = ' '.join(sublist[1] for sublist in gesture_list)
                    most_similar_word = gesture_recognizer.find_most_similar_word_for_sequence(query_sequence)
                    print(most_similar_word)
                    if check_sign_language == most_similar_word:
                        print("Sign Language Successfully Done")
                        update_status("Sign Language Successfully Done")
                        time.sleep(1.5)
                        cap.release()
                        cv2.destroyAllWindows()
                        return

        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(0.1)

    cap.release()

def update_status(message):
    global status_message
    status_message = message

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args

def update_status(message):
    global status_message
    status_message = message

def generate():
    while True:
        data = f"data: {{'message': '{status_message}', 'sign': '{check_sign_language}'}}\n\n"
        yield data.encode('utf-8')
        time.sleep(0.01)  # Adjust this interval as needed

@app.route('/')
def index():
    return render_template('index.html', check_sign_language=check_sign_language)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status_updates')
def status_updates():
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)