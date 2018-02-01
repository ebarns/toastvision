from SimpleCV import *

c = Camera()
img = c.getImage()

for i in range(10):
    img = c.getImage()
    img.save("./post/AFK/train/afk" + str(i) + ".png")

for i in range(10):
    img = c.getImage()
    img.save("./post/AFK/test/afk" + str(i) + ".png")
