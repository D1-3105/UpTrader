from django.contrib import admin
from .forms import CreatePageForm
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    change_form_template = 'administrating/custom_admin_view.html'
    form = CreatePageForm

# Register your models here.
