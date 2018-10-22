class klant:

    def __init__(self, vn, an, strt, hn, pstcd, std, prvnc, ml, tn, ww):
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

    def wijzig_wachtwoord(self):
        while True:
            old_ww = input('Geef oud wachtwoord:')
            if old_ww == self.wactwoord:
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


def registreren():
    vn = input("Voornaam:")
    an = input("Achternaam:")
    strt = input("Straat:")
    hn = input("Straatnummer:")
    pstcd = input("Postcode:")
    std = input("Stad:")
    prvncs = input("Provincie:")
    ml = input("Email:")
    tn = input("Telefoonnummer:")
    while True:
        import getpass
        ww = getpass.getpass('Wachtwoord:')
        hhww = getpass.getpass('Herhaal wachtwoord:')
        if ww == hhww:
            break
        else:
            print('Wachtwoorden komen niet overheen')
    klant1 = klant(vn, an, strt, hn, pstcd, std, prvncs, ml, tn, ww)
    import sqlite3
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("INSERT INTO klanten VALUES(?,?,?,?,?,?,?,?,?,?,?)", (vn, an, strt, hn, pstcd, std, prvncs, ml, tn, ww, klant1.get_hash()))
    conn.commit()
    conn.close()
    return klant1

def stalling_verkrijgen(klant1, stallingen, plaats):
    for stl in stallingen:
        if stl.vrij:
            stalling1 = stl
            break
    import sqlite3
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    stalling1.set_klant(klant1)
    c.execute("UPDATE stallingen SET klant_hash = ? WHERE stallingnummer = ?", (klant1.get_hash(),
                                                                                 stalling1.get_stallingnummer()))
    conn.commit()
    conn.close()
    print('Stalling ', stalling1.get_stallingnummer(), ' verkregen voor ', klant1.get_voornaam())
    return stallingen



def stalling_vrijgeven(hash, stallingen, plaats):
    for stl in stallingen:
        if stl.get_klant() is not None and stl.get_klant().get_hash() == hash:
            stalling1 = stl
            break

    import sqlite3
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute("UPDATE stallingen SET klant_hash = ? WHERE stallingnummer = ?", (0,
                                                                                 stalling1.get_stallingnummer()))
    conn.commit()
    conn.close()
    print('Stalling ', stalling1.get_stallingnummer(), ' vrijgegeven voor ', stalling1.get_klant().get_voornaam())


def get_klanten(plaats):
    import sqlite3
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    klanten1 = {}
    for row in c.execute('SELECT * FROM klanten ORDER BY voornaam'):
        klanten1[row[10]] = klant(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9])
        klanten1[row[10]].set_hash(row[10])
    conn.close()
    return klanten1


def get_stallingen(plaats, klanten):
    import sqlite3
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


def create_table(plaats):
    import sqlite3
    naam = plaats + '.db'
    conn = sqlite3.connect(naam)
    c = conn.cursor()
    c.execute('''CREATE TABLE klanten
                 (voornaam text, achternaam text, straat text, huisnummer text, postcode text, stad text, provincie text
                 , email text, telefoonnummer text, wachtwoord text, hash INTEGER)''')
    c.execute('''CREATE TABLE stallingen
                     (stallingnummer INTEGER, vrij INTEGER, klant_hash INTEGER)''')
    for i in range(1, 101):
        c.execute("INSERT INTO stallingen VALUES(?,?,?)",(i, 1, 0))
    conn.commit()
    conn.close()


while True:
    plaats = input("geef uw plaatsnaam op:")
    import os
    if os.path.isfile(plaats+".db"):
        break
    else:
        print("no such place exists in our database")
#create_table('Vianen')
klanten = get_klanten(plaats)
stallingen = get_stallingen(plaats, klanten)
#new_klant = registreren()
#klanten[new_klant.get_hash()] = new_klant
#    stalling_verkrijgen(klant1, stallingen, plaats)
#stalling_vrijgeven(new_klant.get_hash(), stallingen, plaats)
import sqlite3
file = plaats + '.db'
conn = sqlite3.connect(file)
c = conn.cursor()

for row in c.execute('SELECT * FROM klanten ORDER BY voornaam'):
    print(row)
for row in c.execute('SELECT * FROM stallingen'):
    print(row)
conn.close()
