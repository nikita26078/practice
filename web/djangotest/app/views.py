from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_addanother.views import CreatePopupMixin

from .forms import UserRegistrationForm, LoginForm, ShippingForm, EmployeeForm, FinanceReviewForm, AdCampaignForm, \
    ItemForm
from .models import Item, ShipRequest, Employee, AdCampaign, FinanceReview, OrderQuantity, Order


def index(request):
    return render(request, 'app/index.html')


def home(request):
    return render(request, 'app/home.html')


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')


def shipping(request):
    return render(request, 'app/shipping/main.html')


def staff(request):
    return render(request, 'app/staff/main.html')


def sales(request):
    return render(request, 'app/sales/main.html')


def finances(request):
    return render(request, 'app/finances/main.html')


def log_out(request):
    logout(request)
    return render(request, 'app/index.html')


def shipping_delete_ship(request, id):
    obj = ShipRequest.objects.get(id=id)
    obj.delete()
    mydictionary = {
        "object_list": ShipRequest.objects.all()
    }
    return redirect("/shipping/list_shipping", context=mydictionary)


def shipping_delete_order(request, id):
    obj = Order.objects.get(id=id)
    obj.delete()
    mydictionary = {
        "object_list": Order.objects.all()
    }
    return redirect("/shipping/list_orders", context=mydictionary)


def profile(request):
    if request.user.is_anonymous:
        return user_login(request)
    else:
        data = {
            'profile': request.user.employee.user,
        }
        return render(request, 'app/profile.html', data)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            employee = new_user.employee
            employee.patronym = user_form.cleaned_data['patronym']
            employee.save()
            return render(request, 'app/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'app/register.html', {'user_form': user_form, 'employee_form': EmployeeForm()})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'app/login_done.html', {'new_user': user})
                else:
                    return render(request, 'app/login_failed.html', {'text': 'Аккаунт отключен'})
            else:
                return render(request, 'app/login_failed.html', {'text': 'Неверные данные'})
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


def search(request):
    q = request.GET['query']
    mydictionary = {
        "object_list": Item.objects.filter(name__contains=q)
    }
    return render(request, "app/home.html", context=mydictionary)


def staff_delete(request, id):
    obj = Employee.objects.get(user_id=id)
    obj.delete()
    mydictionary = {
        "object_list": Employee.objects.all()
    }
    return redirect("/staff/list", context=mydictionary)


def staff_edit(request, id):
    error = ''
    obj = Employee.objects.get(user_id=id)

    form = EmployeeForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            mydictionary = {
                "object_list": Employee.objects.all()
            }
            return redirect("/staff/list", context=mydictionary)
        else:
            print(form.errors)
            error = 'Ошибка валидации'
    data = {
        'form': form,
        'error': error
    }
    return render(request, "app/staff/edit.html", data)


def sales_delete(request, id):
    obj = AdCampaign.objects.get(user_id=id)
    obj.delete()
    mydictionary = {
        "object_list": AdCampaign.objects.all()
    }
    return redirect("/sales/list", context=mydictionary)


class QuantityCreateView(CreatePopupMixin, CreateView):
    model = OrderQuantity
    template_name = 'app/shipping/quantity.html'
    fields = ['product', 'quantity']


class ShipRequestCreateView(CreateView):
    template_name = 'app/shipping/request.html'
    form_class = ShippingForm
    success_url = reverse_lazy('shipping')


class OrderListView(ListView):
    model = Order
    template_name = 'app/shipping/list_orders.html'


class ShipRequestListView(ListView):
    model = ShipRequest
    template_name = 'app/shipping/list_shipping.html'


class ItemCreateView(CreateView):
    template_name = 'app/shipping/item.html'
    form_class = ItemForm
    success_url = reverse_lazy('shipping')


class ItemListView(ListView):
    model = Item
    template_name = 'app/shipping/list_items.html'


class StaffListView(ListView):
    model = Employee
    template_name = 'app/staff/list.html'


class CampaignListView(ListView):
    model = AdCampaign
    template_name = 'app/sales/list.html'


class CampaignCreateView(CreateView):
    template_name = 'app/sales/campaign.html'
    form_class = AdCampaignForm
    success_url = reverse_lazy('sales')


class ReviewsListView(ListView):
    model = FinanceReview
    template_name = 'app/finances/list.html'


class FinancesCreateView(CreateView):
    template_name = 'app/finances/review.html'
    form_class = FinanceReviewForm
    success_url = reverse_lazy('finances')
