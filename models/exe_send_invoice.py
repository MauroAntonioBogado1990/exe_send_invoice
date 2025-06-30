from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    email_send_count = fields.Integer(string='Cantidad de envíos', tracking=True)
    mail_logs = fields.Text(string='Historial resumido de emails', tracking=True)

    def action_send_and_print(self):
        res = super().action_send_and_print()

        for invoice in self:
            partner_email = invoice.partner_id.email or 'Sin email'
            user_name = self.env.user.name
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sale_order = self.env['sale.order'].search([
                ('name', '=', invoice.invoice_origin)
            ], limit=1)

            # Actualiza factura
            log_line = f"{timestamp} - Enviado a {partner_email} por {user_name}"
            invoice.email_send_count += 1
            invoice.mail_logs = f"{invoice.mail_logs or ''}\n{log_line}".strip()

            # Actualiza orden de venta si existe
            if sale_order:
                sale_order.email_send_count += 1
                sale_order.mail_logs = f"{sale_order.mail_logs or ''}\n{log_line}".strip()

            _logger.info(f"📧 Registro guardado para factura {invoice.name}, cliente: {partner_email}")

        return res

'''
def action_send_and_print(self):
    res = super().action_send_and_print()

    for invoice in self:
        partner_email = invoice.partner_id.email or 'Sin email'
        user_name = self.env.user.name
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sale_order = self.env['sale.order'].search([
            ('name', '=', invoice.invoice_origin)
        ], limit=1)

        # 📄 Generar PDF de deuda y adjuntar
        contexto = str([
            ('partner_id', '=', invoice.partner_id.id),
            ('invoice_date', '>=', (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')),
            ('invoice_date', '<=', datetime.now().strftime('%Y-%m-%d')),
        ])
        data = invoice.get_report_values_debt(contexto, [invoice])
        pdf_binary = invoice.generate_pdf_res_partner_debt(data)

        attachment = self.env['ir.attachment'].create({
            'name': 'Informe_de_valores_a_abonar.pdf',
            'type': 'binary',
            'datas': pdf_binary,
            'store_fname': 'Informe_de_valores_a_abonar.pdf',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'mimetype': 'application/pdf',
        })

        # ✉️ Crear y enviar el correo con adjunto
        mail_values = {
            'email_to': partner_email,
            'subject': f"Factura y deuda {invoice.name}",
            'body_html': f"<p>Estimado/a {invoice.partner_id.name},</p><p>Adjuntamos su factura y el resumen de deuda correspondiente.</p>",
            'attachment_ids': [attachment.id],
        }
        self.env['mail.mail'].create(mail_values).send()

        # 📝 Logs en factura y orden de venta
        log_line = f"{timestamp} - Enviado a {partner_email} por {user_name}"
        invoice.email_send_count += 1
        invoice.mail_logs = f"{invoice.mail_logs or ''}\n{log_line}".strip()

        if sale_order:
            sale_order.email_send_count += 1
            sale_order.mail_logs = f"{sale_order.mail_logs or ''}\n{log_line}".strip()

        _logger.info(f"📧 Email + informe enviado para {invoice.name}, cliente: {partner_email}")

    return res
'''

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    email_send_count = fields.Integer(
        string='Cantidad de envíos',
        tracking=True
    )

    mail_logs = fields.Text(
        string='Historial resumido de emails',
        tracking=True
    )