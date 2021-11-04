from django import forms
from .models import Hesap

class HesapForm(forms.ModelForm):
    class Meta:
        model= Hesap
        fields=["total","shopping_type"]
