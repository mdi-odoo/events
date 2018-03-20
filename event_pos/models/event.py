# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools

class EventMailScheduler(models.Model):
    _inherit = 'event.mail'
    
    @api.one
    def execute(self):
        if self.interval_type == 'after_sub':
            # update registration lines
            lines = []
            reg_ids = [mail_reg.registration_id for mail_reg in self.mail_registration_ids]
            for registration in filter(lambda item: item not in reg_ids, self.event_id.registration_ids):
                lines.append((0, 0, {'registration_id': registration.id}))
            
            if lines and not self.env.context.get('from_pos',False):
                self.write({'mail_registration_ids': lines})
            # execute scheduler on registrations
            self.mail_registration_ids.filtered(lambda reg: reg.scheduled_date and reg.scheduled_date <= datetime.strftime(fields.datetime.now(), tools.DEFAULT_SERVER_DATETIME_FORMAT)).execute()
        else:
            if not self.mail_sent:
                self.event_id.mail_attendees(self.template_id.id)
                self.write({'mail_sent': True})
        return True
