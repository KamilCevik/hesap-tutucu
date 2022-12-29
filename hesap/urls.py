from re import template
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from hesap.views import AddShoppingView,DeleteHesapView,VerifyView


app_name = "hesap"

urlpatterns = [
    path("addshopping/",AddShoppingView.as_view(),name='addshopping'),
    path("index/", views.index, name="index"),
    path("delete/<int:pk>", DeleteHesapView.as_view(), name="delete"),
    path("deleteall/", views.deleteall, name="deleteall"),
    path("index/verifypassword/",VerifyView.as_view() , name="verifypassword"), 
    
]
