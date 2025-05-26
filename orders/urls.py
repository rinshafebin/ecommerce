from django.urls import path
from .views import OrderListCreate

urlpatterns = [
    path('', OrderListCreate.as_view(), name='orders'),
]
