import json

import requests

url = 'https://rezafastapi.herokuapp.com/user/78'
myobj = {
	"phone_num": 78,
	"email": "em1",
	"name": "rza",
	"home_num": "5",
	"role": 0 ,
	"passwor"
	"d": "1234"
}
date = {
	"phone": 78,
	"password": "1234"
}

patch = {
	"apartment_id": 7
}
x = requests.patch(url=url, json=patch)

print(x.json())
