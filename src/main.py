import cv2
import mediapipe as mp
import numpy as np
import pyaudio
import time
import yaml

config = None
with open("./config.yml", "r") as f:
    config = yaml.safe_load(f)

vid = cv2.VideoCapture(0)
mph = mp.solutions.hands
hands = mph.Hands()
mp_draw = mp.solutions.drawing_utils

p = pyaudio.PyAudio()
fs = 44100  # sampling rate, Hz, must be integer
duration = 0.1  # in seconds, may be float
stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

while 1:
    success, image = vid.read()
    if config["mirror_camera"]: # only need this if camera is mirrored
        image = cv2.flip(image, 1) 
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    dimensions = image.shape # (height, width, channels)

    if results.multi_hand_landmarks:
        mhp = []
        for hand_land_mark in results.multi_hand_landmarks:
            mhpx, mhpy = 0, 0
            for id, lm in enumerate(hand_land_mark.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if cx > mhpx:
                    mhpx = cx
                if cy > mhpy:
                    mhpy = cy
                
                cv2.circle(image, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
                mp_draw.draw_landmarks(image, hand_land_mark, mph.HAND_CONNECTIONS)
            mhp.append((mhpx, mhpy))
        if len(mhp) == 2:
            # figure out which is pitch and which is volume
            if mhp[0][0] > mhp[1][0]:
                pitch = ((mhp[0][0] - (dimensions[1]/2))/(dimensions[1]/2)) * (config["max_pitch"] - config["min_pitch"]) + config["min_pitch"] # normalize pitch
                volume = (dimensions[0] - mhp[1][1]) / dimensions[0]
            else:
                pitch = ((mhp[1][0] - (dimensions[1]/2))/(dimensions[1]/2)) * (config["max_pitch"] - config["min_pitch"]) + config["min_pitch"] # normalize pitch
                volume = (dimensions[0] - mhp[0][1]) / dimensions[0]
            
            if pitch > 0:
                samples = (np.sin(2 * np.pi * np.arange(fs * duration) * pitch / fs)).astype(np.float32)
                output_bytes = (volume * samples).tobytes()
                start_time = time.time()
                stream.write(output_bytes)
    cv2.imshow("Theremin", image)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

vid.release()
cv2.destroyAllWindows()

stream.stop_stream()
stream.close()

p.terminate()