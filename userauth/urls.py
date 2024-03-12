
from django.urls import path
from . import views


urlpatterns = [
    path('',views.main_view, name = 'mainview'),
    path('metamask/', views.metamask_register_login, name='metamaskpage'),
    path('logout/', views.logout_view, name='logoutpage'),
    path('profile/', views.ProfileView, name = 'profilepage'),
    path('refferal/', views.ReffaralLinkView, name = 'refferallinkpage'),
    path('<str:ref_code>/',views.main_view, name = 'mainview'),
]