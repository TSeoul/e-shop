from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category
from orders.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    products = Product.objects.all()
    return render(request, 'product_detail.html', {'product': product,'products': products})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'products/category_detail.html', {'category': category})


@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(product=product_id, cart=cart)
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
