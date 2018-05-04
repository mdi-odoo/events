odoo.define('event_pos.screens', function(require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var gui = require('point_of_sale.gui');
    var Model = require('web.Model');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var session = require('web.session');
    var models = require('point_of_sale.models');



    var PaymentScreen = screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
            if (this.order_is_valid(force_validation)) {
                if (this.pos.config.x_event_id) {
                    if (session.attendeeDetails) {
                        var self = this;
                        $.blockUI()
                        ajax.jsonRpc('/pos/resigter_attendees', 'call', {
                            attendees: session.attendeeDetails,
                            order_ref: this.pos.get_order().name,
                        }).then(function(result) {
                            session.ticket_ids = result;
//                            self.chrome.do_action('event_pos.report_event_registration_badge_pos', {
//                                additional_context: {
//                                    active_ids: result,
//                                }
//                            });
                        }).done(function() {
                            self.finalize_validation();
                            $.unblockUI()
                        }).fail(function(error) {
                        	$.unblockUI()
                        	var msg = arguments && arguments[1] && arguments[1].data && arguments[1].data.message;
                            self.gui.show_popup('error', {
                                'title': _t('No Ticket'),
                                'body': msg,
                            });
                        });
                    } else {
                        this.gui.show_popup('error', {
                            'title': _t('No Ticket'),
                            'body': _t('No Ticket Found.'),
                        });
                    }
                } else {
                    this.finalize_validation();
                }
            }
        },
    });

    /*
     *   Implementation logic for,
     *  Popup and get the filled details
     *
     */
    var AttendeesDetailPopup = PopupWidget.extend({
        template: 'AttendeesDetailPopup',
        show: function(options) {
            var self = this;
            this._super(options);
            if (this.pos.config.x_event_id) {
                this.$('.event_btn_confirm').click(function() {
                    var contain = [];
                    var counter = 1;
                    var tempDict = {};
                    var formValid = true;
                    var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;


                    $(".event input").each(function() {
                        if (counter == 1) {
                            if ($(this).val()) {
                                tempDict.name = $(this).val();
                            }
                            counter++;
                        } else if (counter == 2) {
                            if ($(this).val()) {
                                tempDict.email = $(this).val();
                                if (tempDict.email) {
                                    if (!re.test(tempDict.email)) {
                                        formValid = false;
                                        $(this).css('background-color', '#ffb4b47d');
                                    } else {
                                        $(this).css('background-color', 'white');
                                    }
                                }
                            }
                            counter++;
                        } else if (counter == 3) {
                            if ($(this).val()) {
                                tempDict.phone = $(this).val();
                            }

                            tempDict.event_id = $(this).attr('event_id');
                            tempDict.ticket_id = $(this).attr('ticket_id');
                            tempDict.partner_id = $(this).attr('partner_id');
                            tempDict.event_name = $(this).attr('event_name');

                            contain.push(tempDict);
                            tempDict = {};
                            counter = 1;
                        }
                    });
                    if(formValid) {
                        session.attendeeDetails = contain;
                        self.gui.show_screen('payment');
                    }
                });
            }
        },
    });

    gui.define_popup({name:'attendees-detail', widget: AttendeesDetailPopup});

    screens.ActionpadWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            if (this.pos.config.x_event_id) {
                this.$('.pay').click(function() {
                    var client_details = self.pos.get_client();
                    var order = self.pos.get_order();
                    var has_valid_product_lot = _.every(order.orderlines.models, function(line) {
                        return line.has_valid_product_lot();
                    });
                    if (!has_valid_product_lot) {
                        self.gui.show_popup('confirm', {
                            'title': _t('Empty Serial/Lot Number'),
                            'body': _t('One or more product(s) required serial/lot number.'),
                            confirm: function() {
                                self.gui.show_screen('payment');
                            },
                        });
                    } else if (!client_details) {
                        self.gui.show_screen('clientlist');
                    } else {
                        self.gui.show_screen('products');
                        
                        // Get OrderDetails 1
                        var orderDetails = [];
                        var def = [];
                        var event_valid = true;
                        var client = self.pos.get_client();
                        var orderlines = self.pos.get_order().get_orderlines();
                        _.each(orderlines, function(orderline) {
                            var level2 = $.Deferred();
                            def.push(level2);
                            (new Model('event.event.ticket')).call('search_read', [
                                [
                                    ['product_id', '=', orderline.product.id]
                                ]
                            ], { limit: 1 }).then(function(ticket) {
                                ticket = ticket[0];
                                if (ticket.seats_availability == "limited" && ticket.seats_available < orderline.quantity) {
                                    event_valid = false;
                                } else {
                                    if (client) {
                                        orderDetails.push({
                                            ticket_name: ticket.name,
                                            qty: orderline.quantity,
                                            product_id: orderline.product.id,
                                            ticket_id: ticket.id,
                                            event_id: ticket.event_id[0],
                                            event_name: ticket.event_id[1],                            
                                            partner_id: client.id,
                                            client_name: client.name,
                                            client_phone: client.phone ? client.phone : '',
                                            client_email: client.email ? client.email : '',
                                        });
                                    }
                                }
                                level2.resolve();
                            });
                        });
                        $.when.apply(this, def).then(function() {
                            if (event_valid) {
                                session.orderDetails = orderDetails;
                                if (orderDetails.length) {
                                    self.gui.show_popup('attendees-detail', orderDetails);
                                }
                            } else {
                                self.gui.show_popup('error', {
                                    'title': _t('No More Ticket Available'),
                                    'body': _t('One or More Tickets in orderline has Sold Out.'),
                                });
                            }
                        });
                    }
                });
                this.$('.set-customer').click(function() {
                    self.gui.show_screen('clientlist');
                });
            }
        },
    });

    screens.ReceiptScreenWidget.include({

        render_change: function() {
            this._super();

            if (this.pos.config.x_event_id) {
                this.render_event_badge();
            }
        },
        render_event_badge: function() {
            if (session.ticket_ids) {
                var def = [];
                var bookingDetails = [];
                var self = this;
                var event_logo = "";
                var level1 = $.Deferred();
                def.push(level1);
                ajax.jsonRpc('/pos/get_event_logo', 'call', {event:self.pos.config.x_event_id[0]}).then(function(logo) {
                    if (logo) {
                        event_logo = 'data:image/png;base64,'+logo;
                    } else {
                        event_logo = self.pos.company_logo_base64;
                    }
                    level1.resolve();
                });
                _.each(session.ticket_ids, function(register_id) {
                    var level2 = $.Deferred();
                    def.push(level2);
                    (new Model('event.registration')).call('search_read', [[['id', '=', register_id]]]).then(function(booking) {
                        booking = booking[0];
                        bookingDetails.push({
                            barcode: booking.barcode,
                            email: booking.email,
                            name: booking.name,
                            phone: booking.phone,
                            event_name: self.pos.config.x_event_id[1],
                            ticket_name: booking.event_ticket_id[1],
                        });
                        level2.resolve();
                    });
                });
                $.when.apply($, def).then(function() {
                    self.$('.pos-receipt-container').append(QWeb.render('EventBadgePos', {
                        widget: self,
                        url:window.location.origin,
                        events: bookingDetails,
                        company_logo:event_logo,
                    }));
            
//                    _.each(bookingDetails, function(event) {
//                        ajax.jsonRpc('/pos/get_as_base64', 'call', {barcode:event.barcode}).then(function(image_base64) {
//                            var newEvent = {
//                                event: event,
//                                widget: self,
//                                barcode_base64:image_base64,
//                                company_logo:event_logo,
//                            };
//                            var receipt = QWeb.render('XmlReceiptPOS',newEvent);
//                            self.pos.proxy.print_receipt(receipt);
//                        });
//                    });
                });
            }
        },
    });
    
    var ClientListScreenWidget = screens.ClientListScreenWidget.extend({
        show: function() {
            this._super();
            var self = this;
            if (this.pos.config.x_event_id) {
                this.$('.searchbox .search-clear').click();
            	this.$('.next').click(function(){
                    self.save_changes();
                    self.gui.back();    // FIXME HUH ?
                    
                    // Get orderDetails 2
                    var orderDetails = [];
                    var def = [];
                    var event_valid = true;
                    var client = self.pos.get_client();
                    var orderlines = self.pos.get_order().get_orderlines();
                    _.each(orderlines, function(orderline) {
                        var level2 = $.Deferred();
                        def.push(level2);
                        (new Model('event.event.ticket')).call('search_read', [
                            [
                                ['product_id', '=', orderline.product.id]
                            ]
                        ], { limit: 1 }).then(function(ticket) {
                            ticket = ticket[0];
                            if (ticket.seats_availability == "limited" && ticket.seats_available == 0) {
                                event_valid = false;
                            } else {
                                if (client) {
                                    orderDetails.push({
                                        ticket_name: ticket.name,
                                        qty: orderline.quantity,
                                        product_id: orderline.product.id,
                                        ticket_id: ticket.id,
                                        event_id: ticket.event_id[0],
                                        event_name: ticket.event_id[1],                            
                                        partner_id: client.id,
                                        client_name: client.name,
                                        client_phone: client.phone ? client.phone : '',
                                        client_email: client.email ? client.email : '',
                                    });
                                }
                            }
                            level2.resolve();
                        });
                    });
                    $.when.apply(this, def).then(function() {
                        if (event_valid) {
                            session.orderDetails = orderDetails;
                            if (orderDetails.length) {
                                self.gui.show_popup('attendees-detail', orderDetails);
                            }
                        } else {
                            self.gui.show_popup('error', {
                                'title': _t('No More Ticket Available'),
                                'body': _t('One or More Tickets in orderline has Sold Out.'),
                            });
                        }
                    });
                });
            }
        },
    });
    gui.define_screen({ name: 'clientlist', widget: ClientListScreenWidget });
});
