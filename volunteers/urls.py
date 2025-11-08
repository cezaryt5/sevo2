from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('register/', views.volunteer_register, name='register'),
    path('partner-inquiry/', views.partner_inquiry, name='partner_inquiry'),
]

