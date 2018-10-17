import sqlite3


db = sqlite3.connect('gouda.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE users
             (name text, location text, pushover text, ean text)''')