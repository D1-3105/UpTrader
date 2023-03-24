from html.parser import HTMLParser
from django.utils.safestring import SafeString
from io import TextIOWrapper
import re


def get_html_tag(tag: str | SafeString):
    """
        Wraps tag with div
    """
    return f"""
    <div>
        {tag}
    </div>
    """


class MenuParser(HTMLParser):
    """
        Find position for new tag
        Actually I would like to use bs4, but it's restricted
    """

    draw_menu_positions = []
    div_end_tags = []
    block_pos: int = 3

    def handle_data(self, data: str) -> None:
        if re.search(r'\{%draw_menu \'.+\'%}', data):
            self.draw_menu_positions.append(self.getpos()[0])
        elif data == '{%block content%}':
            self.block_pos = self.getpos()[0]

    def handle_endtag(self, tag: str) -> None:
        if tag == 'div':
            self.div_end_tags.append(self.getpos()[0])

    def append_menu_position(self, menu_pos: int):
        menu_pos -= 1
        if len(self.draw_menu_positions) == 0 or menu_pos == 0:
            pos = self.block_pos + 1
        elif len(self.draw_menu_positions) < menu_pos:
            pos = self.div_end_tags[len(self.draw_menu_positions) - 1] - 1
        elif len(self.draw_menu_positions) == menu_pos:
            pos = self.div_end_tags[-1] + 1
        elif len(self.draw_menu_positions) > menu_pos:
            pos = self.div_end_tags[menu_pos] + 1
        else:
            raise ValueError('No such position!')
        return pos


class TemplateUpdater:
    _w: TextIOWrapper | None
    _r: TextIOWrapper | None

    def __init__(self, field_file):
        self.ff = field_file
        self._r = None
        self._w = None

    @property
    def read_stream(self):
        self._r = self._r or self.ff.open('r+')
        return self._r

    @property
    def write_stream(self):
        self._w = self._w or self.ff.open('w')
        return self._w

    def add_data(self, lineno, input_data: str | SafeString):
        lines = self.read_stream.readlines()
        lines.insert(lineno - 1, input_data)
        self.write_stream.writelines(lines)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._w:
            self._w.close()
        if self._r:
            self._r.close()

    def __enter__(self):
        return self
