from bottle import redirect, request
import re


class FilterMiddleware(object):

    """
       A simple database-handling middleware that inserts the SQLAlchemy
       object at bottle.request.environ['ctfmiddleware.db'] by default.
       Meant to facilitate using SQLAlchemy within the CTF, and avoid
       having SQL connection strings, SQL code, DDLs, & the like
       throughout the code base.
    """

    def __init__(self, app, config={}, **kwargs):
        """ Initialize the DatabaseMiddleware for the CTF; allows
        developers to access the current SQLAlchemy session
        via a configurable key (defaults to ctfmiddleware.db)
        """

        self.app = app
        self.config = config

        self.config.update(kwargs)

        self.env_key = config.get('environment_key', 'kana.filter')
        self.seclevel = 0

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/seclevel':
            self.seclevel += 1
        environ[self.env_key] = self.seclevel
        print "ENVIRON: ", environ.get(self.env_key, "Nothing")
        return self.app(environ, start_response)



def xssfilter(field):
    seclevel = request.environ.get('kana.filter')

    if seclevel == 0:
        return field
    elif seclevel == 1:
        t = "<invalidTag".join(field.split("<script"))
        t = "</invalidTag".join(t.split("</script"))
        return t
    elif seclevel == 2:
        for tag in ["a", "img", "script", "div", "p", "span"]:
            t = "<invalidtag".join(field.split("<{0}".format(tag)))
            t = "</invalidTag".join(t.split("</{0}".format(tag)))
            field = t
        return t
    else:
        t = '&lt;'.join(field.split("<"))
        t = '&gt;'.join(t.split(">"))
        return t
