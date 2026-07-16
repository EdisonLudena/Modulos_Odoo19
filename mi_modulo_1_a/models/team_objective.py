
from odoo import fields, models

class TeamObjective(models.Model):
    _name = 'team.objective'  
    _description = 'Objetivo de Equipo'  

    name = fields.Char(string="Objetivo", required=True)


    deadline = fields.Date(string="Fecha Límite")

    is_done = fields.Boolean(string="Cumplido")

    team_id = fields.Many2one(
        'team.teams',
        string="Equipo",
        ondelete='cascade'
    )