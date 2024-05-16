from django import forms

from app.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "gender", "phone_number"]
        widgets = {
            "gender": forms.Select(choices=Customer.GENDER_CHOICES),
        }
