from urllib.parse import urlencode
import json
import logging 
import requests
from bottle import route, template, redirect, static_file, error, request, response, run

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/handle_user_decision"
SCOPE = "read write"


@route('/home')
def show_home():
    return template('home')


@route('/')
def handle_root_url():
    redirect('/home')


@route('/zendesk_profile')
def make_request():

    if request.get_cookie('owat'):
        # Get user data
        logging.warning('I now have the code ->' + request.get_cookie('owat'))
        access_code = request.get_cookie('owat')
        if request.get_cookie('ztok'):
            logging.warning('I now have the authorization code! ->' + request.get_cookie('ztok'))
            access_token = request.get_cookie('ztok')
            bearer_token = 'Bearer ' + access_token
            header = {'Authorization': bearer_token}
            logging.warning('Doing GET request with headers: ')
            logging.warning(header)
            url = 'https://www.zopim.com/api/v2/account'
            r = requests.get(url, headers=header)
            logging.warning('SERVER RESPONSE:' + r.text)
            if r.status_code != 200:
                error_msg = 'Failed to get data with error {}'.format(r.status_code) 
                return template('error', error_msg=error_msg)
            else:
                data = r.json()
                logging.warning(data)
                profile_data = {
                    'name': data['billing']['first_name']}
            
                return template('details', data=profile_data)
        else:
            logging.warning('Getting the Authorization Code!')
            param = {
                'grant_type': 'authorization_code',
                'code': access_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'scope': 'read write'
            }
            url = 'https://www.zopim.com/oauth2/token'
            rr = requests.post(url, params=param)
            rdata = rr.json()
            logging.warning('Storing authorization code in a cookie (ztok)')
            token = rdata['access_token']
            response.set_cookie('ztok', token)
            redirect('/zendesk_profile')
    else:
        # kick off authorization flow
        logging.warning('Step 1 - Getting the Code!')
        parameters = {
            'response_type': 'code',
            'grant_type':'client_credentials',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET,
            'scope': 'read write'}
        url = 'https://www.zopim.com/oauth2/authorizations/new?' + urlencode(parameters)
        redirect(url)


@route('/css/<filename>')
def send_css(filename):
    return static_file(filename, root='static/css')

@route('/handle_user_decision')
def handle_decision():
    if 'error' in request.query_string:
        return template('error', error_msg=request.query.error_description)
    else:
        logging.warning('Storing Step 1 code in a cookie (owat)')
        token = request.query.code
        response.set_cookie('owat', token)
        redirect('/zendesk_profile')

@error(404)
def error404(error):
    return template('error', error_msg='404 error. Nothing to see here')


run(host='localhost', port=8080, debug=True)