# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website.controllers.main import QueryURL

class EventTicket(website_account):

    @http.route()
    def account(self, **kw):
        response = super(EventTicket, self).account()
        user = request.env.user
        tickets_count = request.env['event.registration'].sudo().search_count([('partner_id', '=', user.partner_id.id)])
        response.qcontext.update({'event_tickets': tickets_count})
        return response

    @http.route(['/my/event-tickets',
        '/my/event-tickets/page/<int:page>',
        ], type='http', auth="user", website=True)
    def my_event_tickets(self, page=1,search='', **kw):
        event = request.env['event.registration']
        values = self._prepare_portal_layout_values()
        user = request.env.user
        registrations = event.sudo().search_count([('partner_id', '=', user.partner_id.id)])
        order = 'date_open'
        scope = (registrations + 10 - 1) / 10
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=registrations,
            page=page,
            step=10,
            scope=scope,
            url_args=kw
        )
        event_domain = [('partner_id', '=', user.partner_id.id)]
        if search:
            event_domain += ['|',('event_id','ilike', search),('name','ilike', search)]
        registrations = event.search(event_domain,order=order, limit=10, offset=pager['offset'])
        values.update({
            'registrations': registrations,
            'default_url': '/my/event-tickets',
            'pager': pager,
            'search': search,
        })
        return request.render("website_portal_event.portal_event_ticket", values)

    @http.route(['/my/event-tickets/pdf/<int:ticket_id>'], type='http', auth="user", website=True)
    def portal_get_ticket(self, ticket_id=None, **kw):
        ticket = request.env['event.registration'].browse([ticket_id])
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        pdf = request.env['report'].sudo().get_pdf([ticket_id], 'event.event_registration_report_template_badge')
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename=Registration_Badge.pdf;')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route(['/my/event-tickets/pdf/tickets'], type='http', auth="user", website=True)
    def portal_get_tickets(self, **kw):
        ticket_ids = map(int,kw.get('tickets').split('_'))
        ticket = request.env['event.registration'].browse(ticket_ids)
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        pdf = request.env['report'].sudo().get_pdf(ticket_ids, 'event.event_registration_report_template_badge')
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename=Registration_Badge.pdf;')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
