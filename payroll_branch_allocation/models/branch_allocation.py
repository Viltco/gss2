from odoo import fields, models, _, api
from odoo.exceptions import UserError


class BranchAllocationLines(models.Model):
    _name = 'branch.allocation.line'
    _rec_name = 'branch_id'

    contract_id = fields.Many2one('hr.contract', string='Contract')
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True, related='contract_id.employee_id')
    branch_id = fields.Many2one('res.branch', default=lambda r: r.env.user.branch_id.id)
    analytic_tag_id = fields.Many2many('account.analytic.tag', string='Analytic Tag',
                                       domain="[('branch_id', '=', branch_id)]", readonly=True)
    percentage = fields.Float('Percentage')
    date_from = fields.Date()
    date_to = fields.Date()

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        tags = self.env['account.analytic.tag'].search([('branch_id', '=', self.branch_id.id)])
        for rec in self:
            if rec.branch_id:
                rec.analytic_tag_id = tags.ids

    @api.constrains('percentage')
    def _check_percentage(self):
        record = self.env['hr.contract'].search([('name', '=', self.contract_id.name)])
        sum = 0
        for line in record.branch_allocation_id:
            if line.percentage < 0:
                raise UserError(f'Negative values are not allowed')
            sum += line.percentage
        if sum > 0 and sum < 100:
            req = 100 - sum
            raise UserError(f'{req}% still needs to be allocated. Total allocation must be equal to 100%.')
        if sum > 100:
            req = 100 - sum
            raise UserError(f'{req}% Allocation difference. Total allocation must be equal to 100%.')
