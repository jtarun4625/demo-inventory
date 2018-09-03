from django import forms
from .models import Company


class CompanyUpdateform(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "code",
            "name"
        ]
