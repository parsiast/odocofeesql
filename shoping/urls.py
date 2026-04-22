from django.urls import path
from .views import (
    AddToBasket,
    GetBasket,
    UpdateBasketItem,
    SetBasketAddress,
    Checkout,
    OrderList,
    OrderDetail,
    DeleteBasketItem
)

urlpatterns = [
    # Basket endpoints
    path("basket/add/", AddToBasket.as_view(), name="basket-add"),
    path("basket/", GetBasket.as_view(), name="basket-get"),
    path("basket/update/", UpdateBasketItem.as_view(), name="basket-update"),
    path("basket/address/", SetBasketAddress.as_view(), name="basket-set-address"),
    path("basket/delete/<int:basket_item_id>/", DeleteBasketItem.as_view()),


    # Checkout
    path("checkout/", Checkout.as_view(), name="basket-checkout"),

    # Orders
    path("orders/", OrderList.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderDetail.as_view(), name="order-detail"),
]
