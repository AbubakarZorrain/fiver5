from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

#
# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = "__all__"
