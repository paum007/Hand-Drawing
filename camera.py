import cv2

class Camera():
    def __init__(self):
        self.feed = cv2.VideoCapture(1)
        self.feed.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.fps = self.feed.set(cv2.CAP_PROP_FPS, 60)
        self.width = self.feed.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.feed.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.timestamp_ms = 0

    def frames(self):

        self.timestamp_ms += round(1000/self.fps)
        ret, frame = self.feed.read()

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
                
        return frame, self.timestamp_ms # return enhanced alongside frame if the lighting is a big issue
    
    def camera_info(self):
        return self.fps, 
    
    def close(self):
        self.feed.release()
        cv2.destroyAllWindows()

