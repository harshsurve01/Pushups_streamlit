import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np
import time

st.set_page_config(
    page_title="Push-Up Counter",
    page_icon="💪",
    layout="centered"
)

detector = PoseDetector()
pushup_count = 0
pushup_position = "up"
threshold_angle = 45
min_time_between_pushups = 1.0
last_pushup_time = 0
position_text = "Position: Not Detected"


def calculate_angle(a, b, c):
    angle = np.arctan2(c[2] - b[2], c[1] - b[1]) - np.arctan2(a[2] - b[2], a[1] - b[1])
    return np.abs(angle * 180.0 / np.pi)


def is_horizontal(shoulder_left, shoulder_right, hip_left, hip_right):
    shoulder_mid = (shoulder_left[2] + shoulder_right[2]) / 2
    hip_mid = (hip_left[2] + hip_right[2]) / 2
    return abs(shoulder_mid - hip_mid) < 50


def video_frame_callback(frame):
    global pushup_count, pushup_position, last_pushup_time, position_text

    img = frame.to_ndarray(format="bgr24")

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    if lmList:
        shoulder_left = lmList[11]
        shoulder_right = lmList[12]
        elbow_left = lmList[13]
        elbow_right = lmList[14]
        hip_left = lmList[23]
        hip_right = lmList[24]

        left_angle = calculate_angle(shoulder_left, elbow_left, hip_left)
        right_angle = calculate_angle(shoulder_right, elbow_right, hip_right)

        current_time = time.time()

        if left_angle < threshold_angle and right_angle < threshold_angle and is_horizontal(shoulder_left, shoulder_right, hip_left, hip_right):
            position_text = "Position: DOWN"

            if pushup_position == "up" and (current_time - last_pushup_time) > min_time_between_pushups:
                pushup_count += 1
                pushup_position = "down"
                last_pushup_time = current_time

        elif left_angle > threshold_angle and right_angle > threshold_angle:
            position_text = "Position: UP"
            pushup_position = "up"

        else:
            position_text = "Position: Not Detected"

    cv2.putText(img, f"Push-Ups: {pushup_count}",
                (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    cv2.putText(img, position_text,
                (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    return frame.from_ndarray(img, format="bgr24")


st.title("💪 Push-Up Counter")
st.markdown("Real-time push-up detection using your webcam")

with st.expander("How to use"):
    st.markdown("""
    1. Click **START** to enable your webcam
    2. Position yourself so your full body is visible
    3. Perform push-ups with proper form
    4. The app will count your push-ups automatically

    **Tips:**
    - Ensure good lighting
    - Keep your body horizontal during push-ups
    - Face the camera from the side for best results
    """)

webrtc_streamer(
    key="pushup-detection",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

st.markdown("---")
st.markdown("MEGA KNIGHT 🛡️")
