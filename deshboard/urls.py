

from django.urls import path,include
from . import views

urlpatterns = [
    
    path('myprofile/', views.Myprofile, name='myprofilepage'),
    
]
