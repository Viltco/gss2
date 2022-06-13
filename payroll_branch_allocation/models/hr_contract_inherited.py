# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ContractInherited(models.Model):
    _inherit = 'hr.contract'
    branch_allocation_id = fields.One2many('branch.allocation.line', 'contract_id', string='Branch Allocation')

    @api.onchange('branch_allocation_id.branch_id')
    def _onchange_branch_id(self):
        tags = self.env['account.analytic.tag'].search([('branch_id', '=', self.branch_id.id)])
        for rec in self:
            if rec.branch_allocation_id.branch_id:
                rec.branch_allocation_id.analytic_tag_id = tags.ids

    @api.constrains('branch_allocation_id')
    def _check_percentage(self):
        sum = 0
        for rec in self:
            for line in rec.branch_allocation_id:
                if line.percentage < 0:
                    raise UserError(f'Negative values are not allowed')
                sum += line.percentage
            if sum > 0 and sum < 100:
                req = 100 - sum
                raise UserError(f'{req}% still needs to be allocated. Total allocation must be equal to 100%.')
            if sum > 100:
                req = 100 - sum
                raise UserError(f'{req}% Allocation difference. Total allocation must be equal to 100%.')

    @api.onchange('employee_id')
    def _onchange_employee(self):
        for rec in self:
            if rec.employee_id:
                rec.branch_allocation_id.employee_id = rec.employee_id.id
