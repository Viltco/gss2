# -*- coding: utf-8 -*-

from odoo import models, api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class EmpConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    loan_account = fields.Many2one('account.account', string='Loan Account',
                                   config_parameter='payslip_partner.loan_account')
    advance_account = fields.Many2one('account.account', string='Advance Account',
                                      config_parameter='payslip_partner.advance_account')


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.move_type == 'entry':
            slip = self.env['hr.payslip'].search([('number', '=', self.ref)])
            if slip:
                slip.loan_line.status = 'paid'
                slip.loan_line.paid = True
                slip.loan_line.paid_on = datetime.today()
                slip.loan_line.paid_amount = slip.loan_line.amount

                slip.advance_line.status = 'paid'
                slip.advance_line.paid = True
                slip.advance_line.paid_on = datetime.today()
                slip.advance_line.paid_amount = slip.advance_line.amount
        return super(AccountMoveInh, self).action_post()


class HrAdvanceInh(models.Model):
    _inherit = 'hr.advance'

    journal_id = fields.Many2one('account.journal')
    is_payment_created = fields.Boolean('Is Created', default=False)
    move_id = fields.Many2one('account.move')
    branch_id = fields.Many2one('res.branch', related='employee_id.branch_id')

    def action_submit(self):
        if self.loan_amount > self.employee_id.contract_id.wage:
            raise UserError('Advance Amount cannot be greater than Gross Salary.')
        self.compute_installment()
        self.write({'state': 'waiting_approval_1'})

    def action_view_entry(self):
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'object',
            'domain': [('ref', '=', self.name)],
            'target': 'current',
            'name': 'Journal Item',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }

    def action_create_payment(self):
        self._action_general_entry()

    def get_accounts(self):
        loan_account = self.env['ir.config_parameter'].get_param('payslip_partner.loan_account')
        advance_account = self.env['ir.config_parameter'].get_param('payslip_partner.advance_account')
        # print(loan_account)
        # print(advance_account)
        return advance_account

    def _action_general_entry(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for rec in self:
            if not rec.journal_id:
                raise UserError('Please Select Journal.')
            # debit_account = self.env['account.account'].search([('name', '=', 'Advances to Employees against Salary')])
            debit_account = self.get_accounts()
            if not debit_account:
                raise UserError('Debit Account not Found.')
            move_dict = {
                'ref': rec.name,
                'journal_id': rec.journal_id.id,
                'branch_id': rec.branch_id.id,
                'partner_id': rec.employee_id.address_home_id.id,
                'date': rec.date_payment,
                'state': 'draft',
            }
            debit_line = (0, 0, {
                'name': 'Advances to Employees against Salary',
                'debit': abs(rec.loan_amount),
                'credit': 0.0,
                'branch_id': rec.branch_id.id,
                'analytic_tag_ids': rec.branch_id.analytic_account_tag_id.ids,
                'partner_id': rec.employee_id.address_home_id.id,
                'account_id': int(debit_account),
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': 'Advances to Employees against Salary',
                'debit': 0.0,
                'branch_id': rec.branch_id.id,
                'analytic_tag_ids': rec.branch_id.analytic_account_tag_id.ids,
                'partner_id': rec.employee_id.address_home_id.id,
                'credit': abs(rec.loan_amount),
                'account_id': rec.journal_id.default_account_id.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            line_ids = []
            rec.is_payment_created = True
            rec.move_id = move.id
            print("General entry created")


class HrAdvanceLineInh(models.Model):
    _inherit = 'hr.advance.line'

    paid_on = fields.Date()
    paid_amount = fields.Float()
    status = fields.Selection([
        ('unpaid', 'Due'),
        ('paid', 'Deducted'),
    ], string="Status", default='unpaid', copy=False )


class HrLoanInh(models.Model):
    _inherit = 'hr.loan'

    journal_id = fields.Many2one('account.journal')
    is_payment_created = fields.Boolean('Is Created', default=False)
    move_id = fields.Many2one('account.move')
    branch_id = fields.Many2one('res.branch', related='employee_id.branch_id')

    def action_view_entry(self):
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'object',
            'domain': [('ref', '=', self.name)],
            'target': 'current',
            'name': 'Journal Item',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }

    def action_create_payment(self):
        self._action_general_entry()

    def get_accounts(self):
        loan_account = self.env['ir.config_parameter'].get_param('payslip_partner.loan_account')
        return loan_account

    def _action_general_entry(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for rec in self:
            if not rec.journal_id:
                raise UserError('Please Select Journal.')
            # debit_account = self.env['account.account'].search([('name', '=', 'Loan against PF')])
            debit_account = self.get_accounts()
            if not debit_account:
                raise UserError('Debit Account not Found.')
            move_dict = {
                'ref': rec.name,
                'journal_id': rec.journal_id.id,
                'branch_id': rec.branch_id.id,
                'partner_id': rec.employee_id.address_home_id.id,
                'date': rec.date_payment,
                'state': 'draft',
            }
            debit_line = (0, 0, {
                'name': 'Loan Against PF',
                'debit': abs(rec.loan_amount),
                'credit': 0.0,
                'branch_id': rec.branch_id.id,
                'analytic_tag_ids': rec.branch_id.analytic_account_tag_id.ids,
                'partner_id': rec.employee_id.address_home_id.id,
                'account_id': int(debit_account),
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': 'Loan Against PF',
                'debit': 0.0,
                'branch_id': rec.branch_id.id,
                'analytic_tag_ids': rec.branch_id.analytic_account_tag_id.ids,
                'partner_id': rec.employee_id.address_home_id.id,
                'credit': abs(rec.loan_amount),
                'account_id': rec.journal_id.default_account_id.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            line_ids = []
            rec.is_payment_created = True
            rec.move_id = move.id
            print("General entry created")


class HrLoanLineInh(models.Model):
    _inherit = 'hr.loan.line'

    paid_on = fields.Date()
    paid_amount = fields.Float()
    status = fields.Selection([
        ('unpaid', 'Due'),
        ('paid', 'Deducted'),
    ], string="Status", default='unpaid', copy=False )


class HrPayslipInh(models.Model):
    _inherit = 'hr.payslip'

    loan_amount = fields.Float()
    advance_amount = fields.Float()
    loan_line = fields.Many2one('hr.loan.line')
    advance_line = fields.Many2one('hr.advance.line')

    def compute_sheet(self):
        for rec in self:
            # Loans
            loan = self.env['hr.loan'].search([('employee_id', '=', rec.employee_id.id), ('state', '=', 'approve'),
                                               ('is_payment_created', '=', True)])
            amount = 0
            if loan and loan.move_id.state == 'posted':
                for line in loan.loan_lines:
                    if rec.date_from.month == line.date.month and line.status != 'paid':
                        amount = amount + line.amount
                        rec.loan_line = line.id
            rec.loan_amount = amount

            # Advances
            loan = self.env['hr.advance'].search([('employee_id', '=', rec.employee_id.id), ('state', '=', 'approve'),
                                                  ('is_payment_created', '=', True)])
            ad_amount = 0
            if loan and loan.move_id.state == 'posted':
                for line in loan.advance_lines:
                    if rec.date_from.month == line.date.month and line.status != 'paid':
                        ad_amount = ad_amount + line.amount
                        rec.advance_line = line.id
            rec.advance_amount = ad_amount

            return super(HrPayslipInh, self).compute_sheet()

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