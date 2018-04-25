
def is_valid_date(title):
    try:
        [month, day, year] = title.split('-')
        month = int(month)
        day = int(day)
        year = int(year)
        
        if month<13 and day<32 and year>1000:
            return True
        else:
            return False
        
    except:
        return False
        
    