from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=False)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return str(self.name)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
       return str(self.id)

    @property
    def shipping(self):
        shipping = False
        items = self.orderitem_set.all()
        for item in items:
            print(item)
            if item.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_item_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return str(self.product)

    @property
    def get_item_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200, null=True,blank=True)
    city = models.CharField(max_length=200, null=True,blank=True)
    state = models.CharField(max_length=200, null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.customer


