from django.urls import include, path
from .views import UserInfoView, LoginView, LogoutView

urlpatterns = [
    path('user_info/', UserInfoView.as_view(), name="user_info"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
