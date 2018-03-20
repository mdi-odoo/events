# -*- coding: utf-8 -*-
from odoo import api, fields, models, modules, tools
from datetime import datetime


class Event(models.Model):
	_inherit = ['event.event']

	cover_image = fields.Binary("Image", attachment=True,
		help="This field holds the image used as top cover for this event, limited to 1024x1024px",)
