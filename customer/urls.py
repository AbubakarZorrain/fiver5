from django.urls import path
from . import views
from django.urls import re_path
# app_name = "customers"

urlpatterns = [
    path('', views.home, name='home'),
    path('users/sign_up', views.register, name='sign_up'),
    path('login/', views.login_user, name='login'),
    # path('logout', views.logout_request, name='logout'),
    # # path('customers', views.customers_list, name='customers_list'),
    # path('customers', views.client_list, name='clients_list'),
    # path('customers/new', views.customers_create, name='customers_create'),
    # path('suppliers', views.suppliers_list, name='suppliers_list'),
    # path('suppliers/new', views.suppliers_create, name='suppliers_create'),
    # path('passwords/new', views.password_reset, name='password_reset'),
    # path('client_create/new', views.client_create, name='client_create'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       views.activate, name='activate'),
]
