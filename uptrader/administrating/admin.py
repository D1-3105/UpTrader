from django.contrib import admin
from django.shortcuts import redirect, reverse
from django.urls import path
from .models import Page
from .views import IndexEditorView


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    change_form_template = 'administrating/custom_admin_view.html'

# Register your models here.
