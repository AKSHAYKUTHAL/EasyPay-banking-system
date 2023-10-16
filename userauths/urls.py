from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('sign_up/',views.register_view,name='sign_up'),
    path('sign_in/',views.login_view,name='sign_in'),
    path('sign_out/',views.logout_view,name='sign_out'),

]