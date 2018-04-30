# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Event Ticket Tags',
    'summary': 'Event Ticket Tags',
    'sequence': 55,
    'website': 'https://www.odoo.com/page/events',
    'category': 'Marketing',
    'description': """
Event Ticket Tags
=================
* Event Ticket Manged by Tags
* Event Ticket Print color Badge 
    """,
    'depends': ['website_event_sale', 'website_event_snippet','website_event_track'],
    'data': [
        #views
        'views/event_views.xml',

        #template
        'views/event_tag_template.xml',

        # report
        'views/event_event_templates.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
#     'qweb': ['static/src/xml/*.xml'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
