import numpy as np
import rpyc
import cv2
from VideoShow import VideoShow

conn = rpyc.connect("localhost",18861)

y = conn.root.threadBoth(0)

print(len(y))
nparr = np.fromstring(y[0],np.uint8)
img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)



video_shower = VideoShow(img).start()

for i in y:
    nparr = np.fromstring(i,np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)

    video_shower.frame = img


