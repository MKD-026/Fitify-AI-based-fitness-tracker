import cv2
import mediapipe as mp
from utils import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
#---------------------------------------------------------------------
#Loading icons
Larrow = cv2.imread("assets/arrow.png")
Rarrow = cv2.flip(Larrow, 1)
Start = cv2.imread("assets/start.png")
Stop = cv2.imread("assets/stop.png")

#---------------------------------------------------------------------
# VIDEO FEED
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

#Frame: 525x335 hxw
#webcam hxw 480x640

#---------------------------------------------------------------------
# Curl counter variables
counter = 0
stage = None
#---------------------------------------------------------------------

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, img = cap.read()
        #img = cv2.flip(img, 1)

        imgScaled = cv2.resize(img, (0, 0), None, 0.53, 1.11)
        # width 339
        # height 533

        #Background
        imgBG = cv2.imread("assets/background.jpg")
        imgBG[80:80 + 533, 32:32 + 339] = imgScaled

        # Make detection
        results = pose.process(imgBG)

        LS = []
        LE = []
        LW = []

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            Lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            Lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            Lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(Lshoulder, Lelbow, Lwrist)
            # Draw left arm
            x1, y1 = int(Lshoulder[0] * imgBG.shape[1]), int(Lshoulder[1] * imgBG.shape[0])
            x2, y2 = int(Lelbow[0] * imgBG.shape[1]), int(Lelbow[1] * imgBG.shape[0])
            x3, y3 = int(Lwrist[0] * imgBG.shape[1]), int(Lwrist[1] * imgBG.shape[0])

            cv2.line(imgBG, (x1, y1), (x2, y2), (255, 255, 255), 6)
            cv2.line(imgBG, (x2, y2), (x3, y3), (255, 255, 255), 6)
            cv2.circle(imgBG, (x1, y1), 12, (0, 0, 255), cv2.FILLED)
            cv2.circle(imgBG, (x2, y2), 12, (0, 0, 255), cv2.FILLED)
            cv2.circle(imgBG, (x3, y3), 12, (0, 0, 255), cv2.FILLED)
            '''
            # Get coordinates for right arm
            Rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            Relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Draw right arm
            x1, y1 = int(Rshoulder[0] * imgBG.shape[1]), int(Rshoulder[1] * imgBG.shape[0])
            x2, y2 = int(Relbow[0] * imgBG.shape[1]), int(Relbow[1] * imgBG.shape[0])
            x3, y3 = int(Rwrist[0] * imgBG.shape[1]), int(Rwrist[1] * imgBG.shape[0])
            cv2.line(imgBG, (x1, y1), (x2, y2), (255, 255, 255), 6)
            cv2.line(imgBG, (x2, y2), (x3, y3), (255, 255, 255), 6)
            cv2.circle(imgBG, (x1, y1), 12, (0, 0, 255), cv2.FILLED)
            cv2.circle(imgBG, (x2, y2), 12, (0, 0, 255), cv2.FILLED)
            cv2.circle(imgBG, (x3, y3), 12, (0, 0, 255), cv2.FILLED)
            '''
            # Curl counter logic
            if angle > 160:
                stage = "DOWN"
            if angle < 30 and stage == 'down':
                stage = "UP"
                counter += 1
                print(counter)

            cv2.putText(imgBG, str(counter), (210, 662),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (50, 108, 53), 4)  # , cv2.LINE_AA)
            cv2.putText(imgBG, stage, (150, 705),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        except:
            pass



        # Render detections
        '''
        mp_drawing.draw_landmarks(imgBG, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=3, circle_radius=4),

                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        '''

        cv2.imshow('PROTOTYPE DEMO', imgBG)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()