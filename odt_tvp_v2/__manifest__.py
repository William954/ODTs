# -*- coding: utf-8 -*-
{
    'name': "ODTs",
    'summary': """
        Modulo para ODT's""",
    'description': """
        Este modulo es exclusivo para la empresa GTVP cuya funcionalidad es proporcionar vistas kanban para el manejo de la informacion "Ordenes de Trabajo"
    """,
    'author': "Xmarts",
    'website': "http://www.xmarts.com",
    'category': 'Modulo',
    'version': '2.0',

    'depends': ['base',
            'contacts',
            'hr',
            'sale',
            'crm',
            'project',
            'sale_management',
            'account',
            'account_accountant',
            'account_budget'
            ],
    'data': [
        'views/btlpdv.xml',
        'views/contact.xml',
        'views/diseno.xml',
        'views/estrategia.xml',
        'views/gestoria.xml',
        'views/marketing.xml',
        'views/produccion.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/medios.xml',
        'views/contact.xml',
        'views/logistica.xml',
        'views/groups_odts.xml',
        'security/ir.model.access.csv',
        'sequence/odt_sequence.xml',
        'wizard/selection_odt.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable': True,
    'aplication': True,
    'auto_install': False,
}