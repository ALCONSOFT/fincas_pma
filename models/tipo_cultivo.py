from odoo import models, fields, api

class tipo_cultivo(models.Model):
    _name="fincas_pma.tipo_cultivo"

    name = fields.Char('Nombre:', required=True)
    active = fields.Boolean('Activo', default=True) 
    codigo = fields.Char('Código', required=True)
    description = fields.Text(string='Descripción')