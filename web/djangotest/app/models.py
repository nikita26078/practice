from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField('Имя', max_length=255)
    price = models.IntegerField('Стоимость')
    desc = models.TextField('Описание')
    category = models.CharField('Категория', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField('Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class OrderQuantity(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество')

    def __str__(self):
        return str(self.quantity) + 'x ' + self.product.name

    class Meta:
        verbose_name = "Количество товара"
        verbose_name_plural = "Количество товара"


class Order(models.Model):
    items = models.ManyToManyField(OrderQuantity, verbose_name='Товары')
    store = models.ForeignKey(Store, related_name='store', on_delete=models.SET_NULL,
                                default=None, null=True, blank=True, verbose_name='Магазин')
    status = models.CharField('Статус', max_length=255)

    def __str__(self):
        return 'Заказ ' + str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Shipper(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class FinanceReview(models.Model):
    title = models.CharField('Название', max_length=255)
    plots = models.ImageField('Графики', upload_to='images/')
    desc = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Финансовый отчет"
        verbose_name_plural = "Финансовые отчеты"


class AdCampaign(models.Model):
    title = models.CharField('Название', max_length=255)
    plots = models.ImageField('Графики', upload_to='images/')
    desc = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"


class ShipRequest(models.Model):
    title = models.CharField('Название', max_length=255)
    shipper = models.ForeignKey(Shipper, related_name='shipper', on_delete=models.SET_NULL,
                                default=None, null=True, blank=True, verbose_name='Поставщик')
    desc = models.TextField('Описание')
    items = models.ManyToManyField(OrderQuantity, verbose_name='Товары')
    status = models.CharField('Статус', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заявка на поставку"
        verbose_name_plural = "Заявки на поставку"


class Post(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronym = models.CharField('Отчество', max_length=255)
    post = models.ForeignKey(Post, related_name='post', on_delete=models.SET_NULL,
                             default=None, null=True, blank=True, verbose_name='Должность')
    phone = models.CharField('Телефон', max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Employee.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.employee.save()
        except ObjectDoesNotExist:
            Employee.objects.create(user=instance)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
