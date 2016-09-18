from time import strftime, gmtime, sleep
import random

from pymongo import MongoClient
client = MongoClient()
db = client.test

import requests
import yaml
import json
import os

c = {"username":""}
c["password"] = ""
url = ''
i = 0
while True:
	# Create dummy data
	b = random.normalvariate(10,5)
	data = {"value":b}
	data["time"] = i
	data["group"] = "a"
	print(data)
	#r = requests.post(url, data=json.dumps(data), auth=(c['username'],c['password']))
	db.test.insert_one(data)
	i+=1
	sleep(1)
