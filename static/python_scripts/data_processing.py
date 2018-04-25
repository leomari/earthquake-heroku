import numpy as np
import pandas as pd    
import geojson
from django.templatetags.static import static
#from django.core.files import File

def data_processing(excel_file, date, epi_lon, epi_lat):


    #Import
    #date='02-17-2018'
    df=pd.read_excel(excel_file)


    #Clean Data

    lowercols = []
    columns = df.columns
    for col_name in columns:
        name = col_name.lower()
        if name == 'serial':
            name = 'sn'

        lowercols.append(name)

    df.columns = lowercols


    origin=0
    count=0
    time=[]
    tp=0
    for i in range(len(df)):
        if 'hssendtime' in lowercols:
            t = df['hssendtime'][i].second
        else:
            df['hssenddate']=pd.to_datetime(df['hssenddate'])
            t = df['hssenddate'][i].second

        while t<tp:
            t+=60

        time.append(t-origin)
        tp=t

    df['time']=time

    df=df[['sn','lat','lon','s_gal','mdact','time']]
    b=df['mdact']=='ON'
    df['mdact']=b


    #Get cluster
    #http://localhost:8000/static/python_scripts/all_sensors.csv
    #all_sensors=pd.read_csv("{% static 'python_scripts/all_sensors.csv' %}")
    all_sensors=pd.read_csv("static/python_scripts/all_sensors.csv")
    #all_sensors=pd.read_csv('all_sensors.csv')

    clusters = list(np.zeros(len(df)))
    count=0
    sensors_without_cluster=[]
    for i in range(len(df)):
        cluster=all_sensors['Cluster'][df['sn'][i] == all_sensors['Serie']]
        if len(cluster) == 1:
            clusters[i]=cluster.item()
        else:
            sensors_without_cluster.append(df['sn'][i])
            count+=1

    sensors_without_cluster = pd.Series(sensors_without_cluster).unique()
    for i in range(len(df)):
        for j, sn in enumerate(sensors_without_cluster):
            if df['sn'][i] == sn:
                clusters[i] = 'no_cluster' + str(j) 

    df['cluster'] = clusters
    clusterlist = df['cluster'].unique()

    sensors=df['sn'].unique()
    sensorframes=[]

    for i in range(len(sensors)):
        sensorframes.append(df[df['sn']==sensors[i]].reset_index().drop('index',axis=1))

    t_max=df['time'].max()


    timeSensorFrames = []
    newTime=list(range(t_max))
    for sensorframe in sensorframes:
        timeSeries = np.asarray(sensorframe['time'])
        S_GalSeries = np.asarray(sensorframe['s_gal'])
        MdActSeries = np.asarray(sensorframe['mdact'])
        counter = 0

        S_Gal_new = np.zeros(t_max)
        Md_Act_new = np.zeros(t_max)
        Sn_new = np.ones(t_max)*sensorframe['sn'][0]
        Lat_new = np.ones(t_max)*sensorframe['lat'][0]
        Lon_new = np.ones(t_max)*sensorframe['lon'][0]
        i = timeSeries[0]

        local_max = timeSeries.max()
        while i < local_max+1 and i < t_max:


            if i == timeSeries[counter]:
                v=[]
                w=[]
                while i == timeSeries[counter] and counter < len(timeSeries)-1:
                    v.append(S_GalSeries[counter])
                    w.append(int(MdActSeries[counter]))
                    counter+=1


                if len(v) > 0: 
                    max_v = max(v)
                    max_w = max(w)
                S_Gal_new[i] = max_v
                Md_Act_new[i] = max_w


                i += 1
            else:
                S_Gal_new[i] = max_v
                Md_Act_new[i] = max_w
                i += 1



        S_Gal_new[i:]=S_GalSeries[-1]*np.ones(len(S_Gal_new[i:]))        
        frame=pd.DataFrame()
        frame['sn'] = Sn_new
        frame['lat'] = Lat_new
        frame['lon'] = Lon_new
        frame['mdact'] = Md_Act_new
        frame['s_gal'] = S_Gal_new
        frame['time'] = newTime
        frame['cluster'] = sensorframe['cluster'][0]
        timeSensorFrames.append([sensorframe['cluster'][0], frame])

    cluster_of_frames = []
    for clustername in clusterlist:
        local_cluster=[]
        for element in timeSensorFrames:
            if element[0] == clustername:
                local_cluster.append(element[1])

        cluster_of_frames.append(local_cluster)


    for cluster in cluster_of_frames:
        is_max = np.zeros((len(cluster[0]),len(cluster)))
        for i in range(len(cluster[0])):
            intensities=np.zeros(len(cluster))
            for j, frame in enumerate(cluster):
                intensities[j] = frame['s_gal'][i]

            #print(intensities)
            is_max[i, np.argmax(intensities)] = 1

        for k, frame in enumerate(cluster):
            frame['max'] = is_max[:, k]


    cluster_concat = []
    for cluster in cluster_of_frames:
        cluster_concat.append(pd.concat(cluster,ignore_index = True))

    all_concat = pd.concat(cluster_concat, ignore_index = True)

    only_max = all_concat[all_concat['max'] == 1]


    #To geojson

    def data2geojson_private(df):
        features = []
        insert_features = lambda X: features.append(
                geojson.Feature(geometry=geojson.Point((X["lon"],
                                                        X["lat"])),
                                properties=dict(Sn=X["sn"],
                                                S_Gal=X["s_gal"],
                                                MdAct=int(X['mdact']),
                                                Time=X['time'],
                                                #Max=X['max']
                                                Description= '<strong> Sensor </strong> <p>Serial number: '
                                                + str(int(X['sn']))+'</p> <p>Cluster: '+ X['cluster'] + '<p/> <p> Activated: ' + str(bool(X['mdact'])) + 
                                                '</p> <p> Intensity: '+str(X['s_gal'])+'</p>'
                                               )))
        df.apply(insert_features, axis=1)
        with open('media/private_' + date + '.geojson', 'w', encoding='utf8') as fp:
            geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)


    def data2geojson_public(df):
        features = []
        insert_features = lambda X: features.append(
                geojson.Feature(geometry=geojson.Point((X["lon"],
                                                        X["lat"])),
                                properties=dict(Sn=X["sn"],
                                                S_Gal=X["s_gal"],
                                                #MdAct=int(X['mdact']),
                                                Time=X['time'],
                                                Max=X['max']
                                                #Description= '<strong> Sensor </strong> <p>Serial number: '
                                                #+ str(int(X['sn']))+'</p> <p>Cluster: '+ X['cluster'] + '<p/> <p> Activated: ' + str(bool(X['mdact'])) + 
                                                #'</p> <p> Intensity: '+str(X['s_gal'])+'</p>'
                                               )))
        df.apply(insert_features, axis=1)
        with open('media/edit_public_' + date + '.geojson', 'w', encoding='utf8') as fp:
            geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)
        #with open('media/raw_public_' + date + '.geojson', 'w', encoding = 'utf8') as fp: 
        #    geojson.dump(geojson.FeatureCollection(features), fp, sort_keys = True, ensure_ascii = False)
	    

    data2geojson_public(only_max)
    data2geojson_private(all_concat)
    print('geojson laget')
    #f = open('public_' + date + '.geojson', 'r') 
    #return File(f)
    
    
    epi_df = pd.DataFrame()
    epi_df['time'] = list(range(t_max))
    epi_df['radius'] = list(range(t_max))
    epi_df['lon'] = epi_lon
    epi_df['lat'] = epi_lat
    
    def data2geojson_epicenter(df):
        features = []
        insert_features = lambda X: features.append(
                geojson.Feature(geometry=geojson.Point((X["lon"],
                                                        X["lat"])),
                                properties=dict(                                             Rad=X["radius"],
                                                Time=X['time'],
                                               )))
        df.apply(insert_features, axis=1)
        with open('media/epicenter_' + date + '.geojson', 'w', encoding='utf8') as fp:
            geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)
            
    data2geojson_epicenter(epi_df)