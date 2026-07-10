# -*- coding: utf-8 -*-
from odoo import fields, models

# Este es un modelo COMPLETAMENTE NUEVO (no hereda de nada).
# Representa cada "fila" de la tabla de objetivos que vamos a
# mostrar dentro del formulario de Team.
class TeamObjective(models.Model):
    _name = 'team.objective'  # <- nombre técnico del modelo nuevo
    _description = 'Objetivo de Equipo'  # <- descripción legible

    name = fields.Char(string="Objetivo", required=True)
    # required=True significa que el campo es OBLIGATORIO,
    # no se puede guardar la fila si está vacío.

    deadline = fields.Date(string="Fecha Límite")

    is_done = fields.Boolean(string="Cumplido")

    # -----------------------------------------------------------
    # ESTE ES EL CAMPO MÁS IMPORTANTE DE TODOS:
    # -----------------------------------------------------------
    # team_id conecta cada objetivo con SU equipo (team.teams).
    # Es un Many2one: "muchos objetivos pertenecen a UN equipo".
    # ondelete='cascade' significa: "si se borra el equipo,
    # borra también todos sus objetivos" (para no dejar basura).
    team_id = fields.Many2one(
        'team.teams',
        string="Equipo",
        ondelete='cascade'
    )