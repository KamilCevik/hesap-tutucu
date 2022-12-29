from attr import fields
from django import forms
from .models import  Hesap,CommunicationModel
from django.core.mail import send_mail

class HesapForm(forms.ModelForm):
    class Meta:
        model= Hesap
        fields=["total","shopping_type"]

class VerifyPasswordForm(forms.Form):
    password=forms.CharField(label="parola",widget=forms.PasswordInput())
    
class CommunicationForm(forms.ModelForm):
    class Meta:
        model=CommunicationModel
        fields=('isim_soyisim','email','mesaj')
    
    def send_mail(self,mesaj):
        send_mail(
            subject='İletişim Formundan Yeni Mesaj Var',
            message=mesaj,
            recipient_list=[],
            fail_silently=False
        )
    