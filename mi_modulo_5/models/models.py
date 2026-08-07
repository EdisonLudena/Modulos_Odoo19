from odoo import api, fields, models

class PharmacyMedicine(models.Model):
    _inherit = 'pharmacy.medicine'

    manual_qty = fields.Float(string="Available Qty (Manual)", default=0.0)


class HospitalPharmacy(models.Model):
    _inherit = 'hospital.pharmacy'

    min_stock_threshold = fields.Float(string="Umbral Mínimo de Alerta", default=10.0)
    is_low_stock = fields.Boolean(string="Requiere Reabastecimiento", default=False, readonly=True)

    @api.model
    def _cron_check_pharmacy_stock(self):
        pharmacies = self.search([('active', '=', True)])
        
        for pharmacy in pharmacies:
            low_stock_found = False
            
            for med_line in pharmacy.medicine_ids:
                if med_line.manual_qty <= pharmacy.min_stock_threshold:
                    low_stock_found = True
                    break  

            pharmacy.is_low_stock = low_stock_found
            
            if low_stock_found and pharmacy.pharmacist_id and pharmacy.pharmacist_id.user_id:
                pharmacy._create_restock_activity()

    def _create_restock_activity(self):
        self.ensure_one()
        user_to_notify = self.pharmacist_id.user_id
        
        existing_activity = self.env['mail.activity'].search([
            ('res_model', '=', 'hospital.pharmacy'),
            ('res_id', '=', self.id),
            ('user_id', '=', user_to_notify.id),
            ('summary', '=', 'Alerta Crítica: Reabastecimiento de Farmacia')
        ], limit=1)
        
        if not existing_activity:
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get('hospital.pharmacy').id,
                'res_id': self.id,
                'user_id': user_to_notify.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Alerta Crítica: Reabastecimiento de Farmacia',
                'note': f'El servidor detectó medicamentos por debajo del umbral mínimo ({self.min_stock_threshold} unidades). Por favor revise el inventario.',
                'date_deadline': fields.Date.context_today(self),
            })