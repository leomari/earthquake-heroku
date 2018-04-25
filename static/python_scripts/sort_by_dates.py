import pandas as pd

def get_date_list(objects):
    
    date_list = []
    for obj in objects.all():
        date_list.append(obj.title)
        
    return date_list

def sort_by_dates(objects): 
    
    date_list = []
    for obj in objects.all():
        date_list.append(obj.title)
        
    
    months=[]
    days=[]
    years=[]
    for date in date_list:
        [month, day, year] = date.split('-')
        months.append(month)
        days.append(day)
        years.append(year)
    df = pd.DataFrame()
    df['Month']=months
    df['Day']=days
    df['Year']=years
    
    df_sort = pd.to_datetime(df,format='%m%d%Y', errors='ignore')
    df_sort = df_sort.sort_values()
    sort_index = list(df_sort.index) 
    
    earthquakes_sorted= [objects.all()[x] for x in sort_index]
    
    return earthquakes_sorted