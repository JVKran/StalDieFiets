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
    '''
     class for klanten object
    '''
    def __init__(self, vn, an, strt, hn, pstcd, std, prvnc, ml, tn, ww, po, ean):
        '''

        method to create a klant object

        Args:
            vn (str): voornaam klant
            an (str): achternaam  klant
            strt (str): straat klant
            hn (str): huisnummer klant
            pstcd (str): postcode klant
            std (str): stad klant
            prvnc (str): provincie klant
            ml (str) email van klant
            tn (str): telefoonnumer klant
            ww (str): wachtwoord van klant
            po (str): push over token van klant
            ean (int): barcode klant
        '''
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
        '''
        getter voor voornaam
        :return: voornaam
        '''
        return self.voornaam

    def get_achternaam(self):
        '''
        getter voor achternaam
        :return: achternaam
        '''
        return self.achternaam

    def get_adres(self):
        '''
        getter voor adress in de vorm straat:huisnummer:postcode:stad
        :return: straat:huisnummer:postcode:stad
        '''
        return self.straat+':'+self.huisnummer+':'+self.postcode+':'+self.stad

    def get_provincie(self):
        '''
        getter voor provincie
        :return: provincie
        '''
        return self.provincie

    def get_telefoonnummer(self):
        '''
        getter voor telefoonnummer
        :return: telefoonnummer
        '''
        return self.telefoonnummer

    def get_email(self):
        '''
        getter voor email
        :return: email
        '''
        return self.email

    def get_hash(self):
        '''
        getter voor hash
        :return: hash
        '''
        return self.hash

    def get_pushover(self):
        '''
        getter voor pushover
        :return: pushover
        '''
        return self.pusho

    def get_ean(self):
        '''
        getter voor hash
        :return: hash
        '''
        return self.ean

    def set_voornaam(self, new_vn):
        '''
        setter voor voornaam
        :param new_vn: nieuwe voornaam
        :return: None
        '''
        self.voornaam = new_vn

    def set_achternaam(self, new_an):
        '''
        setter voor achternaam
        :param new_an: nieuwe achternaam
        :return: None
        '''
        self.achternaam = new_an

    def set_Adres(self,  new_strt, new_hn, new_pstcd, new_std, new_prvnc):
        '''
        setter voor adres
        :param new_strt: nieuwe straat
        :param new_hn: nieuwe huisnummer
        :param new_pstcd: nieuw postcode
        :param new_std: nieuwe stad
        :param new_prvnc: nieuwe provincie
        :return: None
        '''
        self.straat = new_strt
        self.huisnummer = new_hn
        self.postcode = new_pstcd
        self.stad = new_std
        self.provincie = new_prvnc

    def set_email(self, new_ml):
        '''
        setter voor email
        :param new_ml: nieuwe email
        :return: None
        '''
        self.email = new_ml

    def set_telefoonnummer(self, new_tn):
        '''
        setter voor telefoonnummer
        :param new_tn: nieuw telefoon nummer
        :return: None
        '''
        self.telefoonnummer = new_tn

    def set_hash(self, hash1):
        '''
        setter voor hash_code
        :param hash1: nieuwe hash code
        :return: None
        '''
        self.hash = hash1

    def get_wachtwoord(self):
        '''
        getter voor wachtwoord
        :return: wachtwoord
        '''
        return self.wachtwoord


class stalling:
    '''
    class voor een stalling met stalling nummer of stalling vrij is en de klant
    '''
    def __init__(self, stnm):
        '''
        initialize stalling met meegegeven stallingnnummer
        vrij word true gezet
        klant word none gemaakt
        :param stnm:
        '''
        self.stalingnnumer = stnm
        self.vrij = True
        self.klant = None

    def get_klant(self):
        '''
        getter voor klant behoorend bij deze stalling
        :return: klant object
        '''
        return self.klant

    def get_stallingnummer(self):
        '''
        getter voor stallingnummer
        :return: stallingnummer
        '''
        return self.stalingnnumer

    def get_vrij(self):
        '''
        getter voor vrij geeft aan of stalling vrij is of niet in de vorm van een boolean
        :return: boolean
        '''
        return self.vrij

    def set_klant(self, klant):
        '''
        setter voor klant maakt stalling gelijk niet meer vrij
        :param klant: klant object
        :return: None
        '''
        self.klant = klant
        self.vrij = False

    def vrij_stalling(self):
        '''
        maakt stalling vrij en zet klant weer None
        :return: None
        '''
        self.klant = None
        self.vrij = True


def registreren(nieuwe_klant):
    '''
    registreren word gebruikt om een klant in de database op te slaan
    :param nieuwe_klant:
    :return: klant object
    '''
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
    '''
    hiermee word een stalling verkregen voor de gegeven klant en plaats
    en checkt welke stallingen vrij zijn en geeft de eerste die vrij is
    aan klant
    :param klant1: klant object
    :param stallingen: stalling list
    :param plaats: string van plaats
    :return:
    '''
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
    '''
    hiermee word een stalling vrijgegeven voor de gegeven klant en plaats
    en maakt de stalling weer vrij
    :param klant1: klant object
    :param stallingen: stalling list
    :param plaats: string van plaats
    :return:
    '''
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
    '''
    returnt de klanten met een dict met hash als key of email als key
    :param plaats: string plaats
    :param sortby: string sorteer op hash of email
    :return: dict klanten
    '''
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
    '''
    returnt stallingen als list van stalling object
    :param plaats: string plaats
    :param klanten: dict van klanten
    :return: list stallingen
    '''
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
    '''
    returnt stallingen als dict van stallingen met als keys klant hash
    :param plaats: string plaats
    :param klanten: dict van klanten
    :return: dict stallingen
    '''
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
    '''
    creeerd een database voor een nieuwe stad met klanten en stallingen
    :param plaats: naam van de plaats die gecreeerd moet worden
    :return: None
    '''
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
    '''
    funtie om locatie op te vragen
    :return: string locatie (stad)
    '''
    location = 'http://ip-api.com/csv'
    with requests.Session() as lijst:
        download = lijst.get(location)
        decoded_content = download.content.decode('utf-8    ')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            return row[5]


def log_in_out(plaats, email, password):
    '''
    log in met gegeven email en wachtwoord voor een plaats hij kijkt of je in database
    staat en dan of wachtwoord klopt en dan of de barcode werkt zo niet return None zoja return klant
    :param plaats: string plaats
    :param email: string email
    :param password: string wachtwoord
    :return: klant object of None als login mislukt
    '''
    # Maakt een foto via de webcam en slaat deze op als barcode.png. minimaal 8 MP dus nep barcode_scan.jpg gebruikt. Levert de barcode in nummers terug #
    try:
        klanten = get_klanten(plaats, "email")
        print(plaats)
        klant = klanten[email]
    except KeyError:
        return None
    if klant.get_wachtwoord() != password:
        return None
    camera = cv2.VideoCapture(0)
    camera.set(3, 1280)
    camera.set(4, 720)
    return_value, image = camera.read()
    cv2.imwrite('barcode.png', image)
    camera.release()
    del camera
    cv2.destroyAllWindows()
    multipart_data = MultipartEncoder(
        fields={
            'file': ('barcode.png', open('barcode.png', 'rb'), 'image/png'),
            'apikey': '7b1e1c27-3115-46a3-8720-730497e2f85f'
        }
    )
    response = requests.post('https://api.havenondemand.com/1/api/sync/recognizebarcodes/v1', data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type})
    data = str(response.text).split(',')
    ean = data[0][20:]
    print(klant.get_ean())
    print(ean)
    try:
        if int(klant.get_ean()) == int(ean.strip('"')[:12]):
            return klant
        else:
            return
    except ValueError:
        return None


def alert(user_token, message, bool):
    '''
    functie om push over te sturen met barcode of zonder ligt aan bool
    :param user_token: user token
    :param message: string message
    :param bool: boolean
    :return:
    '''
    priority = '1'
    app_token = 'a2b11c66wgm777aavcokfh1dhu9q4o'
    title = 'Fietsenstalling'
    if bool:
        multipart_data = MultipartEncoder(
        fields={
               'attachment': ('barcode.png', open('barcode.png', 'rb'), 'image/png'),
               'token': app_token,
               'user': user_token,
               'title': title,
               'message': message,
               'priority': priority
            }
     )
    else:
        multipart_data = MultipartEncoder(
            fields={
                'token': app_token,
                'user': user_token,
                'title': title,
                'message': message,
                'priority': priority
            }
        )
    r = requests.post('https://api.pushover.net/1/messages.json', data=multipart_data, headers={'User-Agent': 'Python', 'Content-Type': multipart_data.content_type})
    return str(r.text)

def get_steden():
    '''
    get steden uit database
    :return: database
    '''
    conn = sqlite3.connect("Steden.db")
    c = conn.cursor()
    steden = []
    for row in c.execute('SELECT * FROM Steden ORDER BY plaats'):
        steden.append(row[0])
    conn.commit()
    conn.close()
    return steden


def update_steden():
    '''
    update steden
    :return: None
    '''
    global steden
    steden = get_steden()


def update():
    '''
    update alle global variable
    :return: None
    '''
    global klanten_hash
    global klanten_email
    global stallingen
    global stallingen_hash
    klanten_hash = get_klanten(plaats, "hash")
    klanten_email = get_klanten(plaats, "email")
    stallingen_hash = get_hash_stallingen(plaats, klanten_hash)
    stallingen = get_stallingen(plaats, klanten_hash)

#
#
#
#
#
#
#
#
#
#
#
#

class NsStalling(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        w = 500
        h = 500
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("NS Fietsenstalling")
        self.configure(bg='#FFF100')
        self.resizable(False, False)
        self.title_font = tkfont.Font(family='Helvetica', size=titlesize)
        label = Label(self)
        photo = PhotoImage(file="ns.png")
        label.configure(bg='#FFF100', image=photo)
        label.image = photo
        label.grid(row=14, column=0, rowspan=2, columnspan=2)
        cont = tk.Frame(self)
        cont.grid(row=0, column=2)
        self.frames = {}
        for F in (StartPage, LogIn, Register, Klant_Page, Choice_City, Create_City, Captcha):
            page_name = F.__name__
            frame = F(parent=cont, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        global steden
        global plaats
        try:
            if geo() in steden:
                plaats = geo()
                update()
                self.frames[StartPage.__name__].set_info()
                self.show_frame("StartPage")
            else:
                self.show_frame("Choice_City")
        except:
            self.show_frame("Choice_City")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_info(self):
        self.frames[Klant_Page.__name__].set_info()

    def set_info_stad(self):
        self.frames[StartPage.__name__].set_info()

    def timer(self):
        self.after(3000, self.show_frame("StartPage"))


class StartPage(tk.Frame):
    label_plaats= None

    def __init__(self, parent, controller):
        global label_plaats
        tk.Frame.__init__(self, parent)
        self.configure(bg='#FFF100')
        label_plaats = Label(self)
        self.controller = controller
        self.bind("<Key>", lambda: controller.show_frame("LogIn"))
        label = tk.Label(self, bg='#FFF100', text="Start pagina", font=controller.title_font)
        label.grid(row=1, column=1)
        button1 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Log in", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("LogIn"), relief=GROOVE)
        button2 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Registreer", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("Register"), relief=GROOVE)
        button3 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Andere stad", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("Choice_City"), relief=GROOVE)
        button1.grid(row=3, column=1)
        button2.grid(row=3, column=0)
        button3.grid(row=3, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=130)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=rowsize)

    def set_info(self):
        global plaats
        global label_plaats
        label_plaats.configure(text=plaats, bg='#FFF100', font=('Helvetica', 12))
        label_plaats.grid(row=2, column=1)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=130)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=rowsize)


class Choice_City(tk.Frame):
    def __init__(self, parent, controller):
        global steden
        tk.Frame.__init__(self, parent)
        self.configure(bg='#FFF100')
        label = tk.Label(self, bg='#FFF100', text="Kies locatie van fietsenstalling", font=controller.title_font)
        label.grid(row=0, column=2, columnspan=3)
        self.controller = controller
        row, column = 1, 1
        div = len(steden) / 3
        round(div)
        int(div)

        def choice(stad):
            global plaats
            plaats = stad
            update()
            controller.set_info_stad()
            controller.show_frame("StartPage")

        for stad in steden:
            button = tk.Button(self, fg="#ffffff", bg='#4f54ad', text=stad, font=('Helvetica', buttonsize), command=lambda stad=stad: choice(stad), relief=GROOVE)
            button.grid(row=row, column=column)
            row += 1
            if row > div:
                row = 1
                column += 1

        col_count, row_count = self.grid_size()

        button = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Nieuwe stad", font=('Helvetica', buttonsize))
        button.configure(command=lambda: controller.show_frame("Create_City"), relief=GROOVE)
        button.grid(row=row_count+1, column=col_count-1)

        col_count, row_count = self.grid_size()

        for col in range(0, col_count):
            if col == 0 or col == 1:
                self.grid_columnconfigure(col, minsize=10)
            else:
                self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=rowsize)


class Create_City(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#FFF100')
        label = tk.Label(self, bg='#FFF100', text="Stad toevoegen", font=controller.title_font)
        label.grid(row=0, column=0)

        def creeer():
            global steden
            if e1.get() not in steden:
                create_table(e1.get())
                update_steden()
                global plaats
                plaats = e1.get()
                controller.set_info_stad()
                controller.show_frame("StartPage")
        label = Label(self, bg='#FFF100', text="Geef naam van stad:", font=('Helvetica', textsize))
        e1 = Entry(self, bg='#fff58c')
        button = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Maak aan", font=('Helvetica', buttonsize), command=creeer, relief=GROOVE)
        e1.grid(row=1, column=1, padx=5, pady=5)
        label.grid(row=1, column=0)
        button.grid(row=1, column=2)
        button1 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Back", font=('Helvetica', buttonsize),
                            command=lambda: controller.show_frame("Choice_City"), relief=GROOVE)
        button1.grid(row=2, column=1)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=rowsize)

class Captcha(tk.Frame):
    def __init__(self, parent, controller):
        global cap
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#FFF100')
        plaatje = ImageCaptcha()
        for i in range(4):
            cap += chr(random.randrange(65, 90))
        plaatje.write(cap, 'captchaim.png')
        photo = PhotoImage(file="captchaim.png")
        label = tk.Label(self, bg='#FFF100', image=photo)
        label.image = photo
        label.grid(row=1, column=2)

        def click():
            global cap
            global foute_cap
            if ant.get().upper() == cap.upper():
                foute_cap = 0
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
                controller.show_frame("StartPage")
                top = Toplevel()
                top.title('Gelukt')
                Message(top, text='''Welkom bij NS stalling.
                
                U staat geregistreerd bij deze stalling.
                
                U word nu teruggestuurd naar de startpagina.
                
                U kunt nu inloggen met uw email en wachtwoord.
                ''', padx=20, pady=20).pack()
                top.after(3000, top.destroy)
                klant_globaal = None
                alert(klant_globaal.get_pushover(), "Je bent geregistreerd hierbij je barcode", True)
            else:
                foute_cap += 1
                if foute_cap > 4:
                    controller.show_frame("StartPage")
                    top = Toplevel()
                    top.title('Mislukt')
                    Message(top, text="te vaak fout captcha", padx=20, pady=20).pack()
                    top.after(3000, top.destroy)
                    return
                plaatje = ImageCaptcha()
                cap = ""
                for x in range(4):
                    cap += chr(random.randrange(65, 91))
                plaatje.write(cap, 'captchaim.png')
                photo = PhotoImage(file="captchaim.png")
                label.configure(image=photo)
                label.image = photo
                ant.delete(0, 'end')

        ant = Entry(self, bg='#fff58c')
        but = Button(self, fg="#ffffff", bg='#4f54ad', text="Verzend", command=lambda: click())
        self.bind('<Return>', click)
        but.grid(row=3, column=2)
        ant.grid(row=2, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(0, row_count):
            self.grid_rowconfigure(row, minsize=rowsize)


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
        label_stalling = tk.Label(self, bg='#FFF100')
        self.configure(bg='#FFF100')
        label1 = tk.Label(self, bg='#FFF100')
        label2 = tk.Label(self, bg='#FFF100')
        label3 = tk.Label(self, bg='#FFF100')
        self.controller = controller
        label = tk.Label(self, bg='#FFF100', text="Klanten pagina", font=controller.title_font)
        label.grid(row=1, column=1)
        label_fiets = tk.Label(self, bg='#FFF100', text="", font=('Helvetica', textsize))
        global klant_globaal
        global stallingen_hash

        def vrijgeven():
            global klant_globaal
            label_fiets.configure(text=stalling_vrijgeven(klant_globaal, stallingen_hash, plaats), bg='#FFF100')
            label_fiets.grid(row=6, column=1)
            update()
            alert(klant_globaal.get_pushover(), "Je stalling is vrijgegeven op locatie: "+plaats, False)
            controller.set_info()

        def verkrijgen():
            global klant_globaal
            global stallingen
            global stallingen_hash
            try:
                stallingen_hash[klant_globaal.get_hash()]
                label_fiets.configure(text="Max 1 stalling per gebruiker")
                label_fiets.grid(row=6, column=1)
            except KeyError:
                label_fiets.configure(text=stalling_verkrijgen(klant_globaal, stallingen, plaats))
            update()
            alert(klant_globaal.get_pushover(), "Je hebt een stalling aangevraagd in locatie: ", False)
            controller.set_info()

        def log_uit():
            global klant_globaal
            klant_globaal = None
            global label_stalling
            global label1
            global label2
            global label3
            label_fiets.forget()
            label1.forget()
            label2.forget()
            label3.forget()
            label_stalling.forget()
            controller.show_frame("StartPage")

        button1 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Fiets Vrijgeven", font=('Helvetica', buttonsize),
                            command=vrijgeven, relief=GROOVE)
        button2 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="stalling Verkrijgen", font=('Helvetica', buttonsize),
                            command=verkrijgen, relief=GROOVE)
        button3 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Log uit", font=('Helvetica', buttonsize),
                            command=log_uit, relief=GROOVE)

        button1.grid(row=7, column=0)
        button2.grid(row=7, column=1)
        button3.grid(row=7, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            if col == 1:
                self.grid_columnconfigure(col, minsize=180)
            else:
                self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(0, row_count):
            if row == 2 or row == 3 or row == 4 or row == 5:
                self.grid_rowconfigure(row, minsize=20)
            else:
                self.grid_rowconfigure(row, minsize=rowsize)
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
            label_stalling.configure( text="Fietsen stalling : geen")

        label3.configure(text="Plaats stalling: " + plaats,
                       font=('Helvetica', textsize))
        label1.forget()
        label2.forget()
        label3.forget()
        label_stalling.forget()
        label1.grid(row=2, column=1)
        label2.grid(row=3, column=1)
        label_stalling.grid(row=4, column=1)
        label3.grid(row=5, column=1)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            if col == 1:
                self.grid_columnconfigure(col, minsize=180)
            else:
                self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(0, row_count):
            if row == 2 or row == 3 or row == 4 or row == 5:
                self.grid_rowconfigure(row, minsize=20)
            else:
                self.grid_rowconfigure(row, minsize=rowsize)


class LogIn(tk.Frame):
    label_log_in = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global label_log_in
        label_log_in = Label(self)
        self.controller = controller
        self.configure(bg='#FFF100')
        label = tk.Label(self, bg='#FFF100', text="Log in page", font=controller.title_font)
        label.grid(row=1, column=1)
        label_log_in.config(bg='#FFF100', font=('Helvetica', textsize))
        Label(self, bg='#FFF100', text="E-mail:", font=('Helvetica', textsize)).grid(row=2, column=0, sticky=E, padx="5")
        e1 = Entry(self, bg='#fff58c', width=30)
        e1.grid(row=2, column=1)
        Label(self, bg='#FFF100', text="Password", font=('Helvetica', textsize)).grid(row=3, column=0, sticky=E, padx="5")
        e2 = Entry(self, bg='#fff58c', show="*", width=30)
        e2.grid(row=3, column=1)

        def log_in():
            global klant_globaal
            klant_globaal = log_in_out(plaats, e1.get(), e2.get())
            if klant_globaal is None:
                label_log_in.configure(text="Log in mislukt",bg= "#ff0c00")
                label_log_in.grid(row=5, column=1)
                return
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            controller.set_info()
            controller.show_frame("Klant_Page")

        def back():
            global label_log_in
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            label_log_in.forget()
            controller.show_frame("StartPage")

        button1 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Back", font=('Helvetica', buttonsize),
                            command=back, relief=GROOVE)
        button2 = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Log in", font=('Helvetica', buttonsize), command=log_in, relief=GROOVE)

        button1.grid(row=4, column=2)
        button2.grid(row=4, column=1)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            self.grid_columnconfigure(col, minsize=110)
        for row in range(0, row_count):
            if row == 2 or row == 3:
                self.grid_rowconfigure(row, minsize=10)
            else:
                self.grid_rowconfigure(row, minsize=rowsize)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#FFF100')
        label = tk.Label(self, bg='#FFF100', text="Register", font=controller.title_font)
        label.grid(row=1, column=2)

        label_vn = Label(self, bg='#ff0c00', text="Voornaam is ongeldig", font=('Helvetica', textsize))
        label_ong = Label(self, bg='#ff0c00', text="alle velden moeten ingevuld worden", font=('Helvetica', textsize))
        label_an = Label(self, bg='#ff0c00', text="achternaam is ongeldig", font=('Helvetica', textsize))
        label_strt = Label(self, bg='#ff0c00', text="Straat is ongeldig", font=('Helvetica', textsize))
        label_std = Label(self, bg='#ff0c00', text="Stad is ongeldig", font=('Helvetica', textsize))
        label_prvnc = Label(self, bg='#ff0c00', text="Provincie is ongeldig", font=('Helvetica', textsize))
        label_ww = Label(self, bg='#ff0c00', text="Wachtwoorden komen niet overeen", font=('Helvetica', textsize))
        label_em = Label(self, bg='#ff0c00', text="email bestaat al", font=('Helvetica', textsize))
        label_em_wr = Label(self, bg='#ff0c00', text="email ongeldig", font=('Helvetica', textsize))
        label_ww_tk = Label(self, bg='#ff0c00', text="Wachtwoord is tekort", font=('Helvetica', textsize))
        label_tn = Label(self, bg='#ff0c00', text="Telefoonnummer ongeldig", font=('Helvetica', textsize))
        label_tn_len = Label(self, bg='#ff0c00', text="Telefoonnummer ongeldig", font=('Helvetica', textsize))
        label_pstcd_1 = Label(self, bg='#ff0c00', text="postcode is ongeldig", font=('Helvetica', textsize))
        label_pstcd_2 = Label(self, bg='#ff0c00', text="postcode is ongeldig", font=('Helvetica', textsize))
        label_pstcd_len = Label(self, bg='#ff0c00', text="postcode is ongeldige lengte", font=('Helvetica', textsize))

        Label(self, bg='#FFF100', text="Voornaam:", font=('Helvetica', textsize), anchor='e').grid(row=2, column=1, sticky=E, padx="5")
        e1 = Entry(self, bg='#fff58c')
        e1.config(font=inputsize)
        e1.grid(row=2, column=2)
        Label(self, bg='#FFF100', text="Achternaam:", font=('Helvetica', textsize), anchor='e').grid(row=3, column=1,
         sticky = E, padx = "5")
        e2 = Entry(self, bg='#fff58c')
        e2.config(font=inputsize)
        e2.grid(row=3, column=2)
        Label(self, bg='#FFF100', text="Straat:", font=('Helvetica', textsize), anchor='e').grid(row=4, column=1,
         sticky = E, padx = "5")
        e3 = Entry(self, bg='#fff58c')
        e3.config(font=inputsize)
        e3.grid(row=4, column=2)
        Label(self, bg='#FFF100', text="Huisnummer:", font=('Helvetica', textsize), anchor='e').grid(row=5, column=1, sticky=E, padx="5")
        e4 = Entry(self, bg='#fff58c')
        e4.config(font=inputsize)
        e4.grid(row=5, column=2)
        Label(self, bg='#FFF100', text="Postcode:", font=('Helvetica', textsize), anchor='e').grid(row=6, column=1, sticky=E, padx="5")
        e5 = Entry(self, bg='#fff58c')
        e5.config(font=inputsize)
        e5.grid(row=6, column=2)
        Label(self, bg='#FFF100', text="Stad:", font=('Helvetica', textsize), anchor='e').grid(row=7, column=1, sticky=E, padx="5")
        e6 = Entry(self, bg='#fff58c')
        e6.config(font=inputsize)
        e6.grid(row=7, column=2)
        Label(self, bg='#FFF100', text="Provincie:", font=('Helvetica', textsize), anchor='e').grid(row=8, column=1, sticky=E, padx="5")
        e7 = Entry(self, bg='#fff58c')
        e7.config(font=inputsize)
        e7.grid(row=8, column=2)
        Label(self, bg='#FFF100', text="E-mail:", font=('Helvetica', textsize), anchor='e').grid(row=9, column=1, sticky=E, padx="5")
        e8 = Entry(self, bg='#fff58c')
        e8.config(font=inputsize)
        e8.grid(row=9, column=2)
        Label(self, bg='#FFF100', text="Telefoonnummer:", font=('Helvetica', textsize), anchor='e').grid(row=10, column=1, sticky=E, padx="5")
        e9 = Entry(self, bg='#fff58c')
        e9.config(font=inputsize)
        e9.grid(row=10, column=2)
        Label(self, bg='#FFF100', text="Wachtwoord", font=('Helvetica', textsize), anchor='e').grid(row=11, column=1, sticky=E, padx="5")
        e10 = Entry(self, bg='#fff58c', show="*")
        e10.config(font=inputsize)
        e10.grid(row=11, column=2)
        Label(self, bg='#FFF100', text="Herhaal Wachtwoord:", font=('Helvetica', textsize), anchor='e').grid(row=12, column=1, sticky=E, padx="5")
        e11 = Entry(self, bg='#fff58c', show="*")
        e11.config(font=inputsize)
        e11.grid(row=12, column=2)
        Label(self, bg='#FFF100', text="Push over token:", font=('Helvetica', textsize), anchor='e').grid(row=13, column=1, sticky=E, padx="5")
        e12 = Entry(self, bg='#fff58c')
        e12.config(font=inputsize)
        e12.grid(row=13, column=2)

        def getInfo():
            label_em.grid_forget()
            label_em_wr.grid_forget()
            label_vn.grid_forget()
            label_an.grid_forget()
            label_strt.grid_forget()
            label_std.grid_forget()
            label_prvnc.grid_forget()
            label_ww_tk.grid_forget()
            label_ww.grid_forget()
            label_tn.grid_forget()
            label_tn_len.grid_forget()
            label_pstcd_1.grid_forget()
            label_pstcd_2.grid_forget()
            label_ong.grid_forget()
            if len(e1.get()) < 1 or len(e2.get()) < 1 or len(e3.get()) < 1 or len(e4.get()) < 1 or len(e5.get()) < 1 or\
                    len(e6.get()) < 1 or len(e7.get()) < 1 or len(e8.get()) < 1 or len(e9.get()) < 1 or\
                    len(e10.get()) < 1 or len(e11.get()) < 1 or len(e12.get()) < 1:
                label_ong.grid(row=15, column=2, rowspan=2)
                return
            try:
                klanten_email[e8.get()]
                label_em.grid(row=15, column=2, rowspan=2)
                return
            except KeyError:
                None

            good = False
            for char in e8.get():
                if char == "@":
                    good = True
            if not good:
                label_em_wr.grid(row=15, column=2, rowspan=2)
                return
            for char in e1.get():
                if not char.isalpha() and (char != " " and char != "'" and char != "." and char != "-"):
                    label_vn.grid(row=15, column=2, rowspan=2)
                    return
                    break
            for word in e2.get().split():
                for char in word:
                    if not char.isalpha() and (char != " " and char != "'" and char != "." and char != "-"):
                        label_an.grid(row=15, column=2, rowspan=2)
                        return
                        break
            for char in e3.get():
                if not char.isalpha() and (char != " " and char != "'" and char != "." and char != "-"):
                    label_strt.grid(row=15, column=2, rowspan=2)
                    return
                    break
            for char in e6.get():
                if not char.isalpha() and (char != " " and char != "'" and char != "." and char != "-"):
                    label_std.grid(row=15, column=2, rowspan=2)
                    return
                    break
            for char in e7.get():
                if not char.isalpha() and (char != " " and char != "'" and char != "." and char != "-"):
                    label_prvnc.grid(row=15, column=2, rowspan=2)
                    return
                    break
            if e10.get() != e11.get():
                label_ww.grid(row=15, column=2, rowspan=2)
                return
            else:
                if len(e10.get()) < 8:
                    label_ww_tk.grid(row=15, column=2, rowspan=2)
                    return
            if not e9.get().isnumeric():
                label_tn.grid(row=15, column=2, rowspan=2)
                return
            if len(e9.get()) < 10 or len(e9.get()) > 11:
                label_tn.grid(row=15, column=2, rowspan=2)
                return
            if len(e5.get()) == 6:
                for char in e5.get()[:4]:
                    if not char.isnumeric():
                        label_pstcd_1.grid(row=15, column=2, rowspan=2)
                        return
                        break
                for char in e5.get()[4:6]:
                    if not char.isalpha():
                        label_pstcd_2.grid(row=15, column=2, rowspan=2)
                        return
                        break
            else:
                label_pstcd_len.grid(row=15, column=2, rowspan=2)
                return

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

        button = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Back", font=('Helvetica', buttonsize),
                           command=back, relief=GROOVE)
        button.grid(row=14, column=1)
        button.grid(row=14, column=1)
        button = tk.Button(self, fg="#ffffff", bg='#4f54ad', text="Registreer", font=('Helvetica', buttonsize),
                           command=getInfo, relief=GROOVE)
        button.grid(row=14, column=2)
        col_count, row_count = self.grid_size()
        for col in range(0, col_count):
            if col == 0 or col == 1 or col == 2:
                self.grid_columnconfigure(col, minsize=0)
            else:
                self.grid_columnconfigure(col, minsize=60)
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

class testStallingClass(unittest.TestCase):

    def setUp(self):
        global plaats
        plaats = "test"
        self.klanten = get_klanten("test", "hash")
        self.stallingen = get_stallingen("test", self.klanten)
        self.hash_stallingen = get_hash_stallingen("test", self.klanten)
        #print(stalling_vrijgeven(self.klanten[478594418], self.hash_stallingen, "test"))


    def testGetKlanten(self):
        klant = self.klanten[478594418]
        self.assertEqual(klant.get_voornaam(), "Joey", "text of get klanten klant geeft")

    def testGetStalingen(self):
        self.assertRaises(KeyError, lambda: self.hash_stallingen[478594418])

    def testStallingverkrijgen(self):
        stalling_verkrijgen(self.klanten[478594418], self.stallingen, "test")
        self.hash_stallingen = get_hash_stallingen("test", self.klanten)
        self.assertEqual(self.hash_stallingen[478594418].get_vrij(), False, " test of stalling word verkregen")

    def testStallingvrijgeven(self):
        self.hash_stallingen = get_hash_stallingen("test", self.klanten)
        stalling_vrijgeven(self.klanten[478594418], self.hash_stallingen, "test")
        self.hash_stallingen = get_hash_stallingen("test", self.klanten)
        self.assertRaises(KeyError, lambda: self.hash_stallingen[478594418])

if __name__ == "__main__":
    buttonsize = 10
    textsize = 10
    titlesize = 15
    inputsize = 5
    columnsize = 80
    rowsize = 60
    plaats = ''
    cap = ""
    foute_cap = 0
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


