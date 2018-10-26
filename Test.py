
import webbrowser
import random
import sqlite3
import requests
import csv


# Maakt, leest en schrijft naar een database. Daarnaast wordt er een random barcode met EAN gegenereerd

def geo():
    location = 'http://ip-api.com/csv'
    with requests.Session() as lijst:
        download = lijst.get(location)
        decoded_content = download.content.decode('utf-8    ')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            return row[7:9]


def register():
    ean = random.randint(1000000000000000, 99999999999999999)
    try:
        name = str(input("Uw voornaam: "))
        surname = str(input("Uw achternaam: "))
        name = name + ' ' + surname
        phone = int(input("Uw telefoonnummer: "))
        email = str(input("Uw email-adres: "))
        password = str(input("Uw wachtwoord: "))
        # location =
        pushover = int(input("Gebruikerstoken: "))
    except:
        register()
    webbrowser.open('http://barcodes4.me/barcode/c128a/{}.png'.format(ean))
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO users(name, phone, email, password)
                      VALUES(?,?,?,?)''', (name, phone, email, password))
    db.commit()
    db.close()


def get_information():
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''SELECT name, email, phone, password FROM users''')
    email = str(input("Uw email-adres: "))
    password = str(input("Uw wachtwoord: "))
    all_rows = cursor.fetchall()
    for row in all_rows:
        if row[1] == email and row[-1] == password:
            print("Uw naam is {}, uw emailadres is {} en uw wachtwoord is {}.".format(row[0], row[1], row[-1]))


print(geo())