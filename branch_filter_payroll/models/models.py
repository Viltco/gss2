# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    def _default_company_id(self):
        return self.env.company.id

    def _default_company_counter(self):
        rec = self.env['res.company'].search([])
        return len(rec)

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)
    company_id = fields.Many2one('res.company', string='Company', default=_default_company_id)
    company_counter = fields.Integer(default=_default_company_counter)


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    def _default_company_id(self):
        return self.env.company.id

    def _default_company_counter(self):
        rec = self.env['res.company'].search([])
        return len(rec)

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)
    company_id = fields.Many2one('res.company', string='Company', default=_default_company_id)
    company_counter = fields.Integer(default=_default_company_counter)


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)


class HrPayslipStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    def _default_company_id(self):
        return self.env.company.id

    def _default_company_counter(self):
        rec = self.env['res.company'].search([])
        return len(rec)

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)
    company_id = fields.Many2one('res.company', string='Company', default=_default_company_id)
    company_counter = fields.Integer(default=_default_company_counter)
