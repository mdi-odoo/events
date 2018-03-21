# -*- coding: utf-8 -*-
{
    "name": "Website Partial Payment",
    'summary': "Web",
    'description': """
Ability to make partial payment on ecommerce
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['website_sale', 'website_event_sale'],
    'data': [
        'views/event_views.xml',
        'views/website_sale_templates.xml'
    ],
    'license': 'OEEL-1',
    'installable': True
}