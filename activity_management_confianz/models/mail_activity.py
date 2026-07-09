# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.fields import Domain
from odoo.addons.mail.tools.discuss import Store

class MailActivity(models.Model):
    _inherit = "mail.activity"

    team_id = fields.Many2one('team.teams', string="Team")
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
            self.user_id =  False

    def action_done_schedule_next(self):
        self.ensure_one()
        team_id = self.team_id.id
        action = super(MailActivity, self).action_done_schedule_next()
        if team_id:
            if 'context' not in action:
                action['context'] = {}
            action['context']['default_team_id'] = team_id
        return action

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, archiving activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automaticaly created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to archive. This way, we
        # can link them to the message posted and prevent their disparition. The move is done in
        # sudo to avoid losing inaccessible attachments.
        activity_attachments = self.env['ir.attachment'].sudo().search_fetch([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['res_id']).grouped('res_id')

        for model, activity_data in self.filtered('res_model')._classify_by_model().items():
            # Allow user without access to the record to "mark as done" activities assigned to them. At the end of the
            # method, the activity is archived which ensure the user has enough right on the activities.
            records_sudo = self.env[model].sudo().browse(activity_data['record_ids'])
            for record_sudo, activity in zip(records_sudo, activity_data['activities']):
                # extract value to generate next activities
                if activity.chaining_type == 'trigger':
                    vals = activity.with_context(activity_previous_deadline=activity.date_deadline)._prepare_next_activity_values()
                    next_activities_values.append(vals)

                is_team_member = False
                if activity.team_id:
                     is_team_member = self.env.user in activity.team_id.member_ids or self.env.user == activity.team_id.team_leader

                # post message on activity, before deleting it
                activity_message = record_sudo.message_post_with_source(
                    'mail.message_activity_done',
                    attachment_ids=attachment_ids,
                    author_id=self.env.user.partner_id.id,
                    render_values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user,
                        'display_team': activity.team_id and not is_team_member,
                    },
                    mail_activity_type_id=activity.activity_type_id.id,
                    subtype_xmlid='mail.mt_activities',
                )
                if attachment_ids:
                    activity.attachment_ids = attachment_ids

                # Moving the attachments in the message
                # TODO: Fix void res_id on attachment when you create an activity with an image
                # directly, see route /web_editor/attachment/add
                if message_attachments := activity_attachments.get(activity.id):
                    message_attachments.write({
                        'res_id': activity_message.id,
                        'res_model': activity_message._name,
                    })
                    activity_message.attachment_ids = message_attachments
                messages += activity_message

        next_activities = self.env['mail.activity']
        if next_activities_values:
            next_activities = self.env['mail.activity'].create(next_activities_values)

        # once done, archive to keep history without keeping them alive
        self.action_archive()
        if feedback:
            self.feedback = feedback
        return messages, next_activities

    def action_feedback_schedule_next(self, feedback=False, attachment_ids=None):
        team_id = self.team_id.id
        action = super(MailActivity, self).action_feedback_schedule_next(feedback=feedback, attachment_ids=attachment_ids)
        if team_id:
            if 'context' not in action:
                action['context'] = {}
            action['context']['default_team_id'] = team_id
        return action

    def activity_format(self):
        res = super(MailActivity, self).activity_format()
        if 'mail.activity' in res:
            for activity in res['mail.activity']:
                activity_record = self.browse(activity['id'])
                if activity_record.team_id:
                    activity['team_id'] = {
                        'id': activity_record.team_id.id,
                        'name': activity_record.team_id.display_name,
                        'image_url': f'/web/image/team.teams/{activity_record.team_id.id}/image_128'
                    }
                else:
                    activity['team_id'] = False
        return res

    def _to_store_defaults(self, target):
        res = super()._to_store_defaults(target)
        res.append(Store.Attr("team_id", lambda rec: {
            "id": rec.team_id.id,
            "name": rec.team_id.display_name,
            "image_url": f"/web/image/team.teams/{rec.team_id.id}/image_128",
        } if rec.team_id else False))
        return res

class MailActivityMixin(models.AbstractModel):
    """
    Extend mail.activity.mixin to make activity search methods
    aware of team (team_id) membership.

    The systray navigation uses these hidden search filters:
      - search_default_filter_activities_my   → activity_user_id = uid
      - search_default_activities_overdue     → my_activity_date_deadline < today
      - search_default_activities_today       → my_activity_date_deadline = today
      - search_default_activities_upcoming_all→ my_activity_date_deadline > today

    Both 'activity_user_id' and 'my_activity_date_deadline' use only
    user_id, ignoring team_id.  We override the search methods here so
    that records whose activities are assigned to a team that includes the
    current user also show up.
    """
    _inherit = 'mail.activity.mixin'

    @api.model
    def _search_activity_user_id(self, operator, operand):
        """
        Extend: also match activities where the current user is a member
        of the activity's team (team_id).
        """
        if operator in Domain.NEGATIVE_OPERATORS:
            return NotImplemented

        base_domain = super()._search_activity_user_id(operator, operand)

        if not self.env.context.get('group_activities_only'):
            return base_domain

        # Team/Teammate logic: records where any activity's team includes the current user
        # OR where the activity is assigned to a teammate.
        user_teams = self.env['team.teams'].sudo().search([
            '|',
                ('team_leader', '=', self.env.uid),
                ('member_ids', 'in', [self.env.uid]),

        ])

        if not user_teams:
            return [('id', '=', False)]

        teammate_ids = (user_teams.mapped('member_ids') | user_teams.mapped('team_leader')).ids
        if self.env.uid in teammate_ids:
            teammate_ids.remove(self.env.uid)

        team_domain = [
            ('activity_ids', 'any', [
                ('active', 'in', [True, False]),
                '|',
                    ('team_id', 'in', user_teams.ids),
                    ('user_id', 'in', teammate_ids),
            ])
        ]
        return team_domain

    def _search_my_activity_date_deadline(self, operator, operand):
        """
        Extend: also match records where a team activity (team_id with
        current user as member) has a deadline matching the filter.
        """
        if operator in Domain.NEGATIVE_OPERATORS:
            return NotImplemented

        base_domain = super()._search_my_activity_date_deadline(operator, operand)

        if not self.env.context.get('group_activities_only'):
            return base_domain

        user_teams = self.env['team.teams'].sudo().search([
            '|',
                ('team_leader', '=', self.env.uid),
                ('member_ids', 'in', [self.env.uid]),
        ])

        if not user_teams:
            return [('id', '=', False)]

        teammate_ids = (user_teams.mapped('member_ids') | user_teams.mapped('team_leader')).ids
        if self.env.uid in teammate_ids:
            teammate_ids.remove(self.env.uid)

        team_domain = [('activity_ids', 'any', [
            ('active', '=', True),
            ('date_deadline', operator, operand),
            ('res_model', '=', self._name),
            '|',
                ('team_id', 'in', user_teams.ids),
                ('user_id', 'in', teammate_ids)
        ])]
        return team_domain

