from bottle import *
from dropbox import client, rest, session
from login import *

from datetime import *
from docs import *
from urllib import quote_plus

@route('/')
def index():
	return template('index')


@route('/doclist')
def doclist():
	name = user_info()['display_name']
	template_list = ['LNCS', 'ACM', 'IEEE']
	doc_list = getDocs()
	
	docs_html = ''.join([template('docitem', name=doc['name'], link='/editor/' + doc['doc_id'], modified=doc['modified']) for doc in doc_list])

	templates_html = ''.join([template('templateitem', name=tmpl, tmpl_id=tmpl) for tmpl in template_list])

	return template('doclist', name=name, docs=docs_html, templates=templates_html)

@post('/newdoc')
def createNewDoc():
	req = request.json
	#print req
	#print req['name']
	#print req['template']
	return { 'doc_id': 'mydoc' }

@route('/editor/<doc_id:path>')
def editor(doc_id):
	content = get_doc_content(doc_id)
	print content
	return template('editor', doc_name=doc_id, doc_content=content)

@get('/doc/<doc_id>/tex')
def get_document_tex(doc_id):
	response.content_type = 'application/x-latex'
	return get_doc_content(doc_id)

@get('/doc/<doc_id>/pdf')
def get_document_pdf(doc_id):
	response.content_type = 'application/pdf'
	return get_doc_pdf(doc_id)

@post('/doc/<doc_id>')
def update_document(doc_id):
	# 1. push content to dropbox
	# 2. get zip of document from dropbox
	# 3. push zip to S3
	# 4. order build on cluster
	# 5. when complete, respond with info
	return {
		'success': True,
		'pdf': 'http://www.selab.isti.cnr.it/ws-mate/example.pdf',
		'errors': []
	}


@route('/static/<path:path>')
def static(path):
	return static_file(path, root='static')


if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True, reloader = True)
