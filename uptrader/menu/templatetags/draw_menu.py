from django import template
from django.template.loader import get_template
from django.db.models import F
from menu.models import Menu, MenuElement

from typing import List

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name: str):
    """
        if not context then get only root of menu
        else perform retrieving sliced tree of menu
        context: {
            "expanded": int, - currently expanded node
            "host_menu": str, - current host_menu
        }
    """
    print(context.get('expanded'))
    if not context.get('expanded'):
        elements = Menu.objects.elements_by_menu_name(menu_name)
    else:
        elements = MenuElement.objects.get_element_tree(
            menu_name,
            int(context['expanded'][0])  # idk why vanilla django requires re-validating
        )
    tmp: template.Template = get_template('menu/menu.html')
    context = {
        'elems': elements,
        'host_menu': menu_name
    }
    return tmp.render(context)
