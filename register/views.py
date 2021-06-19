import django.forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from IOT.settings import EMAIL_HOST_USER
from .forms import CreateUserForm
from .models import Customer
from credit_card_checker import CreditCardChecker
from passlib.hash import pbkdf2_sha256
import random


def register(request):
    global form
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                if not User.objects.filter(email=form.cleaned_data.get('email')).exists():
                    form.save()
                    return redirect('validator')
                else:
                    messages.info(request, 'This account is already taken')

        context = {'form': form}
        return render(request, 'register/register.html', context)


def validator(request):
    obj = Customer()
    x = str(request.POST.get('cardnumber'))
    if CreditCardChecker(x).valid():
        obj.username = form.cleaned_data.get('username')
        obj.email = form.cleaned_data.get('email')
        m = form.cleaned_data.get('password1')
        obj.password1 = pbkdf2_sha256.hash(m)
        obj.cardnumber = x
        obj.save()

        return redirect('login')
    else:
        messages.info(request, 'please enter the right credit card number')
        context = {}
        return render(request, 'register/valid.html', context)


def loginpage(request):

    if request.user.is_authenticated:

        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


def home(response):
    return render(response, "register/home.html")


def loc(response):
    return render(response, "register/location.html")


def email(request):
    if request.method == 'POST':
        current_user = request.user
        recepient = current_user.email
        subject = 'Confirming your booking'
        code = str(random.randint(1111, 9999))
        message = 'Here is the code that you need to confirm your booking' + ' ' + code
        current_user = request.user
        t = Customer.objects.get(email=current_user.email)
        t.codenumber = code
        t.save()

        send_mail(subject,
                  message, EMAIL_HOST_USER, [recepient], fail_silently=False)
    return render(request, 'register/email.html')


def sel(response):
    return render(response, "register/index.html")



