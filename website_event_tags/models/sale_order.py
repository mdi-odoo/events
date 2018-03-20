from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
	_inherit = "sale.order"

	def is_uniq_event(self, event):
		if len(self.order_line):
			if len(self.order_line.mapped('event_id')) == 1 and self.order_line.mapped('event_id') == event:
				return True
			return False
		return True