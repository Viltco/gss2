# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _


# class CompanyInh(models.Model):
#     _inherit = 'res.company'

    # check_in = fields.Datetime(invisible=True)
    # check_out = fields.Datetime(invisible=True)
    # grace_time = fields.Integer(invisible=True)


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    check_in = fields.Float('Check In', config_parameter='ozi_payroll.check_in', help="""Standard Check In Time""")
    check_out = fields.Float('Check Out', config_parameter='ozi_payroll.check_out', help="""Standard Check Out Time""")
    grace_time = fields.Integer(string='Grace Time', config_parameter='ozi_payroll.grace_time', help="""Standard Grace Time""")

    def set_values(self):
        res = super(ConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('ozi_payroll.check_in', self.check_in)
        self.env['ir.config_parameter'].set_param('ozi_payroll.check_out', self.check_out)
        self.env['ir.config_parameter'].set_param('ozi_payroll.grace_time', self.grace_time)
        return res