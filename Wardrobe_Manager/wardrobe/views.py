from django.shortcuts import render,redirect
from .models import Clothitem
from .models import Outfit
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


def home(request):
    return render(request,'wardrobe/home.html')

def closet(request):
    clothes = Clothitem.objects.filter(owner = request.user)
    return render(request, 'wardrobe/closet.html', {'clothes': clothes})

def outfit(request):
    outfit = Outfit.objects.filter(owner= request.user)
    return render(request, 'wardrobe/outfit.html', {'outfits': outfit})

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            password=password
        )

    return render(request, 'wardrobe/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
        username=username,
        password=password
    )
        
        if user is not None:
            login(request, user)
            return redirect('closet')
        else:
            print('try again')
    return render(request, 'wardrobe/login.html')
    
   

    