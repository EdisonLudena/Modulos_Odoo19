# -*- coding: utf-8 -*-
{
    'name': "Dashboard de Gimnasio (mi_modulo_4)",

    'summary': "Agrega vistas analíticas (BI), calendario y mejoras UX",

    'description': """
        Este módulo extiende la funcionalidad del sistema de gimnasio agregando:
        - Vistas de Calendario para planificar entrenamientos.
        - Vistas Gráficas (Graph) y Tablas Dinámicas (Pivot) para Business Intelligence.
        - Widgets visuales como barras de progreso y valoraciones (priority).
    """,

    'author': "Edison Ludeña",
    'website': "https://www.ute.edu.ec",

    'category': 'Services',
    'version': '19.0.1.0.0',

    # DEPENDENCIAS CRÍTICAS: 
    # Si no pones 'gym_mgmt_system' aquí, Odoo dará error al instalar
    # porque no encontrará el modelo 'workout.plan' que estamos heredando.
    'depends': ['base', 'gym_mgmt_system'],

    'data': [
        # Comentamos la seguridad porque no creamos modelos nuevos hoy
        # 'security/ir.model.access.csv',
        
        # Aquí cargamos el archivo XML con nuestras nuevas vistas
        'views/views.xml',
    ],
    
    'installable': True,
    'application': False,
}