# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    voucher_code = fields.Char('Voucher', size=5)
    voucher_ids = fields.Many2many('voucher', 'rel_sale_order_voucher', 'sale_id', 'voucher_id', 'Used voucher')

    @api.multi
    def get_first_event(self):
        """
        Get the first sale order line with an event (Customer choice)
        :return: An event
        """
        self.ensure_one()
        for line in self.order_line:
            if line.event_id:
                return line.event_id

    @api.multi
    def check_voucher_code(self):
        self.ensure_one()
        voucher = self.env['voucher'].search([('name', '=', self.voucher_code),
                                              ('stage', 'in', ['new', 'sent']),
                                              ('is_template', '=', False),
                                              ('endorsable', '=', True)])
        if not voucher:
            raise ValidationError(_('No valid voucher found !'))
        sol_values = voucher.consume_voucher(self)
        self.voucher_ids += voucher
        self.order_line += self.env['sale.order.line'].new(sol_values)
        self.voucher_code = ''


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_reward_line = fields.Boolean()
