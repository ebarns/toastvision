class VideoFilters:
    def __init__(self, filter_cycle=200):
        self.NAME = "VIDEO FILTER"
        self.FILTER_CYCLE = filter_cycle
        self.filter_bounds = []
        self.updateFilterBounds(filter_cycle)

    def getRed(self, img):
        (r, g, b) = img.splitChannels(False)
        r = r.toXYZ()
        return r + g + b

    def getGreen(self, img):
        (r, g, b) = img.splitChannels(False)
        g2 = g.toXYZ()
        return g + g2 + b

    def getBlue(self, img):
        (r, g, b) = img.splitChannels(False)
        b = b.toXYZ()
        return r + g + b

    def getYellow(self, img):
        (r, g, b) = img.splitChannels(False)
        b2 = r.toXYZ()
        return r + b + b2

    def getRedOnly(self, img):
        (r, g, b) = img.splitChannels(False)
        return r + r + r

    def getPink(self, img):
        (r, g, b) = img.splitChannels(False)
        return r + r + b

    def getBlueOnly(self, img):
        (r, g, b) = img.splitChannels(False)
        return b + b + b

    def getOrange(self, img):
        (r, g, b) = img.splitChannels(False)
        return r + r + g

    def getPurpleBlue(self, img):
        (r, g, b) = img.splitChannels(False)
        return r + b + b

    def getHSV(self, img):
        return img.toHSV()

    def mergeImageChannels(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r + g2 + b

    def mergeImageChannels1(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r + g + b2

    def mergeImageChannels2(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r + g2 + b2

    def mergeImageChannels3(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r2 + g + b

    def mergeImageChannels4(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r2 + g + b2

    def mergeImageChannels5(self, img1, img2):
        (r, g, b) = img1.splitChannels(False)
        (r2, g2, b2) = img2.splitChannels(False)

        return r2 + g2 + b

    def getXYZ(self, img):
        return img.toXYZ()

    def readImageText(self, img):
        text = img.readText()
        if (len(text) > 0):
            print(text)

    def getFilterFromAudio(self, img, audioSum):
        colorChooser = audioSum
        ##        colorChooser = audioSum % 6
        ##        print(colorChooser)

        if (colorChooser == 0):
            return self.getYellow(img)
        elif colorChooser == 1:
            return self.getBlue(img)
        elif colorChooser == 2:
            return self.getGreen(img)
        elif colorChooser == 3:
            return self.getRed(img)
        elif colorChooser == 4:
            return self.getHSV(img)
        else:
            return self.getGreen(img)

    def updateFilterBounds(self, new_max):
        self.FILTER_CYCLE = new_max
        index_increments = int(self.FILTER_CYCLE / 8)
        self.filter_bounds = [bound * index_increments for bound in range(1, 8)]

    def chooseFilter(self, index, img, img2=None, max_index=200):
        if max_index != self.FILTER_CYCLE:
            self.updateFilterBounds(max_index)

        if index <= self.filter_bounds[0]:
            if img2 is not None:
                return self.mergeImageChannels(img, img2)
            else:
                return self.getBlueOnly(img)
        if index <= self.filter_bounds[1]:
            if img2 is not None:
                return self.mergeImageChannels1(img, img2)
            else:
                return self.getRedOnly(img)
        if index <= self.filter_bounds[2]:
            if img2 is not None:
                return self.mergeImageChannels2(img, img2)
            else:
                return self.getBlue(img)
        if index <= self.filter_bounds[3]:
            if img2 is not None:
                return self.mergeImageChannels3(img, img2)
            else:
                return self.getPink(img)
        if index <= self.filter_bounds[4]:
            if img2 is not None:
                return self.mergeImageChannels4(img, img2)
            else:
                return self.getPurpleBlue(img)
        if index <= self.filter_bounds[5]:
            if img2 is not None:
                return self.mergeImageChannels5(img, img2)
            else:
                return self.getOrange(img)
        if index <= self.filter_bounds[6]:
            return self.getYellow(img)
        else:
            return self.getGreen(img)
        # if index <= 25:
        #     return self.getBlueOnly(img)
        # if index <= 50:
        #     return self.getRedOnly(img)
        # if index <= 75:
        #     return self.getBlue(img)
        # if index <= 100:
        #     return self.getPink(img)
        # if index <= 125:
        #     return self.getPurpleBlue(img)
        # if index <= 150:
        #     return self.getOrange(img)
        # if index <= 175:
        #     return self.getYellow(img)
        # else:
        #     return self.getGreen(img)
