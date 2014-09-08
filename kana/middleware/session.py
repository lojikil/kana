from bottle import hook, request, redirect


@hook('before_request')
def session_check():
    if request.urlparts.path != "/login" and \
       not request.urlparts.path.startswith("/images") and \
       not request.urlparts.path.startswith("/static"):
        beaker_session = request.environ.get('beaker.session')

        if beaker_session is None:
            redirect('/login')

        if beaker_session.get('user') is None:
            redirect('/login')
    pass
