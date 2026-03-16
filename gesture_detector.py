import cv2
import mediapipe as mp
from canvas import Canvas
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


class GestureDetector:
    def __init__(self, camera):
        
        self.canvas = Canvas(camera)
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.model_path = 'gesture_recognizer.task'

        self.left_gesture = []
        self.right_gesture = []
        self.hand_landmarks_left = []
        self.hand_landmarks_right = []
        self.hand = []
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
        self.text = ""
        self.left_text = ""
        self.right_text = ""

        self.options = self.GestureRecognizerOptions(
            num_hands = 2,
            base_options=self.BaseOptions(model_asset_path=self.model_path), # Selecting the model
            running_mode=self.VisionRunningMode.LIVE_STREAM, # Configure the gesture recognizer for live stream mode.
            result_callback=self.gesture_result) # When a result is ready, MediaPipe will automatically call print_result.
        
    # Create a gesture recognizer instance with the live stream mode
    def gesture_result(self, result, output_image: mp.Image, timestamp_ms: int):

        # checking if the gestures is empty
        self.left_text = ""
        self.right_text = ""
        self.text = ""
        self.left_gesture = []
        self.right_gesture = []
        self.hand_landmarks_left = []
        self.hand_landmarks_right = []
        self.hand = []
        if result.gestures:
            for i in range(len(result.gestures)):
                gesture = result.gestures[i][0].category_name
                self.hand = result.handedness[i][0].category_name
                landmark_list = landmark_pb2.NormalizedLandmarkList()
                # might be a bit confusing but this makes sense since the screen would be mirrored so this appears nicely on the screen
                if self.hand == "Left":
                    self.left_gesture = gesture
                    self.right_text = f"Right hand: {self.left_gesture}"
                    for lm in result.hand_landmarks[i]:
                        landmark_list.landmark.add(x=lm.x, y=lm.y, z=lm.z)
                    self.hand_landmarks_right.append(landmark_list)
                else:
                    self.right_gesture = gesture
                    self.left_text = f"Left hand: {self.right_gesture}"

                    for lm in result.hand_landmarks[i]:
                        landmark_list.landmark.add(x=lm.x, y=lm.y, z=lm.z)
                    self.hand_landmarks_left.append(landmark_list)

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
                result = recognizer.recognize_async(mp_image, timestamp_ms) # get the result
                # Putting the text over the image
                colour = (0, 255, 0) if self.text!="Waiting for gesture" else (0, 0, 255)

                if self.text == "Waiting for gesture":
                    cv2.putText(frame, self.text, (int(camera.width//2)-130, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2) 

                cv2.putText(frame, self.left_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)
                cv2.putText(frame, self.right_text, (int(camera.width-300), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)
                
                if self.hand_landmarks_right:
                    self.canvas.draw(self.left_gesture, self.right_gesture, self.hand_landmarks_right[0].landmark[8])
                    if self.canvas.mode == "RANDOMISING COLOUR":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2-100), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.canvas.colour, 2)

                    elif self.canvas.mode == "DRAWING":
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.canvas.colour, 2)

                    else:
                        cv2.putText(frame, self.canvas.mode, (int(camera.width//2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)

                blended = self.canvas.blend(frame)

                for hand in self.hand_landmarks_left:
                    solutions.drawing_utils.draw_landmarks(
                        blended,
                        hand,
                        solutions.hands.HAND_CONNECTIONS,
                        solutions.drawing_styles.get_default_hand_landmarks_style(),
                        solutions.drawing_styles.get_default_hand_connections_style())

                for hand in self.hand_landmarks_right:
                    solutions.drawing_utils.draw_landmarks(
                        blended,
                        hand,
                        solutions.hands.HAND_CONNECTIONS,
                        solutions.drawing_styles.get_default_hand_landmarks_style(),
                        solutions.drawing_styles.get_default_hand_connections_style())


                cv2.imshow("camera", blended)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        camera.close()

            