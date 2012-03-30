from bottle import *
from bottle_sqlite import SQLitePlugin
# Include the Dropbox SDK libraries
from dropbox import client, rest, session
import sqlite3, cPickle

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'gkucvfe9xptshud'
APP_SECRET = '08nvepsv953j8b9'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'


sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

def getDocs():
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		md = cl.metadata('/')
		print type(md)
		out = []
		contents = md['contents']
		for i in range(len(contents)):
			temp = contents[i]
			if temp['is_dir']:
				doc = get_doc(cl,temp)
				if not doc == None:
					out.append(doc)
		temp = str(out)
		return out

def get_doc(cl,temp):
	md = cl.metadata(temp['path'])
	contents = md['contents']
	out = []
	for i in range(len(contents)):
		t2 = contents[i]
		if not bool(t2['is_dir']):
			path = t2['path']
			dot = path.rfind('.')
			slash = path.rfind('/')
			fname = path[slash:dot]
			ext = path[dot:]
			if fname == temp['path'] and ext == '.tex':
				return {'name':path[slash+1:],'modified':t2['modified'], 'key':path}
	return None

def putDoc():
	pass

def templateList():
	pass
