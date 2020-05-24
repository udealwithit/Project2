from django.shortcuts import render
import socket
from restserver.models import AirQData
from django.http import JsonResponse
from firstapp.forms import AreaForm
import requests
import json
# Create your views here.

def index(request):
	form = AreaForm(initial = {'current_area':socket.gethostname().capitalize()})
	context = {
				'peer_num': socket.gethostname(),
				'form': form,
				'time': [0],
				'no2mean': [0],
				'comean': [0],
				'so2mean': [0],
				'o3mean': [0],
				'no2aqi': [0],
				'coaqi' : [0],
				'so2aqi': [0],
				'o3aqi': [0]
			}
	return render(request, "firstapp/index.html", context)

def update_chart(request):
	temp =	AirQData.objects.all().order_by('-id')[:10][::-1]
	time = []
	no2mean = []
	comean = []
	so2mean = []
	o3mean = []
	no2aqi = []
	coaqi = []
	so2aqi = []
	o3aqi = []

	for i,dataset in enumerate(temp) :
		time.append(i)
		no2mean.append(dataset.NO2_Mean)
		comean.append(dataset.CO_Mean)
		so2mean.append(dataset.SO2_Mean)
		o3mean.append(dataset.O3_Mean)
		no2aqi.append(dataset.NO2_AQI)
		coaqi.append(dataset.CO_AQI)
		so2aqi.append(dataset.SO2_AQI)
		o3aqi.append(dataset.O3_AQI)

	context = {
		'time': time,
		'no2mean': no2mean,
		'comean': comean,
		'so2mean': so2mean,
		'o3mean': o3mean,
		'no2aqi': no2aqi,
		'coaqi': coaqi,
		'so2aqi': so2aqi,
		'o3aqi': o3aqi
	}
	return JsonResponse(context)

def update_area(request):
	if(request.GET['current_area'] == 'Area1'):
		return index(request)

	response = requests.get('http://13.82.17.205:8443/getpeers/', params={'acode':request.GET['current_area']})
	content = json.loads(response.content)	
	if(content['query_status'] == 'success'):
		otherIP = content['iplist'][0]['ip']
		form = AreaForm(initial = {'current_area': request.GET['current_area']})
		context = {
					'peer_num': socket.gethostname(),
					'form': form,
					'time': [0],
					'no2mean': [0],
					'comean': [0],
					'so2mean': [0],
					'o3mean': [0],
					'no2aqi': [0],
					'coaqi' : [0],
					'so2aqi': [0],
					'o3aqi': [0],
					'peerip': otherIP
					}
		return render(request, "firstapp/otherpeer.html", context)
	else:	
		return JsonResponse({'status':'failed'})	


def update_chart_from_peer(request):
	peerip = request.GET['peer']
	url = 'http://'+ peerip + ":8443/quality"
	resp = requests.get(url)
	data = resp.json()
	
	time = []
	no2mean = []
	comean = []
	so2mean = []
	o3mean = []
	no2aqi = []
	coaqi = []
	so2aqi = []
	o3aqi = []

	for i, d in enumerate(data):
		time.append(i)
		no2mean.append(d['NO2_Mean'])
		comean.append(d['CO_Mean'])
		so2mean.append(d['SO2_Mean'])
		o3mean.append(d['O3_Mean'])
		no2aqi.append(d['NO2_AQI'])
		coaqi.append(d['CO_AQI'])
		so2aqi.append(d['SO2_AQI'])
		o3aqi.append(d['O3_AQI'])

	context = {
		'time': time,
		'no2mean': no2mean,
		'comean': comean,
		'so2mean': so2mean,
		'o3mean': o3mean,
		'no2aqi': no2aqi,
		'coaqi': coaqi,
		'so2aqi': so2aqi,
		'o3aqi': o3aqi
	}
	return JsonResponse(context)

def predict(request):
	temp =	AirQData.objects.all().order_by('-id')[:1]
	temp = list(temp.values())
	url = "http://40.117.101.88:8000/predict/"
	temp_data = temp[0]

	resp = requests.post(url, data=temp_data)
	data = resp.json()

	context = {"demo":[data]}
	return render(request, 'firstapp/predict.html', context)