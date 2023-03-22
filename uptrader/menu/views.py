# django
from django.views import View
from django.shortcuts import render, Http404
from django.http.response import HttpResponseBadRequest
from django.core.exceptions import ValidationError
# local
from .forms import ExpandRequestForm


class IndexView(View):

    def get(self, request, **kwargs):
        request_form = ExpandRequestForm(data=request.GET)
        if request_form.is_valid():
            return render(
                request,
                'menu/index.html',
                context=request_form.data
            )
        else:
            return HttpResponseBadRequest(request_form.errors.as_json())

# Create your views here.
