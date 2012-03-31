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
	<div id="editor"></div>
	<div id="view">VIEW</div>
</body>
</html>
