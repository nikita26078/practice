from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('shipping', views.shipping, name='shipping'),
    path('shipping/list_shipping', ShipRequestListView.as_view(), name='shipping_list_ship'),
    path('shipping/list_orders', OrderListView.as_view(), name='shipping_list_order'),
    path('shipping/list_items', ItemListView.as_view(), name='shipping_list_items'),
    path('shipping/request', ShipRequestCreateView.as_view(), name='shipping_request'),
    path('shipping/delete_shipping/<int:id>', views.shipping_delete_ship, name='shipping_delete'),
    path('shipping/delete_order/<int:id>', views.shipping_delete_order, name='shipping_delete'),
    path('shipping/quantity', QuantityCreateView.as_view(), name='shipping_quantity'),
    path('shipping/item', ItemCreateView.as_view(), name='shipping_item'),
    path('staff', views.staff, name='staff'),
    path('staff/list', StaffListView.as_view(), name='staff_list'),
    path('staff/delete/<int:id>', views.staff_delete, name='staff_delete'),
    path('staff/edit/<int:id>', views.staff_edit, name='staff_edit'),
    path('sales', views.sales, name='sales'),
    path('sales/list', CampaignListView.as_view(), name='sales_list'),
    path('sales/campaign', CampaignCreateView.as_view(), name='sales_campaign'),
    path('sales/delete/<int:id>', views.sales_delete, name='sales_delete'),
    path('finances', views.finances, name='finances'),
    path('finances/list', ReviewsListView.as_view(), name='finances_list'),
    path('finances/review', FinancesCreateView.as_view(), name='finances_review'),
    path('logout', views.log_out, name='logout'),
]
