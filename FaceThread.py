from threading import Thread
import cv2

class FaceThread:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None,face_cascade=None):
        self.count =0
        self.frame = frame
        self.face_cascade = face_cascade
        self.stopped = False

    def start(self):
        Thread(target=self.detect, args=()).start()
        return self

    def detect(self):
        while not self.stopped:
            print("face detect")
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            self.count = self.count + 1
            # Display the resulting frame
            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 4)



    def stop(self):
        self.stopped = True



