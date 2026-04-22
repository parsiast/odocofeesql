# dashboard/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUp, Usermanager, UserView, CustomTokenObtainPairView

urlpatterns = [
    # ثبت نام و لاگین
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # مدیریت کاربران (فقط سوپر یوزر)
    path('usermanager/<int:pk>/', Usermanager.as_view(), name='user-manager'),
    path('showusers/', UserView.as_view(), name='show-users'),
]