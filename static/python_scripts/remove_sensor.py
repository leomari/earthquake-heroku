import numpy as np
import pandas as pd    
import geojson
from django.templatetags.static import static

def remove_sensor(url, sn): 
	print('starter remove')
	
	with open(url, 'r') as data_file:
		data = geojson.load(data_file)
	print(data)
	print(len(data['features']))
		  
	data['features'] = [element for element in data['features'] if not int(element['properties']['Sn']) == int(sn)]
	print(len(data['features']))
	print(int(data['features'][0]['properties']['Sn'])