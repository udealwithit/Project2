from django.db import models

# Create your models here.
class AirQData(models.Model):
	State = models.CharField(max_length=50)
	City = models.CharField(max_length=50)
	NO2_Mean = models.FloatField()
	NO2_1st_Max_Value = models.FloatField()
	NO2_AQI = models.FloatField()
	O3_Mean = models.FloatField()
	O3_1st_Max_Value = models.FloatField()
	O3_AQI = models.FloatField()
	SO2_Mean = models.FloatField()
	SO2_1st_Max_Value = models.FloatField()
	SO2_AQI = models.FloatField()
	CO_Mean = models.FloatField()
	CO_1st_Max_Value = models.FloatField()
	CO_AQI = models.FloatField()
