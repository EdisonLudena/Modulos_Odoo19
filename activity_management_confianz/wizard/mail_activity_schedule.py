# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    team_id = fields.Many2one('team.teams', string="Team", store=True)
    allowed_user_ids = fields.Many2many('res.users', string='Allowed Users', compute='_compute_allowed_user_ids')

    @api.depends('team_id', 'team_id.member_ids', 'team_id.team_leader')
    def _compute_allowed_user_ids(self):
        for rec in self:
            users = rec.team_id.member_ids
            if rec.team_id.team_leader:
                users |= rec.team_id.team_leader
            rec.allowed_user_ids = users

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id:
            self.activity_user_id = False

    def _action_schedule_activities(self):
        """Override to propagate team_id (Team) to document-linked activities."""
        activity = super()._action_schedule_activities()
        if activity and self.team_id:
            activity.write({'team_id': self.team_id.id})
        return activity