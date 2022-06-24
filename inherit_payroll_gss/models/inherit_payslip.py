# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from odoo import models, fields, api


class FieldSettingPayroll(models.Model):
    _inherit = 'hr.payslip'

    loan_balance = fields.Many2one('account.account' , string='Loan Balance', compute="set_loan_balance")
    eobi_balance = fields.Many2one('account.account' ,string='Eobi Balance', compute="set_eobi_balance")
    pf_balance = fields.Many2one('account.account' ,string='PF balance', compute="set_pf_balance")
    tax_deduction = fields.Many2one('account.account' , string='Tax Deduction Till Date', compute="set_tax_deduction")

    def set_loan_balance(self):
        loan = self.env['ir.config_parameter'].get_param('inherit_payroll_gss.loan_balance')
        rec = self.env['account.account'].search([('id', '=', loan)])
        self.loan_balance = rec.id
        print(rec.name)

    def set_eobi_balance(self):
        eobi = self.env['ir.config_parameter'].get_param('inherit_payroll_gss.eobi_balance')
        rec = self.env['account.account'].search([('id', '=', eobi)])
        self.eobi_balance = rec.id
        print(rec.name)

    def set_pf_balance(self):
        pf = self.env['ir.config_parameter'].get_param('inherit_payroll_gss.pf_balance')
        rec = self.env['account.account'].search([('id', '=', pf)])
        self.pf_balance = rec.id
        print(rec.name)

    def set_tax_deduction(self):
        tax = self.env['ir.config_parameter'].get_param('inherit_payroll_gss.tax_deduction')
        rec = self.env['account.account'].search([('id', '=', tax)])
        self.tax_deduction = rec.id
        print(rec.name)

    def get_loan_balance_account(self):
        print('Loan Balance')
        result = self.env['hr.payslip'].browse(self.id)
        print(result)
        config_id = self.env['ir.config_parameter'].sudo().get_param('inherit_payroll_gss.loan_balance')
        emp = self.env['account.move.line'].search(
            [('partner_id', '=', result.employee_id.address_home_id.id), ('move_id.state', '=', 'posted'),
             ('account_id.id', '=', config_id)])
        print(emp)
        db = 0
        for rec in emp:
            db = db + (rec.debit - rec.credit)
        return db

    def get_eobi_balance_account(self):
        print('Eobi Balance')
        result = self.env['hr.payslip'].browse(self.id)
        print(result)
        config_id = self.env['ir.config_parameter'].sudo().get_param('inherit_payroll_gss.eobi_balance')
        emp = self.env['account.move.line'].search(
            [('partner_id', '=', result.employee_id.address_home_id.id), ('move_id.state', '=', 'posted'),
             ('account_id.id', '=', config_id)])
        print(emp)
        db = 0
        for rec in emp:
            db = db + (rec.debit - rec.credit)
        return db

    def get_pf_balance_account(self):
        print('PF Balance')
        result = self.env['hr.payslip'].browse(self.id)
        print(result)
        config_id = self.env['ir.config_parameter'].sudo().get_param('inherit_payroll_gss.pf_balance')
        emp = self.env['account.move.line'].search(
            [('partner_id', '=', result.employee_id.address_home_id.id), ('move_id.state', '=', 'posted'),
             ('account_id.id', '=', config_id)])
        print(emp)
        db = 0
        for rec in emp:
            db = db + (rec.debit - rec.credit)
        return db

    def get_tax_deduction_account(self):
        print('Tax Deduction')
        result = self.env['hr.payslip'].browse(self.id)
        print(result)
        config_id = self.env['ir.config_parameter'].sudo().get_param('inherit_payroll_gss.tax_deduction')
        acc_config = self.env.company.fiscalyear_last_day
        acc_config_month = self.env.company.fiscalyear_last_month
        d = str(acc_config) + '-' + str(acc_config_month) + '-' + str(datetime.today().year - 1) + ' ' + "00:00:00"
        date_object = datetime.strptime(d, "%d-%m-%Y %H:%M:%S").date()
        final_date = date_object + timedelta(days=1)
        print(final_date)
        emp = self.env['account.move.line'].search(
            [('partner_id', '=', result.employee_id.address_home_id.id), ('move_id.state', '=', 'posted'),
             ('account_id.id', '=', config_id), ('date', '>=', final_date), ('date', '<=', datetime.today())])
        print(emp)
        db = 0
        for rec in emp:
            db = db + (rec.debit - rec.credit)
        return db
