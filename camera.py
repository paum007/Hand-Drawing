import cv2

class Camera():
    def __init__(self):
        self.feed = cv2.VideoCapture(1)
        self.feed.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.fps = self.feed.set(cv2.CAP_PROP_FPS, 20)
        self.width = self.feed.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.feed.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.timestamp_ms = 0

    def frames(self):

        self.timestamp_ms += round(1000/self.fps)
        ret, frame = self.feed.read()

        if not ret:
            self.close()
            return
                
        return cv2.flip(frame, 1), self.timestamp_ms
    
    def camera_info(self):
        return self.fps, 
    
    def close(self):
        self.feed.release()
        cv2.destroyAllWindows()

