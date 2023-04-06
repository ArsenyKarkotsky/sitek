from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('index.html', index, name='index'),
    path('cart.html', cart, name='cart'),
    path('blog.html', blog, name='blog'),
    path('about-us.html', about_us, name='about_us'),
    path('collection.html', collection, name='collection'),
    path('contact-us.html', contact_us, name='contact_us'),
    path('login.html', login, name='login'),
    path('register.html', register, name='register'),
    path('search.html', search, name='search'),
    path('single-blog.html', single_blog, name='single_blog'),
    path('single-product.html', single_product, name='single_product'),
    path('add_card', cart_add, name='cart_add'),
    path('cart_update/', cart_update, name='cart_update'),
    path('cart_remove/', cart_remove, name='cart_remove'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)