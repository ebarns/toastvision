from SimpleCV import Camera, Display, Image
from facedetection import FaceDetection
from MorphController import MorphController


class ToastVision:
    def __init__(self, audioRecord=False, cameraCount=1, recordVideo=False, linkTwitter=False):
        self.camera = Camera(0, {"width": 640, "height": 480})
        if (cameraCount >= 2):
            self.secondCamera = Camera(1, {"width": 640, "height": 480})
        else:
            self.secondCamera = self.camera
        self.display = Display()
        self.faceDetection = FaceDetection()
        self.pauseFrameCapture = False
        self.counter_max_value = 200
        self.width = 0
        self.height = 0
        self.displayImage = None
        self.videoWriter = None
        self.outputFrame = None
        self.RECORD_VIDEO_SWITCH = recordVideo
        self.RECORD_AUDIO_SWITCH = audioRecord
        self.baseImage = Image()
        self.secondBaseImage = Image()
        self.morphController = MorphController(audioRecord, linkTwitter)

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

    def start(self):
        self.baseImage = self.camera.getImage()
        self.secondBaseImage = self.secondCamera.getImage()
        self.baseImage = self.baseImage.scale(self.baseImage.width, self.baseImage.height )
        self.secondBaseImage = self.secondBaseImage.scale(self.secondBaseImage.width, self.secondBaseImage.height)

        self.displayImage = self.createDisplayImage(self.baseImage)
        self.width = self.displayImage.size()[0]
        self.height = self.displayImage.size()[1]
        # self.setupVideoCapture()
        counter = 0
        while self.display.isNotDone():
            if not self.pauseFrameCapture:
                self.defaultBehavior()
            else:
                counter = (counter + 1) % self.counter_max_value
                img = self.camera.getImage()
                img2 = self.secondCamera.getImage()
                img = img.scale(img.width, img.height)
                img2 = img2.scale(img2.width , img2.height )
                img = self.morphController.morph(img, img2, self.baseImage, self.secondBaseImage, counter, self.displayImage)
                # self.mergeImages(img, img2)
                img.show()
                # self.displayImages()
            self.mouseEventCapture()


t = ToastVision(False, 2 , False, False)
t.start()
