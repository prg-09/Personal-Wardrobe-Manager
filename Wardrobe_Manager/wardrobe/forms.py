from django import forms
from .models import Clothitem
from .models import Outfit

class ClothitemForm(forms.ModelForm):
    class Meta:
        model = Clothitem
        fields = ["name", "category", "season","color","style","photo"]
        
class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ["name", "items"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["items"].queryset = Clothitem.objects.filter(
            owner=user
        )
        
class OutfitGeneratorForm(forms.Form):
    occasion = forms.CharField(max_length=100)
    season = forms.CharField(max_length=100)
    style = forms.CharField(max_length=100)