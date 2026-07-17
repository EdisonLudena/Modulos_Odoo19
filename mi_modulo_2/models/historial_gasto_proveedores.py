# -*- coding: utf-8 -*-
from odoo import api, fields, models

class VendorSpendSnapshot(models.Model):
    _name = "vendor.spend.snapshot"
    _description = "Historial de Gasto por Proveedor"
    _order = "snapshot_datetime desc"

    snapshot_datetime = fields.Datetime(
        string="Fecha de Consulta",
        default=fields.Datetime.now,
        readonly=True
    )
    vendor_id = fields.Many2one('res.partner', string="Proveedor", readonly=True)
    company_id = fields.Many2one('res.company', string="Compañía", readonly=True)
    amount = fields.Float(string="Monto Gastado", readonly=True)
    percentage = fields.Float(string="% del Total", readonly=True)

    risk_level = fields.Selection([
        ('low', 'Bajo'),
        ('medium', 'Medio'),
        ('high', 'Alto')
    ], string="Riesgo de Concentración", compute="_compute_risk_level", store=True)

    @api.depends('percentage')
    def _compute_risk_level(self):
        for rec in self:
            if rec.percentage >= 50:
                rec.risk_level = 'high'
            elif rec.percentage >= 20:
                rec.risk_level = 'medium'
            else:
                rec.risk_level = 'low'


class VendorSpendInherit(models.AbstractModel):
    _inherit = "finance.vendor.spend"

    @api.model
    def get_vendor_data(self, options=None):
        res = super(VendorSpendInherit, self).get_vendor_data(options=options)
        for row in res.get("rows", []):
            self.env['vendor.spend.snapshot'].sudo().create({
                'vendor_id': row.get('id'),
                'company_id': self.env.company.id,
                'amount': row.get('amount', 0.0),
                'percentage': (row.get('pct', 0.0) or 0.0) / 100.0,
            })
        return res