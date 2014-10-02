from bottle import request, redirect, route, jinja2_view, abort
from loginbackends import DummyBackend, SQLBackend
from kana.util import view

backend = None


@route('/login', method=["post", "get"])
@view('login.html')
def login_handler():
    ctx = {}
    global backend
    if request.method == "POST":
        # this style could totally be cleaned up...
        backend_t = request.environ.get('kana.db_type')
        if backend_t == "Production":
            if backend is None:
                backend = SQLBackend()
            engine = request.environ.get('kana.db')
            backend.set_engine(engine)
        user = request.forms.get('user')
        password = request.forms.get('password')
        userid = backend.check_credentials(user, password)
        if userid > -1:
            session = request.environ.get('beaker.session')
            session['user'] = user
            session['user_id'] = userid
            if userid == "admin":
                session['is_admin'] = True
            session.save()
            return redirect('/')
        ctx['message'] = 'Unknown username and/or password'

    return ctx


@route('/logout')
def logout_handler():
    session = request.environ.get('beaker.session')
    session.invalidate()
    return redirect('/login')

@route('/account')
@view('account_main.html')
def account_handler():
    ctx = {}
    updateable_p = request.environ.get('kana.account_update', True)
    global backend
    session = request.environ.get("beaker.session")
    if not updateable_p:
        abort(404)
    data = backend.get_user_by_name(session['user'])
    ctx['user'] = data[1]
    ctx['name'] = data[4]
    return ctx

@route('/account/password', method=["post"])
@view('account_password.html')
def account_password():
    ctx = {}
    global backend
    updateable_p = request.environ.get('kana.account_update', True)
    if not updateable_p:
        abort(404)
    session = request.environ.get("beaker.session")
    user = session['user']
    password = request.forms.get("password")
    new_password = request.forms.get("new_password")
    name = request.forms.get("name")
    userid = backend.check_credentials(user, password)
    if userid > -1:
        backend.update_credentials(user, new_password, name)
        return redirect('/account')
    ctx['message'] = "Account update failed; please check the password and try again"
    data = backend.get_user_by_name(session['user'])
    ctx['user'] = data[1]
    ctx['name'] = data[4]
    return ctx

@route('/admin/users', method=["get","post"])
@view('admin_users.html')
def admin_users():
    ctx = {}
    session = request.environ.get("beaker.session")
    if session['user'] != "admin":
        return abort(404)
    users = backend.get_users()
    ctx['users'] = users
    return ctx

@route('/admin/users/new', method=["get", "post"])
@view('admin_users_new.html')
def admin_users_new():
    ctx = {}
    global backend

    session = request.environ.get("beaker.session")
    if session['user'] != "admin":
        return abort(404)

    if request.method == "POST":
        backend_t = request.environ.get('kana.db_type')
        if backend_t == "Production":
            if backend is None:
                backend = SQLBackend()
            engine = request.environ.get('kana.db')
            backend.set_engine(engine)
        user = request.forms.get("user")
        password = request.forms.get("password")
        name = request.forms.get("name")
        if backend.add_credentials(user, password, name):
            ctx['message'] = "User added sucessfully"
        else:
            ctx['message'] = "User was not added."
    return ctx

if __name__ == "__main__":
    backend = DummyBackend()
    from bottle import run
    run(host='0.0.0.0', port='8080')
else:
    backend = SQLBackend()
    backend_t = "Production"
