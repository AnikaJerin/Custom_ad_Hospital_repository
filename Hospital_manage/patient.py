#define new model in the database
from odoo import models, fields,api,_
from odoo.exceptions import ValidationError

class ResPartners(models.Model):
    _inherit = 'res.partner'
    @api.model
    def create(self, vals_list):
        res = super(ResPartners, self).create(vals_list)
        print("yes working")
        # do the custom coding here
        return res

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('Hospital', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'patient record'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'patient_name'


    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s %s' % (rec.name_seq, rec.patient_name)))
        return res

    @api.constrains("patient_age")
    def check_age(self):
        for rec in self:
            if rec.patient_age<=5:
                raise ValidationError('The age must be greater than 5')


    @api.depends('patient_age')
    def set_age_group(self):
        for age in self:
            if age.patient_age < 18:
                self.age_group = 'minor'
            else:
                self.age_group = 'major'

    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_id':False,
            'view_mode': 'tree,form',
            'domain': [('patient_id','=',self.id)],
        }

    def get_appointment_count(self):
        count=self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count=count

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('Hospital_manage.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def test_cron_job(self):
        print("Abcd")

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    patient_name = fields.Char(string='Name',track_visibility='always')
    gender=fields.Selection([
        ('male','Male'),
        ('fe_male','Female'),
    ], default='male',string='Gender')
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Age Group',compute='set_age_group',store=True)
    name=fields.Char(string='Test')
    patient_age = fields.Integer('Age',track_visibility='always', group_operator=False)
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
    name_seq = fields.Char(string='Patient_ID', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    appointment_count=fields.Integer(string='Appointment', compute='get_appointment_count')
    active=fields.Boolean(string="Active", default=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor name")
    user_id = fields.Many2one('res.users', string="PRO")
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Doctor Gender")
    email_id = fields.Char(string="Email")
    contact_no = fields.Char(string="Contact Number")
    # patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')
    @api.model
    def create(self, vals):
        if vals.get('name_seq',_('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    def print_report(self):
        return self.env.ref('Hospital_manage.report_patient_card').report_action(self)




