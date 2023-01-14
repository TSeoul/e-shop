from django.urls import path
from . import views
from .views import update_cart_item

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('cart/', views.cart, name='cart'),
    path('update_cart_item/<int:product_id>/', views.update_cart_item, name='update_cart_item'),

]
