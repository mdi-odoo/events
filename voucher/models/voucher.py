# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import uuid
from odoo.exceptions import ValidationError


class Voucher(models.Model):
    _name = 'voucher'
    _inherit = 'mail.thread'

    @api.model
    def compute_default_name(self):
        return uuid.uuid4().hex[:5]

    name = fields.Char(size=5, default=compute_default_name, required=True, copy=False)
    stage = fields.Selection([('new', 'New'), ('sent', 'Sent'), ('used', 'Used'), ('out_of_date', 'Out of Date')],
                             default='new', track_visibility='onchange', copy=False)
    date_validity_from = fields.Date(required=True)
    date_validity_to = fields.Date(required=True)
    voucher_type = fields.Selection([('amount', 'Amount'), ('percentage', 'Percentage')], required=True, string='Type')
    voucher_value = fields.Float('Value', default=0.)
    recipient_id = fields.Many2one('res.partner', string='Recipient')
    endorsable = fields.Boolean(default=True)
    is_template = fields.Boolean(string='Template', copy=False)
    event_ids = fields.Many2many('event.event', 'rel_voucher_event', 'voucher_id', 'event_id')
    partner_tag_ids = fields.Many2many('res.partner.category', 'rel_voucher_res_partner_category', 'voucher_id',
                                       'res_partner_category_id', string='Partner Tags')
    consumed_partner_ids = fields.Many2many('res.partner', 'rel_voucher_res_partner', 'voucher_id', 'partner_id',
                                            string='Partner who used this voucher', copy=False)

    @api.one
    @api.constrains('name', 'stage')
    def _check_unique_same_active_code(self):
        if self.stage not in ['used', 'out_of_date']:
            if self.search_count([('stage', 'not in', ['used', 'out_of_date']), ('name', '=', self.name)]) > 1:
                raise ValidationError(_('You can\'t have 2 active vouchers with the same code'))

    @api.multi
    def is_valid(self, check_date=fields.Date.context_today):
        self.ensure_one()
        if self.date_validity_from < check_date < self.date_validity_to:
            return True
        raise ValidationError(_('Voucher not applicable for this date'))

    @api.multi
    def is_partner_allowed(self, partner):
        self.ensure_one()
        if self.recipient_id and self.recipient_id == partner or not self.partner_tag_ids:
            return True

        if self.env['res.partner'].search_count([('category_id', 'child_of', self.partner_tag_ids.ids),
                                                 ('id', '=', partner.id)]):
            return True
        raise ValidationError(_('Voucher not applicable for this customer'))

    @api.multi
    def is_event_allowed(self, event_ids):
        self.ensure_one()
        if not self.event_ids or any(event in self.event_ids for event in event_ids):
            return True
        raise ValidationError(_('Voucher not applicable for this event'))

    @api.multi
    def compute_amount(self, sale_order, event_ids):
        self.ensure_one()
        if self.voucher_type == 'amount':
            return - self.voucher_value
        base_percent_total = 0
        if not self.event_ids:
            base_percent_total = sale_order.amount_total
        else:
            base_percent_total = \
                sum(sol.price_subtotal for sol in sale_order.order_line.filtered(lambda sol:
                                                                                 sol.event_id in self.event_ids))

        return self.voucher_value and - base_percent_total / 100 * self.voucher_value or 0.

    @api.model
    def get_voucher_product(self):
        voucher_product_id = self.env['ir.config_parameter'].get_param('voucher_product_id', default=False)
        if not voucher_product_id or not voucher_product_id.isdigit():
            raise ValidationError(_('Voucher Product is not configured. '
                                    'Ask someone who have access rights to configure this product'))
        return self.env['product.product'].browse(int(voucher_product_id))

    @api.multi
    def consume_voucher(self, sale_order):
        self.ensure_one()
        event_ids = sale_order.order_line.mapped('event_id')
        self.is_valid(check_date=sale_order.date_order)
        self.is_partner_allowed(sale_order.partner_id)
        self.is_event_allowed(event_ids)
        if sale_order.partner_id in self.consumed_partner_ids:
            raise ValidationError(_('You can’t use the same voucher twice'))
        self.consumed_partner_ids += sale_order.partner_id
        if self.recipient_id:
            self.stage = 'used'
        product_id = self.get_voucher_product()
        return {
            'product_id': product_id,
            'name': product_id.name + (product_id.description_sale and '\n' + product_id.description_sale or '') +
                    ' (Code: {})'.format(self.name),
            'is_reward_line': True,
            'price_unit': self.compute_amount(sale_order, event_ids)
        }

    @api.model
    def update_out_of_date_state(self):
        today = fields.Date.today()
        self.search([('stage', 'in', ['new', 'sent']),
                     ('is_template', '=', False),
                     ('date_validity_to', '<', today)]).write({'stage': 'out_of_date'})
