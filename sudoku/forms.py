from django import forms
from .models import SudokuImage

class SudokuImageForm(forms.ModelForm):
    class Meta:
        model = SudokuImage
        fields = ['image']
