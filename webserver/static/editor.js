$(window).ready(function() {


    var editor = ace.edit("editor");
    var LatexMode = require("ace/mode/latex").Mode;
    var Range = require("ace/range").Range
    var session = editor.getSession();
    session.setMode(new LatexMode());

    var timer = null;
    var txid = null;
    var pollId = null;

    var pullChanges = function() {
        $('#view').attr('src', function(i,val) { return val; });
        $('#reload').hide();
    }

    var checkForDone = function() {
	console.log('checking');
        $.post('/job/' + docName + '/' + txid, function(data) {
            if(data.finished) {
		console.log('notified done');
                pullChanges();
                clearInterval(pollId);
            }
        });
    }

    var pushChanges = function() {
    	var content = session.getDocument().getValue();
    	$('#reload').show();
    	$.post('/doc/' + docName, content, function(data) {
    		txid = data.txid;
            pollId = setInterval(checkForDone, 1000);
    	});
	}
	
	$(session).bind('change', function() {
		if(timer) clearTimeout(timer);
		timer = setTimeout(pushChanges, 4000);
	})
});
