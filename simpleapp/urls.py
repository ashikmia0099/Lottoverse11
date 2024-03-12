from django.urls import path
from . import views

urlpatterns = [

    path('handle_payment/', views.Payment, name='handle_payment'),
    path('Shopping_history/',views.ShoppingHistory, name = 'shoppinghistorypage')

] 