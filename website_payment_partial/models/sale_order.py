# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    advance_payment = fields.Boolean()

    def get_advance_payment_amount(self, payment_term):
        self.ensure_one()
        payment_amount = self.amount_total
        result = payment_term.with_context(currency_id=self.company_id.currency_id.id).compute(value=self.amount_total)[0]
        if result:
            payment_amount = result[0][1]
        return payment_amount

    def get_event_payment_term(self):
        self.ensure_one()
        payment_term = False
        event_lines = self.order_line.filtered(lambda l: l.event_ticket_id)
        if event_lines and event_lines.ids:
            payment_term = event_lines[0].event_ticket_id.event_id.payment_term_id
        return payment_term
