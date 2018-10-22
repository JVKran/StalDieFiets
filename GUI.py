from tkinter import Tk, Label, PhotoImage
root = Tk()
root.resizable(False, False)
root.configure(background='white')

photo = PhotoImage(file='grad.gif')

grad = Label(master=root,
             image=photo,
             width=600,
             height=300)

text = Label(master=root,
             font=('Helvetica', 16, 'bold'),
             foreground='black',
             background='white',
             text='lmao')


text.pack(side='top')
grad.pack(side='bottom')
root.mainloop()
