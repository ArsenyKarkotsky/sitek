from decimal import Decimal
import random
import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import CartItem, News, Product, Cart
import uuid

def generate_cart_id():
    return random.randint(10000000, 99999999)

@require_POST
def cart_add(request):
    cart_id = request.session.get('cart_id')

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    
    # Если корзина существует в базе данных, получаем ее из БД
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        # Если корзина не существует, создаем новую и сохраняем ее идентификатор в Cookies
        cart = Cart.objects.create(cart_id=generate_cart_id())
        request.session['cart_id'] = cart.cart_id
    cart.add_product(product_id, quantity)
    return redirect('cart')

@require_POST
def cart_remove(request):
    cart_id = request.session.get('cart_id')
    product_id = request.POST.get('product_id')
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    return redirect('cart')

def cart_update(request):
    cart_id = request.session.get('cart_id')
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    # Если корзина существует в базе данных, получаем ее из БД
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=generate_cart_id())
        request.session['cart_id'] = cart.cart_id
    # Обновляем количество товара в корзине или удаляем товар из корзины
    try:
        cart_item = CartItem.objects.get(product_id=product_id, cart_id=cart.id)
        cart_item.quantity = quantity
        cart_item.save()    
    except CartItem.DoesNotExist:
        pass
    return request#redirect('cart')


def index(request):
    products = Product.objects.all()[:3]
    news = News.objects.all()[:2]
    return render(request, 'index.html',  {'news': news, 'products': products})

def cart(request):
    cart_id = request.session.get('cart_id')
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=generate_cart_id())
        request.session['cart_id'] = cart.cart_id

    # Если корзина существует, возвращаем ее и список товаров в корзине
    cart_items = cart.cartitem_set.all()
    if cart:
        total = Decimal('0')
        for item in cart.cartitem_set.all():
            total += item.product.price * item.quantity  # общая сумма товаров в корзине
    else:
        total = 0
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total})


def blog(request):
    news = News.objects.all()
    paginator = Paginator(news, 2)  # создаем пагинатор, отображающий 9 товаров на странице
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})

def about_us(request):
    return render(request, 'about-us.html')

def collection(request):
    sort = request.GET.get('sort_by', 'name')  # получаем параметр запроса "sort"
    if sort == 'name':
        products = Product.objects.order_by('name')  # сортировка по имени товара
    elif sort == 'name_desc':
        products = Product.objects.order_by('-name')  # сортировка по имени товара в обратном порядке (от Я до А)
    elif sort == 'price':
        products = Product.objects.order_by('price')  # сортировка по возрастанию цены
    elif sort == 'price_desc':
        products = Product.objects.order_by('-price')  # сортировка по убыванию цены
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)  # создаем пагинатор, отображающий 9 товаров на странице
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'sort': sort}
    return render(request, 'collection.html', context)

def contact_us(request):
    return render(request,'contact_us')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def search(request):
    return render(request, 'search.html')

def single_blog(request):
    slug = request.GET.get('slug')
    news = get_object_or_404(News, slug=slug)
    return render(request, 'single-blog.html', {'news': news})

def single_product(request):
    slug = request.GET.get('slug')
    product = get_object_or_404(Product, slug=slug)
    cart_id = request.session.get('cart_id')
    
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        # Если корзина не существует, создаем новую и сохраняем ее идентификатор в Cookies
        response = HttpResponse(status=200)
        cart = Cart.objects.create(cart_id=generate_cart_id())
        response.set_cookie('cart_id', cart.cart_id)
    return render(request, 'single-product.html', {'products': product, 'cart_id': cart_id})