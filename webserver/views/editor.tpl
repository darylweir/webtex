<!DOCTYPE html>
<html>
<head>
	<title>WebTex</title>
	<link href="/static/style.css" rel="stylesheet">
	<script src="/static/ace.js" charset="utf-8"></script>
	<script src="/static/mode-latex.js" charset="utf-8"></script>
	<script>
    window.onload = function() {
        var editor = ace.edit("editor");
        var LatexMode = require("ace/mode/latex").Mode;
    	editor.getSession().setMode(new LatexMode());
    };
    </script>
</head>
<body>
	<div id="editor-header">
		<div style="float: right">
			<div class="save button">Save</div>
		</div>
		<span class="doc-name">{{doc_name}}</span><br/>
	</div>
	<div id="editor">{{doc_content}}</div>
	<iframe src="/doc/{{doc_name}}/pdf"
		    frameborder="0" id="view"></iframe>
</body>
</html>
