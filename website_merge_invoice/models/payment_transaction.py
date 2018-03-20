# -*- coding: utf-8 -*-

import logging

from odoo import models, _
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _confirm_so(self, acquirer_name=False):
        for tx in self:
            # check tx state, confirm the potential SO
            if tx.sale_order_id and tx.sale_order_id.state in ['draft', 'sent']:
                # verify SO/TX match, excluding tx.fees which are currently not included in SO
                amount_matches = float_compare(tx.amount, tx.sale_order_id.amount_total, 2) == 0
                if amount_matches:
                    if not acquirer_name:
                        acquirer_name = tx.acquirer_id.provider or 'unknown'
                    if tx.state == 'authorized' and tx.acquirer_id.auto_confirm == 'authorize':
                        _logger.info('<%s> transaction authorized, auto-confirming order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        tx.sale_order_id.with_context(send_email=True).action_confirm()
                    if tx.state == 'done' and tx.acquirer_id.auto_confirm in ['confirm_so', 'generate_and_pay_invoice']:
                        _logger.info('<%s> transaction completed, auto-confirming order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        tx.sale_order_id.with_context(send_email=True).action_confirm()

                        if tx.acquirer_id.auto_confirm == 'generate_and_pay_invoice' and tx.sale_order_id.to_create_invoice:
                            self._generate_and_pay_invoice(tx, acquirer_name)
                    elif tx.state not in ['cancel', 'error'] and tx.sale_order_id.state == 'draft':
                        _logger.info('<%s> transaction pending/to confirm manually, sending quote email for order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        tx.sale_order_id.force_quotation_send()
                else:
                    _logger.warning(
                        '<%s> transaction AMOUNT MISMATCH for order %s (ID %s): expected %r, got %r',
                        acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id,
                        tx.sale_order_id.amount_total, tx.amount,
                    )
                    tx.sale_order_id.message_post(
                        subject=_("Amount Mismatch (%s)") % acquirer_name,
                        body=_("The sale order was not confirmed despite response from the acquirer (%s): SO amount is %r but acquirer replied with %r.") % (
                            acquirer_name,
                            tx.sale_order_id.amount_total,
                            tx.amount,
                        )
                    )
