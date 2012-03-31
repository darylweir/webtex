$(window).ready(function() {


    var editor = ace.edit("editor");
    var LatexMode = require("ace/mode/latex").Mode;
    var Range = require("ace/range").Range
    var session = editor.getSession();
    session.setMode(new LatexMode());

    var timer = null;

    var pushChanges = function() {
    	var content = session.getDocument().getValue();
    	$('#reload').show();
    	$.post('/doc/hanoi', content, function(data) {
    		$('#view').attr('src', function(i,val) { return val; });
    		$('#reload').hide();
    	});
	}
	
	$(session).bind('change', function() {
		if(timer) clearTimeout(timer);
		timer = setTimeout(pushChanges, 4000);
	})
});