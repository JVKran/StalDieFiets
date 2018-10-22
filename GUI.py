from tkinter import Tk, Label, PhotoImage, Button
root = Tk()
root.resizable(False, False)
root.configure(background='white')

photo = PhotoImage(file='grad.gif')

grad = Label(master=root,
             image=photo,
             width=600,
             height=300)

grad.pack()

new = Button(master=root,
             font=('Helvetica', 14),
             foreground='black',
             background='white',
             width=20,
             text='New User')

new.pack(side='left', expand=True)

existing = Button(master=root,
                  font=('Helvetica', 14),
                  foreground='black',
                  background='white',
                  width=20,
                  text='Existing User')

existing.pack(side='right', expand=True)
root.mainloop()
