from django.shortcuts import render, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from .models import PeerTable
from .serializer import PeerTableSerializer
from django.http import JsonResponse

# Create your views here.
class RegisterPeer(generics.ListAPIView):
	serializer_class = PeerTableSerializer

	def get(self,request):
		if request.GET:
			acode = request.GET['acode']
			if PeerTable.objects.filter(area=acode).exists():
				iplist = list(PeerTable.objects.filter(area=acode).values())			
				return JsonResponse({'query_status':'success', 'iplist':iplist})
			else:
				return JsonResponse({'query_status':'failed'})
		else:
			data = PeerTable.objects.all()
			serializer = PeerTableSerializer(data, many=True)
			return JsonResponse({'query_status':'success', 'iplist':serializer.data})

	def post(self, request):
		peerdata = request.data		
		if PeerTable.objects.filter(ip=peerdata['ip']).exists():
			return JsonResponse({'registry_status':'success'})
		else:	
			peer_entry = PeerTable()
			peer_entry.area = peerdata['area']
			peer_entry.ip = peerdata['ip']
			peer_entry.save()
			return JsonResponse({'registry_status':'success'})
