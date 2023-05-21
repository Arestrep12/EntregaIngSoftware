from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        almuerzos = MenuItem.objects.filter(
            category__name__contains='Almuerzo')
        asados = MenuItem.objects.filter(category__name__contains='Asado')
        bebidas = MenuItem.objects.filter(category__name__contains='Bebida')
        postres = MenuItem.objects.filter(category__name__contains='Postre')

        context = {
            'almuerzos': almuerzos,
            'asados': asados,
            'bebidas': bebidas,
            'postres': postres
        }

        return render(request, 'cliente/order.html', context)

    def post(self, request, *args, **kwargs):

        id_cliente = request.POST.get('id_cliente')
        name = request.POST.get('name')
        email = request.POST.get('email')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            id_cliente=id_cliente,
            name=name,
            email=email
        )
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'cliente/order_confirmation.html', context)
