import random
from captcha.image import ImageCaptcha
cap =""
def gen():
    global cap
    image = ImageCaptcha()
    def inhoud():
        letters =""
        for i in range(4):
            wa=random.randrange(65,90)
            letters+=chr(wa)
        return letters
    cap=inhoud()

    data = image.generate('test')
    image.write(cap, 'out.png')
