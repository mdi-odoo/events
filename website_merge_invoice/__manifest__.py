# -*- coding: utf-8 -*-
{
    "name": "Website Merge Invoice",
    'summary': "Web",
    'description': """
Website Payment Invoice
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['website_sale','website_event','website_portal_sale'],
    'data': [
        'views/templates.xml',
        'wizard/sale_orders_to_invoice_views.xml',
    ],
    'license': 'OEEL-1',
}