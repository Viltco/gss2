# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from pytz import timezone


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    late_time = fields.Char('Late Mins')
    late_status = fields.Selection([
        ('none', 'None'),
        ('half', 'Half'),
        ('full', 'Full')
    ], string="Late Status", default='none')

    att_status = fields.Selection([
        ('none', 'None'),
        ('late', 'Late'),
        ('waveoff', 'Waved Off')
    ], string="Attendance Status", default='none')

    is_pressed = fields.Boolean()

    def compute_late_time(self):
        # for rec in self:
        #     rec.att_status = 'none'
        #     rec.late_status = 'none'
        #     rec.late_time = ''
        check_in = self.env['ir.config_parameter'].get_param('ozi_payroll.check_in')
        check_out = self.env['ir.config_parameter'].get_param('ozi_payroll.check_out')
        grace_time = self.env['ir.config_parameter'].get_param('ozi_payroll.grace_time')
        inn = str(timedelta(hours=float(check_in)) + timedelta(minutes=float(grace_time)))
        # outt = str(timedelta(hours=float(check_out)))
        for record in self:
            now_dubai = record.check_in.astimezone(timezone('Asia/Karachi'))
            c_in = str(now_dubai)
            splt = c_in.split(' ')[1]
            sp = splt.split('+')[0]
            FMT = '%H:%M:%S'
            if int(sp.split(':')[0]) >= int(inn.split(':')[0]):
                tdelta = datetime.strptime(sp, FMT) - datetime.strptime(inn, FMT)
                if 'day' not in str(tdelta):
                    record.late_time = str(tdelta)
                v = int(inn.split(':')[0])
                record.check_counter(v, tdelta)
                # record.action_waveoff()

    def action_waveoff(self):
        for rec in self:
            attendance = self.env['hr.attendance'].search([])
            att_list = []
            for att in attendance:
                if rec.check_in.date().month == datetime.today().date().month:
                    att_list.append(att.id)
            all_employees = self.env['hr.attendance'].browse(att_list).mapped('employee_id')
            all_att = self.env['hr.attendance'].browse(att_list)
            if any(line.is_pressed == True for line in all_att):
                raise UserError('Waveoff for All Employee is already done.')
            for emp in all_employees:
                emp_attendance = self.env['hr.attendance'].search([('employee_id', '=', emp.id), ('id', 'in', att_list), ('late_status', '=', 'half'),('att_status', '!=', 'waveoff')], order='id asc')
                if len(emp_attendance) > 1:
                    emp_attendance[0].att_status = 'waveoff'
                    emp_attendance[1].att_status = 'waveoff'
                if len(emp_attendance) == 1:
                    emp_attendance[0].att_status = 'waveoff'

                for k in emp_attendance:
                    k.is_pressed = True
                #
                # full_attendance = self.env['hr.attendance'].search(
                #     [('employee_id', '=', emp.id), ('id', 'in', att_list), ('late_status', '=', 'full'),
                #      ('att_status', '!=', 'waveoff')], order='id asc')
                # if len(full_attendance) > 1:
                #     full_attendance[0].att_status = 'waveoff'
                #     full_attendance[1].att_status = 'waveoff'
                # if len(full_attendance) == 1:
                #     full_attendance[0].att_status = 'waveoff'
                #
                # for r in full_attendance:
                #     r.is_pressed = True
            break

    def check_counter(self, office_time, late):
        for rec in self:
            if rec.late_time and rec.att_status != 'waveoff':
                now_dubai = rec.check_in.astimezone(timezone('Asia/Karachi'))
                a = str(now_dubai).split(' ')[1]
                # min =a.split(':')[1]
                hours = a.split(':')[0]
                if int(hours) >= 11:
                    rec.late_status = 'full'
                    rec.att_status = 'late'
                elif int(hours) > office_time and int(hours) < 11:
                    rec.late_status = 'half'
                    rec.att_status = 'late'
                elif int(str(late).split(':')[1]) > 0 and int(hours) < 11:
                    rec.late_status = 'half'
                    rec.att_status = 'late'
                else:
                    rec.late_status = 'none'
                    rec.att_status = 'none'





