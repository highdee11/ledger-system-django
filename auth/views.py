from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


# Create your views here.

class AuthView(TokenObtainPairView):
    permission_classes = (AllowAny,)
