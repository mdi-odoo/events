# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate


class EventTicketTag(models.Model):
    _name = "event.ticket.tag"
    _inherit = ['website.seo.metadata']
    _description = 'Event Ticket Tags'
    _order = 'name'

    def _default_content(self):
        return '''
            <section class="s_text_block">
                <div class="container">
                    <div class="row">
                        <div class="col-md-12 mb16 mt16">
                            <p class="o_default_snippet_text text-center">''' + _("Place your tag content here...") + '''</p>
                        </div>
                    </div>
                </div>
            </section>
        '''

    name = fields.Char(required=True)
    html_content = fields.Html('Content', default=_default_content, translate=html_translate, sanitize=False)
    description = fields.Text('Description', translate=True, default="Tag Description")


class EventTicket(models.Model):

    _inherit = 'event.event.ticket'

    tag_ids = fields.Many2many('event.ticket.tag', string='Tags')
    color = fields.Char(help="Color of the Ticket eg. 'yellow' or '#ff0505'", default='grey')


class Event(models.Model):

    _inherit = 'event.event'

    official_url = fields.Char('Official Url')
    is_tags_enable = fields.Boolean('Enable Tags')
