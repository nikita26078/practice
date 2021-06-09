from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django_addanother.views import CreatePopupMixin

from .forms import UserRegistrationForm, LoginForm, ShippingForm, EmployeeForm, FinanceReviewForm, AdCampaignForm
from .models import Item, ShipRequest, Employee, AdCampaign, FinanceReview, OrderQuantity, Order


def index(request):
    if request.user.is_anonymous:
        return render(request, 'app/index.html')
    else:
        return render(request, 'app/home.html')


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


def shipping_request(request):
    error = ''
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/shipping')
        else:
            print(form.errors)
            error = 'Ошибка валидации'
    form = ShippingForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'app/shipping/request.html', data)


def shipping_delete(request, id):
    obj = ShipRequest.objects.get(id=id)
    obj.delete()
    mydictionary = {
        "object_list": ShipRequest.objects.all()
    }
    return redirect("/shipping/list", context=mydictionary)


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
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неверные данные')
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


def sales_campaign(request):
    error = ''
    if request.method == 'POST':
        form = AdCampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/sales')
        else:
            print(form.errors)
            error = 'Ошибка валидации'
    form = AdCampaignForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'app/sales/campaign.html', data)


def finances_review(request):
    error = ''
    if request.method == 'POST':
        form = FinanceReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/finances')
        else:
            print(form.errors)
            error = 'Ошибка валидации'
    form = FinanceReviewForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'app/finances/review.html', data)


class QuantityCreateView(CreatePopupMixin, CreateView):
    model = OrderQuantity
    template_name = 'app/shipping/quantity.html'
    fields = ['product', 'quantity']


class OrderListView(ListView):
    model = Order
    template_name = 'app/shipping/list_orders.html'


class ShipRequestListView(ListView):
    model = ShipRequest
    template_name = 'app/shipping/list_shipping.html'


class StaffListView(ListView):
    model = Employee
    template_name = 'app/staff/list.html'


class CampaignListView(ListView):
    model = AdCampaign
    template_name = 'app/sales/list.html'


class ReviewsListView(ListView):
    model = FinanceReview
    template_name = 'app/finances/list.html'

# class NewsListView(ListView):
#     model = News
#     paginate_by = 12
#     template_name = 'app/home.html'
#     context_object_name = 'app'
#     queryset = News.objects.order_by('-date')
#
#
# class CategoryListView(ListView):
#     model = Category
#     template_name = 'app/categories.html'
#
#
# class CategoryNewsListView(ListView):
#     model = News
#     template_name = 'app/home.html'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, id=self.kwargs['category_name'])
#         return News.objects.filter(category=self.category)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = self.category
#         return context
#
#
# def create(request):
#     error = ''
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             print(form.errors)
#             error = 'Ошибка валидации'
#     form = NewsForm()
#     data = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'app/news_add.html', data)

