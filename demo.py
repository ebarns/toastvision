from SimpleCV import *
from SimpleCV.ImageClass import Image, ImageSet
from SimpleCV.DrawingLayer import *
from SimpleCV.Features import FeatureExtractorBase
import time
classes = ['atDesk', 'AFK', ]


def main():
    trainPaths = ['./post/' + c + '/train/' for c in classes]
    testPaths = ['./post/' + c + '/test/' for c in classes]

    print (trainPaths, testPaths)
    trainer = Trainer(classes, trainPaths)
    trainer.train()

    imgs = ImageSet()
    for p in testPaths:
        imgs += ImageSet(p)
    random.shuffle(imgs)

    print "Result test"
    trainer.test(testPaths)

    # svm = trainer.classifiers[0]
    # trainer.visualizeResults(svm, imgs)


def securityChecker():
    trainPaths = ['./post/' + c + '/train/' for c in classes]
    testPaths = ['./post/' + c + '/test/' for c in classes]

    print (trainPaths, testPaths)
    trainer = Trainer(classes, trainPaths)
    trainer.train()
    svm = trainer.classifiers[0]

    imgs = ImageSet()
    for p in testPaths:
        imgs += ImageSet(p)
    random.shuffle(imgs)
    print(imgs)

    # print "Result test"
    # trainer.test(testPaths)

    display = Display()
    camera = Camera()

    while display.isNotDone():
        img = camera.getImage()
        # img.save("test.png")
        print(img)
        result = svm.classify(img)
        # if result == "AFK":
        #     img.drawText("COME BACK", 10, 10, fontsize=60, color=Color.BLUE)
        # else:
        #     img.drawText("HEY ERIK", 10, 10, fontsize=60, color=Color.RED)

        img.show()
        time.sleep(3)


class Trainer():

    def __init__(self, classes, trainPaths):
        self.classes = classes
        self.trainPaths = trainPaths

    def getExtractors(self):
        hhfe = HueHistogramFeatureExtractor(10)
        ehfe = EdgeHistogramFeatureExtractor(10)
        # haarfe = HaarLikeFeatureExtractor(fname='../SimpleCV/SimpleCV/Features/haar.txt')
        return [hhfe, ehfe]

    def getClassifiers(self, extractors):
        svm = SVMClassifier(extractors)
        tree = TreeClassifier(extractors)
        bayes = NaiveBayesClassifier(extractors)
        knn = KNNClassifier(extractors)
        return [svm, tree, bayes, knn]

    def train(self):
        self.classifiers = self.getClassifiers(self.getExtractors())
        for classifier in self.classifiers:
            classifier.train(self.trainPaths, self.classes, verbose=False)

    def test(self, testPaths):
        for classifier in self.classifiers:
            print classifier.test(testPaths, self.classes, verbose=False)

    def visualizeResults(self, classifier, imgs):
        for index, img in enumerate(imgs):
            className = classifier.classify(img)
            img.drawText(className, 10, 10, fontsize=60, color=Color.BLUE)
            img.save("./post/results/result" + str(index) + ".png")


main()
