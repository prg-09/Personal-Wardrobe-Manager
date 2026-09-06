from django import forms
from .models import Clothitem


class ClothitemForm(forms.ModelForm):
    class Meta:
        model = Clothitem
        fields = ["name", "category", "season", "photo"]
        
