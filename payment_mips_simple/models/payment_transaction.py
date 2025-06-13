import json
import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        if self.provider_code != 'mips':
            return super()._get_specific_rendering_values(processing_values)

        provider = self.provider_id
        if not provider.mips_merchant_id:
            raise ValidationError(_('MIPS credentials are not configured.'))

        payload = {
            'authentify': {
                'id_merchant': provider.mips_merchant_id,
                'id_form': provider.mips_form_id,
                'id_operator': provider.mips_operator_id,
                'operator_password': provider.mips_operator_password,
            },
            'order': {
                'id_order': self.reference,
                'amount': self.amount,
                'currency': self.currency_id.name,
            },
            'request_mode': 'simple',
            'touchpoint': 'web',
            'iframe_behavior': {
                'height': 508,
                'width': 450,
                'language': 'EN',
            }
        }
        try:
            response = requests.post('https://api.mips.mu/api/load_payment_zone',
                                     json=payload,
                                     timeout=60)
            result = response.json()
        except Exception as e:
            raise ValidationError(_('MIPS: failed to create payment: %s') % e)
        iframe_html = result.get('payment_iframe') or result.get('answer', {}).get('payment_zone_data')
        return {'iframe_html': iframe_html}
