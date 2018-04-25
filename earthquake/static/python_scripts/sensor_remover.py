import numpy as np 
import pandas as pd 
import geojson 
from django.templatetags.static import static 
import os 

def remove_and_export(url, public_url,epi_info_url, sn_list):
    print('starting remov func')

    with open (url, 'r') as data_file: 
        data = geojson.load(data_file)
    
    if sn_list[0] != '':
        #remove sensors
        for sn in sn_list:
            data['features'] = [element for element in data['features'] if not int(element['properties']['Sn']) == int(sn)]
    
    if os.path.isfile(public_url):
                os.remove(public_url)
                os.remove(epi_info_url)
                
    with open(public_url, 'w') as new_file: 
        geojson.dump(data, new_file)

def export_func(title):
	public_url = 'media/public_' + title + '.geojson'
	edit_url = 'media/edit_public_' + title + '.geojson'
	raw_url = 'media/raw_public_' + title + '.geojson'
	with open(edit_url, 'r') as edit_file: 
		edited_data = geojson.load(edit_file)
	with open(public_url, 'w') as public_file: 
		geojson.dump(edited_data, public_file)
	print("export success")
def undo_func(title):
	edit_url = 'media/edit_public_' + title + '.geojson'
	public_url = 'media/public_' + title + '.geojson'
	raw_url = 'media/raw_public_' + title + '.geojson'
	with open(raw_url, 'r') as raw_file: 
		raw_data = geojson.load(raw_file)
	with open(edit_url, 'w') as edit_file: 
		geojson.dump(raw_data, edit_file)
	os.remove(public_url)
	