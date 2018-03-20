{
    'name':'Website Events Snippet',
    'description':'Upcoming Events Snippet',
    'category': 'Website',
    'version':'1.0',
    'author':'Odoo IN',
    'data': [
        'views/assets.xml',
        'views/s_events.xml',
        'views/options.xml',
        'views/event_views.xml',
    ],
    'depends': ['website_event'],
    'auto_install': True,
    'images': [
        'static/src/img/s_events.png',
    ],
}
