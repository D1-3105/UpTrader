# django
from django.views import View
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseBadRequest
# local
from .forms import ExpandRequestForm
# 1st party
from administrating.models import Page


class IndexView(View):

    def get(self, request: HttpRequest, **kwargs):
        url = request.path
        request_form = ExpandRequestForm(data=request.GET)
        if request_form.is_valid():
            return render(
                request,
                'menu/index.html',
                context=request_form.cleaned_data
            )
        else:
            return HttpResponseBadRequest(request_form.errors.as_json())

# Create your views here.
