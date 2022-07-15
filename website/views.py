from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from .forms import RegisterForm, LoginForm
from .utils import getCookieData, getCartData, getShippingData
import json
import datetime

# Create your views here.
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
       form = RegisterForm(request.POST)
       if form.is_valid():
            instance = form.save()
            username = form.cleaned_data.get('username')
            email= form.cleaned_data.get('email')

            customer, created = Customer.objects.get_or_create(user=instance)
            customer.name = username
            customer.email = email
            customer.save()

           # messages.success(request, "Account has been creeated for user " + user)
            return redirect('login')

    context ={'form': form}
    return render(request,"register.html", context)

def login_view(request):

    form = LoginForm()
    if request.method =="POST":
        form = LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Authentication Failed!")

    context = {'form': form}
    return render(request,"login.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')

def store_view(request):
    data = getCartData(request, "store_view")
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request,"store.html", context)

def cart_view(request):
    data = getCartData(request,"cart_view")
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    if cartItems <= 0:
        messages.info(request, "Cart is Empty...")
        return redirect('home')

    context = {'items' : items, 'order' : order, 'cartItems': cartItems}
    return render(request,"cart.html", context)

def checkout_view(request):
    data = getCartData(request,"checkout_view")
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request,"checkout.html",context)

def updateorder(request):
        data = json.loads(request.body)
        print(data)
        productId = data['productId']
        action = data['action']
        print("ProductID:" , productId)
        print("Action:" , action)

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == "add":
            orderitem.quantity += 1
        else:
            orderitem.quantity -= 1

        orderitem.save()

        if orderitem.quantity <=0:
            orderitem.delete()

        return JsonResponse("Item is added", safe=False)

def processorder(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        name = data['orderInfo']['name']
        email = data['orderInfo']['email']
        cookieData = getCartData(request,"processorder")

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        items =cookieData['items']
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        for item in items:
            orderItem = OrderItem.objects.create(order=order)
            print("orderitem created")
            orderItem.product = Product.objects.get(id=item['product']['id'])
            orderItem.quantity = item['quantity']
            orderItem.save()

    transaction_id = datetime.datetime.now().timestamp()
    total = data['orderInfo']['total']

    if total == order.get_cart_total:
        order.complete = True
        order.transaction_id = transaction_id
    order.save()

    if order.shipping == True:
        shippingaddress, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        shippingaddress.address = data['shipping']['address']
        shippingaddress.city = data['shipping']['city']
        shippingaddress.state = data['shipping']['state']
        shippingaddress.zipcode = data['shipping']['zipcode']
        shippingaddress.save()
    return JsonResponse("Payment complete!", safe=False)