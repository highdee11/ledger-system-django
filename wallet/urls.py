from django.contrib import admin
from django.urls import path
from .views import WalletView, TransferView

urlpatterns = [
    path('transaction/', WalletView.as_view()),
    path('balance/', WalletView.as_view()),
    path('transfer/', TransferView.as_view())
]
