{
    'name': "mi_modulo_1_A",

    'summary': "Gestión avanzada de actividades y equipos",

    'description': """
Módulo de práctica: agrega prioridad, checklist a actividades
y objetivos a equipos.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'activity_management_confianz'],

    'data': [
        'security/ir.model.access.csv',
        'data/res_groups_data.xml',
        'views/team_view.xml',
        'views/mail_activity.xml',
    ],
}