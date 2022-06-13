# -*- coding: utf-8 -*-

from odoo import models, api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class HrPayslipInh(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        record = super(HrPayslipInh, self).action_payslip_done()
        self._action_general_entry()

    def _action_general_entry(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for rec in self:
            allocation_lines = self.env['branch.allocation.line'].search([('contract_id', '=', rec.contract_id.id), ('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to)])
            if not allocation_lines:
                raise UserError('There are no Allocation Lines on Contract for Employee ' + rec.employee_id.name)
            print(allocation_lines)
            move_dict = {
                'ref': rec.number,
                'journal_id': rec.journal_id.id,
                'branch_id': rec.employee_id.branch_id.id,
                # 'address_id': rec.address_id.id,
                # 'partner_id': rec.employee_id.address_home_id.id,
                'date': datetime.today(),
                'state': 'draft',
            }
            for oline in rec.line_ids:
                for all_line in allocation_lines:
                    if oline.salary_rule_id.account_debit and oline.salary_rule_id.account_credit and oline.total > 0:
                        print(all_line.branch_id.id)
                        print(all_line.analytic_tag_id.ids)
                        debit_line = (0, 0, {
                            'name': oline.name,
                            'branch_id': all_line.branch_id.id,
                            'analytic_tag_ids': all_line.analytic_tag_id.ids,
                            'debit': abs((oline.total * all_line.percentage)/100),
                            'credit': 0.0,
                            'partner_id': rec.employee_id.address_home_id.id,
                            'account_id': oline.salary_rule_id.account_debit.id,
                        })
                        line_ids.append(debit_line)
                        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                        credit_line = (0, 0, {
                            'name': oline.name,
                            'branch_id': all_line.branch_id.id,
                            'analytic_tag_ids': all_line.analytic_tag_id.ids,
                            'debit': 0.0,
                            'partner_id': rec.employee_id.address_home_id.id,
                            'credit': abs((oline.total * all_line.percentage)/100),
                            'account_id': oline.salary_rule_id.account_credit.id,
                        })
                        line_ids.append(credit_line)
                        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            if line_ids:
                print(line_ids)
                move_dict['line_ids'] = line_ids
                move = self.env['account.move'].create(move_dict)
                line_ids = []
                rec.move_id = move.id
                # print("General entry created")