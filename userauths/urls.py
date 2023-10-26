from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('sign_up/',views.register_view,name='sign_up'),
    path('sign_in/',views.login_view,name='sign_in'),
    path('sign_out/',views.logout_view,name='sign_out'),
    path('change_password/',views.change_password,name='change_password'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<str:uidb64>/<str:token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('confirm_otp/<user_id>/',views.confirm_otp,name='confirm_otp'),
    path('send_otp_again/<user_id>/',views.send_otp_again,name='send_otp_again'),
]