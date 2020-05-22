from django.shortcuts import render, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from .models import PeerTable
from .serializer import PeerTableSerializer

# Create your views here.
class RegisterPeer(generics.ListAPIView):
	serializer_class = PeerTableSerializer

	def get_queryset(self):
		acode = self.request.query_params.get('acode')
		ipset = PeerTable.objects.filter(area=acode)
		return ipset

	def post(self, request):
		peer_entry = PeerTable()
		peerdata = request.data
		peer_entry.area = peerdata['area']
		peer_entry.ip = peerdata['ip']
		peer_entry.save()
		return peerdata