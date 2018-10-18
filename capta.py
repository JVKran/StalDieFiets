from tkinter import *


def makencap():     #zorgen dan bij importeren de code niet gelijk runt
    global waar
    waar = False
    import random
    from captcha.image import ImageCaptcha
    cap =""
    def gen():                  #captcha genereren
        global cap
        image = ImageCaptcha()
        def inhoud():
            letters =""
            for i in range(4):
                wa=random.randrange(65,90)
                letters+=chr(wa)
            return letters
        cap=inhoud()

        data = image.generate('cap')
        image.write(cap, 'captchaim.png')








    def capt():
        def click(event=None):
            global cap
            global waar
            antwoord = ant.get()
            if antwoord==cap:
                waar=True
                root.destroy()
            else:
                waar=False
                root.destroy()
        root = Tk()

        antframe = Frame(master=root)
        antframe.pack(side=BOTTOM)

        photo = PhotoImage(file="captchaim.png")
        label= Label(master=root, image=photo)
        ant = Entry(master=antframe)
        but = Button(master=antframe, text="g", command=click)
        root.bind('<Return>', click)
        but.pack(side=RIGHT,pady=10)
        label.pack()
        ant.pack(side=LEFT)
        mainloop()
        return waar
    while True:
        if waar ==False:
            gen()
            capt()
        else:
            break
