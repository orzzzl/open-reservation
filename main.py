from flask import Flask, render_template, redirect, url_for, request, make_response
from tools.validators import *
from tools.helper import *
from tools.cookies import make_cookie_resp
from database.users import User
from database.resource import Resource
from database.tag import Tag

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    username = request.cookies.get('username')
    return render_template('front.html', username=username, res=Resource.get_all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User.login(username, password)
        if not u:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            return make_cookie_resp(username)
    return render_template('login.html')

@app.route('/logout')
def logout():
    return make_cookie_resp(None, logout=True)

@app.route('/res/<id>')
def res_page(id):
    ans = Resource.by_id(str(id))
    return ans.render()

@app.route('/tag/<id>')
def tag_page(id):
    ans = Tag.by_key(id)
    tagname = ans.name
    tags = Tag.by_name(tagname)
    res = []
    for t in tags:
        res.append(Resource.by_id(t.rid))
    return render_template('tags.html', tagname=tagname, res=res)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        have_error = False
        params = dict(username=request.form['username'])

        if not valid_username(request.form['username']):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(request.form['password']):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if request.form['password'] != request.form['verify']:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if User.by_name(request.form['username']):
            params['error_username'] = 'That user already exists.'

        if have_error:
            return render_template('signup.html', **params)

        u = User.register(request.form['username'], request.form['password'])
        u.put()

        return make_cookie_resp(request.form['username'])

    return render_template('signup.html')


@app.route('/add_resource', methods=['GET', 'POST'])
def add_res():
    if request.method == 'POST':
        if convert_date(request.form['start_time']) > convert_date(request.form['end_time']):
            return render_template('add_resource.html', error=True)
        res = Resource.create_res(
            request.form['name'],
            convert_date(request.form['start_time']),
            convert_date(request.form['end_time']),
            get_numeric_val(request.form['start_time']),
            get_numeric_val(request.form['end_time']),
            request.cookies.get('username')
                                  )
        res.put()
        tags = request.form['tag'].split(';')
        for t in tags:
            tg = Tag.create_tag(t, str(res.key()))
            tg.put()
        return redirect('/')
    return render_template('add_resource.html', username=request.cookies.get('username'))



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
