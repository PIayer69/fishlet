from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import MyUserCreationForm, LoginForm
from learningSets.models import Set

# Create your views here.
def home(request):
    sets = Set.objects.all()
    context = {
        'sets': sets
    }
    return render(request, 'base/home.html', context)
    

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            next_page = request.GET.get('next') if request.GET.get('next') is not None else 'home'
            return redirect(next_page)
        messages.error(request, 'Wrong credentials')
        
    form = LoginForm()
    context = {'form': form}
    return render(request, 'base/login.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    form  = MyUserCreationForm()
    context = {'form': form}
    return render(request, 'base/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')