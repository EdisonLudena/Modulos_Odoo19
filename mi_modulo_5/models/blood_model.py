from odoo import api, fields, models
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class BloodDiscardLog(models.Model):
    _name = 'blood.discard.log'
    _description = 'Registro de Descarte de Sangre'
    _order = 'discard_date desc'

    name = fields.Char(related='blood_bank_id.name', string='Referencia', store=True)
    blood_bank_id = fields.Many2one('blood.bank', string='Bolsa de Sangre', required=True, readonly=True, ondelete='cascade')
    blood_type = fields.Selection(related='blood_bank_id.blood_type', string='Grupo Sanguíneo', store=True)
    discard_date = fields.Datetime(string='Fecha de Descarte', default=fields.Datetime.now, readonly=True)
    reason = fields.Char(string='Motivo', required=True, readonly=True)
    responsible_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user, readonly=True)


class BloodBank(models.Model):
    _inherit = 'blood.bank'

    state = fields.Selection(
        selection_add=[('expired', 'Caducada (Desechada)')],
        ondelete={'expired': 'set default'}
    )
    
    expiration_date = fields.Date(string='Fecha de Caducidad', compute='_compute_expiration_date', store=True)
    days_to_expire = fields.Integer(string='Días Restantes', compute='_compute_days_to_expire')
    is_critical = fields.Boolean(string='Caducidad Crítica', compute='_compute_days_to_expire', store=True)
    discard_log_count = fields.Integer(compute='_compute_discard_log_count')

    @api.depends('date')
    def _compute_expiration_date(self):
        for record in self:
            if record.date:
                record.expiration_date = record.date + timedelta(days=35)
            else:
                record.expiration_date = False

    @api.depends('expiration_date', 'state')
    def _compute_days_to_expire(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.expiration_date and record.state == 'avail':
                delta = record.expiration_date - today
                record.days_to_expire = delta.days
                record.is_critical = True if 0 <= delta.days <= 3 else False
            else:
                record.days_to_expire = 0
                record.is_critical = False

    def _compute_discard_log_count(self):
        for record in self:
            record.discard_log_count = self.env['blood.discard.log'].search_count([('blood_bank_id', '=', record.id)])

    @api.model
    def action_change_availability(self):
        today = fields.Date.context_today(self)
        
        expired_bags = self.search([
            ('state', '=', 'avail'),
            ('expiration_date', '<', today)
        ])
        
        if expired_bags:
            discard_logs_data = []
            
            for bag in expired_bags:
                bag.state = 'expired'
                discard_logs_data.append({
                    'blood_bank_id': bag.id,
                    'reason': 'Caducidad automática del servidor (35 días superados)',
                    'responsible_id': self.env.ref('base.user_root').id
                })
            
            if discard_logs_data:
                self.env['blood.discard.log'].create(discard_logs_data)
                
            _logger.info(f"CRON: Procesamiento en lote (Batch). {len(expired_bags)} bolsas descartadas.")

    def action_view_discard_logs(self):
        self.ensure_one()
        return {
            'name': 'Logs de Descarte',
            'type': 'ir.actions.act_window',
            'res_model': 'blood.discard.log',
            'view_mode': 'list,form',
            'domain': [('blood_bank_id', '=', self.id)],
        }