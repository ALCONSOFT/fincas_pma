from odoo import models, fields, api


class tipo_equipo(models.Model):
    _name = "fincas_pma.tipo_equipo"
    _description = "Equipos y Maquinarias"

    name = fields.Char('Tipo de equipo:', required=True)
    active = fields.Boolean('Activo', default=True) 

    _sql_constraints = [
 
        ('name_unique',
         'UNIQUE(name)',
         "El nombre de tipo de equipo debe ser único"),
    ]    

