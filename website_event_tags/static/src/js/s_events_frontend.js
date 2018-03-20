odoo.define('website_event_tags.s_events_frontend', function(require) {
    'use strict';
    
	var ajax = require('web.ajax');

    $( window ).on( "load", function() {
	    // var parms = $.bbq.getState(true);
	    // if (parms.tag) {
	    // 	$('.nav-tabs a[href="#' + parms.tag + '"]').tab('show');
	    // }

		var $empty_cart = $(".o_event_empty_cart");
		$empty_cart.on("click", function (ev) {
			ev.preventDefault();
			ev.stopPropagation();
			ajax.jsonRpc('/event/empty_cart', 'call', {}).then(function(result) {
	        	if(result) {
		        	location.reload();
	        	}
			});
		});

		// var $nav = $(".nav");
		// $nav.on( "click .nav", function(el) {
		// 	if (el.target.attributes.href) {
		// 		$.bbq.pushState({'tag':el.target.attributes.href.value.split('#')[1]});
		// 	}
		// });

		$(".noRegistration").on( "click .noRegistration", function(el) {
			$("#noLogin").modal('hide');
		});
	});
});

//Fixed EventRegistrationForm bug of button and table not appear after click 'Order' button
odoo.define('website_event_tags.website_event_tags', function(require) {
    'use strict';
   
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var web_editor_base = require('web_editor.base')
    var event_registration_form = require('website_event.website_event');

    // Catch registration form event, because of JS for attendee details
    event_registration_form.EventRegistrationForm.include({
        start: function() {
            var self = this;
            $('#registration_form .a-submit')
                .off('click')
                .removeClass('a-submit')
                .click(function (ev) {
                    ev.stopPropagation();
                    // $(this).attr('disabled', true);
                    self.on_click(ev);
                });
            return this._super.apply(this, arguments);
        },
        on_click: function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var $form = $(ev.currentTarget).closest('form');
            var post = {};
            $("#registration_form select").each(function() {
                post[$(this).attr('name')] = $(this).val();
            });
            return ajax.jsonRpc($form.attr('action'), 'call', post).then(function (modal) {
                var $modal = $(modal);
                $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
                $modal.modal('show');
                $modal.on('click', '.js_goto_event', function () {
                    $modal.modal('hide');
                });
            });
        },
    });

});