import csv
import requests

def geo():
    CSV_URL = 'http://ip-api.com/csv'


    with requests.Session() as lijst:
        download = lijst.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)
geo()