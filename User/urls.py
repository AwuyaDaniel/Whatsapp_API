from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserInfoView, UserRegistrationView, ChangePasswordView, UpdateUserDetails


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('user_information/', UserInfoView.as_view(), name='user_information'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('update_password/', ChangePasswordView.as_view(), name='password-update'),
    path('update_user/', UpdateUserDetails.as_view(), name='user-update'),
]
