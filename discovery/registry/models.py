from django.db import models

# Create your models here.
class PeerTable(models.Model):
	area = models.CharField(max_length=30)
	ip = models.CharField(max_length=20)