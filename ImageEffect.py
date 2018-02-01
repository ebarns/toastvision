import math
from threading import Thread
from SimpleCV import *
from TwitterImage import TwitterConnection
import string
import re


class ImageEffect:
    def __init__(self, record_audio=False, twitter_switch=False):
        self.NAME = "Image effects"
        self.RECORD_AUDIO_SWITCH = record_audio
        self.TWITTER_SWITCH = twitter_switch

        if twitter_switch: self.twitterController = TwitterConnection()
        self.recentTweetImages = []

    #
    # img, img2 = self.applyAudioWarp(counter, img, img2)
    # img, img2 = self.twitter_handler(counter, img, img2)
    # img = self.videoFilter.chooseFilter(counter, img, img2, self.counter_max_value)
    # img2 = self.videoFilter.chooseFilter(counter + 25, img=img, img2=img2, max_index=self.counter_max_value)
    # if counter % 2 == 0:
    #     img = self.imageDifference(img, baseImage)
    #     img2 = self.imageDifference(img2, secondBaseImage)

    def twitter_handler(self, counter, img1, img2):
        if self.TWITTER_SWITCH:
            # if len(self.recentTweetImages) != 0:
            #     print("changing photo")
            #     # self.twitterController.setRecentImage(self.recentTweetImages[0])
            #     self.recentTweetImages = []
            if counter == 105:
                print("updating tweet")
                try:
                    # self.twitterController.updateTweetsAndMedia()
                    t = Thread(target=self.twitterController.updateTweetsAndMedia)
                    t.setDaemon(True)
                    t.start()
                except:
                    print("thread failed to start")
            if counter % 8 <= 4 and self.twitterController.getRecentImage() is not None:
                img2 = self.twitterController.getRecentImage()
                img2 = img2.scale(img1.width, img1.height)

            return img1, img2
        else:
            return img1, img2

    def calculateFontSize(self, width, height, text):
        x = 0
        y = -height / 4
        z = height
        return x, y * .6, int((z * 2) * .6)

    def getTwitterText(self, image):
        text = self.twitterController.recentTweetText
        text = string.replace(text, "@ezbreeezzzy", "")
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
        if len(text) > 0:
            newlayer = DrawingLayer(image.size())
            cy = int(image.height * 2 * (3.3 / len(text)))
            newlayer.setFontSize(cy)
            newlayer.text(text, (0, (image.height / 2) - (cy / 2)), color=Color.WHITE, alpha=150)
            image.addDrawingLayer(newlayer)

        return image

    def imageDifference(self, img1, img2):
        return img1 - img2

    def imageAddition(self, img1, img2):
        return img1 + img2

    def getImageDifferenceMask(self, img, img2, baseImage, secondBaseImage, counter):
        if counter % 2 == 0:
            img = self.imageDifference(img, baseImage)
            img2 = self.imageDifference(img2, secondBaseImage)

        if counter % 4 == 0:
            baseImage = img
            secondBaseImage = img2

        return img, img2, baseImage, secondBaseImage

    def getCorners(self, counter, soundSum, width, height):
        # adjustCounter = (counter) % 4
        selectedCorner = (counter / 4) % 4

        if (selectedCorner == 0):
            return [(soundSum, soundSum), (width, 0), (width, height), (0, height)]
        elif (selectedCorner == 1):
            return [(0, 0), (width - soundSum, soundSum), (width, height), (0, height)]
        elif (selectedCorner == 2):
            return [(0, 0), (width, 0), (width - soundSum, height - soundSum), (0, height)]
        else:
            return [(0, 0), (width, 0), (width, height), (soundSum, height - soundSum)]

    def getRotatingCorners(self, counter, width, height):
        modCounter = (counter % 4) + 1
        soundSum = 20 * modCounter
        decreasingSoundSum = (((modCounter * 3) % 4) + 1) * 20
        selectedCorner = (math.floor(counter / 4.0)) % 4

        if (selectedCorner == 0):
            return [(soundSum, soundSum),
                    (width, 0),
                    (width, height),
                    (decreasingSoundSum, height - decreasingSoundSum)]
        elif (selectedCorner == 1):
            return [(decreasingSoundSum, decreasingSoundSum),
                    (width - soundSum, soundSum),
                    (width, height),
                    (0, height)]
        if (selectedCorner == 2):
            return [(0, 0),
                    (width - decreasingSoundSum, decreasingSoundSum),
                    (width - soundSum, height - soundSum),
                    (0, height)]
        else:
            return [(0, 0),
                    (width, 0),
                    (width - decreasingSoundSum, height - decreasingSoundSum),
                    (soundSum, height - soundSum)]
            # return [(0, 0), (width, 0), (width, height), (0, height)]
        # return [(soundSum, soundSum), (width - adjustCounter, adjustCounter), (width, height),
        #             (adjustCounter, height - adjustCounter)]
        # else:

    def applyCircularWarp(self,counter, img, img2):
        corners = self.getRotatingCorners(counter, img.width, img.height)
        img = img.warp(corners)
        img2 = img2.warp(corners)
        return img, img2

    def applyAudioWarp(self, counter, img, img2, soundSum, override=False):
        if self.RECORD_AUDIO_SWITCH or override:
            if not math.isnan(soundSum):
                if soundSum >= 1:
                    adjustedSum = soundSum * 15
                    if adjustedSum < img.width and adjustedSum < img.height:
                        corners = self.getCorners(counter, adjustedSum, img.width, img.height)
                        img = img.warp(corners)
                        img2 = img2.warp(corners)
                        # img = self.videoFilter.getFilterFromAudio(img, soundSum)
                        # img2 = self.videoFilter.getFilterFromAudio(img2, soundSum)

        return img, img2
