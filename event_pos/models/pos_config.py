# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    x_event_id = fields.Many2one('event.event', string='Event')
    default_partner_id = fields.Many2one('res.partner', string="Default Partner", domain=[('customer', '=', True)], help="If partner is set, that partner will be set by default on every new order for this pos.")
