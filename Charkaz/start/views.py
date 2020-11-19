from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse,redirect
from .forms import registerForm,loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginProfil,logout
from .models import userProfile
from django.contrib import messages


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
        
    logForm = loginForm(request.POST or None)
    context = {
        'form':logForm
    }

    if logForm.is_valid():
        istifadeci = logForm.cleaned_data.get('istifadeci')
        sifre = logForm.cleaned_data.get('sifre')
        user = authenticate(username = istifadeci,password = sifre)
        if user is None:
            messages.success(request,"Itifadeci adi ve ya sifre xetalidir !",extra_tags='danger')
            return render(request,'landing/login.html',context=context)
        else:
            try:
                loginProfil(request,user)
                return render(request,'soft/dashboard.html')
            except:
                print("problem")

    return render(request,'landing/login.html',context=context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
       
    regForm = registerForm(request.POST or None)
    context = {
        'form':regForm
    }
    if regForm.is_valid():
        try:
            ad = regForm.cleaned_data.get('ad')
            soyad = regForm.cleaned_data.get('soyad')
            telefon = regForm.cleaned_data.get('telefon')
            email = regForm.cleaned_data.get('email')
            istifadeciadi = regForm.cleaned_data.get('istifadeciadi')
            sirket = regForm.cleaned_data.get('sirket')
            sifre = regForm.cleaned_data.get('sifre')
            istifadeci = User(first_name = ad, last_name = soyad , email=email, username=istifadeciadi)
            istifadeci.set_password(sifre)
            userprofile = userProfile(user = istifadeci,kassa=0.0,sirket=sirket,telefon=telefon)
            istifadeci.save()
            userprofile.save()
            messages.success(request,"Qeydiyyat ugurla basa catdi.",extra_tags='success')
            return HttpResponseRedirect(reverse('login'))
        except Exception as e:
            messages.success(request,"Problem yarandi."+" "+"e",extra_tags='danger')
            return render(request,'landing/register.html',context=context)
    return render(request,'landing/register.html',context=context)



