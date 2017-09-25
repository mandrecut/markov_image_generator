from markovimg import MarkovImg
from PIL import Image

if __name__ == '__main__':
    img = Image.open("./test_images/lena.png")
    img.show()
    print(img.format, img.size, img.mode)
    order,salt = 4,0.1
    mc = MarkovImg(order)
    mc.learn(img,salt)
    im = mc.generate(img.size)
    im.show()


