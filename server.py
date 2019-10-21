import rpyc
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
from FaceThread import FaceThread

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class MyService(rpyc.Service):
    def on_connect(self, conn):
        print("Client Connected")

    def putIterationsPerSec(frame, iterations_per_sec):
        cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
                    (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        return frame

    def exposed_threadBoth(self,source=0):

        video_getter = VideoGet(source).start()
        face_thread = FaceThread(video_getter.frame, face_cascade).start()
        # video_shower = VideoShow(video_getter.frame).start()
        cps = CountsPerSec().start()

        frames = []
        count = 0
        while True:
            if video_getter.stopped or face_thread.stopped:
                # video_shower.stop()
                video_getter.stop()
                face_thread.stop()
                break

            frame = video_getter.frame
            face_thread.frame = frame
            # frame = putIterationsPerSec(frame, cps.countsPerSec())

            # video_shower.frame = face_thread.frame
            cps.increment()
            img_encoded = cv2.imencode('.jpg', face_thread.frame)[1].tostring()

            frames.append(img_encoded)
            count=count+1
            if count == 500:
                break

        return frames

    def exposed_readImage(self):

        img = cv2.imread("faces.jpg")
        img_encoded = cv2.imencode('.jpg', img)[1].tostring()

        return img_encoded

    def on_disconnect(self, conn):
        print("Client disconnected")

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(MyService, port=18861, protocol_config={
        'allow_public_attrs': True,
    })
    server.start()