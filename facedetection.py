from SimpleCV import *
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
        if (len(coords) > 0):
            facebox_dim = (100, 100)
            ##            for coord in coords:
            ##                print(coord)
            coords = coords[0]
            facelayer = DrawingLayer((img.width, img.height))
            facebox = facelayer.centeredRectangle(coords, facebox_dim, color=(255, 255, 255), filled=True)
            facelayer.text("Human", coords)
            img.addDrawingLayer(facelayer)

            img.applyLayers()

        return img