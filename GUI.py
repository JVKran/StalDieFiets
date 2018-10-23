from tkinter import *
import tkinter as tk
def create_window():
    login=tk.Toplevel(master=root,
                        width=500,
                        background='grey',
                        height=300)
root = Tk()
root.resizable(False, False)
root.configure(background='grey')

explanation = "Als je gebruik wilt maken van StalDieFiets heb je een account nodig:"

exp = Label(master=root,
            padx=9,
            pady=5,
            width=35,
            height=10,
            background='grey',
            foreground='black',
            text=explanation,
            wraplength=400,
            justify='left',
            font=('Helvetica', 16))

exp.pack()


new = Button(master=root,
             font=('Helvetica', 14),
             pady=10,
             padx=10,
             foreground='black',
             background='white',
             width=19,
             text='New User',
             command=create_window)

new.pack(side='left')

existing = Button(master=root,
                  font=('Helvetica', 14),
                  pady=10,
                  padx=10,
                  foreground='black',
                  background='white',
                  width=19,
                  text='Existing User',
                  command=create_window)

existing.pack(side='right')
root.mainloop()
