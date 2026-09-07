from django.shortcuts import render,redirect,get_object_or_404
from .models import Clothitem
from .models import Outfit
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ClothitemForm,OutfitForm, OutfitGeneratorForm
from .ai import generate_outfit
from django.core.cache import cache

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
 
@login_required
def add_outfit(request):

    if request.method == "POST":
        form = OutfitForm(request.POST, user=request.user)

        if form.is_valid():
            outfit = form.save(commit=False)
            outfit.owner = request.user
            outfit.save()
            form.save_m2m()

            return redirect("outfit")

    else:
        form = OutfitForm(user=request.user)

    return render(
        request,
        "wardrobe/add_outfit.html",
        {"form": form}
    )
    
@login_required
def edit_outfit(request, id):
    outfit = get_object_or_404(
        Outfit,
        id=id,
        owner=request.user
    )

    if request.method == "POST":
        form = OutfitForm(
            request.POST,
            instance=outfit,
            user=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("outfit")

    else:
        form = OutfitForm(
            instance=outfit,
            user=request.user
        )

    return render(
        request,
        "wardrobe/edit_outfit.html",
        {"form": form}
    )
    
@login_required
def delete_outfit(request, id):
    outfit = get_object_or_404(
        Outfit,
        id=id,
        owner=request.user
    )

    if request.method == "POST":
        outfit.delete()
        return redirect("outfit")

    return render(
        request,
        "wardrobe/delete_outfit.html",
        {"outfit": outfit}
    )
    
@login_required
@login_required
def ai_generator(request):

    clothes = Clothitem.objects.filter(owner=request.user)

    cache_key = f"ai_generator_{request.user.id}"

    if request.method == "POST":

        # SAVE OUTFIT
        if "save_outfit" in request.POST:

            outfit_name = request.POST.get("outfit_name")
            item_ids = request.POST.getlist("item_ids")

            outfit = Outfit.objects.create(
                name=outfit_name,
                owner=request.user
            )

            items = Clothitem.objects.filter(
                id__in=item_ids,
                owner=request.user
            )

            outfit.items.set(items)

            return redirect("outfit")

        # GENERATE OUTFIT
        form = OutfitGeneratorForm(request.POST)

        if form.is_valid():

            if cache.get(cache_key):

                return render(
                    request,
                    "wardrobe/ai_generator.html",
                    {
                        "form": form,
                        "error": "Please wait 30 seconds before generating another outfit.",
                        "cooldown": True,
                    }
                )

            cache.set(cache_key, True, 30)

            occasion = form.cleaned_data["occasion"]
            season = form.cleaned_data["season"]
            style = form.cleaned_data["style"]

            recommendation = generate_outfit(
                clothes,
                occasion,
                season,
                style
            )

            return render(
                request,
                "wardrobe/ai_generator.html",
                {
                    "form": form,
                    "recommendation": recommendation,
                    "cooldown": True,
                }
            )

    else:
        form = OutfitGeneratorForm()

    return render(
        request,
        "wardrobe/ai_generator.html",
        {
            "form": form,
        }
    )