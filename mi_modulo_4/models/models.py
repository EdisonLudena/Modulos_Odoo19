# -*- coding: utf-8 -*-
from odoo import api, fields, models

class WorkoutPlan(models.Model):
    _inherit = "workout.plan"

    difficulty = fields.Selection([
        ('1', 'Principiante'),
        ('2', 'Intermedio'),
        ('3', 'Avanzado')
    ], string='Nivel de Dificultad', default='1', tracking=True)

    date_start = fields.Datetime(string="Fecha de Inicio Programada")
    date_end = fields.Datetime(string="Fecha de Fin Programada")
    
    trainer_id = fields.Many2one('hr.employee', string="Entrenador Asignado")

    total_exercises = fields.Integer(
        string="Total Ejercicios", 
        compute="_compute_totals", 
        store=True # Obligatorio para poder usarlo en gráficos y pivot
    )
    completed_exercises = fields.Integer(string="Ejercicios Completados", default=0)
    
    progress = fields.Float(
        string="Progreso del Plan (%)", 
        compute="_compute_progress"
    )

    @api.depends('workout_plan_option_ids')
    def _compute_totals(self):
        """Calcula el total de ejercicios para las métricas de BI."""
        for plan in self:
            plan.total_exercises = len(plan.workout_plan_option_ids)

    @api.depends('total_exercises', 'completed_exercises')
    def _compute_progress(self):
        """Calcula el porcentaje de completitud para el widget progressbar."""
        for plan in self:
            if plan.total_exercises > 0:
                plan.progress = (plan.completed_exercises / plan.total_exercises) * 100
            else:
                plan.progress = 0.0