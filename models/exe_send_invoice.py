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