# -*- coding: utf-8 -*-
{
    'name': "fincas_pma",

    'summary': """
        Adecuación de fincas para Panamá y ejemplo de programación de modulos en ORM-Odoo
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Máestro de fincas con  parametros de Pamama
    """,

    'author': "Alconsoft",
    'website': "http://www.alconsoft.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1-20-11-05 - 21:34',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'project'],

    # always loaded: Aqui se cargan los formularios de vista.
    # IMPORTANTE: SE QUITA EL CARACTER "#" PARA QUE SE PUEDA CARGAR ARCHIVO CON LA LISTA DE ACCESO DE SEGURIDAD
    'data': [
        ####### ESTO IMPEDIA QUE SE PUDIERA VER EL MENU ########################
        'security/ir.model.access.csv',
        ###############################
        'views/views.xml',
        'views/templates.xml',
        ####### CARGA AUTOMATICA AL INSTALAR DE DATOS ESTATICOS ########################
        'static/xls/fincas_pma.fincas_pma.csv'
        ###############################
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # Aplicacion:  si aparace cierto (true) esta modulo sera una aplicacion que aprecera en el listado de aplicaciones de odoo.
    'application': True,
}
