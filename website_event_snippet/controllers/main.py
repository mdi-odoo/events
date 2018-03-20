from odoo import http, fields
from odoo.http import request
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from babel.dates import format_datetime, format_date


class website_event_snippet_controller(http.Controller):


	@http.route(['/website_event_snippet/render'], type='json', auth='public', website=True)
	def render_events(self, domain, limit=None, order='date_begin asc'):
		domain.append(['date_end', '>', fields.Datetime.to_string(datetime.now())])
		events = request.env['event.event'].sudo().search_read(domain, limit=limit, order=order)
		for event in events:
			city = request.env['res.partner'].sudo().search_read([('id', '=', event.get('address_id')[0])], ['city'])
			event.update({
				'city': city[0].get('city'),
				'date_begin': datetime.strftime(fields.Datetime.from_string(event.get('date_begin')).date(), '%d/%m/%Y'),
				'date_end': datetime.strftime(fields.Datetime.from_string(event.get('date_end')).date(), '%d/%m/%Y')
			})
		return events

