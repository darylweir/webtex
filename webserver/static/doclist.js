function createNewDoc() {

	var content = $('<div>');
	showDialog('New Document', content, function() {

	});
}

function clearDialog() {
	$('#newDocName').val('');
	$('#newDocTemplate').val($('#newDocTemplate:first').val());
}

function initDialog() {
	$('#dialog .cancel').click(function() {
		$('#dialog').hide();
	});

	$('#dialog .ok').click(function() {

	});
}

$(window).ready(function() {
	initDialog();
	$('#create').click(createNewDoc);
	$('#docs').dataTable();
});