from django.urls import path
from . import views

urlpatterns = [
	path('index', views.index, name='index'),
	path('update_chart', views.update_chart, name='update_chart'),
	path('update_area',views.update_area, name='update_area')	
]
