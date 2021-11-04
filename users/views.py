from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
# Create your views here.


def login_user(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.info(request, "Kullanıcı Adı veya Parola Hatalı")
            return render(request, "login.html", context)
        messages.success(request, "Başarıyla Giriş Yaptınız")
        login(request, user)
        return redirect("hesap:index")
    return render(request, "login.html", context)


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Güle Güle")
    return redirect("home")
