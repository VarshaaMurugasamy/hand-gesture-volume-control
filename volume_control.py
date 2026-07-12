import cv2
import mediapipe as mp
import numpy as np
import math
import platform
import subprocess

system = platform.system()

# --- Volume control setup per OS ---
if system == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
    vol_range = volume_ctrl.GetVolumeRange()
    min_vol, max_vol = vol_range[0], vol_range[1]

def set_system_volume(vol_percent):
    vol_percent = max(0, min(100, vol_percent))
    if system == "Windows":
        vol_scalar = vol_percent / 100
        volume_ctrl.SetMasterVolumeLevelScalar(vol_scalar, None)
    elif system == "Darwin":
        subprocess.run(["osascript", "-e", f"set volume output volume {vol_percent}"])
    elif system == "Linux":
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{vol_percent}%"])

# --- Mediapipe hand tracking setup ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

            cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            length = math.hypot(x2 - x1, y2 - y1)

            vol_percent = np.interp(length, [30, 200], [0, 100])
            vol_percent = int(vol_percent)

            set_system_volume(vol_percent)

            bar_height = np.interp(vol_percent, [0, 100], [400, 150])
            cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(frame, (50, int(bar_height)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{vol_percent}%', (40, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()