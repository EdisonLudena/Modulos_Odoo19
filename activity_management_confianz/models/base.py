# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.fields import Domain
from odoo.exceptions import AccessError


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _search(self, domain, *args, **kwargs):

        target_model = self.env.context.get('group_activity_target_model')

        if self.env.context.get('group_activities_only') and self._name == target_model:

            try:
                self.check_access("read")
            except AccessError:
                return super()._search(domain, *args, **kwargs)

            user = self.env.user

            user_teams = self.env["team.teams"].sudo().with_context(
                group_activities_only=False
            ).search([
                '|',
                ('team_leader', '=', user.id),
                ('member_ids', 'in', [user.id]),
            ])

            if user_teams:
                teammate_ids = (
                    user_teams.mapped('member_ids') |
                    user_teams.mapped('team_leader')
                ).ids

                if user.id in teammate_ids:
                    teammate_ids.remove(user.id)

                if self._name == 'mail.activity':
                    personal_user_ids = teammate_ids + [user.id]

                    team_domain = [
                        '|',
                        ('team_id', 'in', user_teams.ids),
                        '&',
                        ('user_id', 'in', personal_user_ids),
                        ('team_id', '=', False)
                    ]
                else:
                    team_domain = [
                        ('activity_ids', 'any', [
                            ('active', 'in', [True, False]),
                            '|',
                            ('team_id', 'in', user_teams.ids),
                            '&',
                            ('user_id', 'in', teammate_ids),
                            ('team_id', '=', False)
                        ])
                    ]

                domain = list(Domain(domain) & Domain(team_domain))

            else:
                # fallback same as original
                domain = list(Domain(domain) & Domain([('user_id', '=', user.id)]))

        return super()._search(domain, *args, **kwargs)