# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class AccountMovevv(models.Model):
    _inherit = 'account.edi.document'

    def action_export_xml(self):
        pass

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        print('-------------------------------------------')
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id, required=True)

    # @api.onchange("branch_id")
    # def _onchange_analytic_tag(self):
    #     for rec in self:
    #         record = self.env['account.analytic.tag'].search([('branch_id', '=', rec.branch_id.id)])
    #         rec.line_ids.branch_id = rec.branch_id.id
    #         print(record)
    #         rec.line_ids.analytic_tag_ids = record
    #
    # @api.model
    # def create(self, values):
    #     res = super(AccountMove, self).create(values)
    #     print(res.invoice_line_ids)
    #     print(res.branch_id)
    #     print('----------------------------------------')
    #     for invoice in res.invoice_line_ids:
    #         print(invoice)
    #         invoice.branch_id = res.branch_id
    #         tags = self.env['account.analytic.tag'].search([('branch_id.id', '=', res.branch_id.id)])
    #         print(tags)
    #         invoice.analytic_tag_ids = tags
    #
    #     for line1 in res.line_ids:
    #         print(line1)
    #         line1.branch_id = res.branch_id
    #         tags = self.env['account.analytic.tag'].search([('branch_id.id', '=', res.branch_id.id)])
    #         print(tags)
    #         line1.analytic_tag_ids = tags
    #
    #     return res
    #
    # def write(self, values):
    #     res = super(AccountMove, self).write(values)
    #     print('----------------------------------------')
    #     tags = self.env['account.analytic.tag'].search([('branch_id', '=', self.branch_id.id)])
    #     for line in self.invoice_line_ids:
    #         line.branch_id = self.branch_id
    #         line.analytic_tag_ids = tags.ids
    #
    #     for line1 in self.line_ids:
    #         line1.branch_id = self.branch_id
    #         line1.analytic_tag_ids = tags.ids
    #     return res

    def action_register_payment(self):

        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
                'default_branch_id': self.branch_id.id,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id, readonly=True)

    # @api.model
    # def create(self, values):
    #     print(values['move_id'])
    #     record = self.env['account.move'].search([('id', '=', values['move_id'])])
    #     print(record.branch_id.name)
    #     values['branch_id'] = record.branch_id.id
    #     tags = self.env['account.analytic.tag'].search([('branch_id.id', '=', record.branch_id.id)])
    #     print(tags.name)
    #     values['analytic_tag_ids'] = tags
    #     return super(AccountMoveLine, self).create(values)
