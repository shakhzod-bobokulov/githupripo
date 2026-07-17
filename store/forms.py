from django import forms

from .models import ContactMessage, Order


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ismingiz"}),
            "phone": forms.TextInput(attrs={"placeholder": "Telefon raqamingiz"}),
            "message": forms.Textarea(attrs={"placeholder": "Xabaringiz", "rows": 4}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "note"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Ism familiyangiz"}),
            "phone": forms.TextInput(attrs={"placeholder": "+998 90 123 45 67"}),
            "address": forms.TextInput(attrs={"placeholder": "Yetkazib berish manzili"}),
            "note": forms.Textarea(attrs={"placeholder": "Qo'shimcha izoh (ixtiyoriy)", "rows": 3}),
        }
