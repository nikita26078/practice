from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import FinanceReview, ShipRequest, Item, Store, Order, Shipper, Employee, Post, OrderQuantity


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


admin.site.register(Item)
admin.site.register(Store)
admin.site.register(OrderQuantity)
admin.site.register(Order)
admin.site.register(Shipper)
admin.site.register(FinanceReview)
admin.site.register(ShipRequest)
admin.site.register(Post)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
