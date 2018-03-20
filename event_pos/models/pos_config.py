# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    x_event_id = fields.Many2one('event.event', string='Event')
