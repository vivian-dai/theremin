import cv2
import mediapipe as mp
import yaml

config = None
with open("./config.yml", "r") as f:
    config = yaml.safe_load(f)

vid = cv2.VideoCapture(0)
mph = mp.solutions.hands
hands = mph.Hands()
mp_draw = mp.solutions.drawing_utils

while 1:
    success, image = vid.read()
    if config["mirror_camera"]: # only need this if camera is mirrored
        image = cv2.flip(image, 1) 
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_land_mark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_land_mark.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(cx, cy, id)

                cv2.circle(image, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
                mp_draw.draw_landmarks(image, hand_land_mark, mph.HAND_CONNECTIONS)

    cv2.imshow("Theremin", image)
    if cv2.waitKey(50) & 0xFF == ord('q'): 
        break

vid.release()
cv2.destroyAllWindows()