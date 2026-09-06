from django.shortcuts import render,redirect,get_object_or_404
from .models import Clothitem
from .models import Outfit
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ClothitemForm

def home(request):
    return render(request,'wardrobe/home.html')

@login_required
def closet(request):
    clothes = Clothitem.objects.filter(owner = request.user)
    return render(request, 'wardrobe/closet.html', {'clothes': clothes})

@login_required
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
    
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def add_clothing(request):
    if request.method == "POST":
        form = ClothitemForm(request.POST, request.FILES)

        if form.is_valid():
            clothing = form.save(commit=False)
            clothing.owner = request.user
            clothing.save()

            return redirect("closet")

    else:
        form = ClothitemForm()

    return render(request, "wardrobe/add_clothing.html", {"form": form})

@login_required
def edit_clothing(request, id):
    clothing = get_object_or_404(
        Clothitem,
        id=id,
        owner=request.user
    )

    if request.method == "POST":
        form = ClothitemForm(
            request.POST,
            request.FILES,
            instance=clothing
        )

        if form.is_valid():
            form.save()
            return redirect("closet")

    else:
        form = ClothitemForm(instance=clothing)

    return render(
        request,
        "wardrobe/edit_clothing.html",
        {"form": form}
    )
    
@login_required
def delete_clothing(request, id):
    clothing = get_object_or_404(
        Clothitem,
        id=id,
        owner=request.user
    )

    if request.method == "POST":
        clothing.delete()
        return redirect("closet")

    return render(
        request,
        "wardrobe/delete_clothing.html",
        {"clothing": clothing}
    )