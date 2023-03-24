# django
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.template import Template, Context
from django.utils.functional import cached_property
# local
from .forms import ExpandRequestForm
# 1st party
from administrating.models import Page
import re


class IndexView(View):

    def make_get_context(self, request) -> dict:
        page = self.page
        request_form = ExpandRequestForm(data=request.GET)
        if request_form.is_valid():
            context = request_form.cleaned_data
            context.update({'title': page.title})
            context.update({'base_url': self.request.path})
            return context
        else:
            return HttpResponseBadRequest(request_form.errors.as_json())

    @cached_property
    def page(self):
        """
            Gets page object
        """
        url = self.request.path
        page = get_object_or_404(Page, **{'url': url})  # it's not rendering!!!
        return page

    def _tmp_name_from_path(self) -> str:
        path = re.split(r'[\\/]', self.page.template.path)[-2:]
        if path[0] != 'templates':
            ext_str = '/'.join(path)
        else:
            ext_str = path[1]
        return ext_str

    @staticmethod
    def template(page: 'Page'):
        return page.template

    def make_template(self, context):
        template = Template(self.template(self.page).open().read().decode())
        context = Context(context)
        return template.render(context)

    def get(self, request: HttpRequest, **kwargs):
        context = self.make_get_context(request)
        if isinstance(context, dict):
            return HttpResponse(content=self.make_template(context))
        elif isinstance(context, HttpResponse):
            return context
        else:
            raise Exception(f'Exception occurred: unexpected type of Response - {type(context)}')

# Create your views here.
