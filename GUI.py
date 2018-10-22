from tkinter import *
root = Tk()
root.resizable(False, False)
root.configure(background='white')
root.wm_attributes('-transparentcolor', 'blue')

photo = PhotoImage(file='grad.gif', width=600, height=300)
explanation = "Als je gebruik wilt maken van StalDieFiets heb je een account nodig:"

grad = Label(master=root,
             image=photo)

grad.pack()

exp = Label(master=root,
             padx=10,
             text=explanation)

exp.pack()

new = Button(master=root,
             font=('Helvetica', 14),
             foreground='black',
             background='white',
             width=19,
             text='New User')

new.pack(side='left', expand=True)

existing = Button(master=root,
                  font=('Helvetica', 14),
                  foreground='black',
                  background='white',
                  width=19,
                  text='Existing User')

existing.pack(side='right', expand=True)
root.mainloop()
