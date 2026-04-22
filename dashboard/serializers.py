# dashboard/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from dashboard.models import Customer, Address


def normalize_phone(value: str) -> str:
    if value.startswith("0") and len(value) == 11:
        return "+98" + value[1:]
    return value


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'phonenumber', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customer.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['customer', 'locationame', 'address']


# سریالایزر مخصوص لاگین و توکن
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # اضافه کردن اطلاعات سفارشی به توکن
        token['username'] = user.username
        token['phonenumber'] = user.phonenumber

        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # احراز هویت با مدل Customer سفارشی
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        # فراخوانی متد والد برای تولید توکن
        data = super().validate(attrs)

        # اضافه کردن اطلاعات کاربر به پاسخ
        data['user_id'] = user.id
        data['username'] = user.username
        data['phonenumber'] = user.phonenumber
        data['is_superuser'] = user.is_superuser

        return data