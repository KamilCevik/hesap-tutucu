from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm

# Create your views here.


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("hesap:index")

                else:
                    messages.info(request, "Disabled Account")

            else:
                messages.info(request, "Kullanıcı adı ve Parolanızı Kontrol Edin.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesap Başarıyla Oluşturuldu.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.success(request, "Güle Güle")
    return redirect("home")
