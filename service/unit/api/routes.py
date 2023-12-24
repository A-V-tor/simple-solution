import time
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from unit.models import Item, Order
from service.settings import (
    PUBLISH_API_STRIPE,
)
import json
from unit.utils import StripeManager


class SessionStripeAPIView(View):
    """Создание товара и отдача на фронт session_id и публичного ключа."""

    def get(self, request, pk):
        quantity = request.GET.get('quantity', 1)
        current_item = get_object_or_404(Item, id=pk)
        money, value_price = request.GET.get('money').split('-')
        stripe_manager = StripeManager(
            current_item.name,
            current_item.description,
            round(float(value_price.replace(',', '.'))),
            money,
        )

        price = stripe_manager.create_product_and_make_price()

        line_items = [
            {
                'price': price,
                'quantity': int(quantity),
            }
        ]
        session_params = StripeManager.get_session_params(line_items, request)
        session = StripeManager.get_stripe_session(session_params)

        return JsonResponse(
            {'session_id': session.id, 'public_key': PUBLISH_API_STRIPE}
        )


class InOrderAPIView(View):
    """Добавление товара в заказ."""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        item_id = data.get('item_id', None)
        quantity = abs(int(data.get('quantity', 1)))

        if quantity == 0:
            quantity = 1

        money, value_price = data.get('money').split('-')
        user = request.META.get('HTTP_X_FORWARDED_FOR', None)
        status = 'Not created'
        item = get_object_or_404(Item, id=int(item_id))

        if user and item:
            order = Order.objects.filter(user=user, is_paid=False).first()
            data_item = {
                time.time(): {
                    'name': item.name,
                    'description': item.description,
                    'price': round(float(value_price.replace(',', '.'))),
                    'quantity': quantity,
                    'currency': money,
                }
            }
            if order:
                order.data_item.update(data_item)
                order.save()
            else:
                Order.objects.create(data_item=data_item, user=user)
            status = 'Created'
        return JsonResponse({'status': status})
