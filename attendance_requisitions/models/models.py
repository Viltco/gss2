# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

from odoo.exceptions import UserError


class AttendanceRequisitions(models.Model):
    _name = 'attendance.requisitions'
    _description = 'attendance_requisitions.attendance_requisitions'
    _rec_name = 'employee_id'

    req_date = fields.Date(string='Requisition Date', default=datetime.today())
    employee_id = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id.id)
    description = fields.Text('Description')
    att_req_line_id = fields.One2many('attendance.requisitions.line', 'att_req_id',
                                      string='Attendance Requisitions Line')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('approve', 'Approved'),
        ('reject', 'Rejected')
    ], string="Status", default='draft')

    def unlink(self):
        if self.state in ['approve']:
            raise UserError('You cannot Delete Requisition once it is Approved.')
        return super(AttendanceRequisitions, self).unlink()

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            for res in rec.att_req_line_id:
                if res.attendance_id.att_status == 'waveoff':
                    raise UserError('Attendance of this date is already Waved Off.')
                if res.attendance_id.att_status == 'none':
                    raise UserError('You are not late on this Date.')
            rec.state = 'confirm'

    def action_approve(self):
        for rec in self:
            for res in rec.att_req_line_id:
                res.attendance_id.att_status = "waveoff"
            rec.state = 'approve'

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'


class AttendanceRequisitionsLines(models.Model):
    _name = 'attendance.requisitions.line'

    att_req_id = fields.Many2one('attendance.requisitions', string='Attendance Requisitions')
    att_date = fields.Date(string='Attendance Date')
    check_in = fields.Datetime(string='Check In', compute='_compute_check_in')
    late_type = fields.Selection([
        ('none', 'None'),
        ('half', 'Half'),
        ('full', 'Full')], default='none', string='Late Type')

    late_minutes = fields.Char(string='Late Minutes')
    attendance_id = fields.Many2one('hr.attendance')

    @api.depends('att_date')
    def _compute_check_in(self):
        for i in self:
            attendances = self.env['hr.attendance'].search([('employee_id', '=', i.att_req_id.employee_id.id)])
            date = ''
            late = ''
            att = False
            late_type = 'none'
            for rec in attendances:
                if i.att_date == rec.check_in.date():
                    date = rec.check_in
                    att = rec.id
                    late = rec.late_time
                    late_type = rec.late_status
                    break
            i.check_in = date
            i.attendance_id = att
            i.late_minutes = late
            i.late_type = late_type
