from django.urls import path
from dashboard.views import CookieTokenObtainPairView

urlpatterns = [
    path("admincookie ", CookieTokenObtainPairView.as_view()),
]