from django.urls import path
from cart.views import AddToCartView,AddToWishView

urlpatterns = [
    path('addtocart/',AddToCartView.as_view(),name='cartview'),
    path('addtowishlist/',AddToWishView.as_view(),name='Wishlist')

]
