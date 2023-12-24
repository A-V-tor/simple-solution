import stripe
from service.settings import USD_EXCHANGE_RATE, EUR_EXCHANGE_RATE
from .models import Discount, Tax
import random


class StripeManager:
    dollar_exchange_rate = USD_EXCHANGE_RATE
    euro_exchange_rate = EUR_EXCHANGE_RATE

    def __init__(self, name, description, unit_amount, money):
        self.name = name
        self.description = description
        self.unit_amount = unit_amount
        self.money = money

    def create_product_and_make_price(self):
        """Создание товара и установка цены для него."""
        product = stripe.Product.create(
            name=self.name,
            description=self.description,
            type='good',
        )

        price = stripe.Price.create(
            product=product.id,
            unit_amount=self.unit_amount * 100,
            currency=self.money,
        )

        return price

    @staticmethod
    def get_session_params(line_items, request):
        """Получение параметров для сессии."""
        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': request.build_absolute_uri('/unit/success-order/'),
            'cancel_url': request.build_absolute_uri('/unit/cancel/'),
        }

        return session_params

    @staticmethod
    def get_coupon_discount():
        """Получение скидочного купона."""
        discounts_list = Discount.objects.all()
        if discounts_list:
            discount = random.choice(discounts_list)
            if discount.duration == 'repeating':
                coupon = stripe.Coupon.create(
                    percent_off=discount.percent,
                    duration=discount.duration,
                    duration_in_months=discount.duration_in_month,
                )
            else:
                coupon = stripe.Coupon.create(
                    percent_off=discount.percent,
                    duration=discount.duration,
                )

            return coupon

    @staticmethod
    def get_stripe_session(session_params):
        session = stripe.checkout.Session.create(**session_params)
        return session

    @staticmethod
    def include_tax():
        """Получение налоговой ставки для платежа."""
        tax_list = Tax.objects.all()
        if tax_list:
            tax = random.choice(tax_list)

        tax_rate = stripe.TaxRate.create(
            display_name=tax.display_name,
            inclusive=tax.inclusive,
            percentage=tax.percentage,
            country=tax.country,
        )

        return tax_rate


def transfer_money_to_rubles(money, current_item):
    """Перевод валютных средств в рубли."""
    if money == 'usd':
        rubles = int(current_item) * USD_EXCHANGE_RATE
    elif money == 'eur':
        rubles = int(current_item) * EUR_EXCHANGE_RATE
    else:
        rubles = int(current_item)

    return rubles
