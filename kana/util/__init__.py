from functools import partial
from bottle import jinja2_view

# from here:
# http://reliablybroken.com/b/2013/12/jinja2-templates-and-bottle/
view = partial(jinja2_view, template_lookup=["templates"])

