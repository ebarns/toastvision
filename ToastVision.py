from SimpleCV import Camera, Display, Image
import numpy as np
import math
import cv2
from videofilter import VideoFilters
from audiorecorder import AudioRecorder
from facedetection import FaceDetection
from TwitterImage import TwitterConnection
from threading import Thread
from ImageEffect import ImageEffect


class ToastVision:
    def __init__(self, audioRecord=False, cameraCount=1, recordVideo=False, linkTwitter=False):
        self.camera = Camera(0, {"width": 640, "height": 480})
        if (cameraCount >= 2):
            self.secondCamera = Camera(1, {"width": 640, "height": 480})
        else:
            self.secondCamera = self.camera
        self.display = Display()
        self.videoFilter = VideoFilters()
        self.faceDetection = FaceDetection()
        self.pauseFrameCapture = False
        self.counter_max_value = 200
        self.recorder = AudioRecorder()
        self.recorder.record()
        self.width = 0
        self.height = 0
        self.displayImage = None
        self.videoWriter = None
        self.outputFrame = None
        # self.twitterController = TwitterConnection()
        self.imageEffects = ImageEffect(audioRecord, linkTwitter, )
        self.RECORD_VIDEO_SWITCH = recordVideo
        self.RECORD_AUDIO_SWITCH = audioRecord
        self.TWITTER_SWITCH = linkTwitter
        self.recentTweetImages = []
        self.baseImage = Image()
        self.secondBaseImage = Image()

    def createDisplayImage(self, image):
        displayImage = image.scale(1280, 480)
        displayImage = displayImage - displayImage
        return displayImage

    def mergeImages(self, firstImage, secondImage):
        self.displayImage.dl().blit(firstImage)
        self.displayImage.dl().blit(secondImage, (640, 0))

    def displayImages(self, display=True):
        if display and self.displayImage: self.displayImage.show()

    def defaultBehavior(self):
        img = self.camera.getImage()
        img2 = self.secondCamera.getImage()
        self.mergeImages(img, img2)
        self.displayImages()

    def mouseEventCapture(self):

        if self.display.mouseLeft:
            print("pause/play")
            self.pauseFrameCapture = not self.pauseFrameCapture
        if self.display.mouseRight:
            self.baseImage = self.camera.getImage()
            self.secondBaseImage = self.secondCamera.getImage()
        if self.display.mouseMiddle:
            if self.RECORD_AUDIO_SWITCH: self.recorder.stop()
            self.display.done = True

    def eriksMorph(self, img, img2, counter):
        img, img2 = self.imageEffects.twitter_handler(counter, img, img2)
        img, img2 = self.audioMorph(img, img2, counter)
        img = self.videoFilter.chooseFilter(counter, img, img2, self.counter_max_value)
        img2 = self.videoFilter.chooseFilter(counter + 5, img2, max_index=self.counter_max_value)
        # img2 = self.videoFilter.chooseFilter(counter + 25, img=img, img2=img2, max_index=self.counter_max_value)

        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)
        return img, img2

    def audioMorph(self, img, img2, counter):
        if self.RECORD_AUDIO_SWITCH:
            soundSum = self.recorder.getVolumeUnits()
            img, img2 = self.imageEffects.applyAudioWarp(counter, img, img2, soundSum)
            img = self.videoFilter.getFilterFromAudio(img, soundSum)
            img2 = self.videoFilter.getFilterFromAudio(img2, soundSum)
            return img, img2

    def eriksMorph2(self, img, img2, counter):
        img, img2 = self.imageEffects.applyAudioWarp(counter, img, img2)
        # img, img2 = self.imageEffects.twitter_handler(counter, img, img2)
        img = self.videoFilter.chooseFilter(counter, img, img2, 50)
        img2 = self.videoFilter.chooseFilter(counter + 5, img2, 50)

        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)
        return img, img2

    def start(self):
        self.baseImage = self.camera.getImage()
        self.secondBaseImage = self.secondCamera.getImage()
        self.displayImage = self.createDisplayImage(self.baseImage)
        self.width = self.displayImage.size()[0]
        self.height = self.displayImage.size()[1]
        # self.setupVideoCapture()
        counter = 0
        self.recentTweetImages = []
        while self.display.isNotDone():
            if not self.pauseFrameCapture:
                self.defaultBehavior()
            else:
                counter = (counter + 1) % self.counter_max_value
                img = self.camera.getImage()
                img2 = self.secondCamera.getImage()
                img, img2 = self.eriksMorph(img, img2, counter)
                self.mergeImages(img, img2)
                # self.displayImage = self.imageEffects.getTwitterText(self.displayImage)
                self.displayImages()
            self.mouseEventCapture()


t = ToastVision(False, 2, False, False)
t.start()
