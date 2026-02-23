from django.shortcuts import render
from rest_framework import  viewsets
from rest_framework_simplejwt.views import TokenObtainPairView


class CookieTokenObtainPairView(TokenObtainPairView):
    cookie_prefix = ""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            prefix = self.cookie_prefix

            response.set_cookie(
                key=f"{prefix}access",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Strict"
            )

        return response
