from tkinter import *
import tkinter as tk
def create_window():
    login=tk.Toplevel(master=root,
                      width=300,
                      background='#d8d6d2',
                      height=300)
root = Tk()
root.title("LIGMA")
root.resizable(False, False)
root.configure(background='#ededed')

exp = "Om verder te gaan bij StalDieFiets heb je een account nodig."
eu = "Log hier in als bestaande gebruiker:"
nu = "Maak hier een nieuw account aan:"

exp = Label(master=root,
            font=('Helvetica', 16, 'bold'),
            text=exp)

exp.grid(row=0, column=0, columnspan=2)

spacing = Label(master=root,
                background='#ededed')

spacing.grid(row=1, column=0, columnspan=2)

eu = Label(master=root,
            padx=0,
            pady=0,
            width=0,
            height=0,
            background='#ededed',
            foreground='black',
            text=eu,
            wraplength=250,
            justify='left',
            font=('Helvetica', 16),
            anchor=N)

eu.grid(row=2, column=0)

nu = Label(master=root,
            padx=0,
            pady=0,
            width=0,
            height=0,
            background='#ededed',
            foreground='black',
            text=nu,
            wraplength=250,
            justify='left',
            font=('Helvetica', 16),
            anchor=N)

nu.grid(row=2, column=1)

exiuser = Entry(master=root,
                width=35)

exiuser.grid(row=3, column=0, sticky='e')

exiusername = Label(master=root,
                    font=('Helvetica', 12),
                    text='Username:')

exiusername.grid(row=3, column=0, sticky='w')

new = Button(master=root,
             font=('Helvetica', 14),
             pady=10,
             padx=0,
             foreground='black',
             background='white',
             width=19,
             text='New User',
             command=create_window)

new.grid(row=4, column=1)

existing = Button(master=root,
                  font=('Helvetica', 14),
                  pady=10,
                  padx=0,
                  foreground='black',
                  background='white',
                  width=19,
                  text='Existing User',
                  command=create_window)

existing.grid(row=4, column=0)
root.mainloop()