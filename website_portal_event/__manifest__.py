# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Event Portal',
    'version': '1',
    'category': 'Marketing',
    'sequence': 60,
    'summary': 'Ticketing',
    'website': 'https://www.odoo.com/page/events',
    'depends': [
        'website_portal',
        'event_sale',
        'website_event_sale',
    ],
    'description': """
        Bridge module for Event modules using the website
        * Event Tickets for Portal Users.
        * Portal Users can print badges for their own tickets.
    """,
    'data': [
        'views/event_portal_template.xml',
        'views/event_template.xml',
        'views/event_view.xml',

    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
