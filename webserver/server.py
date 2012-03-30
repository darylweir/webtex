from bottle import *
from dropbox import client, rest, session
from login import *
import datetime


@route('/')
def index():
	return template('index')


@route('/doclist')
def doclist():
	name = 'Iain McGinniss'
	template_list = ['LNCS', 'ACM', 'IEEE']
	doc_list = [
	  {'name': 'Paper 1', 'key': '/paper1', 'modified': datetime.datetime.now()},
	  {'name': 'Hanoi: A Typestate DSL for Java', 'key': '/hanoi', 'modified': datetime.datetime.now() },
	]
	
	docs_html = ''.join([template('docitem', name=doc['name'], link='/editor?key='+doc['key'], modified=doc['modified']) for doc in doc_list])
	templates_html = ''.join([template('templateitem', name=tmpl) for tmpl in template_list])

	return template('doclist', name=name, docs=docs_html, templates=templates_html)


@route('/editor')
def editor():
	return template('editor')


@route('/static/<path:path>')
def static(path):
	return static_file(path, root='static')


if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True, reloader = True)
