from functools import partial
from bottle import jinja2_view
from timestamp import timestamp

view = partial(jinja2_view, template_lookup=["templates"])

