from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comments(models.Model):
    username = models.CharField(max_length=30, verbose_name="Имя пользователя")
    text = models.CharField(max_length=50, verbose_name="Текст")


class Product(models.Model):
    """Модель продукта"""

    class Meta:
        abstract = True

    title = models.CharField(max_length=30, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Стоимость")
    photo = models.ImageField(upload_to="product-photos/", verbose_name="Картинка")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата опубликования")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE, verbose_name="Коментарии", null=True)

    def get_absolute_url(self):
        return reverse(viewname="product_detail", kwargs={
            "ct_model": self.__class__.__name__.lower(),
            "pk": self.pk
        })

    def get_ct_model(self):
        return f"{self.__class__.__name__}".lower()


class Watches(Product):
    SMALL_SIZE = 30
    MIDDLE_SIZE = 35
    BIG_SIZE = 40

    QUARTZ_EDITION = "QE"
    AUTOMATIC_EDITION = "AE"

    SIZE_CHOICES = [
        (SMALL_SIZE, 30),
        (MIDDLE_SIZE, 35),
        (BIG_SIZE, 40)
    ]

    WATCH_TYPE_CHOICES = [
        (QUARTZ_EDITION, "Кварцевые изделия"),
        (AUTOMATIC_EDITION, "Автоматические изделия")
    ]

    size = models.PositiveSmallIntegerField(verbose_name="Размер",
                                            choices=SIZE_CHOICES, default=SMALL_SIZE)
    color = models.CharField(max_length=30, verbose_name="Цвет")
    watch_type = models.CharField(max_length=30, verbose_name="Тип",
                                  choices=WATCH_TYPE_CHOICES, default=QUARTZ_EDITION)
    details = models.TextField(verbose_name="Подробности")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Часы"
        verbose_name_plural = "Часы"
        ordering = ["id"]


class Chains(Product):
    SMALL_LENGTH = 30
    MIDDLE_LENGTH = 50
    BIG_LENGTH = 70

    SILVER_TYPE_METAL = "silver"
    GOLD_TYPE_METAL = "gold"

    LENGTH_CHOICES = [
        (SMALL_LENGTH, 30),
        (MIDDLE_LENGTH, 50),
        (BIG_LENGTH, 70)
    ]

    TYPE_METAL_CHOICES = [
        (SILVER_TYPE_METAL, "Серебро"),
        (GOLD_TYPE_METAL, "Золото")
    ]

    length = models.PositiveSmallIntegerField(verbose_name="Длина", choices=LENGTH_CHOICES, default=SMALL_LENGTH)
    weight = models.PositiveSmallIntegerField(verbose_name="Вес")
    type_metal = models.CharField(max_length=30, verbose_name="Тип металла",
                                  choices=TYPE_METAL_CHOICES, default=SILVER_TYPE_METAL)
    assay = models.PositiveSmallIntegerField(verbose_name="Проба металла")
    country = models.CharField(max_length=30, verbose_name="Страна")
    details = models.TextField(verbose_name="Подробности")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цепочка"
        verbose_name_plural = "Цепочки"
        ordering = ["id"]


class Customers(User):
    CURRENCY_SUM = "UZS"
    CURRENCY_DOLLAR = "USD"
    CURRENCY_RUBLE = "RUB"

    CURRENCY_CHOICES = [
        (CURRENCY_SUM, "Узбекский сум"),
        (CURRENCY_DOLLAR, "Американский доллар"),
        (CURRENCY_RUBLE, "Российский рубль"),
    ]

    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="customer_avatars", verbose_name="Аватар пользователя", null=True)
    currency = models.CharField(max_length=255, verbose_name="Валюта", choices=CURRENCY_CHOICES,
                                default=CURRENCY_SUM)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Cart(models.Model):
    owner = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Владелец")
    products = models.ManyToManyField("CartProduct", related_name="related_cart")
    total_products = models.PositiveSmallIntegerField(verbose_name="Общее кол-во товаров", default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая стоимость корзины",
                                      default=0)
    in_order = models.BooleanField(default=False, verbose_name="Статус корзины")

    def __str__(self):
        return f"Корзина № {self.pk} - {self.owner.username} - В заказе: {self.in_order}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["pk"]


class CartProduct(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Покупатель")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id - ID продукта
    object_id = models.PositiveSmallIntegerField()
    # content_object - поле, которое будет иметь связь с Watches/Chains/Rings
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    quantity = models.PositiveSmallIntegerField(verbose_name="Кол-во продуктов", default=1)
    final_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая стоимость продуктов",
                                      default=0)


class Orders(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_READY = "is_ready"
    STATUS_COMPLETE = "complete"
    STATUS_DENIED = "denied"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новый заказ"),
        (STATUS_IN_PROGRESS, "Заказ в обработке"),
        (STATUS_READY, "Заказ готов"),
        (STATUS_COMPLETE, "Заказ выполнен"),
        (STATUS_DENIED, "Заказ отклонен")
    ]

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Покупатель",
                                 related_name="related_orders")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    order_status = models.CharField(max_length=255, verbose_name="Статус заказа", choices=STATUS_CHOICES,
                                    default=STATUS_NEW)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    time_create = models.DateTimeField(verbose_name="Дата создания заказа", auto_now=True)
    time_order = models.DateField(verbose_name="Дата получения заказа", null=True)
