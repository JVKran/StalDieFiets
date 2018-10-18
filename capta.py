from tkinter import *
import time
import cca
waar=False

def capt():
    def click(event=None):
        global waar
        antwoord = ant.get()
        if antwoord==cca.cap:
            waar=True
            root.destroy()
        else:
            waar=False
            root.destroy()
    root = Tk()

    antframe = Frame(master=root)
    antframe.pack(side=BOTTOM)

    photo = PhotoImage(file="out.png")
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
        cca.gen()
        print(capt())
    else:
        break