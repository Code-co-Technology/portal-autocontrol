from django.urls import path
from authen.auth.views import UserRegisterView, UserLoginView
from authen.profile.views import UserProfileView
from authen.change_password.views import change_password, RequestPasswordRestEmail, SetNewPasswordView

urlpatterns = [
    # Auth
    path('authen/user/register/', UserRegisterView.as_view()),
    path('authen/user/login/', UserLoginView.as_view()),
    # profile
    path('authen/user/profile/', UserProfileView.as_view()),
    # Password
    path('authen/user/change/password/', change_password),
    path('forget/password/reset/', RequestPasswordRestEmail.as_view()),
    path('forget/password/new/', SetNewPasswordView.as_view()),

]