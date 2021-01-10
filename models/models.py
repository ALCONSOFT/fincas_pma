# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

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

    _sql_constraints = [
        ('code_finca_unique',
         'UNIQUE(code_finca)',
         "El código de Finca debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de Finca debe ser único"),
    ]    

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

    _sql_constraints = [
        ('code_zafra_unique',
         'UNIQUE(code_zafra)',
         "El código de zafra debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de zafra debe ser único"),
    ]    


class frentes(models.Model):
    _name = "fincas_pma.frentes"
    _description = "Código de Frentes de Cosecha en Zafra"

    name = fields.Char('Nombre de Frente de Cosecha:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_frente = fields.Char('Código de Frente', required=True)
    employee_in_charge = fields.Many2one('hr.employee', string='Empleado', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', compute='_compute_employee_fincas_pma', store=True, readonly=False,
        default=lambda self: self.env.company, required=True)
    employee_in_charge2 = fields.Many2one('hr.employee', string='Responbles', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    value_area_mts = fields.Integer('Area en mts.')
    value_area_ha = fields.Float(compute="_value_pc", store=True)
    description = fields.Text(string='Descripción')

    _sql_constraints = [
        ('code_frente_unique',
         'UNIQUE(code_frente)',
         "El código de Frente debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de Frente debe ser único"),
    ]    


class subfincas(models.Model):
    _name = "fincas_pma.subfincas"
    _description = "Código de Sub-Fincas de Cultivo de Caña"

    name = fields.Char('Nombre de Sub Finca:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_subfinca = fields.Char('Código de Sub-Finca', required=True)
    description = fields.Text(string='Descripción')

    _sql_constraints = [
        ('code_subfinca_unique',
         'UNIQUE(code_subfinca)',
         "El código de subfinca debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de subfinca debe ser único"),
    ]    


class up(models.Model):
    _name = "fincas_pma.up"
    _description = "Código de Unidad de Producción de Cultivo de Caña"

    name = fields.Char('Nombre de Unidad de Producción:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_up = fields.Char('Código de U.P.', required=True)
    description = fields.Text(string='Descripción')
    partner_id = fields.Many2one('res.partner', string='Proveedor', required=False, change_default=True, tracking=True)


    _sql_constraints = [
        ('code_up_unique',
         'UNIQUE(code_up)',
         "El código de UP debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de UP debe ser único"),
    ]    


class tiposcortes(models.Model):
    _name = "fincas_pma.tiposcortes"
    _description = "Código de Tipos de Cortes de Cosecha de Caña"

    name = fields.Char('Nombre de Tipos de Cortes:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_tipocorte = fields.Char('Código de T.D.C.', required=True)
    description = fields.Text(string='Descripción')

    _sql_constraints = [
        ('code_tipocorte_unique',
         'UNIQUE(code_tipocorte)',
         "El código de tipo de corte debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de tipocorte debe ser único"),
    ]    


class variedades(models.Model):
    _name = "fincas_pma.variedades"
    _description = "Código de Variedades Cultivadas"

    name = fields.Char('Nombre de Vareidad de Cultivo:', required=True)
    active = fields.Boolean('Activo', default=True)
    code_variedad = fields.Char('Código de Variedad', required=True)
    description = fields.Text(string='Descripción')

    _sql_constraints = [
        ('code_variedad_unique',
         'UNIQUE(code_variedad)',
         "El código de variedad debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de variedad debe ser único"),
    ]    


class distritos(models.Model):
    _name = "fincas_pma.distritos"
    _description = "Distritos de la Rep. de Panamá"

    name = fields.Char('Nombre de Distrito de la Ubicación de la U.P.+Lot:', required=True)
    active = fields.Boolean('Activo', default=True)
    provincia = fields.Many2one('fincas_pma.provincias', string = 'Provincia', tracking=True)
    description = fields.Text(string='Descripción')

    _sql_constraints = [

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de distrito debe ser único"),
    ]    


class corregs(models.Model):
    _name = "fincas_pma.corregs"
    _description = "Corregimentos de la Rep. de Panamá"

    name = fields.Char('Nombre de Corregimiento de la Ubicación de la U.P.+Lot:', required=True)
    active = fields.Boolean('Activo', default=True)
    distrito = fields.Many2one('fincas_pma.distritos', string = 'Distrito', tracking=True)
    description = fields.Text(string='Descripción')



class tipo_cane(models.Model):
    _name = "fincas_pma.tipo_cane"
    _description = "Tipo de Caña"

    name = fields.Char('Nombre Tipo de Caña:', required=True)
    active = fields.Boolean('Activo', default=True)
    description = fields.Text(string='Descripción')
