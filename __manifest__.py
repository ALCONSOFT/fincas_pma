# -*- coding: utf-8 -*-
{
    'name': "fincas_pma",

    'summary': """
        Adecuación de fincas para Panamá y ejemplo de programación de modulos en ORM-Odoo
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Máestro de fincas con parametros de Pamama.
        - Rama: Main
        - - Correccion bug de desinstalacion: Causado tal vez por???
        - - Agregando etiquetas: up y lote en Kanba Project.project
        Máestro de fincas con  parametros de Pamama.
    """,

    'author': "Alconsoft",
    'website': "http://www.alconsoft.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2021-01-11 - 19:00',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'project', 'hr_timesheet', 'sale_management','purchase','maintenance','abs_project_po'],

    # always loaded: Aqui se cargan los formularios de vista.
    # IMPORTANTE: SE QUITA EL CARACTER "#" PARA QUE SE PUEDA CARGAR ARCHIVO CON LA LISTA DE ACCESO DE SEGURIDAD
    'data': [
        ####### ESTO IMPEDIA QUE SE PUDIERA VER EL MENU ########################
        'security/ir.model.access.csv',
        ###############################
        'views/views.xml',
        'views/templates.xml',
        'views/Frentes.xml',
        'views/up.xml',
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
        'static/xls/fincas_pma.tipo_activo.csv',
        'static/xls/fincas_pma.tipo_equipo.csv',
        'static/xls/fincas_pma.frentes.csv',
        'static/xls/fincas_pma.marca.csv',
        'static/xls/fincas_pma.provincias.csv',
        'static/xls/fincas_pma.distritos.csv',
        'static/xls/fincas_pma.corregs.csv',
        'static/xls/fincas_pma.tipo_cane.csv',
        'static/xls/fincas_pma.calendario.csv',##error al cargar la fechahora-se corrigio erae el formato de fecha##
        ####### archivos dependientes
        'static/xls/res.partner.csv',
        'static/xls/maintenance.equipment.csv',
        #'static/xls/account_analytic_account.csv',
        'static/xls/project.project.csv',

        ###############################
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
    # Aplicacion:  si aparace cierto (true) esta modulo sera una aplicacion que aprecera en el listado de aplicaciones de odoo.
    'application': True,
}
