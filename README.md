# Hand Gesture Drawing

A real-time hand gesture drawing application using MediaPipe and OpenCV. Use your hands to draw on screen, change colours, erase, and lift the pen — all without touching a keyboard or mouse.

## Requirements

### Python Version
This project requires **Python 3.12**. Newer versions of MediaPipe (0.10.28+) have dropped the `solutions` API which this project depends on. You will need to create a virtual environment with Python 3.12 to ensure compatibility.

### Creating a Virtual Environment
```bash
py -3.12 -m venv drawing_venv
drawing_venv\Scripts\activate
```

### Installing Dependencies
```bash
pip install mediapipe==0.10.21
pip install opencv-python==4.8.0.76
pip install "numpy<2"
```

### Model File
Download the MediaPipe Gesture Recognizer model file and place it in the root of the project directory:

- File: `gesture_recognizer.task`
- Download from: https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task

## Project Structure

```
drawing/
├── main.py               # Entry point
├── camera.py             # Camera feed handler
├── gesture_detector.py   # MediaPipe gesture detection
├── canvas.py             # Drawing surface and blend logic
└── gesture_recognizer.task
```

## Camera Setup
The app uses camera device index `1` by default, which assumes you are using an external camera such as an iPhone via **Camo**. If you are using a built-in webcam, change the index to `0` in `camera.py`.

## Running the App
```bash
python main.py
```

Press **Q** to quit.

## Gesture Controls

The app uses **two hands**. Due to the mirrored camera feed, gestures are mapped as follows:

| Hand (on screen) | Gesture | Action |
|---|---|---|
| Right | Open Palm | Enable drawing mode |
| Left | Pointing Up | Draw |
| Right | Closed Fist | Lift pen (stop drawing) |
| Right | Thumb Down | Erase |
| Right | Victory | Randomise brush colour |

> Note: Drawing and erasing track the **index fingertip** (landmark 8) of the left hand.

## Known Issues
- There may be slight latency between hand movement and detection due to the async nature of MediaPipe's live stream mode.
- The `Victory` gesture randomises the colour on every frame while held — tap it briefly for a single colour change.