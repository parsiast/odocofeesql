from rest_framework import serializers
from .models import Basket, BasketItem, Order, OrderItem


class BasketItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = BasketItem
        fields = ["id", "item_name", "quantity", "price_at_time", "total_price"]


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ["id", "items", "total", "address"]

    def get_total(self, obj):
        return obj.total_price()

    def get_address(self, obj):
        if obj.address:
            return {
                "id": obj.address.id,
                "locationame": obj.address.locationame,
                "address": obj.address.address
            }
        return None




class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "item_name", "quantity", "price_at_time", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "address", "created_at", "items", "total"]

    def get_total(self, obj):
        return obj.total_price()
