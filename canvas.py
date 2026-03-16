import cv2
import random
import numpy as np



class Canvas():
    def __init__(self, camera):
        
        self.colour = (255, 0, 0)
        self.width = round(camera.width)
        self.height = round(camera.height)
        self.drawing_surface = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.x_coord = 0
        self.y_coord = 0
        self.drawing = False
        self.mode = ""


    def draw(self, left_gesture, right_gesture, landmark):

        if right_gesture == "Victory":
            self.drawing = False
            self.mode = "RANDOMISING COLOUR"

            b=random.randint(0, 255)
            g=random.randint(0, 255)
            r=random.randint(0, 255)

            self.colour = (b, g, r)
            # loop through random numbers to get 3 colour values for the change of colour
            # print("Changing colour")


        if right_gesture == "Open_Palm":
            # print("Drawing mode")

            if left_gesture == "Pointing_Up":
                # start changing the pixels
                # print("Drawing now")

                self.mode = "DRAWING"

                # print(f"x coordinates: {self.x_coord}")
                # print(f"y coordinates: {self.y_coord}")

                if not self.drawing:
                    self.x_coord = landmark.x*self.width
                    self.y_coord = landmark.y*self.height
                    self.drawing = True

                elif self.drawing:
                    cv2.line(self.drawing_surface, (round(self.x_coord), round(self.y_coord)), (round(landmark.x*self.width), round(landmark.y*self.height)), color=self.colour, thickness=5)
                    self.x_coord = landmark.x*self.width
                    self.y_coord = landmark.y*self.height

            # else:
            #     print("Doing nothing")

        elif right_gesture == "Closed_Fist":
            # stop drawing. "Lift the pen"
            self.drawing = False
            self.mode = "PEN LIFTED"

            # print("Lifted the pen")


        elif right_gesture == "Thumb_Down":
            # print("Rubbing off")
            self.mode = "ERASING"

            self.clear(landmark)

    def clear(self, landmark):
        cv2.line(self.drawing_surface, (round(self.x_coord), round(self.y_coord)), (round(landmark.x*self.width), round(landmark.y*self.height)), color=(0, 0, 0), thickness=10)
        self.x_coord = landmark.x*self.width
        self.y_coord = landmark.y*self.height

    def blend(self, frame):
        combined = cv2.addWeighted(frame, 1.0, self.drawing_surface, 1.0, 0)
        return combined
