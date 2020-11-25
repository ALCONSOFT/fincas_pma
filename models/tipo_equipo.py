from odoo import models, fields, api


class tipo_equipo(models.Model):
    _name = "fincas_pma.tipo_equipo"
    _description = "Equipos y Maquinarias"

    name = fields.Char('Tipo de equipo:', required=True)
    active = fields.Boolean('Activo', default=True) 
