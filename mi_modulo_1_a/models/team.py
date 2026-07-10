# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError

class Team(models.Model):
    _name = "team.teams"
    _description = "Team"
    _inherit = ['image.mixin']

    name = fields.Char(string="Name")
    team_leader = fields.Many2one('res.users', string="Team Leader")
    member_ids = fields.Many2many('res.users', 'team_user_rel', 'teams_id', 'user_id', string="Team members")
    note = fields.Text("Notes")
    activity_count = fields.Integer(compute="_compute_activity_count")

    objective_ids = fields.One2many(
        'team.objective',   # <- modelo hijo (la tabla)
        'team_id',          # <- campo del hijo que apunta al padre
        string="Objetivos"
    )

    def _compute_activity_count(self):
        for rec in self:
            rec.activity_count = self.env['mail.activity'].search_count([('team_id', '=', rec.id)])

    def action_open_activities(self):
        action = self.env['ir.actions.actions']._for_xml_id('mail.mail_activity_action')
        action['domain'] = [('team_id', '=', self.id)]
        action['context'] = {'search_default_my_activities': 1}
        action['target'] = 'current'
        return action