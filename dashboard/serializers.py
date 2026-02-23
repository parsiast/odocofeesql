from rest_framework import serializers

from dashboard.models import Customer

def normalize_phone(value: str) -> str:
    if value.startswith("0") and len(value) == 11:
        return "+98" + value[1:]
    return value




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields =['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


