from django.contrib import admin
from django.urls import path
from . import views

app_name = "hesap"

urlpatterns = [
    path("addshopping/", views.addshopping, name="addshopping"),
    path("index/", views.index, name="index"),
    path("delete/<int:id>", views.deletehesap, name="delete"),
]
