<!DOCTYPE html>
<html>
<head>
	<title>WebTex</title>
	<link href="/static/style.css" rel="stylesheet">
	<script src="/static/ace.js" charset="utf-8"></script>
	<script src="/static/mode-latex.js" charset="utf-8"></script>
	<script src="/static/jquery-1.7.2.min.js"></script>
	<script>
	var docName = '{{doc_name}}';
	</script>
	<script src="/static/editor.js"></script>
</head>
<body>
	<div id="editor-header">
		<span class="doc-name">{{doc_name}}</span><br/>
		<div id="reload" style="display: none"><img src="/static/loading.gif" width="66" height="66"></img></div>
	</div>
	<div id="editor">{{doc_content}}</div>
	<iframe id="view" src="/doc/{{doc_name}}/pdf"
		    frameborder="0" id="view"></iframe>

</body>
</html>
