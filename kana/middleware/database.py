try:
    from paste.registry import StackedObjectProxy
    gengine = StackedObjectProxy('SQLAlchemy Engine')
except:
    gengine = None


class DatabaseMiddleware(object):

    """
       A simple database-handling middleware that inserts the SQLAlchemy
       object at bottle.request.environ['kana.db'] by default.
       Meant to facilitate using SQLAlchemy within the CTF, and avoid
       having SQL connection strings, SQL code, DDLs, & the like
       throughout the code base.
    """

    def __init__(self, app, engine, config={}, **kwargs):
        """ Initialize the DatabaseMiddleware for the CTF; allows
        developers to access the current SQLAlchemy session
        via a configurable key (defaults to ctfmiddleware.db)
        """

        self.app = app
        self.config = config
        self.engine = engine
        self.gengine = gengine

        self.config.update(kwargs)

        self.env_key = config.get('environment_key', 'kana.db')
        self.type_key = config.get('type_key', 'kana.db_type')

    def __call__(self, environ, start_response):
        if environ.get('paste.registry'):
            if environ['paste.registry'].reglist:
                environ['paste.registry'].register(self.gengine, self.engine)
        environ[self.env_key] = self.engine
        environ[self.type_key] = "Production" # need to make this configurable
        return self.app(environ, start_response)
