from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True
    )



class Item (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = "items")
    name= models.CharField(max_length=100)
    description = models.TextField()
    price1 = models.IntegerField()
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='pics/')
    def __str__(self):
        return f"{self.category.title} - {self.name}"
