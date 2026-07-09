{
    'name': 'Activity Management',
    'version': '19.0.0.0.1',
    'summary': 'Manage personal and team activities from systray with real-time tracking',
    'description': """
Activity Management
===================

Activity Management enhances Odoo's default activity system by introducing
team-based activity tracking and a centralized view of all activities.

Key Features
------------
* View personal and team activities in one place
* Access activities directly from the systray menu
* Real-time counters for overdue and today’s tasks
* Organize users into teams with leaders and members
* Improved visibility and accountability across teams
* Quick access to activity details without navigation

Benefits
--------
* Reduces missed follow-ups
* Improves team coordination
* Increases productivity
* Centralizes activity management

This module seamlessly integrates with Odoo's existing mail activity system
and works across all applications that use activities.
    """,
    'category': 'Productivity',
    'author': 'Confianz Global Inc',
    'website': 'https://www.confianzit.com',
    'support': 'odooappsupport@confianzit.com',
    'license': 'OPL-1',
    'images': ['static/description/banner.png'],
    'depends': ['base','mail'],
    'data': [
        'security/activity_security.xml',
        'security/ir.model.access.csv',
        'wizard/mail_activity_schedule.xml',
        'views/mail_activity.xml',
        'views/team_view.xml',
        'views/mail_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'activity_management_confianz/static/src/core/web/store_service_patch.js',
            'activity_management_confianz/static/src/core/web/group_activity_menu.js',
            'activity_management_confianz/static/src/core/web/group_activity_menu.xml',
            'activity_management_confianz/static/src/core/common/activity_model_patch.js',
            'activity_management_confianz/static/src/core/web/activity.xml',
        ],
    },
}
