# -*- coding: utf-8 -*-


from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    # state = fields.Selection([('draft', 'Draft'),
    #                           ('approve', 'Waiting For Approval'),
    #                           ('posted', 'Validated'),
    #                           ('sent', 'Sent'),
    #                           ('reconciled', 'Reconciled'),
    #                           ('cancelled', 'Cancelled'),
    #                           ('reject', 'Reject')
    #                           ], readonly=True, default='draft', copy=False, string="Status")

    def action_post(self):
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('approval_workflow.group_approve_payment'):
            self.approve_by_id = self.env.user.id
        self.write({
            'state': 'posted'
        })
        rec = super(AccountPaymentInh, self).action_post()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def action_draft(self):
        self.write({
            'state': 'draft'
        })
        rec = super(AccountPaymentInh, self).action_draft()
        return rec

