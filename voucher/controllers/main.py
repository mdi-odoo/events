# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import ValidationError


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/payment/apply_voucher'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def delivery_check(self, voucher_code=''):
        result = {}
        if voucher_code is not '':
            order = request.website.sale_get_order()
            order.voucher_code = voucher_code
            try:
                order.check_voucher_code()
            except ValidationError as e:
                result['error_msg'] = e.name
        return result
