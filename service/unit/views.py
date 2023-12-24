from django.shortcuts import redirect
from django.views.generic import DetailView, View
from django.http import HttpResponse
from .models import Item, Order
import stripe
from .utils import transfer_money_to_rubles, StripeManager


class OrderView(View):
    def get(self, request, *args, **kwargs):
        user = request.META.get('HTTP_X_FORWARDED_FOR', None)
        query_ = Order.objects.filter(user=user, is_paid=False)
        msg = 'Нет товаров в заказе'

        if query_:
            tax_rate = StripeManager.include_tax()

            # список товаров для оплаты
            line_items = []

            for current_item in query_[0].data_item.values():
                money = current_item['currency']
                change_money = transfer_money_to_rubles(
                    money, current_item['price']
                )
                stripe_manager = StripeManager(
                    current_item['name'],
                    current_item['description'],
                    change_money,
                    'rub',
                )
                price = stripe_manager.create_product_and_make_price()
                line_item = {
                    'price': price.id,
                    'quantity': int(current_item['quantity']),
                    'tax_rates': [tax_rate.id],
                }

                line_items.append(line_item)

            session_params = StripeManager.get_session_params(
                line_items, request
            )
            coupon = StripeManager.get_coupon_discount()
            if coupon:
                session_params['discounts'] = [{'coupon': coupon.id}]

            session = stripe.checkout.Session.create(**session_params)
            return redirect(session.url)

        return HttpResponse(msg, content_type='text/html; charset=utf-8')


class DetailItemView(DetailView):
    """Отображение товара."""

    template_name = 'unit/index.html'
    model = Item
    extra_context = {'title': 'Товар'}

    def get(self, request, *args, **kwargs):
        user = request.META.get('HTTP_X_FORWARDED_FOR', None)
        self.object: Item = self.get_object()
        currency = self.object.currency
        price = self.object.price
        usd_price = self.object.converter.money_to_usd(currency, price)
        eur_price = self.object.converter.money_to_eur(currency, price)
        rub_price = self.object.converter.money_to_rub(currency, price)
        context = self.get_context_data(
            object=self.object,
            user=user,
            usd_price=usd_price,
            eur_price=eur_price,
            rub_price=rub_price,
        )

        return self.render_to_response(context)


class SuccessOrderView(View):
    """Callback для успешного платежа - заказа."""

    def get(self, request, *args, **kwargs):
        try:
            user = request.META.get('HTTP_X_FORWARDED_FOR', None)
            query_ = Order.objects.filter(user=user, is_paid=False)
            query_.update(is_paid=True)
            return HttpResponse(
                'Платеж успешно выполнен!</br>Отправьте ваши впечатления на <a href="mailto:avtorca4@gmail.com">avtorca4@gmail.com</a>',
                content_type='text/html; charset=utf-8',
            )
        except Exception:
            return HttpResponse(
                'Что - то пошло не так и все сломалось...',
                content_type='text/html; charset=utf-8',
            )


class SuccessView(View):
    """Callback для успешного платежа."""

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            'Платеж успешно выполнен!</br>Отправьте ваши впечатления на <a href="mailto:avtorca4@gmail.com">avtorca4@gmail.com</a>',
            content_type='text/html; charset=utf-8',
        )


class CancelView(View):
    """Callback для платежа с ошибкой."""

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            'Платеж  был отменен!</br>Напишите по адрессу <a href="mailto:avtorca4@gmail.com">avtorca4@gmail.com</a>',
            content_type='text/html; charset=utf-8',
        )
