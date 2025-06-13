from odoo import fields, models

class PaymentProviderMips(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('mips', 'MIPS')])
    mips_merchant_id = fields.Char('Merchant ID')
    mips_form_id = fields.Char('Form ID')
    mips_operator_id = fields.Char('Operator ID')
    mips_operator_password = fields.Char('Operator Password')
    mips_salt = fields.Char('IMN Salt')
    mips_cipher_key = fields.Char('IMN Cipher Key')

    def _get_supported_currency(self):
        if self.code == 'mips':
            return ['MUR', 'EUR', 'USD', 'GBP', 'ZAR']
        return super()._get_supported_currency()
