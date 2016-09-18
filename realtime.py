#Mongo!
from pymongo import MongoClient, DESCENDING
client = MongoClient()
db = client.test

#Bokeh!
from bokeh.plotting import figure, curdoc
from bokeh.charts import Histogram
from bokeh.models.sources import ColumnDataSource
from bokeh.client import push_session
from bokeh.driving import linear

#Machine learning!
from sklearn import linear_model
import numpy as np
regr = linear_model.LinearRegression()

# Socrata Datasets
import requests
import yaml
import os
import json

c = {"username":""}
c["password"] = ""
url = ''

antialias = 10
N = 60
vals = dict()
vals["x"] = [0 for i in range(N)]
vals["y"] = [0 for i in range(N)]
# Pridicted values
vals["p"] = [0 for i in range(N)]
# Means
vals["m"] = [0 for i in range(N)]


myfigure = figure(plot_width=800, plot_height=400)
datacoords = ColumnDataSource(data=vals)

linea = myfigure.line("x", "y", color="red",source=datacoords)
lineb = myfigure.line("x","m",source=datacoords)
#predicted = myfigure.line("x","p",source=datacoords)


def get_lin_reg(x):
	x = np.array(x)
	c = db.test.find({},{"value":1,"_id":0}).sort("_id",DESCENDING).limit(len(x))
	y = [item['value'] for item in list(c)]
	x = x.reshape(-1,1)
	result = regr.fit(x,y)
	return result.coef_, result.intercept_

#Initialize X
array_of_x = []
def save_x(x):
	array_of_x.append(x)
	xs = np.array(array_of_x)
	return xs

@linear(m=1, b=0) #step will increment by 0.05 every time
def update(step):
	new_x = 0
	beta_x = 0
	intercept = 0
	if len(vals["x"]) > N:
		vals["x"] = vals["x"][1:]
	if len(vals['y']) > N:
		vals["y"] = vals["y"][1:]
	if len(vals["m"]) > N:
		vals["m"] = vals["m"][1:]
	if len(vals["p"]) > N:
		vals["p"] = vals["p"][1:]
	new_x += step
	vals["x"].append(new_x)

	# Newest Socrata Dataset
	#r = requests.get(url, auth=(c['username'],c['password']))
	#print(r.text)
	#d = r.json()[0]
	#new_y1 = d['value']
	#vals["y"].append(float(new_y1))

	# Newest Mongo Data
	c = db.test.find().sort("_id",DESCENDING).limit(1)
	new_y1 = c[0]["value"]
	vals["y"].append(new_y1)

	### GET THE AVERAGE VALUE
	m = mean(vals["y"])
	vals["m"].append(float(m))

	#a = db.test.aggregate([{"$group":{"_id":"$group","average":{"$avg":"$value"}}}])
	#avg = a.next()
	#vals["m"].append(avg["average"])

	### PREDICT VALUES
	#all_x = save_x(step)
	#beta_x, intercept = get_lin_reg(all_x)
	
	#beta_x, intercept = get_lin_reg(vals["x"])
	
	#p = [beta_x*step + intercept for step in vals["x"]]

	#vals["p"] = p
	linea.data_source.data["x"] = vals["x"]
	linea.data_source.data["y"] = vals["y"]
	lineb.data_source.data["m"] = vals["m"]
	#predicted.data_source.data["p"] = vals["p"]

def mean(arr):
	s = sum(arr)
	return s/len(arr)
# open a session to keep our local document in sync with server
session = push_session(curdoc())
curdoc().add_periodic_callback(update, 1000) #period in ms
session.show(myfigure)
session.loop_until_closed()