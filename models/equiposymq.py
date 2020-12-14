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
<<<<<<< Updated upstream
    foto = fields.Char(string= 'Foto')
=======
    # Agregados 2020-12-11
    foto = fields.Binary('Image', attachment=True, tracking=True)
    project_id = fields.Many2one('project.project', 'Proyecto UPLote', track_visibility='onchange', tracking=True)
    frente = fields.Many2one('fincas_pma.frentes', string = 'Frente', tracking=True)
    contrato = fields.Char(string= 'Contrato', tracking=True)
    status = fields.Char(string= 'Estado', tracking=True)
>>>>>>> Stashed changes


