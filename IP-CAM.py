from cv2 import *
import requests



text = input('Take a picture: ')

if text == 'yes':
    cam = VideoCapture('http://145.89.156.42:8080/shot.jpg')  #IP van je IP-Webcam app
    s, img = cam.read()
    cv2.imwrite("filename.jpg", img)


    r = requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": 'a2b11c66wgm777aavcokfh1dhu9q4o',
        "user": 'uv2a4p9zzk6bf4d579uxde8agk5zru',
        "message": ":|"
    },
                      files={
                          "attachment": ("image.jpg", open("filename.jpg", "rb"), "image/jpg")    #File attachment
                      })
    print(r.text)