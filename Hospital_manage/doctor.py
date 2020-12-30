from odoo import models, fields,api,_
class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description ='Doctor Records'
    _inherits = {'hospital.patient': 'related_patient_id'}

    name = fields.Char(string='Doctor Name',track_visibility='always')
    doctor_gender=fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Gender')
    user_id = fields.Many2one('res.users', string='Related User')
    patient_id = fields.Many2one('hospital.patient', string='Related Patient')
    related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
