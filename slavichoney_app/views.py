import json

import telebot
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from slavichoney_app.models import User, Product, Basket, Order, OrderItem
from slavichoney_back.settings import TOKEN, ADMIN

bot = telebot.TeleBot(TOKEN)


# Create your views here.
@csrf_exempt
def save_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            username = data.get('username', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            return JsonResponse({
                'status': 'success',
                'user_id': user.user_id,
                'created': created
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# @api_view(['POST'])
# @permission_classes([JWTAuthentication])
@csrf_exempt
def get_all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_dict = {}

        for product in products:
            products_dict[product.category] = products_dict.get(product.category, list())
            products_dict[product.category].append({
                'product_id': product.id,
                'product_name': product.product_name,
                'price': product.price,
                'category': product.category,
                'description': product.description,
                'image': product.image
            })

        #print(products_dict)
        return JsonResponse({'products': products_dict})
    elif request.method == 'POST':

        try:
            data = json.loads(request.body)
            # print(data)
            # user_id = data.get('user_id')
            username = data.get('username', '')
            # first_name = data.get('first_name', '')
            # last_name = data.get('last_name', '')
            #
            # role_develop = User.objects.get(username=username)
            # users_develop_role = role_develop.telegramusers_set.all()
            basket = Basket.objects.filter(user__username=username)
            print(list(basket.values()))
            return JsonResponse({
                'status': 'success',
                'basket': list(basket.values())
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_basket(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            print(data)
            user_id = data.get('user_id')
            # username = data.get('username', '')
            product_id = data.get('product_id')
            redOrInc = data.get('redOrInc')

            #
            user = User.objects.get(user_id=user_id)
            product = Product.objects.get(id=product_id)
            # users_develop_role = role_develop.telegramusers_set.all()
            basket, created = Basket.objects.get_or_create(user=user, product=product,
                                                           defaults={
                                                               'user': user,
                                                               'product': product,
                                                               'quantity': 0
                                                           }
                                                           )

            if redOrInc == 'red':
                if basket.quantity > 0:
                    basket.quantity -= 1
                else:
                    basket.quantity = 0
            elif redOrInc == 'inc':
                basket.quantity += 1

            print(basket)

            basket.save()
            print(basket.quantity)
            return JsonResponse({
                'status': 'success',
                'product_id': product_id,
                'quantity': basket.quantity,
                'created': created
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def place_order(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            # print(data)
            user_id = data.get('user_id')
            username = data.get('username', '')
            # first_name = data.get('first_name', '')
            # last_name = data.get('last_name', '')
            #
            # role_develop = User.objects.get(username=username)
            # users_develop_role = role_develop.telegramusers_set.all()
            user = User.objects.get(user_id=user_id)
            basket = Basket.objects.filter(user__username=username)
            order, created = Order.objects.get_or_create(user=user,
                                                         defaults={'user': user})
            print(basket)
            print(order)

            order_list = []

            for item in basket:
                print(item)
                orderItem, created = OrderItem.objects.update_or_create(order=order, basket=item,
                                                                        defaults={'order': order,
                                                                                  'basket': item})
                order_list.append({
                    'order_id': order.id,
                    'product_name': item.product.product_name,
                    'price': item.product.price,
                    'quantity': item.quantity
                })

            # orderItems = OrderItem.objects.filter(order=order)
            # product_list = list(orderItems.values())
            print(order)
            print(order_list)
            return JsonResponse({
                'status': 'success',
                'order': order_list
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def confirm_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            order = Order.objects.get(id=order_id)
            orderItems = OrderItem.objects.filter(order=order)
            message_text = 'Ваш заказ № ' + str(order_id) + '\n'
            total = 0
            for item in orderItems:
                cost = item.basket.quantity * item.basket.product.price
                message_text += (item.basket.product.product_name + " " + str(item.basket.product.price) + " X " +
                                 str(item.basket.quantity) + "\nСтоимость..." + str(cost) + ' ₽\n')
                total += cost

                # ОТПРАВИТЬ СООБЩЕНИЕ АДМИНУ
            message_text += 'Итого...' + str(total)
            message_text_admin = ('Пользователь с индексом ' + str(order.user.user_id) + ' оформил заказ № ' +
                                  str(order_id) + message_text[13:])
            try:
                # bot.send_message(int(order.user.user_id), message_text)
                bot.send_message(ADMIN, message_text_admin)
            except Exception as e:
                print(e)

            return JsonResponse({
                'status': 'success',
                'message': message_text
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            order = Order.objects.get(id=order_id)
            order.delete()
            print('Заказ удален')

            return JsonResponse({
                'status': 'success',
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
