from videofilter import VideoFilters
from ImageEffect import ImageEffect
from audiorecorder import AudioRecorder
from SimpleCV import Image, Color, time
from ImageColor import getcolor
from PIL import Image as Pimage


class MorphController:
    def __init__(self, record_audio, link_twitter):
        self.videoFilter = VideoFilters()
        self.imageEffects = ImageEffect(record_audio, link_twitter)
        self.filterRange = 200
        self.RECORD_AUDIO_SWITCH = record_audio
        self.displayImage = None
        self.baseImage = None
        self.secondBaseImage = None
        if record_audio:
            self.recorder = AudioRecorder()
            self.recorder.record()

    def eriksMorph(self, img, img2, counter):
        img, img2 = self.imageEffects.twitter_handler(counter, img, img2)
        img, img2 = self.audioMorph(img, img2, counter)
        img = self.videoFilter.chooseFilter(counter, img, img2, self.filterRange)
        img2 = self.videoFilter.chooseFilter(index=counter + 5, img=img2, max_index=self.filterRange)
        # img2 = self.videoFilter.chooseFilter(counter + 25, img=img, img2=img2, max_index=self.counter_max_value)

        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)
        self.displayImage.dl().blit(img, (0, 0))
        self.displayImage.dl().blit(img2, (img.width, 0))
        return self.displayImage


    def audioMorph(self, img, img2, counter):
        if self.RECORD_AUDIO_SWITCH:
            soundSum = self.recorder.getVolumeUnits()
            img, img2 = self.imageEffects.applyAudioWarp(counter, img, img2, soundSum)
            img = self.videoFilter.getFilterFromAudio(img, soundSum)
            img2 = self.videoFilter.getFilterFromAudio(img2, soundSum)

        return img, img2

    def eriksMorph2(self, img, img2, counter):
        img, img2 = self.imageEffects.applyCircularWarp(counter, img, img2)
        img, img2 = self.imageEffects.twitter_handler(counter, img, img2)
        img = self.videoFilter.chooseFilter(counter, img=img, max_index=50)
        img2 = self.videoFilter.chooseFilter(index=counter + 5, img=img2, max_index=50)

        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)

        self.displayImage.dl().blit(img, (0, 0))
        self.displayImage.dl().blit(img2, (img.width, 0))
        return self.displayImage

    def multiply(self, img, img2, counter):
        img_copy = img.copy()
        img_copy2 = img2.copy()
        img_copy = img_copy.scale(img.width / 2, img.height / 2)
        img_copy2 = img_copy2.scale(img.width / 2, img.height / 2)
        width_padding = img.width - img_copy.width
        height_padding = img.height - img_copy.height

        x_shift = 10 * counter % width_padding
        y_shift = 10 * counter % height_padding

        self.displayImage.dl().blit(img_copy, (0 + x_shift, 0))
        self.displayImage.dl().blit(img_copy2, (width_padding, 0 + y_shift))
        self.displayImage.dl().blit(img_copy2, (0, height_padding - y_shift))
        self.displayImage.dl().blit(img_copy, (width_padding - x_shift, height_padding))

        base_width = img.width + width_padding
        self.displayImage.dl().blit(img_copy, (img.width + x_shift, 0))
        self.displayImage.dl().blit(img_copy2, (base_width, 0 + y_shift))
        self.displayImage.dl().blit(img_copy2, (img.width, height_padding - y_shift))
        self.displayImage.dl().blit(img_copy, (base_width - x_shift, height_padding))



    def greenScreen(self, img, img2, counter):
        mask = img.hueDistance(color=Color.WHITE).binarize()
        background = Image("./deer_decode.jpg")
        background = background.scale(1280, 960)
        a = (img - mask)
        b = (background - mask.invert())
        result = (a) + (b)
        return result, img2

    def multiplyByFactor(self, img, img2, counter, factor=1, shift=True):

        img_copy = img.copy()
        img_copy2 = img2.copy()
        # division_factor = 2 * factor
        division_factor = 2
        img_copy = img_copy.scale(img.width / division_factor, img.height / division_factor)
        img_copy2 = img_copy2.scale(img.width / division_factor, img.height / division_factor)

        width_padding = img.width - img_copy.width
        height_padding = img.height - img_copy.height

        if shift:
            x_shift = 10 * counter % width_padding
            y_shift = 10 * counter % height_padding
        else:
            x_shift = 0
            y_shift = 0

        for i in range(factor):
            pos_x = i * img_copy.width
            pos_y = i * img_copy.height
            self.displayImage.dl().blit(img_copy, (pos_x + x_shift, pos_y))
            self.displayImage.dl().blit(img_copy2, (width_padding - pos_x, pos_y + y_shift))
            self.displayImage.dl().blit(img_copy, (width_padding - x_shift - pos_x, height_padding - pos_y))
            self.displayImage.dl().blit(img_copy2, (pos_x, height_padding - pos_y - y_shift))

            base_pos_x = img.width + pos_x
            base_width = img.width + width_padding
            self.displayImage.dl().blit(img_copy, (base_pos_x + x_shift, pos_y))
            self.displayImage.dl().blit(img_copy2, (base_width - pos_x, pos_y + y_shift))
            self.displayImage.dl().blit(img_copy, (base_width - x_shift - pos_x, height_padding - pos_y))
            self.displayImage.dl().blit(img_copy2, (base_pos_x, height_padding - pos_y - y_shift))

        # self.displayImage.dl().blit(img2, (img.width, 0))
        # self.displayImage.dl().blit(img2, (img.width, 0))
        # return self.displayImage

    def multiplyMorph(self, img, img2, counter):
        img = self.videoFilter.chooseFilter(index=counter + 5, img=img, img2=img2, max_index=self.filterRange)
        img2 = self.videoFilter.chooseFilter(index=counter + 25, img=img2, max_index=self.filterRange)
        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)

        self.multiply(img, img2, counter)
        return self.displayImage

    def tileMorph(self, img, img2, counter):
        img = self.videoFilter.chooseFilter(index=counter + 30, img=img, max_index=self.filterRange)
        img2 = self.videoFilter.chooseFilter(index=counter, img=img2, max_index=self.filterRange)
        self.multiplyByFactor(img, img2, counter, 3, shift=False)
        return self.displayImage

    def scrambleMorph(self, img, img2, counter):
        img = self.videoFilter.chooseFilter(index=counter + 60, img=img, img2=img2, max_index=self.filterRange)
        img2 = self.videoFilter.chooseFilter(index=counter + 80, img=img2, max_index=self.filterRange)
        img, img2, self.baseImage, self.secondBaseImage = \
            self.imageEffects.getImageDifferenceMask(img, img2, self.baseImage, self.secondBaseImage, counter)
        img, img2 = self.imageEffects.applyCircularWarp(counter, img, img2)
        # img = img - img_copy
        self.multiplyByFactor(img, img2, counter, 4)
        return self.displayImage

    def morph(self, img, img2, baseImage, secondBaseImage, counter, displayImage):
        self.secondBaseImage = secondBaseImage
        self.baseImage = baseImage
        self.displayImage = displayImage

        if counter < 10:
            return self.scrambleMorph(img, img2, counter)
        elif counter < 30:
            return self.multiplyMorph(img, img2, counter)
        elif counter < 50:
            return self.tileMorph(img, img2, counter)
        elif counter < 100:
            return self.eriksMorph2(img, img2, counter)
        else:
            return self.eriksMorph(img, img2, counter)
# return self.multiplyMorph(img, img2, counter)
# return self.eriksMorph(img, img2,counter)
