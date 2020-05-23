from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import AirQData
from .serializers import AirQDataSerializer
import json

# Create your views here.
class AirQView(APIView):

	def get(self, request):
		airq = AirQData.objects.all().order_by('-id')[:10][::-1]
		serializer = AirQDataSerializer(airq, many=True)
		return Response(serializer.data)

	def post(self, request):
		airData = request.data

		airObj = AirQData()
		airObj.State = airData['State']
		airObj.City = airData['City']
		airObj.NO2_Mean = airData['NO2_Mean']
		airObj.NO2_1st_Max_Value = airData['NO2_1st_Max_Value']
		airObj.NO2_AQI = airData['NO2_AQI']
		airObj.O3_Mean = airData['O3_Mean']
		airObj.O3_1st_Max_Value = airData['O3_1st_Max_Value']
		airObj.O3_AQI = airData['O3_AQI']
		airObj.SO2_Mean = airData['SO2_Mean']
		airObj.SO2_1st_Max_Value = airData['SO2_1st_Max_Value']
		airObj.SO2_AQI = airData['SO2_AQI']
		airObj.CO_Mean = airData['CO_Mean']
		airObj.CO_1st_Max_Value = airData['CO_1st_Max_Value']
		airObj.CO_AQI = airData['CO_AQI']

		airObj.save()
		return Response(request.data)