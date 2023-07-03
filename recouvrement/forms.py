from django import forms
from dal import autocomplete
from data.models import *

class UniteForm(forms.ModelForm):
    lib_unit = forms.ModelChoiceField(
        queryset=Unite.objects.all(),
        widget=autocomplete.ModelSelect2(url='unite-autocomplete')
    )

    class Meta:
        model = Unite
        fields = ['lib_unit']