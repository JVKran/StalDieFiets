import requests
app_token = 'a2b11c66wgm777aavcokfh1dhu9q4o'
user_token = 'udy2az1ugrag1t55tkutb46qt7nczr'
title = 'Fietsenstalling'
message = 'Uw fiets is opgehaald bij de stalling'

def alert(title, message, priority='1'):
	data = {'token': app_token, 'user': user_token, 'title': title, 'message': message, 'priority': priority}
	r = requests.post('https://api.pushover.net/1/messages.json', data=data, headers={'User-Agent': 'Python'})
	print(str(r.text))

alert(title, message , 1)