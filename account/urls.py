from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path('dashborad/',views.dashboard,name='dashboard'),
    path('',views.account,name='account'),
    path('kyc_reg/',views.kyc_registration,name='kyc_reg'),

]