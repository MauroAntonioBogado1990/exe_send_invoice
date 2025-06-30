{
    'name': 'Factura Email Log',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Registro automático en el chatter al enviar facturas por email',
    'depends': ['account', 'mail','sale'],
    'data': ['views/exe_send_invoice.xml'],
             #'security/ir.model.access.csv'],
              
    'installable': True,
    'application': False,
}