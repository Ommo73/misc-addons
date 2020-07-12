from odoo import models, fields, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    saved_partner_ids = fields.Many2many(
        'res.partner', 'mail_message_res_partner_saved_rel', string='Saved By')

    def save_partner_message(self, message_id):
        message = self.env['mail.message'].browse(message_id)
        partner = message.author_id
        message_body = message.body
        current_user = self.env['res.users'].browse(self._context.get('uid'))

        kwargs = {
            'author_id': current_user.partner_id.id
        }
        partner.message_post(
            body=message_body,
            message_type='comment',
            subtype='mail.mt_note',
            **kwargs,
        )
        message.saved_partner_ids += current_user.partner_id

    @api.multi
    def message_format(self):
        values = super(MailMessage, self).message_format()
        current_user = self.env['res.users'].browse(self._context.get('uid'))
        for value, message in zip(values, self):
            value['saved'] = True if current_user.partner_id in message.saved_partner_ids else False
        return values
