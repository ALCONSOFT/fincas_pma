# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fincas_pma(models.Model):
    _name = 'fincas_pma.fincas_pma'
    _description = 'fincas_pma.fincas_pma - FINCAS PANAMA V.20/10/24-13:04'
    ########## A partir de la versión 13.0, un usuario puede iniciar sesión en varias empresas a la vez.
    #  Esto permite al usuario acceder a información de varias empresas, pero también crear / editar
    #  registros en un entorno de varias empresas.################
    _check_company_auto = True
    ##########################

    name = fields.Char('Nombre de Finca', required=True)
    active = fields.Boolean('Activo', default=True)
    code_finca = fields.Char('Referencia', required=True)
    description = fields.Text(string='Descripción')
    employee_in_charge = fields.Many2one('hr.employee', string='Empleado', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ########## CUANDO SE HAGAN CAMBIOS EN EL MODELO ES NECESARIO DESINSTALAR LA APPS EN ODOO
    # BORRAR LA APPS DE LA LISTA DE APLICACIONES
    # Y REINICIAR EL SERVIDOR DE ODOO #####################
    #company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    company_id = fields.Many2one('res.company', compute='_compute_employee_fincas_pma', store=True, readonly=False,
        default=lambda self: self.env.company, required=True)
    ###############################
    value_area_mts = fields.Integer('Area en mts.')
    value_area_ha = fields.Float(compute="_value_pc", store=True)
    
    @api.depends('value_area_mts')
    def _value_pc(self):
        for record in self:
            record.value_area_ha = float(record.value_area_mts) / 10000
    
    @api.depends('employee_in_charge')
    def _compute_employee_fincas_pma(self):
        for fincas_pma in self.filtered('employee_in_charge'):
            fincas_pma.company_id = fincas_pma.employee_in_charge.company_id

class provincias(models.Model):
    _name="fincas_pma.provincias"

    name = fields.Char('Nombre de Provincia', required=True)
    active = fields.Boolean('Activo', default=True)
    code_provincia = fields.Char('Código', required=True)
    description = fields.Text(string='Descripción')

class zafras(models.Model):
    _name = "fincas_pma.zafras"
    _description = "Codigos de Zafras - Cada anio una nueva: ejm.: 2020, 2021 . . . "

    name = fields.Char('Nombre de Zafra o Año:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_zafra = fields.Char('Código de Zafra', required=True)
    description = fields.Text(string='Descripción')

class frentes(models.Model):
    _name = "fincas_pma.frentes"
    _description = "Código de Frentes de Cosecha en Zafra"

    name = fields.Char('Nombre de Frente de Cosecha:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_frente = fields.Char('Código de Frente', required=True)
    description = fields.Text(string='Descripción')

class subfincas(models.Model):
    _name = "fincas_pma.subfincas"
    _description = "Código de Sub-Fincas de Cultivo de Caña"

    name = fields.Char('Nombre de Sub Finca:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_frente = fields.Char('Código de Sub-Finca', required=True)
    description = fields.Text(string='Descripción')

class up(models.Model):
    _name = "fincas_pma.up"
    _description = "Código de Unidad de Producción de Cultivo de Caña"

    name = fields.Char('Nombre de Unidad de Producción:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_frente = fields.Char('Código de U.P.', required=True)
    description = fields.Text(string='Descripción')

class tiposcortes(models.Model):
    _name = "fincas_pma.tiposcortes"
    _description = "Código de Tipos de Cortes de Cosecha de Caña"

    name = fields.Char('Nombre de Tipos de Cortes:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_frente = fields.Char('Código de T.D.C.', required=True)
    description = fields.Text(string='Descripción')

class variedades(models.Model):
    _name = "fincas_pma.variedades"
    _description = "Código de Variedades Cultivadas"

    name = fields.Char('Nombre de Vareidad de Cultivo:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_variedad = fields.Char('Código de Variedad', required=True)
    description = fields.Text(string='Descripción')

