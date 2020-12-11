# -*- coding: utf-8 -*-
{
    'name': "fincas_pma",

    'summary': """
        Adecuación de fincas para Panamá y ejemplo de programación de modulos en ORM-Odoo
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Máestro de fincas con parametros de Pamama.
        - Rama: dev_project
        - - Correccion bug de desinstalacion: Causado tal vez por???
        - - Agregando etiquetas: up y lote en Kanba Project.project
    """,

    'author': "Alconsoft",
    'website': "http://www.alconsoft.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.Rama: main 20201211 - 13:59',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'project', 'hr_timesheet', 'sale_management','purchase','maintenance'],

    # always loaded: Aqui se cargan los formularios de vista.
    # IMPORTANTE: SE QUITA EL CARACTER "#" PARA QUE SE PUEDA CARGAR ARCHIVO CON LA LISTA DE ACCESO DE SEGURIDAD
    'data': [
        ####### ESTO IMPEDIA QUE SE PUDIERA VER EL MENU ########################
        'security/ir.model.access.csv',
        ###############################
        'views/views.xml',
        'views/templates.xml',
        'views/labores.xml',
        'views/equiposymq.xml',
        'views/variedades.xml',
        'views/subfincas.xml',
        'views/tipo_activo.xml',
        'views/tipo_equipo.xml',
        'views/empleados.xml',
        'views/corregs.xml',
        'views/distritos.xml',
        'views/tipo_cultivo.xml',
        'views/Frentes.xml',
        'views/marca.xml',
        'views/Frentes.xml',
        'views/proyectos_uplotes.xml',
        ####### CARGA AUTOMATICA AL INSTALAR DE DATOS ESTATICOS ########################
        'static/xls/fincas_pma.fincas_pma.csv',
        'static/xls/fincas_pma.labores.csv',
        'static/xls/fincas_pma.up.csv',
        'static/xls/fincas_pma.subfincas.csv',
        'static/xls/fincas_pma.variedades.csv',
        'static/xls/fincas_pma.tiposcortes.csv',
        'static/xls/fincas_pma.zafras.csv',
        'static/xls/res.partner.csv',
        'static/xls/project.project.csv',
        'static/xls/fincas_pma.tipo_activo.csv',
        'static/xls/fincas_pma.tipo_equipo.csv',
        'static/xls/fincas_pma.frentes.csv',
        'static/xls/fincas_pma.marca.csv',
        
       # 'static/xls/maintenance.equipment.csv',
        ###############################
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # Aplicacion:  si aparace cierto (true) esta modulo sera una aplicacion que aprecera en el listado de aplicaciones de odoo.
    'application': True,
}
