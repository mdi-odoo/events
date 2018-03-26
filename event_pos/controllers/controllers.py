# -*- coding: utf-8 -*-
import base64
import requests

from odoo import http
from odoo.http import request


class EventPos(http.Controller):

    @http.route(['/pos/resigter_attendees'], type='json', auth="user")
    def registration_confirm(self, **post):
        Attendees = request.env['event.registration']
        registrations = post.get('attendees')
        for registration in registrations:
            registration['event_id'] = request.env['event.event'].browse(int(registration.get('event_id')))
            registration['event_ticket_id'] = request.env['event.event.ticket'].browse(int(registration.get('ticket_id'))).id
            registration['partner_id'] = request.env['res.partner'].browse(int(registration.get('partner_id')))
            registration['origin'] = post.get('order_ref')

            Attendees += Attendees.sudo().with_context(**{'from_pos':True}).create(
                Attendees._prepare_attendee_values(registration))
        return Attendees.ids

    @http.route(['/pos/get_as_base64'], type='json', auth="user")
    def get_as_base64(self, **post):
        content = request.env['report'].barcode('Code128', post.get('barcode'), width=500, height=120, humanreadable=1)
        return base64.b64encode(content)


    @http.route(['/pos/get_event_logo'], type='json', auth="user")
    def get_organizer_logo(self, **post):
        event = request.env['event.event'].browse(int(post.get('event')))
        if event.organizer_id:
            return event.organizer_id.image#company_id.logo_web
        return False
    