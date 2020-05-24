from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import AirQData
from .serializers import AirQDataSerializer
import json
import numpy as np
from .models import MyPredictor
from django.http import JsonResponse

# Create your views here.
class MLPrediction(APIView):
	def get(self, request):
		pass

	def post(self, request):
		predictionModel = MyPredictor.from_path()
		print("Hello")
		airData = request.data

		instance = []
		instance.append(airData['NO2_Mean'])
		instance.append(airData['NO2_1st_Max_Value'])
		instance.append(airData['NO2_AQI'])
		instance.append(airData['O3_Mean'])
		instance.append(airData['O3_1st_Max_Value'])
		instance.append(airData['O3_AQI'])
		instance.append(airData['SO2_Mean'])
		instance.append(airData['SO2_1st_Max_Value'])
		instance.append(airData['SO2_AQI'])
		instance.append(airData['CO_Mean'])
		instance.append(airData['CO_1st_Max_Value'])
		instance.append(airData['CO_AQI'])
	
		output = predictionModel.predict(instance)

		return JsonResponse(output, safe=False)