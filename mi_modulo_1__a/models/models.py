from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    # 1. AUMENTAR: Nuevos campos para la regla de negocio
    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta')
    ], string="Prioridad", default='1')
    from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    # 1. AUMENTAR: Nuevos campos para la regla de negocio
    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta')
    ], string="Prioridad", default='1')
    
    requires_approval = fields.Boolean(
        string="Requiere Aprobación de Líder", 
        compute="_compute_requires_approval", 
        store=True
    )

    @api.depends('priority', 'team_id')
    def _compute_requires_approval(self):
        for rec in self:
            rec.requires_approval = rec.priority == '2' and bool(rec.team_id)

    # 1. AUMENTAR: Validación estricta (Constraint)
    @api.constrains('date_deadline', 'priority')
    def _check_high_priority_deadline(self):
        for rec in self:
            if rec.priority == '2' and rec.date_deadline and rec.date_deadline < fields.Date.today():
                raise ValidationError("Las actividades de Alta Prioridad no pueden guardarse con fechas de vencimiento pasadas.")

    # 2. MODIFICAR: Interceptar la finalización para añadir logs de auditoría
    def _action_done(self, feedback=False, attachment_ids=None):
        for rec in self:
            if rec.priority == '2' and rec.team_id:
                feedback = f"[ACTIVIDAD CRÍTICA DE EQUIPO] {feedback or ''}"
        
        return super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)
    requires_approval = fields.Boolean(
        string="Requiere Aprobación de Líder", 
        compute="_compute_requires_approval", 
        store=True
    )

    @api.depends('priority', 'team_id')
    def _compute_requires_approval(self):
        for rec in self:
            rec.requires_approval = rec.priority == '2' and bool(rec.team_id)

    # 1. AUMENTAR: Validación estricta (Constraint)
    @api.constrains('date_deadline', 'priority')
    def _check_high_priority_deadline(self):
        for rec in self:
            if rec.priority == '2' and rec.date_deadline and rec.date_deadline < fields.Date.today():
                raise ValidationError("Las actividades de Alta Prioridad no pueden guardarse con fechas de vencimiento pasadas.")

    # 2. MODIFICAR: Interceptar la finalización para añadir logs de auditoría
    def _action_done(self, feedback=False, attachment_ids=None):
        for rec in self:
            if rec.priority == '2' and rec.team_id:
                feedback = f"[ACTIVIDAD CRÍTICA DE EQUIPO] {feedback or ''}"
        
        return super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)