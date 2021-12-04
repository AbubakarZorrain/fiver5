from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import  Template
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django_email_verification import sendConfirm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from .models import *

# Create your views here.


# For Index page with View
from customer.forms import *
from .utilities import *

def home(request):
    # user = User.objects.create_user('ali@ali.com', 'johnpassword')
    # user.is_staff = True
    # user.save()
    #company = get_company(request)
    # if company is None:
    #     return HttpResponseRedirect(reverse('customers:login'))
    return render(request, "customer/index.html")


def register(request):
    #current_company = get_company(request)
    form = CustomersForm()
    if request.method == "POST":
        form = CustomersForm(request.POST)
        # full_name = request.POST.get("full_name")
        # email1 = request.POST.get("email")
        # mobile_number = request.POST.get("mobile_number")
        # password = request.POST.get("password")
        #
        # Customer.objects.create(user=full_name,email = email1, phone = mobile_number,password = password)
        # user = Customer.objects.get(user = full_name)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('customer/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
            mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = CustomersForm()
    print(request.user)
    return render(request, 'customer/register.html', {'form': form})




def login_user(request):
    # user = User.objects.get(
    #     email='super@super.com',
    # )
    #User.objects.create_user( email='a@a.com', password='abc123456789')
    #company = get_company(request)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # if company is not None:
            #     request.session['company_id'] = company.id
            # # return redirect('customers/index.html')
            return HttpResponseRedirect(reverse('customers:home'))
    return render(request, "customer/login.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# def password_reset(request):
#     company = get_company(request)
#     if company is None:
#         return redirect("/login")
#     if request.method == "POST":
#         user_id = request.POST.get("user_id")
#         password = request.POST.get("password")
#         user = User.objects.get(id=user_id, company=company)
#         if user is not None and password is not None:
#             user.password = password
#             user.save()
#             return redirect("/login")
#     user = User.objects.get(company=company, email=request.GET.get("email").replace(' ', '+'))
#     return render(request, "password.html", {'user': user.id})
#
#
# @login_required
# def logout_request(request):
#     logout(request)
#     request.session.flush()
#     return redirect("/login")
#
#
# # @login_required
# # def customers_list(request):
# #     company = get_company(request)
# #     if company is None:
# #         return redirect("/login")
# #     customers = Customer.objects.filter(company=company)
# #     return render(request, 'customers/index.html', {'customers': customers})
#
# @login_required
# def client_list(request):
#     clients = None
#     type = request.GET.get('type', None)
#     if type:
#         clients = Client.objects.filter(customer_type=type)
#     else:
#         clients = Client.objects.all()
#     return render(request, 'customers/index.html', {'customers': clients})
#
#
# @login_required
# def suppliers_list(request):
#     company = get_company(request)
#     if company is None:
#         return redirect("/login")
#     suppliers = Supplier.objects.filter(company=company)
#     return render(request, 'suppliers/index.html', {'suppliers': suppliers})
#
#
# @login_required
# def customers_create(request):
#     company = get_company(request)
#     if company is None:
#         return redirect("/login")
#     if request.method == "POST":
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/customers')
#             except:
#                 pass
#     else:
#         form = CustomerForm()
#     return render(request, 'customers/new.html', {'form': form, 'company': company.id})
#
#
# @login_required
# def suppliers_create(request):
#     company = get_company(request)
#     if company is None:
#         return redirect("/login")
#     if request.method == "POST":
#         form = SupplierForm(request.POST)
#         print(form.is_valid())
#         print(form.errors)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/suppliers')
#             except:
#                 pass
#     else:
#         form = SupplierForm()
#     return render(request, 'suppliers/new.html', {'form': form, 'company': company.id})
#
#
#
# @login_required
# def client_create(request):
#     if request.method == "POST":
#         print(request.POST)
#         customer_type = request.POST.get('customer_type', None)
#         entity = request.POST.get('entity', None)
#         company_name = request.POST.get('company_name', None)
#         trading_name = request.POST.get('trading_name', None)
#         work_email = request.POST.get('work_email', None)
#         landline_number = request.POST.get('landline_number', None)
#         mobile_number = request.POST.get('mobile_number', None)
#         note_field = request.POST.get('note_field', None)
#         financial_year_end = request.POST.get('financial_year_end', None)
#         registration_number = request.POST.get('registration_number', None)
#         registration_date = request.POST.get('registration_date', None)
#         income_tax = request.POST.get('income_tax', None)
#         vat_number = request.POST.get('vat_number', None)
#         vat_month = request.POST.get('vat_month', None)
#         payee_number = request.POST.get('payee_number', None)
#         uif_number = request.POST.get('uif_number', None)
#         coida_number = request.POST.get('coida_number', None)
#         efiling_profile = request.POST.get('efiling_profile', None)
#         last_financials = request.POST.get('last_financials', None)
#         billing_address = request.POST.get('billing_address', None)
#         billing_city = request.POST.get('billing_city', None)
#         billing_state = request.POST.get('billing_state', None)
#         billing_zip = request.POST.get('billing_zip', None)
#         billing_country = request.POST.get('billing_country', None)
#         address = request.POST.get('address', None)
#         address_city = request.POST.get('address_city', None)
#         address_state = request.POST.get('address_state', None)
#         address_zip = request.POST.get('address_zip', None)
#         address_country = request.POST.get('address_country', None)
#
#
#         client = Client.objects.create(
#             customer_type = customer_type,
#             entity = entity,
#             company_name = company_name,
#             trading_name = trading_name,
#             work_email = work_email,
#             landline_number = landline_number,
#             mobile_number = mobile_number,
#             note_field = note_field,
#             financial_year_end = financial_year_end,
#             registration_number = registration_number,
#             registration_date = registration_date,
#             income_tax = income_tax,
#             vat_number = vat_number,
#             vat_month = vat_month,
#             payee_number = payee_number,
#             uif_number = uif_number,
#             coida_number = coida_number,
#             efiling_profile = efiling_profile,
#             last_financials = last_financials,
#             billing_address = billing_address,
#             billing_city = billing_city,
#             billing_state = billing_state,
#             billing_zip = billing_zip,
#             billing_country = billing_country,
#             address = address,
#             address_city = address_city,
#             address_state = address_state,
#             address_zip = address_zip,
#             address_country = address_country,
#         )
#         client.save()
#
#         return HttpResponseRedirect(reverse('customers:clients_list'))
