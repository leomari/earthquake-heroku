import pandas as pd
import numpy as np
from geopy.distance import geodesic


def closest_city(epicenter):
    df=pd.read_csv('static/files/Mexican_cities.csv')
    
    distances = []
    lat = df['Lat']
    lon = df['Lon']
    
    for i in range(len(df)):
        distances.append(geodesic(epicenter, (lat[i],lon[i])).km)

    dist = int(round(np.array(distances).min()))
    city = df['City'][np.array(distances).argmin()]
    
    return city, dist