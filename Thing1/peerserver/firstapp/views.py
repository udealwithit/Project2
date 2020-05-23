from django.shortcuts import render
import socket
from restserver.models import AirQData
from django.http import JsonResponse
# Create your views here.

def index(request):
	context = {'peer_num': socket.gethostname()}
	return render(request, "firstapp/index.html", context)

def chart(request):
	context = {
		'time': [0],
		'aqualities': [0],
	}
	return render(request, "firstapp/chart.html", context)

def update_chart(request):
	temp =	AirQData.objects.all()[:10]
	time = []
	aqualities = []

	for i,dataset in enumerate(temp) :
		time.append(i)
		aqualities.append(dataset.NO2_Mean)

	time = time[:10]
	aqualities = aqualities[:10]
	aqualities.reverse()

	context = {
		'time': time,
		'aqualities': aqualities,
	}
	return JsonResponse(context)
