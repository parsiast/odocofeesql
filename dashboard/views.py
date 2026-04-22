# dashboard/views.py
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from dashboard.permissions import IsSuperUser
from .serializers import CustomerSerializer, CustomTokenObtainPairSerializer
from .models import Customer
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView


@extend_schema(
    tags=["sign up users (AllowAny)"],
)
class SignUp(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Sign up a new customer",
        request=CustomerSerializer,
        responses={201: CustomerSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ویو جدید برای لاگین کاربران عادی
@extend_schema(
    tags=["login (AllowAny)"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Login user and get access token",
        description="با استفاده از username و password لاگین کنید و توکن دریافت کنید",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'نام کاربری'},
                    'password': {'type': 'string', 'description': 'رمز عبور'}
                },
                'required': ['username', 'password']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'phonenumber': {'type': 'string'},
                    'is_superuser': {'type': 'boolean'}
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["user management (authenticated + superuser)"],
)
class Usermanager(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a customer by ID",
        responses={200: CustomerSerializer, 404: None},
    )
    def get(self, request, pk):
        custom = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(custom)
        return Response(serializer.data)

    @extend_schema(
        summary="Update user information",
        request=CustomerSerializer,
        responses={200: CustomerSerializer, 404: None},
    )
    def put(self, request, pk):
        custom = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(custom, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete a user",
        responses={204: None, 404: None},
    )
    def delete(self, request, pk):
        custom = get_object_or_404(Customer, pk=pk)
        custom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Get all users",
    responses={200: CustomerSerializer(many=True)},
    tags=["user management (superuser only)"],
)
class UserView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)