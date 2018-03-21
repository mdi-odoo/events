odoo.define('website_portal_event.website_portal_event', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
	    $('table.table_checkbox_ticket').on('change', 'input.main_checkbox_tickets', function (event) {
	    	var val = $(this).is(':checked') || false;
	    	$('input.checkbox_ticket').each(function () {
	    		this.checked = val;
	    	});
	    	set_print_tickets();
	    });

	    $('table.table_checkbox_ticket').on('change', 'input.checkbox_ticket', function (event) {
	    	var val = $(this).is(':checked') || false;
	    	var main_checkbox = $('input.main_checkbox_tickets')
	    	if (!val && main_checkbox.is(':checked')) {
	    		main_checkbox.attr('checked',false);
	    	}
	    	set_print_tickets();
	    });
	    
	    function set_print_tickets(){
	    	var ticket_ids = [];
	    	var $ancher = $('a.prints');
	    	$('input.checkbox_ticket').each(function () {
	    		if ($(this).is(':checked')) {
	    			ticket_ids.push($(this).data('ticket_id'));
	    		}
	    	});
	    	if (ticket_ids.length) {
	    		$ancher.removeClass('hidden');
	    	}else {
	    		$ancher.addClass('hidden');
	    	}
    		$ancher.attr('href', $ancher.attr('href').split('?')[0]+'?tickets='+ticket_ids.join('_'));
	    }

	    if ($('#seacrh_box').val() != ""){
	    	$('a.clear_search').removeClass('hidden');
	    } else {
	    	$('a.clear_search').addClass('hidden');
	    }
    	$('a.clear_search').on('change', function (event) {
    		$('#seacrh_box').val('');
    	});

	});
});