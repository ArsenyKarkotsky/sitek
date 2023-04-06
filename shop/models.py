import json
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Заголовок',
        unique=True,
        blank=False,
        null=False
    )
    description = models.CharField(
        max_length=256,
        verbose_name='Текст',
        unique=True,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique= True,
        blank=False,
        null=False
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='loading/',
        null=True,
        blank=True
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Product(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='название'
    )
    descr = models.CharField(
        max_length=4096,
        verbose_name='описание',
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='цена',
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='products/',
        null=True,
        blank=True
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

class Cart(models.Model):
    cart_id = models.CharField(verbose_name='id',max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='created',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated',auto_now=True)
    products = models.ManyToManyField(Product, verbose_name='products',through='CartItem')

    def add_product(self, product_id, quantity):
        try:
            # Попытка получить товар из базы данных по id
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # Если товара с таким id не существует, то выбрасываем ошибку
            raise ValueError('Invalid product ID')
        # Попытка получить товар в корзине по id товара и id корзины
        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart_id=self.id)
            # Если товар уже есть в корзине, обновляем его количество
            cart_item.quantity += int(quantity)
            cart_item.save()
        except CartItem.DoesNotExist:
            # Если товара в корзине нет, создаем новую запись
            cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=self)


    def __str__(self):
        return self.cart_id
    
    class Meta:
        verbose_name = 'карзина'
        verbose_name_plural = 'карзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cart.cart_id} - {self.product.name}'
    
    class Meta:
        verbose_name = 'элемент карзины'
        verbose_name_plural = 'элементы карзин'