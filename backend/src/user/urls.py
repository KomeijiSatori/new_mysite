from django.urls import include, path
from .views import TestView, LoginView

urlpatterns = [
    path('', TestView.as_view(), name="test"),
    path('login/', LoginView.as_view(), name="login"),
]
