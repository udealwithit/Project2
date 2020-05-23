from django.apps import AppConfig
import requests
import json

class RestserverConfig(AppConfig):
	name = 'restserver'
	verbose_name = "restserver"
	
	def ready(self):
		content = {'registry_status':'failed'}
		post_data = {'area': 'Area1', 'ip':'52.149.143.178'}
		while(True):
			response = requests.post('http://13.82.17.205:8443/getpeers/', data=post_data)
			content = json.loads(response.content)	
			print(content)
			if(content['registry_status'] == 'success'):
				break
			else:
				time.sleep(5000)
