{
    'name':'Hospital Management',
    'version':'13.0.1.0.0',
    'category':'Extra Tools',
    'summary':'',
    'sequence':'',
    'author':'',
    'website':'',
    'depends':['base','mail','sale','report_xlsx'],
    'data':[
        # 'security/ir.model.access.csv',
        'security/security.xml',
        # 'appointment.xml',
        'patient.xml',
        'data/sequence.xml',
        'data/cron.xml',
        'data/email_template.xml',
        'wizards/create_appointment.xml',

        'doctor.xml',
        'template.xml',
        'reports/patient_card.xml',
        'data/appointment_sequen.xml',
        'reports/report.xml',
        'reports/appointment.xml',
        'lab.xml',
        'settings.xml',
        # 'data/data.xml',
        'sale_order.xml',

        ],
    'installable':True,
    'application':True,
    'auto install':True,
}

