# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from datetime import date


class FinanceReportAudit(models.Model):
    _name = "finance.report.audit"
    _description = "Bitácora de Auditoría de Reportes Financieros"
    _order = "consultation_datetime desc"

    consultation_datetime = fields.Datetime(
        string="Fecha y Hora de Consulta", 
        default=fields.Datetime.now, 
        readonly=True
    )

    user_id = fields.Many2one(
        'res.users', 
        string="Consultado por", 
        default=lambda self: self.env.user, 
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company', 
        string="Compañía", 
        readonly=True
    )

    net_amount = fields.Float(
        string="Utilidad Neta Calculada", 
        readonly=True
    )


    alert_level = fields.Selection([
        ('danger', 'Crítico (Pérdidas)'),
        ('success', 'Saludable (Ganancias)')
    ], string="Estado Financiero", compute="_compute_alert_level", store=True)

    @api.depends('net_amount')
    def _compute_alert_level(self):
        for rec in self:
            if rec.net_amount < 0:
                rec.alert_level = 'danger'
            else:
                rec.alert_level = 'success'


class IncomeExpenseDonutInherit(models.AbstractModel):
    _inherit = "finance.income.expense.donut"

    @api.model
    def get_donut_data(self, options=None):
        res = super(IncomeExpenseDonutInherit, self).get_donut_data(options=options)
        
        self.env['finance.report.audit'].create({
            'company_id': self.env.company.id,
            'net_amount': res.get('net', 0.0),
        })
        
        return res
        
        
        
        
        