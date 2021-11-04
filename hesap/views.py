from collections import UserString

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.db.models import Avg, Count, Min, Sum
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render


from .forms import HesapForm
from .models import Hesap


# Create your views here.
@login_required
def index(request):
    form = HesapForm(request.POST or None)
    hesap = Hesap.objects.all()
    users = (
        User.objects.prefetch_related("hesap_set")
        .filter(is_active=True)
        .annotate(total_price=Sum("hesap__total"))
    )
    users_total = Hesap.objects.aggregate(Sum("total"))
    us=list(users_total.values())
    l=list(users.values("total_price"))
    
    user_count = User.objects.count()
    ort=float(us[0])/user_count
    


    context = {
        "hesaps": hesap,
        "form": form,
        "users": users,
        "ort":ort,
        
        
    }
    if form.is_valid():
        hesap = form.save(commit=False)
        hesap.author = request.user
        hesap.save()
        return redirect("hesap:index")

    return render(request, "index.html", context)


def home(request):
    return render(request, "home.html")


def addshopping(request):
    form = HesapForm(request.POST or None)

    return render(request, "addshopping.html")


def deletehesap(requsest, id):
    hesap = get_object_or_404(Hesap, id=id)
    hesap.delete()
    return redirect("hesap:index")
