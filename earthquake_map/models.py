from django.db import models


class Earthquake_object(models.Model):
    
    title = models.CharField(max_length=100, default='title0')
    #date = models.DateTimeField()
    epi_lon = models.CharField(max_length=100, default=0)
    epi_lat = models.CharField(max_length=100, default=0)
    magnitude = models.CharField(max_length=100, default='n/a')
    public_url = models.CharField(max_length=200, default='url0')
    private_url = models.CharField(max_length=200, default='url0')
    public_exists = models.BooleanField(default=False)
    closest_city = models.CharField(max_length=400, default='false')
    distance = models.CharField(max_length=200, default='false')
    #geojson_public = models.FileField()
    #geojson_private = models.FileField()
    
    
    #def to_geojson(self):
    #    return data_processing(self.excel_data, str(self.date))
        
    


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)