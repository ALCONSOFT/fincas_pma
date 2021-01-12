from odoo import models, fields, api


class equiposymq(models.Model):
    _inherit= 'maintenance.equipment'

    codigo_activo = fields.Char('Codigo Activo:', required=True, tracking=True)
    tipo_activo = fields.Many2one('fincas_pma.tipo_activo', string = 'Tipo de Activo', tracking=True)
    placa = fields.Char(string='Placa', tracking=True)
    tipo_equipo = fields.Many2one('fincas_pma.tipo_equipo', string= 'Tipo de Equipo', tracking=True)
    motor = fields.Char(string= 'Motor', tracking=True)
    #marca = fields.Char(string= 'Marca')
    marca = fields.Many2one('fincas_pma.marca', string= 'Marca', tracking=True)
    anio = fields.Char(string= 'Año', tracking=True)
    localizacion = fields.Char(string= 'Localizacion')
    # Agregados 2020-12-11
    foto = fields.Binary('Image', attachment=True, tracking=True)
    project_id = fields.Many2one('project.project', 'Proyecto UPLote', track_visibility='onchange', tracking=True)
    frente = fields.Many2one('fincas_pma.frentes', string = 'Frente', tracking=True)
    contrato = fields.Char(string= 'Contrato', tracking=True)
    external_id = fields.Char(string='External Reference', states={'open': [('readonly', False)]}, copy=False, readonly=True, help="Used to hold the reference of the external mean that created this statement (name of imported file, reference of online synchronization...)")    

    _sql_constraints = [
        ('code_ACTIVO_unique',
         'UNIQUE(code_labor)',
         "El código de Labor debe ser único"),

        ('name_unique',
         'UNIQUE(name)',
         "El nombre de Equipo debe ser único"),
    ]    

#class fleet_vehicle_asset(models.Model):
#    _inherit = 'fleet.vehicle'
#    asset_number = fields.Char('Asset Number', size=64)

#class AssetImage(models.Model):
#    _name = 'asset.image'

#   name = fields.Char('Name')
#    image = fields.Binary('Image', attachment=True)
#    asset_id = fields.Many2one('asset.asset', 'Related Asset', copy=True)
