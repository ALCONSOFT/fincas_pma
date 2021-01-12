# -*- coding: utf-8 -*-

from odoo import models, fields, api

class labores(models.Model):
    _name = 'fincas_pma.labores'
    _description = 'fincas_pma.labores - LABORES DE FINCAS PANAMA V.20/11/14-17:10'
    ########## A partir de la versión 13.0, un usuario puede iniciar sesión en varias empresas a la vez.
    #  Esto permite al usuario acceder a información de varias empresas, pero también crear / editar
    #  registros en un entorno de varias empresas.################
    _check_company_auto = True
    ##########################

    name = fields.Char('Nombre de Labor', required=True)
    active = fields.Boolean('Activo', default=True)
    code_labor = fields.Char('Código Labor', required=True, index=True)
    description = fields.Text(string='Descripción')
    #employee_in_charge = fields.Many2one('hr.employee', string='Empleado', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ########## CUANDO SE HAGAN CAMBIOS EN EL MODELO ES NECESARIO DESINSTALAR LA APPS EN ODOO
    # BORRAR LA APPS DE LA LISTA DE APLICACIONES
    # Y REINICIAR EL SERVIDOR DE ODOO #####################
    # - company_id = fields.Many2one('res.company', compute='_compute_employee_fincas_pma', store=True, readonly=False,
    # -     default=lambda self: self.env.company, required=True)
    ###############################
    rata_labor = fields.Float(string='Rata de Labor', required=True, digits=(14, 4), store=True)
    unidad_medida = fields.Many2one('uom.uom', string='Unidad de Medida', tracking=True)
    cantidad_minima = fields.Float(string='Cantidad Mínima de Labor', required=True, digits=(14, 4), store=True)
    cantidad_maxima = fields.Float(string='Cantidad Máxima de Labor', required=True, digits=(14, 4), store=True)
    equivalencia_tiempo = fields.Float(string='Equivalencia en Tiempo de Labor', required=True, digits=(14, 4), store=True)
    observacion = fields.Text(string='Observaciones')
    external_id = fields.Char(string='External Reference', states={'open': [('readonly', False)]}, copy=False, readonly=True, help="Used to hold the reference of the external mean that created this statement (name of imported file, reference of online synchronization...)")    
    
    #SQL constraints are defined through the model attribute _sql_constraints.
    #  The latter is assigned to a list of triples of strings 
    # (name, sql_definition, message), where name is a valid SQL constraint
    #  name, sql_definition is a table_constraint expression, and message is
    #  the error message.
    _sql_constraints = [
        ('code_labor_unique',
         'UNIQUE(code_labor)',
         "El código de Labor debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "The Labor title must be unique"),
    ]    