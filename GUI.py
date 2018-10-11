from tkinter import *
root = Tk()
root.configure(background='white')
root.resizable(False, False)


label = Label(master=root,
              text='Are you a new user or an existing user?',
              background='#fff517',
              foreground='black',
              font=('Arial', 39, 'bold',),
              width=20,
              height=5,
              wraplength=500,
              justify='left')
label.pack()

button = Button(master=root,
                background='#c4c4c4',
                font=('Arial', 30, 'bold'),
                width=10,
                height=1,
                text='New')
button.pack(pady=15, side=LEFT, padx=35)

button = Button(master=root,
                background='#c4c4c4',
                font=('Arial', 30, 'bold'),
                width=10,
                height=1,
                text='Existing',)
button.pack(pady=15, anchor='e', padx=35)

root.mainloop()