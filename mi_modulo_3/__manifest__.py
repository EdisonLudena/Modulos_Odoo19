# -*- coding: utf-8 -*-
{
    'name': "Servicios Premium de Vehículos (mi_modulo_3)",

    'summary': "Añade flujos de aprobación y servicios VIP a los vehículos",

    'description': """
        Este módulo extiende el modelo de vehículos en Odoo para incluir:
        - Una máquina de estados (Borrador, En Revisión, Aprobado).
        - Checklists dinámicos para Limpieza Especial y Paquetes VIP.
        - Pestañas invisibles y campos de solo lectura basados en el estado.
        - Campos calculados para sumar el costo total premium.
    """,

    'author': "Edison Ludeña",
    'website': "https://www.ute.edu.ec",

    'category': 'Services',
    # Es buena práctica poner la versión de Odoo al principio
    'version': '19.0.1.0.0', 

    # DEPENDENCIAS IMPORTANTES: 
    # 'fleet' es obligatorio porque estamos heredando 'fleet.vehicle.model'
    # 'hotel_management_odoo' es necesario si el modelo base de tu proyecto lo requiere
    'depends': ['base', 'fleet', 'hotel_management_odoo'],

    # ARCHIVOS DE DATOS: El orden es vital. Siempre la seguridad primero.
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml', 
        'views/mantenimiento.xml',
        # Asegúrate de que el nombre de tu archivo XML coincida con este. 
        # Si le pusiste otro nombre (ej. fleet_vehicle_premium_views.xml), cámbialo aquí.
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}