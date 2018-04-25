from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.conf.urls.static import static
from static.python_scripts.data_processing import data_processing
from static.python_scripts import sensor_remover
from static.python_scripts import sort_by_dates
from static.python_scripts.is_valid_date import is_valid_date
from static.python_scripts.export_epi_info import export_epi_info
#from static.python_scripts.sensor_remover import export_func
from .models import Earthquake_object
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from static.python_scripts.closest_city import closest_city

#from django.templatetags.static import static


import numpy as np
import pandas as pd    
import json
import geojson
import os
import os.path

# Create your views here.
@login_required
def admin_home(request):
    return render(request, 'earthquake_map/admin_home.html')

def public(request):
    earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
    
    #only send edited earthquakes
    index_edited = []
    count = 0
    for earthquake in earthquakes_sorted:
        fname = 'media/public_' + earthquake.title + '.geojson'
        print(fname)
        if os.path.isfile(fname):
            index_edited.append(count)
        count += 1
    
    
    earthquakes_edited = [earthquakes_sorted[x] for x in index_edited]
    
    
    return render(request, 'earthquake_map/public/index_public.html',{'earthquakes': earthquakes_edited})

@login_required
def analysis(request):
    earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
    return render(request, 'earthquake_map/analysis/index_analysis.html',{'earthquakes': earthquakes_sorted})

@login_required
def editpublic(request):
    earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
    print("kommer hit")
    if request.method == 'POST':# and request.POST['export']:# and request.POST['main_title']:
        if request.POST['action'] == "export":
            #if (request.POST['export'] and request.POST['main_title']):
            sn = request.POST['serial_number']
            url = request.POST['url']
            temp_title = request.POST['main_title']
            public_url = 'media/public_' + temp_title +'.geojson'
            epi_info_url = 'media/epi_public_' + temp_title +'.json'
            sn_list = sn.split(',')
            
            #if sn_list[0] != '':
                
            sensor_remover.remove_and_export(url, public_url,epi_info_url ,sn_list)
            print("kjrte remove and export")
            
            
            #sensor_remover.export_func(temp_title)
            if request.POST['epi_speed'] and request.POST['epi_delay']:
                export_epi_info(request.POST['epi_speed'], request.POST['epi_delay'], temp_title)
            
            earthquake = Earthquake_object.objects.all().filter(title=temp_title).update(public_exists = True)
            
            earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
            #earthquakes = Earthquake_object.objects
            return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes_sorted, 'message': 'export successful'})
#else: 
			#    return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes})
        elif request.POST['action'] == "undo":
            temp_title = request.POST['main_title']
            sensor_remover.undo_func(temp_title)
            return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes_sorted})
        #elif request.POST['action'] == "remove": 
         #   if (request.POST['serial_number'] and request.POST['url']):
                
                    
                #return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes})
            #else: 
             #   return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes})
                # add warning message? 
        else: 
            return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes_sorted})
    else: 
        return render(request, 'earthquake_map/editpublic/index.html',{'earthquakes': earthquakes_sorted})

@login_required
def data(request):
    earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
    if request.method == 'POST':
        if request.POST['title'] and request.FILES['excel_data'] and request.POST['epi_lon'] and request.POST['epi_lat']:
            
            title = request.POST['title']
            #excel_data = request.POST['excel_data']
            if is_valid_date(title):
            
                #earthquake.magnitude = request.POST['magnitude']
                public_url = 'media/public_' + title + '.geojson'
                private_url = 'media/private_' + title + '.geojson'
                #earthquake.geojson_public = request.FILES['excel_data']

                magnitude = request.POST['magnitude']
                epi_lon = float(request.POST['epi_lon'])
                epi_lat = float(request.POST['epi_lat'])
                city, distance = closest_city((epi_lat, epi_lon))

                earthquake = Earthquake_object(title=title, public_url=public_url, private_url=private_url, magnitude=magnitude, epi_lon=epi_lon, epi_lat=epi_lat, closest_city=city, distance=distance)

                data_processing(request.FILES['excel_data'], title, epi_lon, epi_lat)


                earthquake.save() #inserts into database      
                earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
                return render(request, 'earthquake_map/data.html', {'message': 'the file is uploaded successfully', 'earthquakes': earthquakes_sorted})
            else:
                return render(request, 'earthquake_map/data.html', {'message': 'Error: not a valid date', 'earthquakes': earthquakes_sorted})
        
        elif request.POST['delete_title']:
            print(request.POST['delete_title'])
    
            title = request.POST['delete_title'][1:-1]
            public_url = 'media/public_'+title+'.geojson'
            private_url = 'media/private_'+title+'.geojson'
            edit_public_url = 'media/edit_public_'+title+'.geojson'
            epicenter_url = 'media/epicenter_'+title+'.geojson'
            epi_info_url = 'media/epi_public_'+title+'.json'
            
            #Delete object
            Earthquake_object.objects.filter(title=title).delete()
            #Delte files
            if os.path.isfile(public_url):
                os.remove(public_url)
                os.remove(epi_info_url)
            
            os.remove(private_url)
            os.remove(edit_public_url)
            os.remove(epicenter_url)
            

            earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
            
            return render(request, 'earthquake_map/data.html', {'message': 'the files were deleted', 'earthquakes': earthquakes_sorted})
        

            
        else:
            return render(request, 'earthquake_map/data.html', {'error': 'one of the required items are missing','earthquakes': earthquakes_sorted})    
    else:
        if Earthquake_object.objects:
            earthquakes_sorted = sort_by_dates.sort_by_dates(Earthquake_object.objects)
            
            return render(request, 'earthquake_map/data.html', {'earthquakes': earthquakes_sorted})
        else:
            return render(request, 'earthquake_map/data.html')



# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
#def 
'''
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

'''




def login(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    else:

        if request.method == 'POST':
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

            if user is not None:
                auth.login(request, user)
                return redirect('admin_home')
            else:
                return render(request, 'earthquake_map/login/login.html', {'error': 'username or password is wrong'})
        else:
            return render(request, 'earthquake_map/login/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('public')