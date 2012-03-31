<!DOCTYPE html>
<html>
<head>
	<title>WebTeX - your documents</title>
	<link href="/static/blueprint.css" rel="stylesheet">
	<link href="http://fonts.googleapis.com/css?family=Crete+Round" rel="stylesheet" type="text/css">
	<link href="/static/jquery.dataTables.css" rel="stylesheet">
	<link href="/static/style.css" rel="stylesheet">
	<script src="/static/jquery-1.7.2.min.js"></script>
	<script src="/static/jquery.dataTables.min.js"></script>
	<script src="/static/doclist.js"></script>

	<style type="text/css">
	#dark {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 50;
		background-color: rgba(0,0,0,0.5);
	}

	#newdialog {
		position: fixed;
		left: 50%;
		top: 50%;
		width: 320px;
		margin-left: -160px;
		z-index: 100;
		background-color: white;
		border: 2px solid #333;
		border-radius: 10px;
	}

	#newdialog .title {
		text-align: center;
		border-bottom: 1px solid #AAA;
	}

	#newdialog .content {
		padding: 0.5em;
	}

	#newdialog label {
		margin-right: 1em;
	}

	#newdialog .buttons {
		text-align: right;
		margin: 1em;
	}

	.button {
		display: inline-block;
		border: 1px solid #AAA;
		background-color: #CCC;
		color: black;
		padding: 0 0.5em 0 0.5em;
		cursor: pointer;
		margin-right: 1em;
	}

	.toolbar .name {
		font-size: 200%;
	}

	#create {
		display: inline-block;
		border: 1px solid #363;
		background-color: #6A6;
		border-radius: 3px;
		color: white;
		padding: 0 0.5em 0 0.5em;
		cursor: pointer;
	}

	#create:hover {
		background-color: #9C9;
		border-color: #6A6;
	}

	.doclist {
		margin-top: 1em;
	}

	#docs {
		border: 1px solid #CCC;
	}
	</style>
</head>
<body>
<div class="container">
	<div class="span-24 toolbar">
		<div class="name">{{name}} - Documents</div>
		<div id="create">Create New Document</div>
	</div>
	<div class="span-24 doclist">
		<div>
			<table id="docs">
				<thead>
					<tr>
						<th>Document name</th>
						<th>Last modified</th>
					</tr>
				</thead>
				<tbody>
				{{!docs}}
				</tbody>
			</table>
		</div>
	</div>
	<div class="span-24 footer">
	WebTeX Copyright &copy; 2012 Iain McGinniss, Daryl Weir, Lauren Norrie.
	</div>
</div>
<div id="dark" style="display: none"></div>
<div id="newdialog" style="display: none">
	<h2 class="title">Create New Document</h2>
	<div class="content">
		<label for="newDocName">Name:</label> <input id="newDocName" name="newDocName" type="text"></input><br>
		<label for="newDocTemplate">Template:</label>
		<select id="newDocTemplate" name="newDocTemplate">
			{{!templates}}
		</select>
	</div>
	<div class="buttons">
		<div class="ok button">OK</div>
		<div class="cancel button">Cancel</div>
	</div>
</div>
</body>
</html>
