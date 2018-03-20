# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.addons.website.models.website import slug
from odoo.http import request

class WebsiteEventControllerTag(WebsiteEventSaleController):

    # @http.route(['/event/<model("event.event"):event>/tags'], type='http', auth="public", website=True)
    # def event_register_tags(self, event, **post):
    #     if event.state == 'done':
    #         return request.redirect("/event/%s" % slug(event))
    #     tags = event.event_ticket_ids.mapped('tag_ids')
    #     values = {
    #         'event': event,
    #         'main_object': event,
    #         'range': range,
    #         'registrable': event._is_event_registrable(),
    #         'tags': tags,
    #     }
    #     return request.render("website_event_tags.event_tags_description", values)

    @http.route(['/event/<model("event.event"):event>/tags/<model("event.ticket.tag"):tag>'], type='http', auth="public", website=True)
    def event_register_tags(self, event, tag, **post):
        if event.state == 'done':
            return request.redirect("/event/%s" % slug(event))
        tags = event.event_ticket_ids.mapped('tag_ids')
        values = {
            'event': event,
            'main_object': tag,
            'range': range,
            'registrable': event._is_event_registrable(),
            'tag': tag,
        }
        return request.render("website_event_tags.event_tags_description", values)

    @http.route(['/event/<model("event.event"):event>/register'], type='http', auth="public", website=True)
    def event_register(self, event, **post):
        if event.state == 'done':
            return request.redirect("/event/%s" % slug(event))
        event = event.with_context(pricelist=request.website.get_current_pricelist().id)
        if post.get('tag') and post.get('tag').isdigit():
            tag = int(post.get('tag'))
            ticket_tag = request.env['event.ticket.tag'].search([('id', '=', tag)])
            if ticket_tag:
                event_tickets = event.event_ticket_ids.filtered(lambda t: tag in t.tag_ids.ids)
                values = {
                    'event': event,
                    'main_object': event,
                    'range': range,
                    'registrable': event._is_event_registrable(),
                    'tag': ticket_tag,
                    'event_tickets': event_tickets,
                }
                return request.render("website_event.event_description_full", values)
        return super(WebsiteEventControllerTag, self).event_register(event, **post)

    @http.route(['/event/empty_cart'], type='json', auth="public", website=True)
    def empty_cart(self):
        sale_order = request.env['website'].get_current_website().sale_get_order().sudo()
        for line in sale_order.order_line:
            if line.sudo().exists():
                sale_order.sudo()._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=None, set_qty=0)
        return True

    @http.route(['/event/<model("event.event"):event>/registration/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, event, **post):
        order = request.website.with_context(default_client_order_ref=event.name).sale_get_order(force_create=1)
        return super(WebsiteEventControllerTag, self).registration_confirm(event, **post)
