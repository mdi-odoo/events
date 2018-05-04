# -*- coding: utf-8 -*-
{
    'name': 'Voucher',
    'version': '1.0',
    'category': 'Others',
    'description': """
- This module allows you to apply a discount coupon to the sale.
- The discount coupon is either a discount in percentage or amount.
- The discount coupon may be related to the sale:
     -an ticket linked to an event
     -of an article
   for all customers or for a named customer.
    """,
    'author': '',
    'depends': ['base', 'event', 'account', 'website_sale'],
    'init_xml': [],
    'data': [
        'views/sale_order.xml',
        'views/voucher.xml',
        'views/templates.xml',
        'data/ir_cron.xml'
    ],
    'test': [],
    'installable': True,
    'active': False
}
