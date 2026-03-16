from camera import Camera
from gesture_detector import GestureDetector


camera = Camera()
gesture = GestureDetector(camera)

gesture.gesture_recognition(camera)