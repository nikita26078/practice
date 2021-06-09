from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    desc = models.TextField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OrderQuantity(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество')

    def __str__(self):
        return str(self.quantity) + 'x ' + self.product.name

    class Meta:
        verbose_name_plural = "Order quantities"


class Order(models.Model):
    items = models.ManyToManyField(OrderQuantity)
    store = models.ForeignKey(Store, related_name='store', on_delete=models.SET_NULL,
                                default=None, null=True, blank=True, verbose_name='Магазин')
    status = models.CharField(max_length=255)

    def __str__(self):
        return 'Заказ ' + str(self.id)


class Shipper(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FinanceReview(models.Model):
    title = models.CharField('Название', max_length=255)
    plots = models.ImageField('Графики', upload_to='images/')
    desc = models.TextField('Описание')

    def __str__(self):
        return self.title


class AdCampaign(models.Model):
    title = models.CharField('Название', max_length=255)
    plots = models.ImageField('Графики', upload_to='images/')
    desc = models.TextField('Описание')


class ShipRequest(models.Model):
    title = models.CharField('Название', max_length=255)
    shipper = models.ForeignKey(Shipper, related_name='shipper', on_delete=models.SET_NULL,
                                default=None, null=True, blank=True, verbose_name='Поставщик')
    desc = models.TextField('Описание')
    items = models.ManyToManyField(OrderQuantity, verbose_name='Товары')
    status = models.CharField('Статус', max_length=255)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField('Отчество', max_length=255)
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

# class News(models.Model):
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     date = models.DateTimeField()
#     desc = models.TextField()
#     image = models.ImageField(upload_to='images/')
#     category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL,
#                                  default=None, null=True, blank=True)
#     user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title  # Иначе при обращение к title будет объект
#
#     class Meta:
#         verbose_name_plural = "News"
