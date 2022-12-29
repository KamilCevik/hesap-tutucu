from django.db import models
from django.utils.translation import deactivate

# Create your models here.


class Hesap(models.Model):
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name="İsim"
    )
    total = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Tutar")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Ödeme Tarihi")

    class ShoppingType(models.TextChoices):
        YEMEK = "YEMEK"
        KAHVALTI = "KAHVALTI"
        ALIŞVERİŞ = "ALIŞVERİŞ"

    shopping_type=models.CharField(max_length=100,choices=ShoppingType.choices,default=ShoppingType.YEMEK,verbose_name="Alışveriş Türü")

class CommunicationModel(models.Model):
    
    email = models.EmailField(max_length=250)
    isim_soyisim = models.CharField(max_length=150)
    mesaj = models.TextField()
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "iletisim"
        verbose_name = "İletişim"
        verbose_name_plural = "İletişim"


def __str__(self):
    return self.email