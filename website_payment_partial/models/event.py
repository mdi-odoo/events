# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    payment_term_id = fields.Many2one('account.payment.term', string="Payment Term")
