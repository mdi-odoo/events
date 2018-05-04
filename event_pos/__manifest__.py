# -*- coding: utf-8 -*-
{
    'name': "Event POS",

    'summary': """
        Sell Event Tickets form Odoo POS""",

    'author': "Odoo India",
    'website': "http://www.odoo.com",

    # for the full list
    'category': 'POS',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'website_event_sale', 'website_event_track', 'event_barcode'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/pos_config.xml',
        'report/pos_event_registration.xml',
    ],
    'qweb': [
        'static/src/xml/attendees_template.xml',
    ],
}