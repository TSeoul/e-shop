from .forms import OrderForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import Cart, Order, CartItem
from .forms import OrderForm

@login_required
def checkout(request):
    user_cart = Cart.objects.get(user=request.user)
    if not user_cart.items.exists():
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            postal_code = form.cleaned_data['postal_code']
            payment_option = form.cleaned_data['payment_option']
            order = Order.objects.create(user=request.user, last_name=last_name, first_name=first_name, email=email, address=address, city=city, state=state,
                                         postal_code=postal_code, payment_option=payment_option)
            order.add_to_order(user_cart)
            return redirect('thank_you')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})




def thank_you(request):
    return render(request, 'thank_you.html')

@login_required
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    items = cart.items.all()
    total = cart.get_total_cost()
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity',1)
        product = Product.objects.get(id=product_id)
        if int(quantity) > product.quantity:
            return redirect('product_detail', product_id)
        else:
            product.quantity -= int(quantity)
            product.save()
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            else:
                cart_item.quantity = int(quantity)
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

def order_view(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process the form data, such as saving it to the database
            # or sending an email
            pass
    return render(request, 'order.html', {'form': form})



def update_cart_item(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(product=product_id, cart=cart)
        """cart_item = CartItem.objects.get(product=product_id)
        if int(quantity) < 0:
            return redirect('cart')
        elif int(quantity) > cart_item.product.quantity:
            return redirect('cart')
        else:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return redirect('cart')"""
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')




