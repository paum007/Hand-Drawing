import cv2
import time

class Camera():
    def __init__(self):
        self.feed = cv2.VideoCapture(1)
        self.feed.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.fps = self.feed.get(cv2.CAP_PROP_FPS)
        self.width = self.feed.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.feed.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.timestamp_ms = 0
        self.live_fps = 0

    def frames(self):

        prev_time=time.time()
        self.timestamp_ms += round(1000/self.fps)
        ret, frame = self.feed.read()
        curr_time = time.time()
        self.live_fps = round(1/(curr_time - prev_time), 0)
        prev_time = curr_time

        if not ret:
            self.close()
            return
        
        # lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        # split = cv2.split(lab) 
        # lightness = split[0]
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        # applied = clahe.apply(lightness)
        # merged = cv2.merge([applied, split[1], split[2]])
        # enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
                
        return cv2.flip(frame, 1), self.timestamp_ms # return enhanced alongside frame if the lighting is a big issue
    
    def close(self):
        self.feed.release()
        cv2.destroyAllWindows()

