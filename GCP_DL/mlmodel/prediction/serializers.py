from rest_framework import serializers
from .models import AirQData

class AirQDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = AirQData
		fields = '__all__'