from django.shortcuts import render
import socket
# Create your views here.

def index(request):
	context = {'peer_num': socket.gethostname()}
	return render(request, "firstapp/index.html", context)