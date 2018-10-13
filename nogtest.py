import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
import json



multipart_data = MultipartEncoder(
    fields={
        'file': ('barcode_scan.jpg', open('barcode_scan.jpg', 'rb'), 'image/jpg'),
        'apikey': '5a525783-f2a4-411b-a15b-358fe2d17ecc'
    }
)
response = requests.post('https://api.havenondemand.com/1/api/sync/recognizebarcodes/v1', data=multipart_data,
                         headers={'Content-Type': multipart_data.content_type})
print(response.text)
data = str(response.text).split(',')
barcode = (data[0][20:])
