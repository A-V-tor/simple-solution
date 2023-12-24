from django.views.generic import View
from django.http import HttpResponse


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        content = """
            <h2>Карта ссылок</h2>
            <div>
                <a href='unit/item/1/'><b> unit/item/1/ </b></a> </br>
                Cтраница товаров/услуг - кнопка "В заказ" добавляет товар в модель заказа в нужной валюте и с нужным кол-вом
                <hr>
                <a href='unit/order/'><b> unit/order/ </b></a> </br>
                Страница оформления товаров из модели заказа. Перед формированием платежа вся валюта конвертируеться в рубли
                Для идентификации берется ip
                <hr>
                Во время оформления модели заказа из существующих записей моделей Tax и Discount, рандомно выбираеться для текущего платежа. </br>
                Stripe Payment Intent - не стал исполнять так как не совсем понял в каком контексте применять, если это важно или есть какие то дополнения, 
                напишите на <a href="mailto:avtorca4@gmail.com">мою почту</a>
            </div>
        """
        return HttpResponse(content, content_type='text/html; charset=utf-8')
