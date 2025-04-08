from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return self.username


class Product(models.Model):
    product_name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=40)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.product_name}'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'Клиент: {self.user} Товар: {self.product} Количество: {self.quantity}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=[
        ('pending', 'В ожидании'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ], default='pending')

    def __str__(self):
        return f'Order id:{self.id} Date: {self.order_date} Status: {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True)

