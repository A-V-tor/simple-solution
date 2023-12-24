from django.db import models
from service.settings import USD_EXCHANGE_RATE, EUR_EXCHANGE_RATE

# Create your models here.


class ConverterMoney:
    """Конвертер валют."""

    dollar_exchange_rate = USD_EXCHANGE_RATE
    euro_exchange_rate = EUR_EXCHANGE_RATE

    @classmethod
    def money_to_usd(cls, currency, price):
        if currency == 'rub':
            return price // USD_EXCHANGE_RATE
        elif currency == 'usd':
            return price
        return float(price) * EUR_EXCHANGE_RATE // USD_EXCHANGE_RATE

    @classmethod
    def money_to_eur(cls, currency, price):
        if currency == 'rub':
            return price // EUR_EXCHANGE_RATE
        elif currency == 'eur':
            return price
        return float(price) * USD_EXCHANGE_RATE // EUR_EXCHANGE_RATE

    @classmethod
    def money_to_rub(cls, currency, price):
        if currency == 'usd':
            rubles = price
            return rubles * USD_EXCHANGE_RATE
        elif currency == 'eur':
            rubles = price
            return rubles * EUR_EXCHANGE_RATE
        else:
            rubles = price
        return rubles


class Item(models.Model):
    converter = ConverterMoney
    CURRENCY_CHOICES = [
        ('rub', 'rub'),
        ('usd', 'usd'),
        ('eur', 'eur'),
    ]
    name = models.CharField(max_length=55, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='цена'
    )
    currency = models.CharField(
        max_length=5, choices=CURRENCY_CHOICES, default='rub'
    )

    class Meta:
        verbose_name = 'продукт/услуга'
        verbose_name_plural = 'продукт/услуга'


class Order(models.Model):
    data_item = models.JSONField()
    is_paid = models.BooleanField(default=False)
    user = models.CharField(max_length=25, verbose_name='юзер')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказ'


class Discount(models.Model):
    DISCOUNT_CHOICES = [
        ('forever', 'forever'),
        ('once', 'once'),
        ('repeating', 'repeating'),
    ]

    percent = models.IntegerField(default=3, verbose_name='% скидки')
    duration = models.CharField(
        max_length=10, choices=DISCOUNT_CHOICES, verbose_name='тип скидки'
    )
    duration_in_month = models.IntegerField(
        default=0, verbose_name='продолжительность в месяцах'
    )

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидка'


class Tax(models.Model):
    COUNTRY_CHOICES = [
        ('BG', 'BG'),
        ('US', 'US'),
        ('RU', 'RU'),
        ('PK', 'PK'),
    ]
    display_name = models.CharField(max_length=100)
    inclusive = models.BooleanField(default=False)
    percentage = models.DecimalField(max_digits=8, decimal_places=4)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налог'
