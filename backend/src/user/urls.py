from django.urls import include, path
from .views import TestView, LoginView, LogoutView

urlpatterns = [
    path('', TestView.as_view(), name="test"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
