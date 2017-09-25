from markovimg import MarkovImg
from PIL import Image

if __name__ == '__main__':
    fname = "./test_images/mandrill.png"
    results = "./test_results/"
    img = Image.open(fname)
    print(img.format, img.size, img.mode)
    order,salt = 3,0.4
    mc = MarkovImg(order)
    mc.learn(img,salt)
    mc.learn(img.rotate(90),salt)
    mc.learn(img.rotate(180),salt)
    mc.learn(img.rotate(270),salt)
    mc.learn(img.transpose(Image.FLIP_LEFT_RIGHT),salt)
    mc.learn(img.transpose(Image.FLIP_TOP_BOTTOM),salt)
    mc.learn(img.transpose(Image.ROTATE_90),salt)
    mc.learn(img.transpose(Image.ROTATE_180),salt)
    mc.learn(img.transpose(Image.ROTATE_270),salt)
    for t in range(3):
        im = mc.generate((img.size[0]*2,2*img.size[1]))
        im.save(results+"img"+str(t)+".png","PNG")
        im.show()
    img.show()


