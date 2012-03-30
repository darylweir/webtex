


from bottle import *

# Include the Dropbox SDK libraries
from dropbox import client, rest, session



@route('/login')
def login():
	# Get your app key and secret from the Dropbox developer website
	APP_KEY = 'gkucvfe9xptshud'
	APP_SECRET = '08nvepsv953j8b9'

	# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
	ACCESS_TYPE = 'app_folder'

	sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

	request_token = sess.obtain_request_token()

	url = sess.build_authorize_url(request_token, 'http://localhost:8080/success')

	redirect(url)

@route('/success')
def success():
	return 'You successfully logged in.'


run(host='localhost', port=8080, debug=True, reloader = True)
	

