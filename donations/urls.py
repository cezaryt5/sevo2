from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('donate/', views.donate, name='donate'),
    path('bank-transfer/<int:donation_id>/', views.bank_transfer, name='bank_transfer'),
    path('payment/<int:donation_id>/', views.mock_payment, name='mock_payment'),
    path('thank-you/<int:donation_id>/', views.thank_you, name='thank_you'),
]

