import cv2
import sqlite3
import random
import csv
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import webbrowser
import barcode
from barcode.writer import ImageWriter


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


def register():
    # Maakt een ean van de barcode aan en slaat de barcode in png formaat op als ean13_barcode.png. Daarnaast worden de rest van de gegevens gevraagd #
    # en wordt de locatie in de vorm lat, long opgeslagen in de database.
    ean_number = str(random.randint(1000000000000000, 99999999999999999))
    try:
        name = str(input("Uw voor- en achternaam: "))
        phone = int(input("Uw telefoonnummer: "))
        email = str(input("Uw email-adres: "))
        password = str(input("Uw wachtwoord: "))
        location = geo()
        pushover = int(input("Gebruikerstoken: "))
    except:
        register()
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(ean_number, writer=ImageWriter())
    fullcode = ean.save('ean13_barcode')
    webbrowser.open("ean13_barcode.png")
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO users(name, phone, email, password, location, pushover, ean)
                      VALUES(?,?,?,?,?,?,?)''', (name, phone, email, password, location, pushover, ean_number))
    db.commit()
    db.close()
    print("Beste {}, bedankt voor uw registratie bij de fietsentallingen van de NS. We hopen u snel te zien.".format(name))


def get_information():
    # Vraagt naar emailadres en wachtwoord en geeft vervolgens de rest van de bijbehorende gegevens #
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute('''SELECT name, email, phone, password, pushover, ean FROM users''')
    email = str(input("Uw email-adres: "))
    password = str(input("Uw wachtwoord: "))
    all_rows = cursor.fetchall()
    db.commit()
    db.close()
    for row in all_rows:
        if row[1] == email and row[-3] == password:
            return "Uw naam is {}\nUw emailadres is {}\nUw pushover token is {}\nUw barcode is {}".format(row[0], row[1], row[-1], row[-2], row[-1])


def log_in_out():
    # Maakt een foto via de webcam en slaat deze op als barcode.png. minimaal 8 MP dus nep barcode_scan.jpg gebruikt. Levert de barcode in nummers terug #
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('barcode.png', image)
    del camera
    multipart_data = MultipartEncoder(
        fields={
            'file': ('barcode_scan.jpg', open('barcode_scan.jpg', 'rb'), 'image/jpg'),
            'apikey': '5a525783-f2a4-411b-a15b-358fe2d17ecc'
        }
    )
    response = requests.post('https://api.havenondemand.com/1/api/sync/recognizebarcodes/v1', data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type})
    data = str(response.text).split(',')
    ean = data[0][20:]
    db = sqlite3.connect('{}.db'.format(input('gouda of utrecht')))
    cursor = db.cursor()
    cursor.execute('''SELECT name, location, pushover, ean FROM users''')
    password = str(input("Uw wachtwoord: "))
    all_rows = cursor.fetchall()
    for row in all_rows:
        if row[-1] == ean and row[-3] == password:
            cursor.execute('''DELETE FROM users''')
            present = True
            if present is False:
                cursor.execute('''INSERT INTO users(name, location, pushover, ean)
                                        VALUES(?,?,?,?)''',
                               (name, location, pushover, ean))
                db.commit()
                db.close()


def alert():
    priority = '1'
    app_token = 'a2b11c66wgm777aavcokfh1dhu9q4o'
    user_token = 'udy2az1ugrag1t55tkutb46qt7nczr'
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


while True:
    choice = int(input("Wat wilt u doen?\n1:registreren\n2:informatie opvragen\n3:in/uitloggen"))
    if choice == 1:
        register()
    elif choice == 2:
        get_information()
    elif choice == 3:
        log_in_out()
    elif choice == 4:
        print(alert())3
    else:
        exit(0)
