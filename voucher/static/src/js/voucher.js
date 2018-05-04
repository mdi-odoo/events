odoo.define("voucher.voucher", function (require) {
   "use strict";
    var base = require("web_editor.base");
    var ajax = require('web.ajax');
    var core = require('web.core');

    $('.oe_website_sale').each(function () {
    	var oe_website_sale = this;
    	$(oe_website_sale).on('click', '#apply_voucher', function (ev){
    		var button = ev.currentTarget;
    		var voucher_code = $(button).parents('.input-group').find('input[name="voucher"]').val();
    		var msg_box = $(button).parents('.panel-body').find('.error_msg');
    		if (voucher_code != '') {
    			ajax.jsonRpc("/shop/payment/apply_voucher", 'call', {
	                'voucher_code': voucher_code,
	            }).then(function (data) {
                    if (data.error_msg) {
                		msg_box.empty();
                		msg_box.append('<span>' + data.error_msg + '</span>');
                    } else {
                        location.reload();
                    }
	            });
    		}
    	});
    });
});