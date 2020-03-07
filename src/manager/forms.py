from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class CreateOrder(forms.Form):
    short_note = forms.CharField(required=False,
                                 widget=forms.Textarea(attrs={"class": "form-control", 'rows': 2, 'cols': 15,
                                                              'placeholder': "Enter your recommendations.(If Any)"}))
    address_line_1 = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': "Example: 117/1 East Tejturi Bazar, Farmgate"}))
    city = forms.CharField(initial='Dhaka', widget=forms.TextInput(attrs={"class": "form-control"}))
    postal_code = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': "Example: 1215"}))

    def clean(self):
        address_line_1 = self.cleaned_data.get('address_line_1')
        postal_code = self.cleaned_data.get('postal_code')
        if not address_line_1 or not postal_code:
            raise forms.ValidationError("Sorry, that input your all info.")
        return self.cleaned_data
