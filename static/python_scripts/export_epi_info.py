import json

def export_epi_info(epi_speed, delay, title):
    
    epi_info = {'epi_speed': epi_speed, 'delay': delay}
    
    epi_url = 'media/epi_public_' + title + '.json'
    
    with open(epi_url, 'w') as public_file: 
        json.dump(epi_info, public_file)