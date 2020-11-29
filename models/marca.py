from odoo import models, fields, api


class marca(models.Model):
    _name = "fincas_pma.marca"
    _description = "Equipos y Maquinarias"

    name = fields.Char('Marca:', required=True)
    active = fields.Boolean('Activo', default=True) 

