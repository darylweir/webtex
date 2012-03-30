


from bottle import *
from bottle_sqlite import SQLitePlugin
# Include the Dropbox SDK libraries
from dropbox import client, rest, session
import sqlite3, cPickle

conn = sqlite3.connect('/tmp/example')
c = conn.cursor()


install(SQLitePlugin(dbfile = '/tmp/example.db'))

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'gkucvfe9xptshud'
APP_SECRET = '08nvepsv953j8b9'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'


sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

@route('/login')
def login(db):
	request_token = sess.obtain_request_token()
	print request_token

	p = cPickle.dumps(request_token, cPickle.HIGHEST_PROTOCOL)
	
	db.execute('create table if not exists login (oauth text, token blob)')
	db.execute('insert into login values (?,?)',[request_token.key,sqlite3.Binary(p)])

	url = sess.build_authorize_url(request_token, 'http://localhost:8080/success')


	redirect(url)

@route('/success')
def success(db):
	tok = str(request.query.oauth_token)
	row = db.execute('select token from login where oauth = ?',[tok]).fetchone()
	if row:
		token = cPickle.loads(str(row['token']))
		access_token = sess.obtain_access_token(token)
		print dir(access_token)
		cl = client.DropboxClient(sess)
		response.set_cookie('access_token',access_token,secret = 'secretkey')
		redirect('/doclist')
	else:	
		return 'Something went wrong'
