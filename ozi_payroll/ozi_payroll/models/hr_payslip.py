from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from pytz import timezone


class HrContractInh(models.Model):
    _inherit = 'hr.contract'

    half_deduction = fields.Float()
    full_deduction = fields.Float()


class HrPayslipInh(models.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        self.get_half_deduction()
        self.get_full_deduction()
        return super(HrPayslipInh, self).compute_sheet()

    def get_half_deduction(self):
        for rec in self:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', rec.employee_id.id), ('late_status', '=','half'), ('att_status', '=', 'late')])
            # print(attendance)
            att_list = []
            for att in attendance:
                if att.check_in.date().month == rec.date_from.month:
                    att_list.append(att.id)
            wage = ((rec.contract_id.wage/30)/2)* len(att_list)
            rec.contract_id.half_deduction = wage

    def get_full_deduction(self):
        for rec in self:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', rec.employee_id.id), ('late_status', '=','full'), ('att_status', '=', 'late')])
            print(attendance)
            att_list = []
            for att in attendance:
                if att.check_in.date().month == rec.date_from.month:
                    att_list.append(att.id)
            wage = (rec.contract_id.wage/30)* len(att_list)
            rec.contract_id.full_deduction = wage

