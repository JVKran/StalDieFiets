import sqlite3
import cv2
import random
import captcha
from captcha.image import ImageCaptcha
import csv
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import webbrowser
import barcode
from barcode.writer import ImageWriter
from tkinter import *
import tkinter as tk
from tkinter import font as tkfont


class klant:

    def __init__(self, vn, an, strt, hn, pstcd, std, prvnc, ml, tn, ww, po, ean):
        self.voornaam = vn
        self.achternaam = an
        self.straat = strt
        self.huisnummer = hn
        self.postcode = pstcd
        self.stad = std
        self.provincie = prvnc
        self.email = ml
        self.telefoonnummer = tn
        self.wachtwoord = ww
        self.pusho = po
        self.ean = ean
        self.hash = hash(vn+an+ml+tn)

    def get_voornaam(self):
        return self.voornaam

    def get_achternaam(self):
        return self.achternaam

    def get_adres(self):
        return self.straat+':'+self.huisnummer+':'+self.postcode+':'+self.stad

    def get_provincie(self):
        return self.provincie

    def get_telefoonnummer(self):
        return self.telefoonnummer

    def get_email(self):
        return self.email

    def get_hash(self):
        return self.hash

    def get_pushover(self):
        return self.pusho

    def get_ean(self):
        return self.ean

    def set_voornaam(self, new_vn):
        self.voornaam = new_vn

    def set_achternaam(self, new_an):
        self.achternaam = new_an

    def set_Adres(self,  new_strt, new_hn, new_pstcd, new_std, new_prvnc):
        self.straat = new_strt
        self.huisnummer = new_hn
        self.postcode = new_pstcd
        self.stad = new_std
        self.provincie = new_prvnc

    def set_email(self, new_ml):
        self.email = new_ml

    def set_telefoonnummer(self, new_tn):
        self.telefoonnummer = new_tn

    def set_hash(self, hash1):
        self.hash = hash1

    def get_wachtwoord(self):
        return self.wachtwoord

    def wijzig_wachtwoord(self):
        while True:
            old_ww = input('Geef oud wachtwoord:')
            if old_ww == self.wachtwoord:
                break
            else:
                print('wachtwoorden komen niet overheen')
        while True:
            new_ww = input("Wachtwoord:")
            hhww = input("Herhaal wachtwoord:")
            if new_ww == hhww:
                break
            else:
                print('Wachtwoorden komen niet overheen')
        self.wachtwoord = new_ww


class stalling:

    def __init__(self, stnm):
        self.stalingnnumer = stnm
        self.vrij = True
        self.klant = None

    def get_klant(self):
        return self.klant

    def get_stallingnummer(self):
        return self.stalingnnumer

    def get_vrij(self):
        return self.vrij

    def set_klant(self, klant):
        self.klant = klant
        self.vrij = False

    def vrij_stalling(self):
        self.klant = None
        self.vrij = True


def registreren(nieuwe_klant):
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("INSERT INTO klanten VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (nieuwe_klant.get_voornaam().capitalize(),
                                        nieuwe_klant.get_achternaam().capitalize(),
                                        nieuwe_klant.get_adres().split(":")[0].capitalize(),
              nieuwe_klant.get_adres().split(":")[1], nieuwe_klant.get_adres().split(":")[2].upper(),
              nieuwe_klant.get_adres().split(":")[3].capitalize(), nieuwe_klant.get_provincie().capitalize(),
              nieuwe_klant.get_email(), nieuwe_klant.get_telefoonnummer(), nieuwe_klant.get_wachtwoord(),
              nieuwe_klant.get_pushover(), nieuwe_klant.get_ean(), nieuwe_klant.get_hash()))
    conn.commit()
    conn.close()
    return nieuwe_klant


def stalling_verkrijgen(klant1, stallingen, plaats):
    for stl in stallingen:
        print(stl.get_klant())
        if stl.vrij:
            stalling1 = stl
            break
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    stalling1.set_klant(klant1)
    c.execute("UPDATE stallingen SET klant_hash = ? WHERE stallingnummer = ?", (klant1.get_hash()
                                                                                , stalling1.get_stallingnummer()))
    c.execute("UPDATE stallingen SET vrij = ? WHERE stallingnummer = ?", (0
                                                                          , stalling1.get_stallingnummer()))
    conn.commit()
    conn.close()
    return 'Stalling '+str(stalling1.get_stallingnummer())+' verkregen voor '+klant1.get_voornaam()


def stalling_vrijgeven(klant1, stallingen, plaats):
    print(klant1.get_hash())
    try:
        stalling1 = stallingen[klant1.get_hash()]
    except:
        return "Geen stallingen bezet"
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("UPDATE stallingen SET klant_hash = ? WHERE stallingnummer = ?", (0,
                                                                                 stalling1.get_stallingnummer()))
    c.execute("UPDATE stallingen SET vrij = ? WHERE stallingnummer = ?", (1,
                                                                                 stalling1.get_stallingnummer()))
    conn.commit()
    conn.close()
    return'Stalling '+str(stalling1.get_stallingnummer())+' vrijgegeven voor '+stalling1.get_klant().get_voornaam()


def get_klanten(plaats,  sortby):
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    klanten1 = {}
    klanten2 = {}
    for row in c.execute('SELECT * FROM klanten ORDER BY voornaam'):
        klanten1[row[12]] = klant(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
        klanten2[row[7]] = klant(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
        klanten1[row[12]].set_hash(row[12])
        klanten2[row[7]].set_hash(row[12])

    conn.close()
    if sortby is "hash":
        return klanten1
    if sortby is "email":
        return klanten2


def get_stallingen(plaats, klanten):
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    stallingen = []
    for row in c.execute('SELECT * FROM stallingen ORDER BY vrij'):
        if row[1] == 1:
            stallingen.append(stalling(row[0]))
        else:
            stalling1 = stalling(row[0])
            stalling1.set_klant(klanten[row[2]])
            stallingen.append(stalling1)
    conn.close()
    return stallingen

def get_hash_stallingen(plaats, klanten):
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    stallingen = {}
    for row in c.execute('SELECT * FROM stallingen ORDER BY vrij'):
        if row[1] == 1:
            stallingen[row[2]] = stalling(row[0])
        else:
            stalling1 = stalling(row[0])
            stalling1.set_klant(klanten[row[2]])
            stallingen[row[2]] = stalling1
    conn.close()
    return stallingen


def create_table(plaats):
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute('''CREATE TABLE klanten
                 (voornaam text, achternaam text, straat text, huisnummer text, postcode text, stad text, provincie text
                 , email text, telefoonnummer text, wachtwoord text,pushover text, ean INTEGER, hash INTEGER)''')
    c.execute('''CREATE TABLE stallingen
                     (stallingnummer INTEGER, vrij INTEGER, klant_hash INTEGER)''')
    for i in range(1, 101):
        c.execute("INSERT INTO stallingen VALUES(?,?,?)", (i, 1, 0))
    conn.commit()
    conn.close()
    conn = sqlite3.connect("Steden.db")
    c = conn.cursor()
    c.execute("INSERT INTO Steden VALUES(?)", [plaats])
    conn.commit()
    conn.close()


def geo():
    location = 'http://ip-api.com/csv'
    with requests.Session() as lijst:
        download = lijst.get(location)
        decoded_content = download.content.decode('utf-8    ')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            return ('{},{}').format(row[7], row[8])


def makencap():     #zorgen dan bij importeren de code niet gelijk runt
    global waar
    waar = False
    cap =""

    def gen():                  #captcha genereren
        global cap
        image = ImageCaptcha()

        def inhoud():
            letters =""
            for i in range(4):
                wa = random.randrange(65, 90)
                letters += chr(wa)
            return letters
        cap = inhoud()

        data = image.generate('cap')
        image.write(cap, 'captchaim.png')

    def capt():
        def click(event=None):
            global cap
            global waar
            antwoord = ant.get()
            if antwoord == cap:
                waar = True
                root.destroy()
            else:
                waar = False
                root.destroy()

        root = Tk()

        antframe = Frame(master=root)
        antframe.pack(side=BOTTOM)

        photo = PhotoImage(file="captchaim.png")
        label = Label(master=root, image=photo)
        ant = Entry(master=antframe)
        but = Button(master=antframe, text="g", command=click)
        root.bind('<Return>', click)
        but.pack(side=RIGHT, pady=10)
        label.pack()
        ant.pack(side=LEFT)
        mainloop()
        return waar

    while True:
        if not waar:
            gen()
            capt()
        else:
            break

    return waar


def get_information(plaats):


    klanten = get_klanten(plaats, "email")
    while True:
        try:
            email = input("Uw email-adres: ")
            password = input("Uw wachtwoord: ")
            klant = klanten[email]
            break

        except KeyError:
            print("email is niet bekend bij ons")

    if klant.get_wachtwoord() == password:
        print("Uw naam is {}\nUw emailadres is {}\nUw pushover token is {}\nUw barcode is {}".format(
            klant.get_voornaam(), klant.get_email(), klant.get_pushover(), klant.get_ean()))


def log_in_out(plaats, email, password):
    # Maakt een foto via de webcam en slaat deze op als barcode.png. minimaal 8 MP dus nep barcode_scan.jpg gebruikt. Levert de barcode in nummers terug #
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('barcode.png', image)
    camera.release()
    del camera
    cv2.destroyAllWindows()
    multipart_data = MultipartEncoder(
        fields={
            'file': ('ean13_barcode.png', open('ean13_barcode.png', 'rb'), 'image/png'),
            'apikey': '7b1e1c27-3115-46a3-8720-730497e2f85f'
        }
    )
    response = requests.post('https://api.havenondemand.com/1/api/sync/recognizebarcodes/v1', data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type})
    data = str(response.text).split(',')
    ean = data[0][20:]

    klanten = get_klanten(plaats, "email")
    klant = klanten[email]
    #if int(klant.get_ean()) == int(ean.strip('"')[:12]) and klant.get_wachtwoord() == password:
    return klant
    #else:
    #   return None

def alert(user_token):
    priority = '1'
    app_token = 'a2b11c66wgm777aavcokfh1dhu9q4o'
    title = 'Fietsenstalling'
    message = 'Uw fiets is opgehaald bij de stalling'
    multipart_data = MultipartEncoder(
        fields={
            'attachment': ('ean13_barcode.png', open('ean13_barcode.png', 'rb'), 'image/png'),
            'token': app_token,
            'user': user_token,
            'title': title,
            'message': message,
            'priority': priority
        }
    )
    r = requests.post('https://api.pushover.net/1/messages.json', data=multipart_data, headers={'User-Agent': 'Python', 'Content-Type': multipart_data.content_type})
    return str(r.text)


def start():
    while True:
        plaats = input("geef uw plaatsnaam op:")
        import os
        if os.path.isfile(plaats+".db"):
            break
        else:
            print("no such place exists in our database")

    while True:
        try:
            choice = int(input("Wat wilt u doen?\n1:registreren\n2:informatie opvragen\n3:in/uitloggen\n4: Fiets teruggeven\n6: fiets afgeven\nInput: "))
        except:
            print('not a numerical input')
        if choice == 1:
            registreren(plaats)
        elif choice == 2:
            get_information(plaats)
        elif choice == 3:
            log_in_out(plaats)
        elif choice == 4:
            klant_1 = log_in_out(plaats)
            if klant is not None:
                stallingen = get_hash_stallingen(plaats, get_klanten(plaats, "hash"))
                stalling_vrijgeven(klant_1, stallingen, plaats)
                #print(alert(klant_1.get_pushover()))

        elif choice == 5:
            if makencap():
                print('werkt')  # returnt True als goed en False als fout
        elif choice == 6:
            klant1 = log_in_out(plaats)
            if klant is not None:
                stallingen = get_stallingen(plaats, get_klanten(plaats, "hash"))
                stalling_verkrijgen(klant1, stallingen, plaats)
        else:
            exit(0)


def get_steden():

    conn = sqlite3.connect("Steden.db")
    c = conn.cursor()
    steden = []
    for row in c.execute('SELECT * FROM Steden ORDER BY plaats'):
        steden.append(row[0])
        print(row[0])
    conn.commit()
    conn.close()
    return steden


def update_steden():
    global steden
    steden = get_steden()


def update():
    global klanten_hash
    global klanten_email
    global stallingen
    global stallingen_hash
    klanten_hash = get_klanten(plaats, "hash")
    klanten_email = get_klanten(plaats, "email")
    stallingen_hash = get_hash_stallingen(plaats, klanten_hash)
    stallingen = get_stallingen(plaats, klanten_hash)


class NsStalling(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=titlesize)
        cont = tk.Frame(self)
        cont.grid(row=0, column=2)

        self.frames = {}
        for F in (StartPage, Continue, LogIn, Register, Klant_Page, Choice_City, Create_City, Captcha):
            page_name = F.__name__
            print(page_name)
            frame = F(parent=cont, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=2, sticky="nsew")

        self.show_frame("Choice_City")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_info(self):
        self.frames[Klant_Page.__name__].set_info()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='grey')
        label = tk.Label(self, text=""
                                    "Start pagina", font=controller.title_font)
        label.grid(row=2, column=2)

        button1 = tk.Button(self, text="Log in", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("LogIn"))
        button2 = tk.Button(self, text="Register", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("Register"))
        button1.grid(row=5, column=1)
        button2.grid(row=5, column=3)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)
        print(row_count)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=20)


class Choice_City(tk.Frame):

    def __init__(self, parent, controller):
        global steden
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Kies locatie van fietsenstalling", font=controller.title_font)
        label.grid(row=0, column=2)
        self.configure(background='grey')
        self.controller = controller
        row, colomn = 1, 1
        div = int(len(steden) / 4)

        def choice(stad):
            global plaats
            plaats = stad
            update()
            controller.show_frame("StartPage")

        for stad in steden:
            button = tk.Button(self, text=stad, font=('Helvetica', buttonsize))
            button.configure(command=lambda: choice(stad))
            button.grid(row=row, column=colomn)
            row += 1
            if row > div:
                row = 1
                colomn += 1

        col_count, row_count = self.grid_size()

        button = tk.Button(self, text="Nieuwe stad", font=('Helvetica', buttonsize))
        button.configure(command=lambda: controller.show_frame("Create_City"))
        button.grid(row=row_count, column=col_count)

        col_count, row_count = self.grid_size()

        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=100)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)

    def update(self):
        tk.Frame.update()


class Create_City(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='grey')
        self.controller = controller
        label = tk.Label(self, text="Stad toevoegen", font=controller.title_font)
        label.grid(row=0, column=2)

        def creeer():
            global steden
            if e1.get() not in steden:
                create_table(e1.get())
                update_steden()
                global plaats
                plaats = e1.get()
                controller.show_frame("LogIn")

        label = Label(self, text="Geef naam van stad:", font=('Helvetica', textsize))
        e1 = Entry(self)
        button = tk.Button(self, text="Maak aan", font=('Helvetica', buttonsize), command=creeer)
        e1.grid(row=1, column=2, padx=5, pady=5, sticky=W+E+N+S)
        label.grid(row=1, column=1)
        button.grid(row=1, column=3)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)

    def update(self):
        tk.Frame.update()


class Continue(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='grey')
        self.controller = controller
        label = tk.Label(self, text=""
                                    "Gelukt!", font=controller.title_font)
        label.grid(row=0, column=0)

        label = Label(self, text="Registreren is gelukt druk continue om naar start pagina te gaan om in te loggen", font=('Helvetica', textsize))
        button = tk.Button(self, text="Continue", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)
        label.grid(row=2, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)


class Captcha(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='grey')
        self.controller = controller
        plaatje = ImageCaptcha()
        cap = ""
        for i in range(4):
            cap += chr(random.randrange(65, 90))
        plaatje.write(cap, 'captchaim.png')
        photo = PhotoImage(file="captchaim.png")
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=1, column=2)

        def click(captcha):
            if ant.get() == captcha:
                print("captcha succes")
                plaatje = ImageCaptcha()
                cap = ""
                for x in range(4):
                    cap += chr(random.randrange(65, 90))
                plaatje.write(cap, 'captchaim.png')
                photo = PhotoImage(file="captchaim.png")
                label.configure(image=photo)
                label.image = photo
                ant.delete(0, 'end')
                global klant_globaal
                webbrowser.open("ean13_barcode.png")
                registreren(klant_globaal)
                controller.show_frame("Continue")
                klant_globaal = None
            else:
                plaatje = ImageCaptcha()
                cap = ""
                for x in range(4):
                    cap += chr(random.randrange(65, 91))
                plaatje.write(cap, 'captchaim.png')
                photo = PhotoImage(file="captchaim.png")
                label.configure(image=photo)
                label.image = photo
                ant.delete(0, 'end')

        ant = Entry(self)
        but = Button(self, text="Verzend", command=lambda: click(cap))
        #self.bind('<Return>', click)
        but.grid(row=3, column=2)
        ant.grid(row=2, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)


class Klant_Page(tk.Frame):
    label_stalling = None
    label1 = None
    label2 = None
    label3 = None
    def __init__(self, parent, controller):
        global label_stalling
        global label1
        global label2
        global label3
        tk.Frame.__init__(self, parent)
        label_stalling = tk.Label(self)
        label1 = tk.Label(self)
        label2 = tk.Label(self)
        label3 = tk.Label(self)
        self.configure(background='grey')
        self.controller = controller
        label = tk.Label(self, text="Klanten Page", font=controller.title_font)
        label.grid(row=0, column=0)
        label_fiets = tk.Label(self, text="", font=('Helvetica', textsize))
        global klant_globaal
        global stallingen_hash

        def vrijgeven():
            label_fiets.configure(text=stalling_vrijgeven(klant_globaal, stallingen_hash, plaats))
            label_fiets.grid(row=5, column=2)
            update()
            controller.set_info()

        def verkrijgen():
            global klant_globaal
            global stallingen
            global stallingen_hash
            label.grid(row=0, column=0)
            try:
                stallingen_hash[klant_globaal.get_hash()]
                label_fiets.configure(text="Max 1 stalling per gebruiker")
                label_fiets.grid(row=5, column=2)
            except KeyError:
                label_fiets.configure(text=stalling_verkrijgen(klant_globaal, stallingen, plaats))
            update()
            controller.set_info()

        def log_uit():
            global klant_globaal
            klant_globaal = None
            controller.show_frame("StartPage")

        button1 = tk.Button(self, text="Fiets Vrijgeven", font=('Helvetica', buttonsize),
                            command=vrijgeven)
        button2 = tk.Button(self, text="stalling Verkrijgen", font=('Helvetica', buttonsize),
                            command=verkrijgen)
        button3 = tk.Button(self, text="Log uit", font=('Helvetica', buttonsize),
                            command=log_uit)

        button1.grid(row=8, column=1)
        button2.grid(row=8, column=2)
        button3.grid(row=10, column=4)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)

    def set_info(self):
        global label_stalling
        global label1
        global label2
        global label3
        label_stalling.configure(text="Fietsen stalling : geen", font=('Helvetica', textsize))
        label1.configure(text="Naam: " + klant_globaal.get_voornaam(), font=('Helvetica', textsize))
        label2.configure(text="Adress: " + klant_globaal.get_adres().split(':')[0] + " " +
                                    klant_globaal.get_adres().split(':')[1] + ", " +
                                    klant_globaal.get_adres().split(':')[3], font=('Helvetica', textsize))
        try:
            label_stalling.configure(
                text="Fietsen stalling : " + str(stallingen_hash[klant_globaal.get_hash()].get_stallingnummer()))
        except KeyError:
            label_stalling.configure(text="Fietsen stalling : geen")

        label3 = Label(self,
                       text="Plaats stalling: " + plaats,
                       font=('Helvetica', textsize))
        label1.forget()
        label2.forget()
        label3.forget()
        label_stalling.forget()
        label1.grid(row=1, column=2)
        label2.grid(row=2, column=2)
        label_stalling.grid(row=3, column=2)
        label3.grid(row=4, column=2)


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='grey')
        label = tk.Label(self, text="Log in page", font=controller.title_font)
        label.grid(row=0, column=2)

        Label(self, text="E-mail:", font=('Helvetica', textsize)).grid(row=1, column=1)
        e1 = Entry(self)
        e1.grid(row=1, column=2)
        Label(self, text="Password", font=('Helvetica', textsize)).grid(row=2, column=1)
        e2 = Entry(self, show="*")
        e2.grid(row=2, column=2)

        def log_in():
            global klant_globaal
            klant_globaal = log_in_out(plaats, e1.get(), e2.get())
            if klant_globaal is None:
                return
            print(klant_globaal.get_voornaam())
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            controller.set_info()
            controller.show_frame("Klant_Page")

        def back():
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            controller.show_frame("StartPage")

        button1 = tk.Button(self, text="Back", font=('Helvetica', buttonsize),
                            command=back)
        button2 = tk.Button(self, text="Log in", font=('Helvetica', buttonsize), command=log_in)

        button1.grid(row=3, column=3)
        button2.grid(row=3, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='grey')
        label = tk.Label(self, text="Register", font=controller.title_font)
        label.grid(row=0, column=2)

        label_vn = Label(self, text="Voornaam is ongeldig", font=('Helvetica', textsize))
        label_ong = Label(self, text="alle velden moeten ingevuld worden", font=('Helvetica', textsize))
        label_an = Label(self, text="achternaam is ongeldig", font=('Helvetica', textsize))
        label_strt = Label(self, text="Straat is ongeldig", font=('Helvetica', textsize))
        label_std = Label(self, text="Stad is ongeldig", font=('Helvetica', textsize))
        label_prvnc = Label(self, text="Provincie is ongeldig", font=('Helvetica', textsize))
        label_ww = Label(self, text="Wachtwoorden komen niet overeen", font=('Helvetica', textsize))
        label_ww_tk = Label(self, text="Wachtwoord is tekort", font=('Helvetica', textsize))
        label_tn = Label(self, text="Telefoonnummer ongeldig", font=('Helvetica', textsize))
        label_tn_len = Label(self, text="Telefoonnummer ongeldig", font=('Helvetica', textsize))
        label_pstcd_1 = Label(self, text="postcode is ongeldig", font=('Helvetica', textsize))
        label_pstcd_2 = Label(self, text="postcode is ongeldig", font=('Helvetica', textsize))
        label_pstcd_len = Label(self, text="postcode is ongeldige lengte", font=('Helvetica', textsize))

        Label(self, text="Voornaam:", font=('Helvetica', textsize), anchor='e').grid(row=1, column=1, sticky=E, padx="5")
        e1 = Entry(self)
        e1.config(font=inputsize)
        e1.grid(row=1, column=2)
        Label(self, text="Achternaam:", font=('Helvetica', textsize), anchor='e').grid(row=2, column=1,
         sticky = E, padx = "5")
        e2 = Entry(self)
        e2.config(font=inputsize)
        e2.grid(row=2, column=2)
        Label(self, text="Straat:", font=('Helvetica', textsize), anchor='e').grid(row=3, column=1,
         sticky = E, padx = "5")
        e3 = Entry(self)
        e3.config(font=inputsize)
        e3.grid(row=3, column=2)
        Label(self, text="Huisnummer:", font=('Helvetica', textsize), anchor='e').grid(row=4, column=1, sticky=E, padx="5")
        e4 = Entry(self)
        e4.config(font=inputsize)
        e4.grid(row=4, column=2)
        Label(self, text="Postcode:", font=('Helvetica', textsize), anchor='e').grid(row=5, column=1, sticky=E, padx="5")
        e5 = Entry(self)
        e5.config(font=inputsize)
        e5.grid(row=5, column=2)
        Label(self, text="Stad:", font=('Helvetica', textsize), anchor='e').grid(row=6, column=1, sticky=E, padx="5")
        e6 = Entry(self)
        e6.config(font=inputsize)
        e6.grid(row=6, column=2)
        Label(self, text="Provincie:", font=('Helvetica', textsize), anchor='e').grid(row=7, column=1, sticky=E, padx="5")
        e7 = Entry(self)
        e7.config(font=inputsize)
        e7.grid(row=7, column=2)
        Label(self, text="E-mail:", font=('Helvetica', textsize), anchor='e').grid(row=8, column=1, sticky=E, padx="5")
        e8 = Entry(self)
        e8.config(font=inputsize)
        e8.grid(row=8, column=2)
        Label(self, text="Telefoonnummer:", font=('Helvetica', textsize), anchor='e').grid(row=9, column=1, sticky=E, padx="5")
        e9 = Entry(self)
        e9.config(font=inputsize)
        e9.grid(row=9, column=2)
        Label(self, text="Wachtwoord", font=('Helvetica', textsize), anchor='e').grid(row=10, column=1, sticky=E, padx="5")
        e10 = Entry(self, show="*")
        e10.config(font=inputsize)
        e10.grid(row=10, column=2)
        Label(self, text="Herhaal Wachtwoord:", font=('Helvetica', textsize), anchor='e').grid(row=11, column=1, sticky=E, padx="5")
        e11 = Entry(self, show="*")
        e11.config(font=inputsize)
        e11.grid(row=11, column=2)
        Label(self, text="Push over token:", font=('Helvetica', textsize), anchor='e').grid(row=12, column=1, sticky=E, padx="5")
        e12 = Entry(self)
        e12.config(font=inputsize)
        e12.grid(row=12, column=2)

        def getInfo():
            mistakes = 0

            if len(e1.get()) < 1 or len(e2.get()) < 1 or len(e3.get()) < 1 or len(e4.get()) < 1 or len(e5.get()) < 1 or\
                    len(e6.get()) < 1 or len(e7.get()) < 1 or len(e8.get()) < 1 or len(e9.get()) < 1 or\
                    len(e10.get()) < 1 or len(e11.get()) < 1 or len(e12.get()) < 1:
                label_ong.grid(row=22, column=2)
                return
            else:
                label_ong.grid_forget()

            for char in e1.get():
                if not char.isalpha():
                    label_vn.grid(row=16, column=2)
                    mistakes += 1
                    break
                else:
                    label_vn.grid_forget()
            for word in e2.get().split():
                for char in word:
                    if not char.isalpha():
                        label_an.grid(row=17, column=2)
                        mistakes += 1
                        break
                    else:
                        label_an.grid_forget()
            for char in e3.get():
                if not char.isalpha():
                    label_strt.grid(row=18, column=2)
                    mistakes += 1
                    break
                else:
                    label_strt.grid_forget()
            for char in e6.get():
                if not char.isalpha():
                    label_std.grid(row=19, column=2)
                    mistakes += 1
                    break
                else:
                    label_std.grid_forget()
            for char in e7.get():
                if not char.isalpha():
                    label_prvnc.grid(row=20, column=2)
                    mistakes += 1
                    break
                else:
                    label_prvnc.grid_forget()
            if e10.get() != e11.get():
                label_ww.grid(row=14, column=2)
                mistakes += 1
            else:
                label_ww.grid_forget()
                if len(e10.get()) < 8:
                    label_ww_tk.grid(row=14, column=2)
                    mistakes += 1
                else:
                    label_ww_tk.grid_forget()

            if not e9.get().isnumeric():
                label_tn.grid(row=15, column=2)
                mistakes += 1
            else:
                label_tn.grid_forget()
            if len(e9.get()) < 10 or len(e9.get()) > 11:
                label_tn.grid(row=15, column=2)
                mistakes += 1
            else:
                label_tn_len.grid_forget()
            if len(e5.get()) == 6:
                label_pstcd_len.grid_forget()
                for char in e5.get()[:4]:
                    if not char.isnumeric():
                        label_pstcd_1.grid(row=21, column=2)
                        mistakes += 1
                        break
                    else:
                        label_pstcd_1.grid_forget()
                for char in e5.get()[4:6]:
                    if not char.isalpha():
                        label_pstcd_2.grid(row=21, column=2)
                        mistakes += 1
                        break
                    else:
                        label_pstcd_2.grid_forget()
            else:
                label_pstcd_len.grid(row=21, column=2)
                mistakes += 1
            if mistakes == 0:
                global klant_globaal
                ean_number = str(random.randint(100000000000, 999999999999))
                EAN = barcode.get_barcode_class('ean13')
                ean = EAN(ean_number, writer=ImageWriter())
                ean.save('ean13_barcode')
                klant_globaal = klant(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(),
                                      e9.get(), e10.get(), e12.get(), ean_number)
                e1.delete(0, 'end')
                e2.delete(0, 'end')
                e3.delete(0, 'end')
                e4.delete(0, 'end')
                e5.delete(0, 'end')
                e6.delete(0, 'end')
                e7.delete(0, 'end')
                e8.delete(0, 'end')
                e9.delete(0, 'end')
                e10.delete(0, 'end')
                e11.delete(0, 'end')
                e12.delete(0, 'end')
                controller.show_frame("Captcha")

        def back():
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')
            e5.delete(0, 'end')
            e6.delete(0, 'end')
            e7.delete(0, 'end')
            e8.delete(0, 'end')
            e9.delete(0, 'end')
            e10.delete(0, 'end')
            e11.delete(0, 'end')
            e12.delete(0, 'end')
            controller.show_frame("StartPage")

        button = tk.Button(self, text="Back", font=('Helvetica', buttonsize),
                           command=back)
        button.grid(row=13, column=1)
        button = tk.Button(self, text="Register", font=('Helvetica', buttonsize),
                           command=getInfo)
        button.grid(row=13, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=170)

        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=30)

import unittest


class testKlantClass(unittest.TestCase):

    def setUp(self):
        self.klant = klant('Joey', 'Balk', 'Marckstraat', '37', '4133HT', 'Vianen', 'Utrecht', 'joeybalk@hotmail.com', '0612345678', 'kaaskop','uv2a4p9zzk6bf4d579uxde8agk5zru','012345678912')
    def testGetVoornaam(self):
       self.assertEqual(self.klant.get_voornaam(), 'Joey', "Test of de getter van voornaam werkt")

    def testGetAchternaam(self):
        self.assertEqual(self.klant.get_achternaam(), 'Balk', "Test of de getter van achternaam werkt")

    def testGetAdres(self):
        self.assertEqual(self.klant.get_adres(), 'Marckstraat:37:4133HT:Vianen', "Test of de getter van adres werkt")

    def testGetNummer(self):
        self.assertEqual(self.klant.get_telefoonnummer(), '0612345678', "Test of de getter van nummer werkt")

    def testGetEmail(self):
        self.assertEqual(self.klant.get_email(), 'joeybalk@hotmail.com', "Test of de getter van email werkt")

    def testGetPO(self):
        self.assertEqual(self.klant.get_pushover(), 'uv2a4p9zzk6bf4d579uxde8agk5zru', "Test of de getter van pushover werkt")

    def testGetEAN(self):
        self.assertEqual(self.klant.get_ean(), '012345678912', "Test of de getter van EAN werkt")

    def testSetVoornaam(self):
        self.klant.set_voornaam('Sil')
        self.assertEqual(self.klant.get_voornaam(), 'Sil', "Test of de setter van voornaam werkt")

    def testSetAchternaam(self):
        self.klant.set_achternaam('Rijnberk')
        self.assertEqual(self.klant.get_achternaam(), 'Rijnberk', "Test of de setter van achternaam werkt")

    def testSetAdres(self):
        self.klant.set_Adres('kaasstraat','1' ,'1234AB', 'Geina', 'Utrecht')
        self.assertEqual(self.klant.get_adres(),'kaasstraat:1:1234AB:Geina', "Test of de setter van adres werkt")

    def testSetMail(self):
        self.klant.set_email('silvanrijnberk@stinkie.nl')
        self.assertEqual(self.klant.get_email(),'silvanrijnberk@stinkie.nl', "Test of de setter van mail werkt")

    def testSetNummer(self):
        self.klant.set_telefoonnummer('0687654321')
        self.assertEqual(self.klant.get_telefoonnummer(), '0687654321', "Test of de setter van telefoon werkt")

    def testGetWW(self):
        self.assertEqual(self.klant.get_wachtwoord(),'kaaskop', "Test of de getter van ww werkt")

    class testStallingClass(unittest.TestCase):
        def setUp(self):
            self.stalling = stalling('10')

            self.stalling.set_klant(klant('Joey', 'Balk', 'Marckstraat', '37', '4133HT', 'Vianen', 'Utrecht', 'joeybalk@hotmail.com', '0612345678', 'kaaskop','uv2a4p9zzk6bf4d579uxde8agk5zru','012345678912'))


        def testGetKlant(self):
            self.assertEqual(self.stalling.get_klant().get_voornaam(), 'Joey', "Test of de getter van klant werkt")

        def testGetstallingnummer(self):
            self.assertEqual(self.stalling.get_stallingnummer(), '10', "Test of de getter van stallingnummer werkt")

        def testGetVrij(self):
            self.assertEqual(self.stalling.get_vrij(), False, "Test of de getter van vrij werkt")

        def testSetKlant(self):
            self.stalling.set_klant(klant('Sil', 'Rijnberk', 'Marckstraat', '37', '4133HT', 'Vianen', 'Utrecht', 'joeybalk@hotmail.com', '0612345678', 'kaaskop','uv2a4p9zzk6bf4d579uxde8agk5zru','012345678912'))
            self.assertEqual(self.stalling.get_klant().get_voornaam(),'Sil', "Test of de setter van klant werkt")

        def testVrijStalling(self):
            self.stalling.vrij_stalling()
            self.assertEqual(self.stalling.get_vrij(), True, "Test of er een vrije stalling is")


if __name__ == "__main__":
    buttonsize = 10
    textsize = 10
    titlesize = 15
    inputsize = 5
    plaats = ''
    klant_globaal = None
    klanten_hash = {}
    klanten_email = {}
    stallingen = []
    stallingen_hash = {}
    steden = get_steden()
    #inp = input("test or app: ")
    #if inp == "app":
    app = NsStalling()
    app.mainloop()
    #elif inp == "test":
    #unittest.main()

