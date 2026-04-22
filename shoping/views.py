from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.permissions import IsSuperUser
from dashboard.models import   Customer ,Address
from products.models import Item
from .models import Basket,BasketItem,OrderItem,Order
from .serializers import BasketSerializer,OrderSerializer,BasketItemSerializer



@extend_schema(
    summary="Add item to basket",
    description="Adds an item to the user's active basket. If basket doesn't exist, it will be created.",
    tags=["basket"],
    request={
        "application/json": {
            "example": {
                "item_id": 3,
                "quantity": 2
            }
        }
    },
    responses={200: BasketItemSerializer},
)
class AddToBasket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        item = Item.objects.get(id=item_id)

        basket, created = Basket.objects.get_or_create(
            customer=request.user,
            is_active=True
        )

        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket,
            item=item,
            defaults={"price_at_time": item.price1}
        )

        if not created:
            basket_item.quantity += quantity
            basket_item.save()

        return Response(BasketItemSerializer(basket_item).data)

@extend_schema(
    summary="Delete basket item",
    description="Deletes a specific item from the user's active basket.",
    tags=["basket"],
    parameters=[
        OpenApiParameter(name="basket_item_id", type=int, required=True),
    ],
    responses={200: OpenApiTypes.OBJECT},
)
class DeleteBasketItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, basket_item_id):
        try:
            basket_item = BasketItem.objects.get(
                id=basket_item_id,
                basket__customer=request.user
            )
        except BasketItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        basket_item.delete()
        return Response({"message": "Item removed"}, status=200)


@extend_schema(
    summary="Get active basket",
    description="Returns the user's active basket with all items.",
    tags=["basket"],
    responses=BasketSerializer,
)
class GetBasket(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        basket = Basket.objects.filter(customer=request.user, is_active=True).first()
        if not basket:
            return Response({"items": [], "total": 0})

        return Response(BasketSerializer(basket).data)



@extend_schema(
    summary="Update basket item",
    description="Updates quantity of a basket item. If quantity <= 0, item will be removed.",
    tags=["basket"],
    request={
        "application/json": {
            "example": {
                "basket_item_id": 5,
                "quantity": 3
            }
        }
    },
    responses={200: BasketItemSerializer},
)
class UpdateBasketItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("basket_item_id")
        quantity = int(request.data.get("quantity"))

        basket_item = BasketItem.objects.get(id=item_id, basket__customer=request.user)

        if quantity <= 0:
            basket_item.delete()
            return Response({"message": "Item removed"})

        basket_item.quantity = quantity
        basket_item.save()

        return Response(BasketItemSerializer(basket_item).data)



@extend_schema(
    summary="Set basket address",
    description="Sets the delivery address for the active basket.",
    tags=["basket"],
    request={
        "application/json": {
            "example": {
                "address_id": 2
            }
        }
    },
    responses={200: BasketSerializer},
)
class SetBasketAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address_id = request.data.get("address_id")

        basket = Basket.objects.get(customer=request.user, is_active=True)
        address = Address.objects.get(id=address_id, customer=request.user)

        basket.address = address
        basket.save()

        return Response(BasketSerializer(basket).data)



@extend_schema(
    summary="Checkout basket",
    description="Converts the active basket into an order and deactivates the basket.",
    tags=["order"],
    responses={200: OrderSerializer},
)
class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        basket = Basket.objects.filter(customer=request.user, is_active=True).first()
        if not basket:
            return Response({"error": "Basket is empty"}, status=400)

        if not basket.address:
            return Response({"error": "No address selected"}, status=400)

        order = Order.objects.create(
            customer=request.user,
            address=basket.address,
            status="pending"
        )

        for bi in basket.items.all():
            OrderItem.objects.create(
                order=order,
                item=bi.item,
                quantity=bi.quantity,
                price_at_time=bi.price_at_time
            )

        basket.is_active = False
        basket.save()

        return Response(OrderSerializer(order).data)



@extend_schema(
    summary="List user orders",
    description="Returns all orders of the authenticated user.",
    tags=["order"],
    responses=OrderSerializer(many=True),
)
class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user).order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)




@extend_schema(
    summary="Order detail",
    description="Returns detailed information about a specific order.",
    tags=["order"],
    responses=OrderSerializer,
)
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, customer=request.user)
        return Response(OrderSerializer(order).data)
