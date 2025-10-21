from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('your_api/', views.getGeocode),
]