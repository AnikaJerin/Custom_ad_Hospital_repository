from odoo import models, fields
class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")



    def create_appointment_button(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code',
        }

        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        self.patient_id.message_post(body="Appointment created successfully ", subject="Appointment Creation")


    def print_report(self):
        print(('kkkk'))
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        # print(self.read()[0]['patient_id'][0])
        return self.env.ref('Hospital_manage.report_appointment').with_context(landscape=True).report_action(self,
                                                                                                         data=data)

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()


    def get_data(self):

        print("printed")
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print("Appointment Name", rec.name)

        # return {
        #     "type":"ir.actions.xy_z"
        # }