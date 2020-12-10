from odoo import models, fields, api


class equiposymq(models.Model):
    _inherit= 'maintenance.equipment'

    codigo_activo = fields.Char('Codigo Activo:', required=True)
    tipo_activo = fields.Many2one('fincas_pma.tipo_activo', string = 'Tipo de Activo')
    placa = fields.Char(string='Placa')
    tipo_equipo = fields.Many2one('fincas_pma.tipo_equipo', string= 'Tipo de Equipo')
    motor = fields.Char(string= 'Motor')
    marca = fields.Char(string= 'Marca')
    anio = fields.Char(string= 'Año')
    localizacion = fields.Char(string= 'Localizacion')
    foto = fields.Char(string= 'Foto')


