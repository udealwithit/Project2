from django.urls import path
from . import views

urlpatterns = [
	path('index', views.index, name='index'),
	path('chart',views.chart, name='chart'),
	path('update_chart', views.update_chart,name='update_chart')	
]
