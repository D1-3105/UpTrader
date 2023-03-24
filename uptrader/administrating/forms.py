from django import forms
from .models import Page
from menu.models import Menu


class MakeTemplateForm(forms.Form):
    new_menu = forms.TypedChoiceField(
    )
    position = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_menu'].choices = Menu.objects.all().values_list('menu_name', 'menu_name')

    class Meta:
        fields = 'new_menu', 'after_menu'


class CreatePageForm(forms.ModelForm):

    class Meta:
        exclude = 'template',
        model = Page

