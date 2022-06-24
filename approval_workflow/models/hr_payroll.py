

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip.run'

    review_by_id = fields.Many2one('res.users', string='Review By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection([
        ('draft', 'New'),
        ('verify', 'Confirmed'),
        ('to_review', 'Waiting For Review'),
        ('to_approve', 'Waiting For Approval'),
        ('approved', 'Approved'),
        ('close', 'Done'),
        ('rejected', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def action_send_review(self):
        self.write(
            {'state': 'to_review'}
        )

    def action_to_review(self):
        if self.env.user.has_group('approval_workflow.group_review_payroll_batch'):
            self.review_by_id = self.env.user.id
        self.write(
            {'state': 'to_approve'}
        )

    def action_review_reject(self):
        self.write(
            {'state': 'rejected'}
        )

    def action_approve(self):
        if self.env.user.has_group('approval_workflow.group_approve_payroll_batch'):
            self.approve_by_id = self.env.user.id
        self.write(
            {'state': 'approved'}
        )

    def action_approve_reject(self):
        self.write(
            {'state': 'rejected'}
        )
