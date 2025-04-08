from django.contrib import admin

from slavichoney_app.models import Product, User, Basket, Order, OrderItem

# Register your models here.


admin.site.register(Product)
admin.site.register(User)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(OrderItem)
