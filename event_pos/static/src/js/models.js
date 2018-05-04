odoo.define('pos_event.models', function (require) {
"use strict";

var models = require('point_of_sale.models');
var all_models = models.PosModel.prototype.models;

models.load_models({
        model: 'pos.config',
        fields: ['name', 'x_event_id', 'default_partner_id'],
        ids: function(self){ return [self.pos_session.config_id[0]]; },
        loaded: function(self, current_pos_id){
            for(var i=0; i < all_models.length ; i++){
                if(all_models[i].model == "product.product"){
                    break;
                }
            }
            self.current_pos_id = current_pos_id;
        },
    },{
        'before': 'product.product'
    });
models.load_models({
        model: 'event.event',
        fields: ['name', 'event_ticket_ids'],
        ids: function(self){if(self.current_pos_id[0].x_event_id){return[self.current_pos_id[0].x_event_id[0]];}
            },
        loaded: function(self, event_ids){
            for(var i=0; i < all_models.length ; i++){
                if(all_models[i].model == "product.product"){
                    break;
                }
            }
            self.event_ids = event_ids;
        },
    },{
        'before': 'product.product'
    });
models.load_models({
        model: 'event.event.ticket',
        fields: ['name', 'product_id'],
        ids: function(self){if(self.event_ids[0]){return self.event_ids[0].event_ticket_ids}},
        loaded: function(self, ticket_ids){
            var ids = [];
            for(var i=0; i<ticket_ids.length; i++){
                if(ticket_ids[i].product_id){
                    ids.push(ticket_ids[i].product_id[0]);
                }
            }
            if(ids.length > 0) // to see all products, when event not assigned
            // if(ids) // to empty POS, when event not assigned
            {
                for(var i=0; i < all_models.length ; i++){
                    if(all_models[i].model == "product.product"){
                        all_models[i].domain.push(['id', 'in', ids]);
                        break;
                    }
                }
            }
            self.ticket_ids = ticket_ids;
        },
    },{
        'before': 'product.product'
    });

//Purpose of extending this order widget is to set the default partner on every new order
var _super_posmodel = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    add_new_order: function() {
        var res = _super_posmodel.add_new_order.apply(this,arguments);
        if (this.config.default_partner_id) {
            var client = this.db.get_partner_by_id(this.config.default_partner_id[0]);
            if (client) {
                this.get_order().set_client(client);
            }
        }
    }
});

});