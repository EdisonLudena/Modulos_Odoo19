# -*- coding: utf-8 -*-

from odoo import  api, models, modules,_
from collections import defaultdict

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_activity_groups(self):
        """Override to return only personal activities."""
        search_limit = int(self.env['ir.config_parameter'].sudo().get_param('mail.activity.systray.limit', 1000))
        activities = self.env["mail.activity"].search(
            [("user_id", "=", self.env.uid)],
            order='id desc', limit=search_limit,
        )
        return self._prepare_activity_groups_data(activities)

    @api.model
    def _get_group_activity_groups(self):
        """Fetch activities assigned to teams or teammates (sharing a team with current user)."""
        search_limit = int(self.env['ir.config_parameter'].sudo().get_param('mail.activity.systray.limit', 1000))

        # Get all team IDs the current user belongs to (or is leading)
        user_teams = self.env['team.teams'].sudo().search([
            '|',
                ('team_leader', '=', self.env.uid),
                ('member_ids', 'in', [self.env.uid]),

        ])
        
        if not user_teams:
            return []

        teammate_ids = (user_teams.mapped('member_ids') | user_teams.mapped('team_leader')).ids
        if self.env.uid in teammate_ids:
            teammate_ids.remove(self.env.uid)

        domain = [
            '|',
                ('team_id', 'in', user_teams.ids),
                ('user_id', 'in', teammate_ids),
        ]

        activities = self.env["mail.activity"].search(
            domain,
            order='id desc', limit=search_limit,
        )

        return self._prepare_activity_groups_data(activities)

    def _prepare_activity_groups_data(self, activities):
        """Common logic to prepare activity group data from a recordset of activities."""
        user_company_ids = self.env.user.company_ids.ids
        is_all_user_companies_allowed = set(user_company_ids) == set(self.env.context.get('allowed_company_ids') or [])

        activities_model_groups = defaultdict(lambda: self.env["mail.activity"])
        activities_rec_groups = defaultdict(lambda: defaultdict(lambda: self.env["mail.activity"]))

        for activity in activities:
            if activity.res_model:
                activities_rec_groups[activity.res_model][activity.res_id] += activity
            else:
                activities_rec_groups["mail.activity"][activity.id] += activity
        model_activity_states = {
            'mail.activity': {'overdue_count': 0, 'today_count': 0, 'planned_count': 0, 'total_count': 0}
        }
        for model_name, activities_by_record in activities_rec_groups.items():
            res_ids = activities_by_record.keys()
            Model = self.env[model_name]
            has_model_access_right = Model.has_access('read')
            if has_model_access_right:
                allowed_records = Model.browse(res_ids)._filtered_access('read')
            else:
                allowed_records = Model
            unallowed_records = Model.browse(res_ids) - allowed_records
            if has_model_access_right and unallowed_records and not is_all_user_companies_allowed:
                unallowed_records -= unallowed_records.with_context(
                    allowed_company_ids=user_company_ids)._filtered_access('read')
            model_activity_states[model_name] = {'overdue_count': 0, 'today_count': 0, 'planned_count': 0, 'total_count': 0}
            for record_id, activities in activities_by_record.items():
                if record_id in unallowed_records.ids:
                    model_key = 'mail.activity'
                    activities_model_groups['mail.activity'] += activities
                elif record_id in allowed_records.ids:
                    model_key = model_name
                    activities_model_groups[model_name] += activities
                elif record_id:
                    continue

                if 'overdue' in activities.mapped('state'):
                    model_activity_states[model_key]['overdue_count'] += 1
                    model_activity_states[model_key]['total_count'] += 1
                elif 'today' in activities.mapped('state'):
                    model_activity_states[model_key]['today_count'] += 1
                    model_activity_states[model_key]['total_count'] += 1
                else:
                    model_activity_states[model_key]['planned_count'] += 1

        model_ids = [self.env["ir.model"]._get_id(name) for name in activities_model_groups]
        user_activities = {}
        for model_name, activities in activities_model_groups.items():
            Model = self.env[model_name]
            module = Model._original_module
            icon = module and modules.module.get_module_icon(module)
            model = self.env["ir.model"]._get(model_name).with_prefetch(model_ids)
            user_activities[model_name] = {
                "id": model.id,
                "name": model.name if model_name != "mail.activity" else _("Other activities"),
                "model": model_name,
                "type": "activity",
                "icon": icon,
                "domain": [('active', 'in', [True, False])] if model_name != "mail.activity" and "active" in Model else [],
                "total_count": model_activity_states[model_name]['total_count'],
                "today_count": model_activity_states[model_name]['today_count'],
                "overdue_count": model_activity_states[model_name]['overdue_count'],
                "planned_count": model_activity_states[model_name]['planned_count'],
                "view_type": getattr(Model, '_systray_view', 'list'),
            }
            if model_name == 'mail.activity':
                user_activities[model_name]['activity_ids'] = activities.ids
        return list(user_activities.values())