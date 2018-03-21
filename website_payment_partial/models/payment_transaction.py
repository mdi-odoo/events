# -*- coding: utf-8 -*-

import logging
from odoo import models, _
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _generate_and_pay_invoice(self, tx, acquirer_name):
        tx.sale_order_id._force_lines_to_invoice_policy_order()

        # force company to ensure journals/accounts etc. are correct
        # company_id needed for default_get on account.journal
        # force_company needed for company_dependent fields
        ctx_company = {'company_id': tx.sale_order_id.company_id.id,
                       'force_company': tx.sale_order_id.company_id.id}
        created_invoice = tx.sale_order_id.with_context(**ctx_company).action_invoice_create()
        created_invoice = self.env['account.invoice'].browse(created_invoice).with_context(**ctx_company)

        if created_invoice:
            _logger.info('<%s> transaction completed, auto-generated invoice %s (ID %s) for %s (ID %s)',
                         acquirer_name, created_invoice.name, created_invoice.id, tx.sale_order_id.name, tx.sale_order_id.id)

            created_invoice.action_invoice_open()
            if tx.acquirer_id.journal_id:
                amount_to_pay = created_invoice.amount_total
                if tx.amount < created_invoice.amount_total:
                    amount_to_pay = tx.amount
                created_invoice.with_context(tx_currency_id=tx.currency_id.id).pay_and_reconcile(tx.acquirer_id.journal_id, pay_amount=amount_to_pay)
                if created_invoice.payment_ids:
                    created_invoice.payment_ids[0].payment_transaction_id = tx
            else:
                _logger.warning('<%s> transaction completed, could not auto-generate payment for %s (ID %s) (no journal set on acquirer)',
                                acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
        else:
            _logger.warning('<%s> transaction completed, could not auto-generate invoice for %s (ID %s)',
                            acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)

    def _confirm_so(self, acquirer_name=False):
        for tx in self:
            # check tx state, confirm the potential SO
            if tx.sale_order_id and tx.sale_order_id.state in ['draft', 'sent']:
                # verify SO/TX match, excluding tx.fees which are currently not included in SO
                payment_amount = tx.sale_order_id.advance_payment and tx.sale_order_id.get_advance_payment_amount(tx.sale_order_id.get_event_payment_term()) or tx.sale_order_id.amount_total
                amount_matches = float_compare(tx.amount, payment_amount, 2) == 0
                if amount_matches:
                    if not acquirer_name:
                        acquirer_name = tx.acquirer_id.provider or 'unknown'
                    if tx.state == 'authorized' and tx.acquirer_id.auto_confirm == 'authorize':
                        _logger.info('<%s> transaction authorized, auto-confirming order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        tx.sale_order_id.with_context(send_email=True).action_confirm()
                    if tx.state == 'done' and tx.acquirer_id.auto_confirm in ['confirm_so', 'generate_and_pay_invoice']:
                        _logger.info('<%s> transaction completed, auto-confirming order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        tx.sale_order_id.with_context(send_email=True).action_confirm()

                        if tx.acquirer_id.auto_confirm == 'generate_and_pay_invoice':
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