from bottle import *
from bottle_sqlite import SQLitePlugin
# Include the Dropbox SDK libraries
from dropbox import client, rest, session
import sqlite3, cPickle
import zipfile, StringIO

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'gkucvfe9xptshud'
APP_SECRET = '08nvepsv953j8b9'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'


sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

def user_info():
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		print cl.account_info()
		return cl.account_info()
	else:
		return None

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
			doc_name = path[path.find('/')+1:slash]
			fname = path[slash:dot]
			ext = path[dot:]
			if fname == temp['path'] and ext == '.tex':
				return {'name':doc_name,'modified':t2['modified'], 'doc_id':doc_name}
	return None

def get_doc_content(doc_id):
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		f, md = cl.get_file_and_metadata('/' + doc_id + '/' + doc_id + '.tex')
		if not md:
			return None

		return f.read()

	return None

def get_doc_pdf(doc_id):
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		f, md = cl.get_file_and_metadata('/' + doc_id + '/' + doc_id + '.pdf')
		if not md:
			return '???'

		return f.read()

	return '???!?'

def putDoc(docname, template=None):
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		try:
			cl.file_create_folder(docname)
		except:
			pass
		f = file(docname+'.tex','w')
		cl.put_file('/'+docname+'/'+docname+'.tex', f)

def zip_files(cl, zp, path):
	md = cl.metadata(path)
	contents = md['contents']
	for i in range(len(contents)):
		temp = contents[i]
		if bool(temp['is_dir']):
			zip_files(cl,zp,temp['path'])
		else:
			f = cl.get_file(temp['path'])
			pos = temp['path'].rfind('/')
			fname = temp['path'][pos+1:]
			print fname
			content = f.read()
			print content, type(content)
			zp.append(fname,content)




@route('/testzip')
def ziptest():
	token = request.get_cookie("access_token",secret="secretkey")
	if token:
		sess.set_token(token.key,token.secret)
		cl = client.DropboxClient(sess)
		path = '/doc1'
		myzip = InMemoryZip()
		zip_files(cl,myzip,path)
		myzip.writetofile('stuff.zip')
	

def templateList():
	pass

class InMemoryZip(object):
   def __init__(self):
       # Create the in-memory file-like object
       self.in_memory_zip = StringIO.StringIO()
      
   def append(self, filename_in_zip, file_contents):
       '''Appends a file with name filename_in_zip and contents of
          file_contents to the in-memory zip.'''
       # Get a handle to the in-memory zip in append mode
       zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED)
      
       # Write the file to the in-memory zip
       zf.writestr(filename_in_zip, file_contents)
      
       # Mark the files as having been created on Windows so that
       # Unix permissions are not inferred as 0000
       for zfile in zf.filelist:
           zfile.create_system = 0       
      
       return self
      
   def read(self):
       '''Returns a string with the contents of the in-memory zip.'''
       self.in_memory_zip.seek(0)
       return self.in_memory_zip.getvalue()
  
   def writetofile(self, filename):
       '''Writes the in-memory zip to a file.'''
       f = file(filename, "wb")
       f.write(self.read())
       f.close()
