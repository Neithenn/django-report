from django import forms
from .models import AssociateBill

class OneRecord(forms.ModelForm):
    class Meta:
        model = AssociateBill
        fields = ('bill1','bill2',)