from flask import redirect, make_response

def make_cookie_resp(username, logout=False):
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    if logout:
        response.set_cookie('username', expires=0)
    else:
        response.set_cookie('username', value=username)
    return response