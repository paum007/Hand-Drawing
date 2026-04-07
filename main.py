from camera import Camera
from single_hand import SingleHand
from gesture_detector import GestureDetector


camera = Camera()
gesture = GestureDetector(camera)
gesture_single = SingleHand(camera)

while True:
    try:
        mode = int(input("Do you want to use [1] hand or [2] hands. Put the number in: "))
        if mode in (1, 2):
            break
        print("Please enter either 1 or 2")
    
    except ValueError:
        print("Please enter a valid NUMBER")


if mode == 1: 
    gesture_single.gesture_recognition(camera)

elif mode == 2:
    gesture.gesture_recognition(camera)