from collections import UserString
from email.errors import HeaderDefect
from re import template
from django.contrib.auth import authenticate
from django.forms.models import ModelForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count, Min, Sum, fields
from django.forms.widgets import PasswordInput
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from flask import request


from .forms import HesapForm, VerifyPasswordForm, CommunicationForm
from .models import Hesap


# Create your views here.


@login_required
def index(request):
    form = HesapForm(request.POST or None)
    form1 = VerifyPasswordForm(request.POST or None)

    hesap = Hesap.objects.all()
    users = (
        User.objects.prefetch_related("hesap_set")
        .filter(is_active=True)
        .annotate(total_price=Sum("hesap__total"))
    )
    users_total = Hesap.objects.aggregate(Sum("total"))
    us = list(users_total.values())
    l = list(users.values("total_price"))

    user_count = User.objects.count()
    try:
        ort = float(us[0]) / user_count
    except TypeError:
        ort = 0

    context = {
        "hesaps": hesap,
        "form": form,
        "users": users,
        "ort": ort,
        "form1": form1,
    }
    if form.is_valid():
        hesap = form.save(commit=False)
        hesap.author = request.user
        hesap.save()
        return redirect("hesap:index")

    return render(request, "index.html", context)


def home(request):
    return render(request, "home.html")


class AddShoppingView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    template_name = "addshopping.html"
    form_class = HesapForm

    def get_success_url(self):
        return reverse("hesap:index")

    def form_valid(self, form):
        hesap = form.save(commit=False)
        hesap.author = self.request.user
        hesap.save()

        return super().form_valid(form)


class DeleteHesapView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    template_name = "delet.html"
    success_url = reverse_lazy("hesap:index")

    def get_queryset(self, **kwargs):

        hesap = Hesap.objects.filter(id=self.kwargs["pk"], author=self.request.user)
        return hesap


class VerifyView(LoginRequiredMixin, View):
    form1 = VerifyPasswordForm
    http_method_names = ["get", "post"]

    def post(self, request):
        form = self.form1(request.POST)
        if form.is_valid():
            form1 = form.cleaned_data.get("password")
            user = self.request.user
            if user.check_password(form1):
                hesap_count = Hesap.objects.count()
                top = Hesap.objects.aggregate(Sum("total"))
                total_del = list(top.values())

                Hesap.objects.all().delete()
                messages.success(
                    request,
                    "Silinen Hesap Sayısı:{}\n Silinen Toplam Tutar:{}".format(
                        hesap_count, total_del[0]
                    ),
                )

            else:
                messages.info(request, "Seni Şam Şeytanı Seniiiii")

            return redirect("home")


class CommunicationFormView(FormView):
    template_name = "pages/iletisim.html"
    form_class = CommunicationForm
    success_url = "email-gonderildi"

    def form_valid(self, form):
        form.save()
        form.send_mail(mesaj=form.cleaned_data.get("mesaj"))
        return super().form_valid(form)


def deleteall(request):
    Hesap.objects.all().delete()
    return redirect("hesap:index")
