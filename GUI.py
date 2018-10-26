import sqlite3
import cv2
import random
from captcha.image import ImageCaptcha
import csv
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import webbrowser
import barcode
from barcode.writer import ImageWriter
from tkinter import *

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
        self.voornaam = new_an

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


def registreren(plaats):
    vn = input("Voornaam:")
    an = input("Achternaam:")
    strt = input("Straat:")
    hn = input("Straatnummer:")
    pstcd = input("Postcode:")
    std = input("Stad:")
    prvncs = input("Provincie:")
    ml = input("Email:")
    while True:
        tn = input("Telefoonnummer:")
        if tn.isnumeric():
            break
    while True:
        ww = input("Geef een wachtwoord op: ")
        hhww = input("Herhaal het wachtwoord: ")
        if ww == hhww:
            break
        else:
            print('Wachtwoorden komen niet overheen')
    po = input("geef Pushover gebruikers Token:")
    ean_number = str(random.randint(100000000000, 999999999999))
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(ean_number, writer=ImageWriter())
    fullcode = ean.save('ean13_barcode')
    webbrowser.open("ean13_barcode.png")
    klant1 = klant(vn, an, strt, hn, pstcd, std, prvncs, ml, tn, ww, po, ean)
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("INSERT INTO klanten VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (vn.capitalize(), an.capitalize(), strt.capitalize(), hn, pstcd.upper(), std.capitalize(), prvncs.capitalize(), ml, tn, ww, po, ean_number, klant1.get_hash()))
    conn.commit()
    conn.close()
    print("Beste {}, bedankt voor uw registratie bij de fietsentallingen van de NS. We hopen u snel te zien.".format(vn + " " + an))
    return klant1


def stalling_verkrijgen(klant1, stallingen, plaats):
    for stl in stallingen:
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
    print('Stalling ', stalling1.get_stallingnummer(), ' verkregen voor ', klant1.get_voornaam())
    return stallingen


def stalling_vrijgeven(klant1, stallingen, plaats):
    try:
        stalling1 = stallingen[klant1.get_hash()]
    except:
        print("klant heeft geen stallingen bezet")
        return
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("UPDATE stallingen SET klant_hash = ? WHERE stallingnummer = ?", (0,
                                                                                 stalling1.get_stallingnummer()))
    c.execute("UPDATE stallingen SET vrij = ? WHERE stallingnummer = ?", (1,
                                                                                 stalling1.get_stallingnummer()))
    conn.commit()
    conn.close()
    print('Stalling ', stalling1.get_stallingnummer(), ' vrijgegeven voor ', stalling1.get_klant().get_voornaam())


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


#or klant in klanten.values():
#    print(klant.get_voornaam())
#for row in c.execute('SELECT * FROM klanten ORDER BY voornaam'):
#    print(row)
#for row in c.execute('SELECT * FROM stallingen'):
#    print(row)
#conn.close()





# Maakt, leest en schrijft naar een database. Daarnaast wordt er een random barcode met EAN gegenereerd
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


def log_in_out(plaats):
    # Maakt een foto via de webcam en slaat deze op als barcode.png. minimaal 8 MP dus nep barcode_scan.jpg gebruikt. Levert de barcode in nummers terug #
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('barcode.png', image)
    camera.release()
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
    email = input("Geef uw email: ")
    password = input("Uw wachtwoord: ")
    klant = klanten[email]
    if int(klant.get_ean()) == int(ean.strip('"')[:12]) and klant.get_wachtwoord() == password:
        print("log in geslaagd")
        return klant
    else:
        print("log in mislukt")
        return None

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



import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class NsStalling(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=40, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LogIn, Register, LoggedIn):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welkom bij StalDieFiets", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Log in", width=20, font=('Helvetica', 20),
                            command=lambda: controller.show_frame("LogIn"))
        button2 = tk.Button(self, text="Registreer", width=20, font=('Helvetica', 20),
                            command=lambda: controller.show_frame("Register"))
        button1.pack()
        button2.pack()

        label = tk.Label(self, bg="#ffffff", font=('Helvetica', 16), wraplength=550, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        label.pack(fill="both", expand="true", pady=10, side="top")



class LogIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Log in page", font=controller.title_font)
        label.pack(side="bottom", fill="x", pady=10)
        label.pack(side="top", fill="x", pady=10)

        Label(self, text="E-mail:", font=('Helvetica', 16, 'bold')).pack()
        e1 = Entry(self, width=40)
        e1.pack(pady=2)
        Label(self, text="Password", font=('Helvetica', 16, 'bold')).pack()
        e2 = Entry(self, show="*", width=40)
        e2.pack(pady=5)

        button1 = tk.Button(self, text="Log In", width=20, font=('Helvetica', 20),
                           command=lambda: controller.show_frame("LoggedIn"))
        button2 = tk.Button(self, text="Terug", width=20, font=('Helvetica', 20),
                           command=lambda: controller.show_frame("StartPage"))
        button1.pack()
        button2.pack()

class LoggedIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=200, height=200)
        self.controller = controller
        label = tk.Label(self, wraplength=600, text="Ingelogd als 'gebruiker'", font=('Helvetica', 16))
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Log out", width=20, font=('Helvetica', 20),
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack()

class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Registreer", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        Label(self, text="Voornaam:", font=('Helvetica', 16, 'bold')).pack()
        e1 = Entry(self)
        e1.pack()
        Label(self, text="Achternaam", font=('Helvetica', 16, 'bold')).pack()
        e2 = Entry(self)
        e2.pack()
        Label(self, text="Straat:", font=('Helvetica', 16, 'bold')).pack()
        e3 = Entry(self)
        e3.pack()
        Label(self, text="Huisnummer:", font=('Helvetica', 16, 'bold')).pack()
        e4 = Entry(self)
        e4.pack()
        Label(self, text="Postcode:", font=('Helvetica', 16, 'bold')).pack()
        e5 = Entry(self)
        e5.pack()
        Label(self, text="Stad:", font=('Helvetica', 16, 'bold')).pack()
        e6 = Entry(self)
        e6.pack()
        Label(self, text="Provincie:", font=('Helvetica', 16, 'bold')).pack()
        e7 = Entry(self)
        e7.pack()
        Label(self, text="E-mail:", font=('Helvetica', 16, 'bold')).pack()
        e8 = Entry(self)
        e8.pack()
        Label(self, text="Telefoonnummer:", font=('Helvetica', 16, 'bold')).pack()
        e9 = Entry(self)
        e9.pack()
        Label(self, text="Wachtwoord", font=('Helvetica', 16, 'bold')).pack()
        e10 = Entry(self)
        e10.pack()
        Label(self, text="Herhaal Wachtwoord:", font=('Helvetica', 16, 'bold')).pack()
        e11 = Entry(self)
        e11.pack()
        Label(self, text="Push over token:", font=('Helvetica', 16, 'bold')).pack()
        e12 = Entry(self)
        e12.pack()

        button1 = tk.Button(self, text="Terug", width=20, font=('Helvetica', 20), pady=5,
                           command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Registreer", width=20, font=('Helvetica', 20), pady=5,
                            command=lambda: controller.show_frame("Registerd"))
        button1.pack()
        button2.pack()

class Registerd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=200, height=200)
        self.controller = controller
        label = tk.Label(self, wraplength=600, text="Je hebt een nieuw account aangemaakt.'", font=('Helvetica', 16))
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Druk op deze knop om terug te gaan naar het startscherm", width=20, font=('Helvetica', 20),
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack()


if __name__ == "__main__":
    app = NsStalling()
    app.mainloop()