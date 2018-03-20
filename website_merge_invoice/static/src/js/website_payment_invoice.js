odoo.define('website_merge_invoice.website_merge_invoice', function (require) {
	"use strict";
	$(document).ready(function() {
		if ($('#div_to_create_invoice').length) {
			var confirm_button = $(document).find('a[href^="/shop/checkout"]');
			$('input[name="is_create_invoice"]').on('change', function (ev){
			    console.log("test");
				confirm_button.attr('href', "/shop/checkout?is_create_invoice=" + (ev.currentTarget.checked == true ? 1 : 0));
			});
		}
	});
});