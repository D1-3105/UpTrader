from django import forms
from django.core.exceptions import ValidationError
from .models import Menu


class ExpandRequestForm(forms.Form):
    expanded = forms.IntegerField(required=False)
    host_menu = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not len(cleaned_data) in [0, 2]:
           raise ValidationError('Invalid request params', code=400)
        print('DATA', cleaned_data)
        return cleaned_data

    class Meta:
        fields = ['expanded', 'host_menu']

