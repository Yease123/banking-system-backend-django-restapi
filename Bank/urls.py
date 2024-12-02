"""
URL configuration for Bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import BankLoginApi,ChangeBankApi,RegisterUserApi,ValidateUserApi,ValidateOtpApi,SignupUserApi,LoginusersApi,transactionApi,Showtransactionapi
urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginbank/',BankLoginApi.as_view(),name="banklogin"),
    path('changebank/',ChangeBankApi.as_view(),name="changebankinfo"),
    path('registeruser/',RegisterUserApi.as_view(),name="registeruser"), 
    path('registeruser/<int:pk>/', RegisterUserApi.as_view(), name='update_user'),
    path('validateuser/', ValidateUserApi.as_view(), name='validateuser'),
    path('validateotp/', ValidateOtpApi.as_view(), name='validateotp'),
    path('signupuser/',SignupUserApi.as_view(),name="signupuser"),
    path('loginuser/',LoginusersApi.as_view(),name="loginuser"),
    path('transaction/',transactionApi.as_view(),name="transaction"),
    path('showtransaction/',Showtransactionapi.as_view(),name="showtransaction")

]
