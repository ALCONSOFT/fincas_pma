from odoo import models, fields, api


class tipo_activo(models.Model):
    _name = "fincas_pma.tipo_activo"
    _description = "Equipos y Maquinarias"

    name = fields.Char('Tipo Activo:', required=True)
    active = fields.Boolean('Activo', default=True) 

    _sql_constraints = [
        
        ('name_unique',
         'UNIQUE(name)',
         "El nombre de activo debe ser único"),
    ]    




