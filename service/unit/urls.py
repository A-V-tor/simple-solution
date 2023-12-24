from django.urls import path

from unit.views import (
    DetailItemView,
    SuccessView,
    CancelView,
    OrderView,
    SuccessOrderView,
)
from unit.api.routes import SessionStripeAPIView, InOrderAPIView


urlpatterns = [
    path('item/<int:pk>/', DetailItemView.as_view(), name='item'),
    path('buy/<int:pk>/', SessionStripeAPIView.as_view(), name='buy'),
    path('to-order/', InOrderAPIView.as_view(), name='to-order'),
    path('order/', OrderView.as_view(), name='order'),
    path('success/', SuccessView.as_view(), name='success'),
    path('success-order/', SuccessOrderView.as_view(), name='success-order'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
