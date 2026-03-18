from camera import Camera
from single_hand import SingleHand
from gesture_detector import GestureDetector


camera = Camera()
gesture = GestureDetector(camera)
gesture_single = SingleHand(camera)

mode = int(input("Do you want to use [1] hand or [2] hands. Put the number in: "))

if mode == 1: 
    gesture_single.gesture_recognition(camera)

else:
    gesture.gesture_recognition(camera)