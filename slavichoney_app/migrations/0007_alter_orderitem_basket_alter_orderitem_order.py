# Generated by Django 5.1.7 on 2025-04-08 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slavichoney_app', '0006_remove_orderitem_product_orderitem_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='basket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='slavichoney_app.basket'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='slavichoney_app.order'),
        ),
    ]
