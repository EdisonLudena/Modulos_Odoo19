# -*- coding: utf-8 -*-
{
    'name': "Automatización de Reabastecimiento de Farmacia (mi_modulo_5)",

    'summary': "Monitoreo desatendido mediante Cron Jobs y asignación automática de actividades.",

    'description': """
        Este módulo implementa lógica de servidor en segundo plano para infraestructura hospitalaria:
        - Tarea programada (ir.cron) para revisión nocturna del inventario de farmacias.
        - Creación programática de actividades de Odoo (mail.activity) para los farmacéuticos responsables.
        - Prevención de duplicados en notificaciones y alertas de bajo stock en tiempo real.
    """,

    'author': "Tu Nombre / Empresa",
    'website': "https://www.tuweb.com",

    'category': 'Healthcare',
    'version': '19.0.1.0.0',

    'depends': ['base', 'mail', 'base_hospital_management'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/views.xml',
        'views/blood_view.xml',
    ],
    
    'installable': True,
    'application': False,
}