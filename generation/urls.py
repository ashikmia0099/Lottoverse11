from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
   
   path('structure/',views.structure, name = 'structurepage'),
   path('generations/',views.GenerationView, name = 'generationspage'),

]