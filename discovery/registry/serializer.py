from rest_framework import serializers
from .models import PeerTable

class PeerTableSerializer(serializers.ModelSerializer):

	class Meta:
		model = PeerTable
		fields = '__all__'