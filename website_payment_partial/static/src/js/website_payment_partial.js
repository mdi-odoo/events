odoo.define('website_payment_partial.website_payment_partial', function(require){
	"use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var ajax = require('web.ajax');

    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;
        var order_id = $("#partial_payment_block").data('order_id');
        var adv_payment = $("#partial_payment_block").data('adv_payment');
        if (adv_payment == 0) {
            $(oe_website_sale).find("input[name='payment_option'][value='0']").prop('checked', true);
        }
        else {
            $(oe_website_sale).find("input[name='payment_option'][value='1']").prop('checked', true);       	
        }
        $(oe_website_sale).on('change', "input[name='payment_option']", function(ev){
        	ajax.jsonRpc('/shop/change_payment_option', 'call', {
        		'order_id': order_id,
        		'advance_payment': $(ev.currentTarget).val() == '1' ? true : false
        	}).then(function(data){
        		window.location.reload();
        	})
        });
    });
});