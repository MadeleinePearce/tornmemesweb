const urlParams = new URLSearchParams(window.location.search);

if (total_pages === 0) {
	$('#pagination-ui').hide();
} else {
	var current_page = parseInt(urlParams.get('page') || '1');
	$('#current-page').html(current_page);
	if (sponsors_on_page === 0) {
		$('#prev-button').removeClass('disabled');
		$('#prev-button-link').attr('href', '/sponsors?page=' + (current_page - 1));
	} else if (sponsors_on_page !== 0 && current_page === 1) {
		if (current_page + 1 <= total_pages) {
			$('#next-button').removeClass('disabled');
			$('#next-button-link').attr('href', '/sponsors?page=' + (current_page + 1));
		}
	} else if (sponsors_on_page !== 0 && current_page > 1) {
		$('#prev-button').removeClass('disabled');
		$('#prev-button-link').attr('href', '/sponsors?page=' + (current_page - 1));
		if (current_page + 1 <= total_pages) {
			$('#next-button').removeClass('disabled');
			$('#next-button-link').attr('href', '/sponsors?page=' + (current_page + 1));
		}
	}
}
