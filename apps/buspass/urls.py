"""File for urls in vpn_user."""
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('select_bus/', views.select_bus, name='select_bus'),
    path('book/<int:pk>/', views.book, name='book'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('payment-successful/<int:pk>/', views.payment_successful, name='payment_successful'),
    path('view-pass/<int:pk>/', views.view_pass, name='view_pass'),
    path('cancel-pass/<int:pk>/', views.cancel_pass, name='cancel_pass'),
]
