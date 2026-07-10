# -*- coding: utf-8 -*-
from odoo import fields, models

class MailActivityChecklist(models.Model):
    _name = 'mail.activity.checklist'
    _description = 'Subtarea de Actividad'

    name = fields.Char(string="Tarea", required=True)
    is_done = fields.Boolean(string="Completado")

    activity_id = fields.Many2one(
        'mail.activity',
        string="Actividad",
        ondelete='cascade'
    )