from flask import Flask, render_template, redirect, request, Response
from tools.validators import *
from tools.helper import *
from tools.cookies import make_cookie_resp
from database.users import User
from database.resource import Resource
from database.tag import Tag
from database.reservation import Reservation

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    username = request.cookies.get('username')
    resv = Reservation.by_username(username)
    return render_template('front.html', username=username, res=Resource.get_all(),
                           res2=Resource.by_user(username), resv=resv
                           )

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
    resv = Reservation.by_rid(str(ans.key()))
    return render_template('res_page.html', r=ans, resv=resv, username=request.cookies.get('username'))

@app.route('/tag/<id>')
def tag_page(id):
    ans = Tag.by_key(id)
    tagname = ans.name
    tags = Tag.by_name(tagname)
    res = []
    for t in tags:
        res.append(Resource.by_id(t.rid))
    return render_template('tags.html', tagname=tagname, res=res, username=request.cookies.get('username'))

@app.route('/make_reservation/<id>', methods=['GET', 'POST'])
def make_reservation(id):
    res = Resource.by_id(str(id))
    resv = Reservation.by_rid(str(res.key()))
    if request.method == 'POST':
        error = None
        st = convert_date_2(request.form['start_time'])
        et = convert_date_2(request.form['end_time'])
        st_day = convert_date(str(st)[-8:-3])
        et_day = convert_date(str(et)[-8:-3])
        if st_day < res.start_time:
            error = "start time earlier than available start time"
        if et_day > res.end_time:
            error = "end time later than available end time"
        if st > et:
            error = "end time should be larger than start time"
        if str(st)[:10] != str(et)[:10]:
            error = "only support reservation ends at same day"
        for resvation in resv:
            if resvation.start_time < st and resvation.end_time > st:
                error = "conflict with earlier reservation: " + str(resvation.start_time) + "~" + str(resvation.end_time)
                break
            if resvation.start_time < et and resvation.end_time > et:
                error = "conflict with earlier reservation: " + str(resvation.start_time) + "~" + str(resvation.end_time)
                break
        if error is not None:
            return render_template('make_reservation.html', r=res, error=error, username=request.cookies.get('username'))
        resv = Reservation.create_reservation(st, et, request.cookies.get('username'), str(res.key()))
        resv.put()
        return redirect('/res/' + str(res.key()))
    return render_template('make_reservation.html', r=res, resv=resv, username=request.cookies.get('username'))

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
            request.cookies.get('username'),
            request.form['tag']
                                  )
        res.put()
        tags = request.form['tag'].split(';')
        for t in tags:
            tg = Tag.create_tag(t, str(res.key()))
            tg.put()
        return redirect('/')
    return render_template('add_resource.html', username=request.cookies.get('username'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_res(id):
    res = Resource.by_id(str(id))
    if request.method == 'POST':
        res = Resource.by_id(str(id))
        Tag.delete_by_key(str(res.key()))
        if convert_date(request.form['start_time']) > convert_date(request.form['end_time']):
            return render_template('add_resource.html', error=True)
        res.name = request.form['name']
        res.start_time = convert_date(request.form['start_time'])
        res.end_time = convert_date(request.form['end_time'])
        res.start_time_n = get_numeric_val(request.form['start_time'])
        res.end_time_n = get_numeric_val(request.form['end_time'])
        res.belonging_user = request.cookies.get('username')
        res.tag = request.form['tag']
        res.put()
        tags = request.form['tag'].split(';')
        for t in tags:
            tg = Tag.create_tag(t, str(res.key()))
            tg.put()
        return redirect('/')
    return render_template('add_resource.html', username=request.cookies.get('username'),
                           edit=True, name=res.name, tag=res.tag,
                           start_time=str(res.start_time)[-8:-3], end_time=str(res.end_time)[-8:-3], id=str(res.key()))


@app.route('/rss/<id>')
def rss(id):
    return Response(dump_to_xml(id), mimetype='text/xml')

@app.route('/del/<id>')
def delete(id):
    Reservation.delete_by_id(str(id))
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
