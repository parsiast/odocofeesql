
from django.db import models
from dashboard.models import Address , Customer
from products.models import Item

class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="baskets")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Basket #{self.id} - {self.customer.username}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.IntegerField()  # snapshot of price

    def total_price(self):
        return self.quantity * self.price_at_time

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("delivering", "Delivering"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.IntegerField()

    def total_price(self):
        return self.quantity * self.price_at_time
