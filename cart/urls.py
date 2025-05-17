from django.urls import path
from cart.views import CartView

urlpatterns = [
    path('cartview/',CartView.as_view(),name='cartview')
]
