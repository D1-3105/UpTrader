from django import forms
from .models import Page
from menu.models import Menu


class MakeTemplateForm(forms.ModelForm):
    link = forms.CharField()
    new_menu = forms.TypedMultipleChoiceField(
        choices=Menu.objects.all().values_list('id', 'menu_name')
    )
    after_menu = forms.TypedMultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super(MakeTemplateForm, self).__init__(*args, **kwargs)
        if kwargs.get('after_menus'):
            self.fields['after_menu'].initial = kwargs.get('after_menus')

    class Meta:
        model = Page
        fields = '__all__'
