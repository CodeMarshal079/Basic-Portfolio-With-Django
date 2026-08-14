from django.urls import path
from .views import *

urlpatterns = [
    path('',registerPage, name='register'),
    path('login/',loginPage, name='login'),
    path('logout/',logoutPage, name='logout'),
    path('profile/',profileUpdatePage, name='profile'),
    path('consume/',consumePage, name='consume'),
    path('dashboard/',dashboardPage, name='dashboard')
]