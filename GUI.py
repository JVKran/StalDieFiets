from tkinter import *
root = Tk()
root.configure(background='#ffff00')

label = Label(master=root,
              text='Are you a new user or an existing user?',
              background='#ffff00',
              foreground='white',
              font=('Arial', 27, 'bold'),
              width=26,
              height=8,
              wraplength=500,
              justify='left')
label.pack()

button = Button(master=root,
                background='white',
                font=('Arial', 12, 'bold'),
                width=20,
                height=3,
                text='New')
button.pack(pady=15, side=LEFT, padx=35)

button = Button(master=root,
                background='white',
                font=('Arial', 12, 'bold'),
                width=20,
                height=3,
                text='Existing',)
button.pack(pady=15, anchor='e', padx=35)

root.mainloop()