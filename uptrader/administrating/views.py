from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
# 1st party
from menu.views import IndexView
from .forms import MakeTemplateForm
from .models import Page
import re


class IndexEditorView(LoginRequiredMixin, IndexView, FormMixin):

    form_class = MakeTemplateForm
    login_url = '/admin/login/'

    def make_get_context(self, request) -> dict:
        context = super().make_get_context(request)
        context.update({'form': self.form_class})
        path = re.split(r'[\\/]', self.page.template.path)[-2:]
        if path[0] != 'templates':
            ext_str = '/'.join(path)
        else:
            ext_str = path[1]
        print('DEBUG', ext_str)
        context.update({'extend_string':  ext_str})
        return context

    @property
    def page(self):
        page_id = self.kwargs.get('id')
        return get_object_or_404(Page, id=page_id)

    @staticmethod
    def template(page: 'Page'):
        return 'administrating/edit.html'

    def make_template(self, context):
        template = get_template(template_name=self.template(self.page))
        return template.render(context)

    def get(self, request, **kwargs):
        return super(IndexEditorView, self).get(request, **kwargs)

    def post(self, **kwargs):
        ...


# Create your views here.
