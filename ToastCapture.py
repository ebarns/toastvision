import cv2
import numpy as np

class ToastCapture:
    def __init__(self, record_video):
        self.NAME = "toast cap"
        self.RECORD_VIDEO_SWITCH = record_video
        self.outputFrame = None
        self.videoWriter = None


    def setupVideoCapture(self, displayImage):
        if self.RECORD_VIDEO_SWITCH:
            self.width = int(displayImage.size()[0])
            self.height = int(displayImage.size()[1])
            self.outputFrame = np.zeros((self.width, self.height, 3))
            fourcc = cv2.cv.CV_FOURCC(*'MJPG')
            self.videoWriter = cv2.VideoWriter("toastvision.avi", fourcc, 20.0,
                                               (self.width, self.height))

    def recordVideoFrame(self):
        if self.RECORD_VIDEO_SWITCH:
            print("recording video")
            print(self.displayImage)
            print(self.outputFrame)
            print(self.height)
            print(self.width)
            print(self.outputFrame[0:self.height, 0:self.width])
            print(len(self.outputFrame))
            print(len(self.displayImage.getNumpy()))
            self.outputFrame[0:self.width, 0:self.height] = self.displayImage.getNumpy()
            self.videoWriter.write(self.outputFrame)
