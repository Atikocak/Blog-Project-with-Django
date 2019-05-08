from django.shortcuts import render,redirect,render_to_response
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        kullaniciadi = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            user = authenticate(username = kullaniciadi)
            if user is None:
                newUser = User(username = kullaniciadi)
                newUser.set_password(password)
                newUser.save()
                login(request,newUser)
                messages.success(request,"<b>" + str(newUser) + "</b>" + " aramıza hoşgeldiniz!", extra_tags="safe")

                context = {
                    "form" : form,
                }
                return redirect("index")
        except IntegrityError:
            messages.info(request,"Kullanıcı adı " + "<b>" + str(newUser) + "</b>" + " zaten mevcut, lütfen başka bir kullanıcı adı deneyin!", extra_tags="safe")
            context = {
                "form" : form,
            }
            return render(request,"register.html",context)

    context = {
        "form" : form,
    }
    return render(request,"register.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(request,"Kullanıcı adı veya parola hatalıdır, lütfen doğru giriniz!")
            return render(request,"login.html",context)

        login(request,user)
        messages.success(request,'<b>' + str(username) + '</b>' + " başarıyla giriş yaptınız!", extra_tags="safe")
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    username = str(request.user)
    if username != "AnonymousUser":
        logout(request)
        messages.success(request,'<b>' + username + '</b>' + " başarıyla çıkış yaptınız, yine bekleriz!", extra_tags="safe")
        return redirect("index")
    else:
        return redirect("index")