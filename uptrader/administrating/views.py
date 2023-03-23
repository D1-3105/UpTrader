from django.shortcuts import render
from django.views import View
from menu.views import IndexView


class IndexEditorView(IndexView):

    def post(self):
        ...


# Create your views here.
