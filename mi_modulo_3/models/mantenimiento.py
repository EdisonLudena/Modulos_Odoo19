# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MaintenanceSpecialty(models.Model):
    """Nuevo modelo para categorizar las especialidades del equipo de mantenimiento"""
    _name = 'maintenance.specialty'
    _description = 'Especialidad de Mantenimiento'

    name = fields.Char(string="Especialidad", required=True)
    code = fields.Char(string="Código de Especialidad")


class MaintenanceTeam(models.Model):
    """Extensión del modelo de equipos de mantenimiento"""
    _inherit = "maintenance.team"

    is_hotel = fields.Boolean(string="Is Hotel Maintenance", default=False)

    name = fields.Char(string='Maintenance Team', help='Name of the maintenance team')
    
    user_id = fields.Many2one(
        'res.users', string='Team Leader',
        help="Leader of Team",
        domain=lambda self: [
            ('group_ids', 'in', self.env.ref('hotel_management_odoo.maintenance_team_group_leader').id)
        ]
    )
    
    member_ids = fields.Many2many(
        'res.users', 
        string='Members',
        domain=[],
        help="Members of the Team"
    )

    state = fields.Selection([
        ('available', 'Disponible'),
        ('in_service', 'En Servicio / Asignado'),
        ('busy', 'Saturado')
    ], string='Estado de Disponibilidad', default='available', tracking=True)

    specialty_ids = fields.Many2many(
        'maintenance.specialty', 
        string='Especialidades del Equipo',
        help="Áreas técnicas que cubre este equipo"
    )

    member_count = fields.Integer(
        string="Total de Miembros", 
        compute='_compute_member_count', 
        store=True,
        help="Número total de técnicos asignados al equipo"
    )

    @api.depends('member_ids')
    @api.onchange('member_ids')
    def _compute_member_count(self):
        """Calcula cuántos miembros tiene el equipo automáticamente."""
        for record in self:
            record.member_count = len(record.member_ids)

    def action_set_in_service(self):
        """Pasa el equipo a 'En Servicio' con una validación de negocio."""
        for record in self:
            if not record.user_id:
                raise ValidationError("¡Atención! No puedes poner en servicio un equipo que no tiene un Líder de Equipo asignado.")
            if record.member_count == 0:
                raise ValidationError("¡Atención! Debe haber al menos 1 miembro en el equipo para ponerlo en servicio.")
            
            record.state = 'in_service'

    def action_set_busy(self):
        for record in self:
            record.state = 'busy'

    def action_set_available(self):
        for record in self:
            record.state = 'available'