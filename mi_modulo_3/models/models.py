# -*- coding: utf-8 -*-
from odoo import api, fields, models

class FleetVipAmenity(models.Model):
    _name = 'fleet.vip.amenity'
    _description = 'Amenidades VIP para Vehículos'

    name = fields.Char(string="Nombre de la Amenidad", required=True)
    cost = fields.Float(string="Costo", help="Costo de agregar esta amenidad")


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('review', 'En Revisión Premium'),
        ('approved', 'Aprobado')
    ], string='Estado Premium', default='draft', tracking=True)

    needs_special_cleaning = fields.Boolean(string="Requiere Limpieza Especial", default=False)
    has_vip_package = fields.Boolean(string="Ofrece Paquete VIP", default=False)

    cleaning_provider = fields.Char(string="Proveedor de Limpieza")
    cleaning_cost = fields.Float(string="Costo de Limpieza")
    
    vip_amenity_ids = fields.Many2many('fleet.vip.amenity', string="Amenidades Incluidas")
    
    total_premium_cost = fields.Float(
        string="Costo Premium Total", 
        compute='_compute_total_premium_cost', 
        store=True, 
        help="Suma automática de limpieza y amenidades VIP"
    )

    @api.depends('needs_special_cleaning', 'cleaning_cost', 'has_vip_package', 'vip_amenity_ids.cost')
    def _compute_total_premium_cost(self):
        """Calcula el costo total basándose en los checklists y las selecciones."""
        for record in self:
            total = 0.0
            if record.needs_special_cleaning:
                total += record.cleaning_cost
            if record.has_vip_package:
                total += sum(record.vip_amenity_ids.mapped('cost'))
            record.total_premium_cost = total

    def action_submit_review(self):
        for record in self:
            record.state = 'review'

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_reset_draft(self):
        for record in self:
            record.state = 'draft'