---
title: Push-Up Counter
emoji: 💪
colorFrom: red
colorTo: yellow
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
python_version: 3.10.8
---

# 💪 Push-Up Counter

Real-time push-up detection and counting web application using computer vision and pose estimation.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- Real-time push-up detection using webcam
- Automatic rep counting
- Position status display (UP/DOWN/Not Detected)
- Pose skeleton visualization
- Works in browser - no installation required for end users

## How It Works

The application uses CVZone's PoseDetector (powered by MediaPipe) to:

1. Detect body landmarks (shoulders, elbows, hips)
2. Calculate joint angles using arctangent formula
3. Check if body is horizontal (proper push-up form)
4. Count reps when transitioning from UP to DOWN position

### Detection Logic

- **DOWN position**: Both elbow angles < 45° AND body is horizontal
- **UP position**: Both elbow angles > 45°
- **Minimum time between reps**: 1 second (prevents double counting)

## Tech Stack

- **Frontend**: Streamlit
- **Video Streaming**: streamlit-webrtc
- **Pose Detection**: CVZone + MediaPipe
- **Computer Vision**: OpenCV

## Local Development

### Prerequisites

- Python 3.10.x
- Webcam

### Installation

```bash
git clone https://github.com/yourusername/pushup-counter.git
cd pushup-counter

conda create -n pushup python=3.10.8
conda activate pushup

pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Deploy to Hugging Face Spaces

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space → Select **Streamlit** SDK
3. Upload all files from this directory
4. App will auto-deploy with HTTPS URL

## Project Structure

```
pushup-web/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies (for HF Spaces)
├── README.md           # This file
└── .streamlit/
    └── config.toml     # Streamlit theme config
```

## Usage Tips

1. Click **START** to enable webcam
2. Position yourself so your **full body is visible**
3. Face the camera from the **side** for best detection
4. Ensure **good lighting**
5. Keep your body **horizontal** during push-ups

## Requirements

```
streamlit==1.28.0
streamlit-webrtc==0.47.1
cvzone==1.6.1
mediapipe==0.10.8
opencv-python-headless==4.8.1.78
numpy==1.24.3
aiortc==1.10.1
```

## Acknowledgments

- [CVZone](https://github.com/cvzone/cvzone) - Computer vision package
- [MediaPipe](https://mediapipe.dev/) - Pose estimation
- [Streamlit](https://streamlit.io/) - Web framework
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) - WebRTC component

## License

MIT License
