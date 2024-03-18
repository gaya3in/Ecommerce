"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.store_view, name="home"),
    path('cart/', views.cart_view, name="cart"),
    path('checkout/', views.checkout_view, name="checkout"),
    path('update_order/', views.updateorder, name="update_order"),
    path('process_order/', views.processorder, name="process_order"),
    path('complete_order/', views.completeorder, name="complete_order"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
