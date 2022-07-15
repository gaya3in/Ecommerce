from website.models import *
from django.core.exceptions import ObjectDoesNotExist
import json

def getCookieData(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print(cart)
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']
    items = []
    for i in cart:
        try:
            product = Product.objects.get(id=i)
        except:
            continue

        cartItems += cart[i]['quantity']
        total = (cart[i]['quantity'] * product.price)
        order['get_cart_total'] += total
        order['get_cart_items'] = cartItems

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL
            },
            'quantity': cart[i]['quantity'],
            'get_item_total': total
        }
        items.append(item)
        order['shipping'] = getShippingData(items)

    return {'items': items, 'order': order, 'cartItems': cartItems}

def getCartData(request, viewname):
    if request.user.is_authenticated:
        customer = request.user.customer
        if viewname == "store_view":
            try:
                order = Order.objects.get(customer=customer, complete=False)
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items
            except ObjectDoesNotExist:
                order = []
                items = []
                cartItems = 0
        else:
             order, created = Order.objects.get_or_create(customer=customer, complete=False)
             items = order.orderitem_set.all()
             cartItems = order.get_cart_items
    else:
        data = getCookieData(request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']

    return {'items': items, 'order': order, 'cartItems': cartItems}

def getShippingData(items):
    shipping = False
    for item in items:
            product = Product.objects.get(id=item['product']['id'])
            if product.digital == False:
                shipping = True
                break
    return shipping
