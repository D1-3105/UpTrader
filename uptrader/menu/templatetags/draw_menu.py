from django import template
from django.template.loader import get_template
from menu.models import Menu, MenuElement
from collections import deque
from menu.forms import ExpandRequestForm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.template.context import RequestContext

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context: 'RequestContext', menu_name: str):
    """
        if not context then get only root of menu
        else perform retrieving sliced tree of menu
        context: {
            "expanded": int, - currently expanded node
            "host_menu": str, - current host_menu
        }
    """
    if context.get('expanded') and context.get('host_menu') == menu_name:
        elements = MenuElement.objects.get_element_tree(
            menu_name,
            context['expanded']
        )
        elements = RawElementQueue.from_plane_list(list(elements))
    else:
        elements = [Menu.objects.elements_by_menu_name(menu_name)]
    tmp: template.Template = get_template('menu/menu.html')
    context = {
        'queue': elements,
        'host_menu': menu_name,
        'base_path': context.get('base_url')
    }
    return tmp.render(context)


class RawElementQueue(deque):

    @classmethod
    def from_plane_list(cls, elements: list[dict]):
        instance = cls([])
        root_id = cls.detect_root(elements)
        # find root
        instance.make_tree(elements, root_id)
        return instance

    @classmethod
    def detect_root(cls, elements):
        for element in elements:
            parent_ptr = cls.detect_level(
                elements,
                menu_id := cls.get_key(element, 'menu_id')
            )
            if not parent_ptr:
                return menu_id

    def pop_level(self):
        return self.popleft()

    @staticmethod
    def get_key(element: dict | MenuElement, key_signature=str):
        """
            Retrieves key
        """
        if isinstance(element, dict):
            return element[key_signature]
        elif isinstance(element, MenuElement):
            return getattr(element, key_signature)
        else:
            raise KeyError(f'Incorrect type of container: {type(element)} - {element}')

    @classmethod
    def detect_level(cls, elements, child_id):
        for element in elements:
            if cls.get_key(element, 'menu_child_id') == child_id:
                return cls.get_key(element, 'menu_id')
        return None

    def make_tree(self, elements: list[dict | MenuElement], root_id: int | None = None):
        if not elements:
            return 0
        level = []
        elements_next = []
        for element in elements:
            if self.get_key(element, 'menu_id') == root_id:
                level.append(element)
            else:
                elements_next.append(element)
        level.sort(key=lambda e: self.get_key(e, 'order'))
        self.append(level)
        return self.make_tree(elements_next, self.detect_root(elements_next))
