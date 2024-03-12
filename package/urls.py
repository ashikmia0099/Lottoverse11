from django.urls import path
from . import views

urlpatterns = [
    path('add_package/', views.AddPackage, name='addpackagepage'),
    path('package/', views.ticket_view, name='packagepage'),
    path('add_to_card/', views.add_to_card, name='addtocardpage'),
    path('shopping_card/', views.shopping_card_view, name='shoppingcardpage'),
    path('user_shopping_card/',views.userShoppingCard, name='user_shopping_card'),
    path('handle_payment/<str:total_price>/', views.handle_payment, name='handle_payment'),
    
    path('select_ticket/<int:package_id>/<str:ticket_number>/',views.select_ticket, name='select_ticket'),
    path('cancel_ticket/<int:id>/', views.cancel_ticket, name='cancel_ticket'),

    
     

    
] 

# Trigger the function to deactivate inactive users
from .views import deactivate_inactive_users

deactivate_inactive_users()  # You can call this function periodically using a cron job or similar method
