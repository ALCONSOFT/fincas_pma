# -*- coding: utf-8 -*-
{
    'name': "Fincas PMA - Gestión Agrícola Multi-Cultivo",

    'summary': """
        Sistema integral de gestión de fincas agrícolas para Panamá,
        Centro América y Colombia. Multi-cultivo: Café, Banano, Piña,
        Palma Aceitera, Caña de Azúcar.""",

    'description': """
Fincas PMA - Sistema de Gestión Agrícola Multi-Cultivo
======================================================

Módulo completo para la gestión de fincas agrícolas basado en las
mejores prácticas internacionales de agricultura sostenible.

CULTIVOS SOPORTADOS
-------------------
* Café (Arábica, Robusta)
* Banano y Plátano
* Piña (MD2, Cayena, etc.)
* Palma Aceitera
* Caña de Azúcar
* Otros cultivos tropicales

FUNCIONALIDADES PRINCIPALES
---------------------------
* Gestión de Fincas y Lotes de Producción
* Catálogo de Cultivos y Variedades
* Ciclos de Producción (Zafras)
* Gestión de Insumos Agrícolas
* Registro de Aplicaciones con Trazabilidad
* Control Fitosanitario (MIP)
* Monitoreo de Plagas y Enfermedades
* Registro de Cosechas Multi-Cultivo
* Certificaciones de Sostenibilidad (RA, GlobalGAP, Orgánico)
* Labores Agrícolas por Lote
* Análisis de Suelos
* Trazabilidad Field-to-Mill

CERTIFICACIONES SOPORTADAS
--------------------------
* Rainforest Alliance / UTZ
* GlobalG.A.P.
* Orgánico (USDA, EU, JAS)
* Fairtrade
* RSPO (Palma)
* Bonsucro (Caña)
* 4C (Café)
* C.A.F.E. Practices

REGIONES
--------
* Panamá
* Costa Rica
* Guatemala
* Honduras
* Colombia
* Otros países de la región

CHANGELOG
---------
* v18.0.1.0.0 - Migración a Odoo 18, arquitectura multi-cultivo
* v0.2021-05-10 - Versión original para caña de azúcar
    """,

    'author': "Alconsoft",
    'website': "http://www.alconsoft.net",

    'category': 'Agriculture',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # Dependencias del módulo
    'depends': [
        'base',
        'mail',
        'hr',
        'project',
        'hr_timesheet',
        'sale_management',
        'purchase',
        'maintenance',
        'uom',
        # 'abs_project_po',  # Comentado - verificar disponibilidad en Odoo 18
    ],

    # Archivos de datos (cargados siempre)
    'data': [
        # Seguridad - Accesos
        'security/ir.model.access.csv',

        # Datos iniciales
        'data/sequences.xml',
        'data/cultivos_data.xml',

        # Vistas - Modelos base
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
        'views/marca.xml',
        'views/proyectos_uplotes.xml',

        # Vistas - Nuevos modelos multi-cultivo
        'views/cultivo_views.xml',
        'views/lote_views.xml',
        'views/insumo_views.xml',
        'views/cosecha_views.xml',
        'views/sanidad_views.xml',
        'views/certificacion_views.xml',
        'views/labor_lote_views.xml',

        # Menús principales
        'views/menus.xml',

        # Datos estáticos iniciales
        'static/xls/fincas_pma.fincas_pma.csv',
        'static/xls/fincas_pma.labores.csv',
        'static/xls/fincas_pma.subfincas.csv',
        'static/xls/fincas_pma.tipo_activo.csv',
        'static/xls/fincas_pma.frentes.csv',
        'static/xls/fincas_pma.provincias.csv',
        'static/xls/fincas_pma.corregs.csv',
        'static/xls/fincas_pma.tipo_cane.csv',
        'static/xls/fincas_pma.calendario.csv',
        'static/xls/res.partner.csv',
        'static/xls/maintenance.equipment.csv',
        'static/xls/project.project.csv',
    ],

    # Datos de demostración
    'demo': [
        'demo/demo.xml',
    ],

    # Configuración
    'installable': True,
    'application': True,
    'auto_install': False,

    # Assets para Odoo 18
    'assets': {
        'web.assets_backend': [
            # Agregar CSS/JS personalizados aquí si es necesario
        ],
    },
}
