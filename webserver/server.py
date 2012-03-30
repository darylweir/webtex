from bottle import *
from dropbox import client, rest, session
from login import *

@route('/')
def index():
	return static_file('index.tmpl', root=".")

@route('/static/<path:path>')
def static(path):
	return static_file(path, root="static")

if __name__ == "__main__":
  run(host='localhost', port=8080, debug=True, reloader = True)
