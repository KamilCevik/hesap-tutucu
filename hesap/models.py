from django.db import models
from django.utils.translation import deactivate

# Create your models here.

class Hesap(models.Model):
    author=models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="İsim")
    total=models.DecimalField(max_digits=10,decimal_places=3,verbose_name="Tutar")
    created_date=models.DateTimeField(auto_now_add=True,verbose_name="Ödeme Tarihi")
    shopping_type=models.CharField(max_length=100,verbose_name="Alışveriş Türü")

