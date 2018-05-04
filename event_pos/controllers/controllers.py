# -*- coding: utf-8 -*-
import base64
import requests
import uuid
from collections import OrderedDict
from odoo import http, fields
from odoo.http import request

class EventPos(http.Controller):
    
    @http.route(['/pos/resigter_attendees'], type='json', auth="user")
    def registration_confirm(self, **post):
        
        Attendees = request.env['event.registration']
        registrations = post.get('attendees')
        origin = post.get('order_ref')
        no_of_tickets = []
        partner_id = request.env['res.partner'].browse(int(registrations[0].get('partner_id')))
        
        for registration in registrations:
            query = "INSERT INTO event_registration (create_date,barcode, state, origin, name, event_id, phone, partner_id, email, event_ticket_id) values (%s , %s,%s, %s, %s, %s , %s, %s, %s, %s) RETURNING id;"
            
            data = OrderedDict([
            ('create_date',fields.Datetime.now()),
            ('barcode',str(int(uuid.uuid4().bytes[:8].encode('hex'), 16))),
            ('state','draft'),
            ('origin',origin),
            ('name', registration.get('name', partner_id.name)),
            ('event_id', registration.get('event_id',False)),
            ('phone' , registration.get('phone', partner_id.phone)),
            ('partner_id' , partner_id.id),
            ('email' ,registration.get('email', partner_id.email)),
            ('event_ticket_id' , int(registration.get('ticket_id'))) ])
            
            params = tuple([str(val) for val in data.values()])
            request.env.cr.execute(query,params)
            result = request.env.cr.fetchone()[0]
            no_of_tickets.append(result)

        tickets = Attendees.browse(no_of_tickets)
        tickets.with_context(from_pos=True,tracking_disable=True).write({'state':'open'})
        return tickets.ids

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
    