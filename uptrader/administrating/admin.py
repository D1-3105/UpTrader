from django.contrib import admin
from django.urls import path


class ModelAdminView(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()

        urls += [
            path('admin/make_index/', )
        ]

# Register your models here.
