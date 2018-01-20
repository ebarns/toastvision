from SimpleCV import *
import pyaudio
import sounddevice as sd
import math

class ToastVision:
    def __init__(self):
        self.camera = Camera(0, {"width": 640, "height": 480})
        self.secondCamera = Camera(1, {"width": 640, "height": 480})
    ##    cameraManager = CameraManager()
        self.display = Display()
        self.videoFilter = VideoFilters()
        self.faceDetection = FaceDetection()
        self.pauseFrameCapture = False
        self.counter = 0
        self.recorder = AudioRecorder()
        self.recorder.record()
        self.width = 0
        self.height = 0


    def imageDifference(self,img1, img2):
        return img1 - img2

    def getCorners(self,counter, soundSum, width, height):
        selectedCorner = (counter/4) % 4
        if(selectedCorner == 0): return [(soundSum, soundSum), (width, 0),(width, height),(0, height)] 
        elif(selectedCorner == 1): return [(0, 0), (width - soundSum, soundSum),(width, height),(0, height)] 
        elif(selectedCorner == 2 ): return [(0, 0), (width, 0),(width - soundSum, height - soundSum),(0, height)] 
        else: return [(0, 0), (width, 0),(width, height),(soundSum, height - soundSum)]

    def start(self):
        baseImage = self.camera.getImage()
        baseImage.show()
        self.width = baseImage.size()[0]
        self.height = baseImage.size()[1]
        displayImage = baseImage.scale(1280,480)
        displayImage = displayImage - displayImage
        displayImage.show()
        counter = 0
        while self.display.isNotDone():
            counter = (counter + 1) % 200
            if not self.pauseFrameCapture:
                img = self.camera.getImage()
                img2 = self.secondCamera.getImage()
                displayImage.dl().blit(img)
                displayImage.dl().blit(img2, (640,0))
                displayImage.show()
            else:
                img = self.camera.getImage()
                img2 = self.secondCamera.getImage()
    ##            faceCoords = faceDetection.getFaceCoordinates(img)
    ##            data = recorder.getRecentRecording()
    ##            peak=np.average(np.abs(data))*2
    ##            bars="#"*int(50*peak/2**16)
    ##            print("%05d %s"%(peak,bars))
                
                soundSum = 0
                soundSum = self.recorder.getVolumeUnits()
    ##            soundSum = abs(round(sum(recorder.getRecentRecording())[0])) % 20
                if(not math.isnan(soundSum)):
                    if(soundSum >= 1):
                        adjustedSum = soundSum * 15
                        if(adjustedSum < self.width and adjustedSum < self.height):
                            corners = self.getCorners(counter,adjustedSum, self.width, self.height)
                            img = img.warp(corners)
                            img2 = img2.warp(corners)
    ##            img = videoFilter.chooseFilter(counter,img)                
                img = self.videoFilter.getFilterFromAudio(img,soundSum)
                img2 = self.videoFilter.getFilterFromAudio(img2,soundSum)
    ##            img = imageDifference(img,baseImage)
    ##            img = faceDetection.addBoxToFace(faceCoords, img)
        
                if(counter % 4 == 0):
                    img = self.imageDifference(img,baseImage)
                    baseImage = img
    ##            displayImage[0:640, 0: 480] = img
                displayImage.dl().blit(img)
                displayImage.dl().blit(img2, (640,0))
                displayImage.show()
            if self.display.mouseLeft:
                self.pauseFrameCapture = True
            if self.display.mouseRight:
                baseImage = self.camera.getImage()
            if self.display.mouseMiddle:
                self.recorder.stop()
                self.display.done = True
                return

def main():
    camera = Camera(0, {"width": 640, "height": 480})
    secondCamera = Camera(1, {"width": 640, "height": 480})
##    cameraManager = CameraManager()
    display = Display()
    baseImage = camera.getImage()
    baseImage.show()
    videoFilter = VideoFilters()
    faceDetection = FaceDetection()
    pauseFrameCapture = False
    counter = 0
    recorder = AudioRecorder()
    recorder.record()
    width = baseImage.size()[0]
    height = baseImage.size()[1]
    displayImage = baseImage.scale(1280,480)
    displayImage = displayImage - displayImage
    displayImage.show()
    
    while display.isNotDone():
        counter = (counter + 1) % 200
        if not pauseFrameCapture:
            img = camera.getImage()
            img2 = secondCamera.getImage()
            displayImage.dl().blit(img)
            displayImage.dl().blit(img2, (640,0))
            displayImage.show()
        else:
            img = camera.getImage()
            img2 = secondCamera.getImage()
##            faceCoords = faceDetection.getFaceCoordinates(img)
##            data = recorder.getRecentRecording()
##            peak=np.average(np.abs(data))*2
##            bars="#"*int(50*peak/2**16)
##            print("%05d %s"%(peak,bars))
            
            soundSum = 0
            soundSum = recorder.getVolumeUnits()
##            soundSum = abs(round(sum(recorder.getRecentRecording())[0])) % 20
            if(not math.isnan(soundSum)):
                if(soundSum >= 1):
                    adjustedSum = soundSum * 15
                    if(adjustedSum < width and adjustedSum < height):
                        corners = getCorners(counter,adjustedSum, width, height)
                        img = img.warp(corners)
                        img2 = img2.warp(corners)
##            img = videoFilter.chooseFilter(counter,img)                
            img = videoFilter.getFilterFromAudio(img,soundSum)
            img2 = videoFilter.getFilterFromAudio(img2,soundSum)
##            img = imageDifference(img,baseImage)
##            img = faceDetection.addBoxToFace(faceCoords, img)
    
            if(counter % 4 == 0):
                img = imageDifference(img,baseImage)
                baseImage = img
##            displayImage[0:640, 0: 480] = img
            displayImage.dl().blit(img)
            displayImage.dl().blit(img2, (640,0))
            displayImage.show()
        if display.mouseLeft:
            pauseFrameCapture = True
        if display.mouseRight:
            baseImage = camera.getImage()
        if display.mouseMiddle:
            recorder.stop()
            display.done = True
            return
    
def imageDifference(img1, img2):
    return img1 - img2

def getCorners(counter, soundSum, width, height):
    selectedCorner = (counter/4) % 4
    if(selectedCorner == 0): return [(soundSum, soundSum), (width, 0),(width, height),(0, height)] 
    elif(selectedCorner == 1): return [(0, 0), (width - soundSum, soundSum),(width, height),(0, height)] 
    elif(selectedCorner == 2 ): return [(0, 0), (width, 0),(width - soundSum, height - soundSum),(0, height)] 
    else: return [(0, 0), (width, 0),(width, height),(soundSum, height - soundSum)]

def video():
    vs = VideoStream("myvideo.avi", 25, True)


class CameraManager:
    def __init__(self):
        self.camera = Camera(0, {"width": 640, "height": 640})
        self.secondCamera = Camera(1, {"width": 640, "height": 640})
        self.chosenCamera = None

    def setChosen(self, switch):
        if switch: self.chosenCamera = self.camera
        else: self.chosenCamera = self.secondCamera

    def getChosen(self):
        return self.chosenCamera

    def getComputerCamera(self):
        return self.camera

    def getUSBCamera(self):
        return self.secondCamera.getImage()

    def chooseCamera(self, counter):
        if(counter % 2 == 0):
            return self.camera
        else: return self.secondCamera

class FaceDetection:
    def __init__(self):
        self.__NAME = "FACEDETECTION"

    def getFaceCoordinates(self, img):
        coords = []
        faces = img.findHaarFeatures("C:\Python27\workspace\haarcascade_frontalface_default.xml")
        if faces:
            face = faces[0]
            coords.append((face.coordinates()[0], face.coordinates()[1]))

        return coords

    def addBoxToFace(self, coords, img):
        if(len(coords) > 0):
            facebox_dim = (100,100)
##            for coord in coords:
##                print(coord)
            coords = coords[0]
            facelayer = DrawingLayer((img.width, img.height))
            facebox = facelayer.centeredRectangle(coords, facebox_dim, color=(255,255,255),filled=True)
            facelayer.text("Human", coords)
            img.addDrawingLayer(facelayer)
                
            img.applyLayers()

        return img

class AudioRecorder:
    def __init__(self):
        self.pAudio = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 0.25
        self.CHUNK = 2 ** 11
        self.recentRecording = []

    def getVolumeUnits(self):
        data = self.getRecentRecording()
        peak=np.average(np.abs(data))*2
        bars=int(50*peak/2**16)
        return bars
##        print("%05d %s"%(peak,bars))

    def getRecentRecording(self):
##        return self.recentRecording
        return np.fromstring(self.recentRecording.read(self.CHUNK),dtype=np.int16)

    def record(self):
        # Learn what your OS+Hardware can do
##        defaultCapability = self.pAudio.get_default_host_api_info()
##        print defaultCapability
##
##        # See if you can make it do what you want
##        isSupported = self.pAudio.is_format_supported(input_format=self.FORMAT, input_channels=1, rate=self.RATE, input_device=0)
##        print isSupported
##        self.recentRecording = sd.rec(self.RECORD_SECONDS *  self.RATE,channels=1)
        try:
            self.recentRecording = self.pAudio.open(format=self.FORMAT,channels=1,rate=self.RATE,input=True,
              frames_per_buffer=self.CHUNK)
        except:
            print("not recording")
    def stop(self):
        self.recentRecording.stop_stream()
        self.recentRecording.close()
        self.pAudio.terminate()

class VideoFilters:
    def getRed(self, img):
        (r,g,b) = img.splitChannels(False)
        r = r.toXYZ()
        return r + g + b

    def getGreen(self, img):
        (r,g,b) = img.splitChannels(False)
        g2 = g.toXYZ()
        return g + g2 + b
    
    def getBlue(self, img):
        (r,g,b) = img.splitChannels(False)
        b = b.toXYZ()
        return r + g + b
    
    def getYellow(self, img):
        (r,g,b) = img.splitChannels(False)
        b2 = r.toXYZ()
        return r + b + b2

    def getHSV(self, img):
        return img.toHSV()

    def getXYZ(self, img):
        return img.toXYZ()

##    def getX(self):
##        (r,g,b) = self.camera.getImage().splitChannels(False)
##        b2 = r.toXYZ()
##        return r + g + b2

    def readImageText(self, img):
        text = img.readText()
        if(len(text) > 0 ):
            print(text)

    def getFilterFromAudio(self, img, audioSum):
        colorChooser = audioSum
##        colorChooser = audioSum % 6
##        print(colorChooser)

        if(colorChooser == 0): return self.getYellow(img)
        elif colorChooser == 1: return self.getBlue(img)
        elif colorChooser == 2: return self.getGreen(img)
        elif colorChooser == 3: return self.getRed(img)
        elif colorChooser == 4: return self.getHSV(img)
        else: return self.getGreen(img)
    
    def chooseFilter(self,index, img):
        if(index <= 50): return self.getYellow(img)
        elif(index <= 100): return self.getBlue(img)
        elif(index <= 150): return self.getRed(img)
        else: return self.getGreen(img)

t = ToastVision()
t.start()
