from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import get_token
from django.http.response import HttpResponseBadRequest
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.utils.safestring import SafeString
# 1st party
from menu.views import IndexView
from .forms import MakeTemplateForm
from .models import Page
# utils
from .utils import MenuParser, get_html_tag, TemplateUpdater
# python
import re
from io import TextIOWrapper


class IndexEditorView(LoginRequiredMixin, IndexView, FormMixin):

    form_class = MakeTemplateForm
    login_url = '/admin/login/'

    def make_get_context(self, request) -> dict:
        context = super().make_get_context(request)
        context.update({'form': self.form_class})
        context.update({'extend_string':  self._tmp_name_from_path()})
        context.update({'provide_name': True})
        return context

    @property
    def page(self):
        page_id = self.kwargs.get('id')
        return get_object_or_404(Page, id=page_id)

    @staticmethod
    def template(page: 'Page'):
        return 'administrating/edit.html'

    def make_template(self, context: dict):
        context.update({'csrf_token': get_token(self.request)})
        template = get_template(template_name=self.template(self.page))
        return template.render(context)

    def get(self, request, **kwargs):
        return super(IndexEditorView, self).get(request, **kwargs)

    def post(self, request, **kwargs):
        form = MakeTemplateForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pos = data.get('position')
            name = SafeString('{% draw_menu '+f"'{data['new_menu']}'" + '%}')
            p = MenuParser()
            with self.page.template.open('r') as f:
                f: TextIOWrapper
                inp_data: bytes = f.read()
                p.feed(inp_data)
                pos_on_template = p.append_menu_position(pos)
                input_data = get_html_tag(name)
            with TemplateUpdater(self.page.template) as upd:
                upd.add_data(pos_on_template, input_data)
            p.close()
            return super().get(request, **kwargs)
        else:
            return HttpResponseBadRequest(content=form.errors.as_json())

# Create your views here.
