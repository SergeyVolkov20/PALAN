from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/cars/', views.get_cars_json, name='cars_json'),
    path('api/start-trip/', views.start_trip, name='start_trip'),
    path('api/end-trip/', views.end_trip, name='end_trip'),
    path('api/init-data/', views.init_data, name='init_data'),
]