import cv2
import numpy as np
import mediapipe as mp
from canvas import Canvas
from canvas_single import CanvasSingle
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


class SingleHand:
    def __init__(self, camera):
        
        self.canvas = CanvasSingle(camera)
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.model_path = 'gesture_recognizer.task'

        self.gesture = []
        self.hand_landmarks = []
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
        self.text = ""
        self.gesture_text = ""

        self.options = self.GestureRecognizerOptions(
            num_hands = 1,
            base_options=self.BaseOptions(model_asset_path=self.model_path), # Selecting the model
            running_mode=self.VisionRunningMode.LIVE_STREAM, # Configure the gesture recognizer for live stream mode.
            result_callback=self.gesture_result) # When a result is ready, MediaPipe will automatically call print_result.
        
    # Create a gesture recognizer instance with the live stream mode
    def gesture_result(self, result, output_image: mp.Image, timestamp_ms: int):

        # checking if the gestures is empty
        self.gesture_text = ""
        self.text = ""
        self.gesture = []
        self.hand_landmarks = []
        if result.gestures:
            for i in range(len(result.gestures)):
                self.gesture = result.gestures[i][0].category_name
                self.gesture_text = f"Gesture detected: {self.gesture}"
                landmark_list = landmark_pb2.NormalizedLandmarkList()
                # might be a bit confusing but this makes sense since the screen would be mirrored so this appears nicely on the screen

                for lm in result.hand_landmarks[i]:
                    landmark_list.landmark.add(x=lm.x, y=lm.y, z=lm.z)
                self.hand_landmarks.append(landmark_list)

            # print('gesture recognition result: {}'.format(result))

        # if no gesture is being received
        else:
            self.text = "Waiting for gesture"

    
    def gesture_recognition(self, camera):

        with self.GestureRecognizer.create_from_options(self.options) as recognizer:
        # The detector is initialized. Use it here.
            while True:
                camera.frames()
                feed = camera.frames()
                if feed is None:
                    break

                frame, timestamp_ms = feed
                
                # change the image into the correct format for MediaPipe to read it
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

                try:
                    recognizer.recognize_async(mp_image, timestamp_ms) # get the result

                except Exception as e:
                    print(f"Exception: {e}")

                    

                # Putting the text over the image
                colour = (0, 255, 0) if self.text!="Waiting for gesture" else (0, 0, 255)
                cv2.putText(frame, self.gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)


                if self.text == "Waiting for gesture":
                    cv2.putText(frame, self.text, (int(camera.width//2)-130, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2) 
                
                if self.hand_landmarks:
                    self.canvas.draw_single(self.gesture, self.hand_landmarks[0].landmark[8])
                    if self.canvas.mode == "RANDOMISING COLOUR":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2-100), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.canvas.colour, 2)

                    elif self.canvas.mode == "DRAWING":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2-50), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.canvas.colour, 2)

                    elif self.canvas.mode == "PEN LIFTED":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2-50), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.canvas.colour, 2)
                    
                    elif self.canvas.mode == "ERASING":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2-50), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    else:
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)

                blended = self.canvas.blend(frame)

                for hand in self.hand_landmarks:
                    solutions.drawing_utils.draw_landmarks(
                        blended,
                        hand,
                        solutions.hands.HAND_CONNECTIONS,
                        solutions.drawing_styles.get_default_hand_landmarks_style(),
                        solutions.drawing_styles.get_default_hand_connections_style())


                cv2.imshow("camera", blended)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('c'):
                    self.canvas.drawing_surface = np.zeros((round(camera.height), round(camera.width), 3), dtype=np.uint8)
                    self.canvas.colour = (255, 255, 255)

                

        camera.close()

            