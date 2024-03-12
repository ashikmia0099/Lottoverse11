
from django.urls import path
from . import views


urlpatterns = [
    path('depositebalance/', views.Depositeview, name = 'deposite_balance'),
    path('balance/', views.Balanceview, name='balancepage'),
    path('myearning/', views.MyEarning, name='myearningpage'),
    
]