# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FieldSettingPayroll(models.TransientModel):
    _inherit = 'res.config.settings'

    loan_balance = fields.Many2one('account.account', string='Loan Balance' ,config_parameter='inherit_payroll_gss.loan_balance')
    eobi_balance = fields.Many2one('account.account', string='Eobi Balance' ,config_parameter='inherit_payroll_gss.eobi_balance')
    pf_balance = fields.Many2one('account.account', string='PF balance' ,config_parameter='inherit_payroll_gss.pf_balance')
    tax_deduction = fields.Many2one('account.account', string='Tax Deduction Till Date' ,config_parameter='inherit_payroll_gss.tax_deduction')



