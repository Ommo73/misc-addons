from odoo import models, fields, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.multi
    def save_partner_message(self, message_id):
        message = self.env['mail.message'].browse(message_id)
        partner = message.author_id
        message_text = message.body
        current_user = self.env['res.users'].browse(self._context.get('uid'))
        import wdb
        wdb.set_trace()
