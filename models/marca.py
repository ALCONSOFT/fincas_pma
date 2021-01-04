from odoo import models, fields, api


class marca(models.Model):
    _name = "fincas_pma.marca"
    _description = "Marcas"

    name = fields.Char('Marca:', required=True)
    active = fields.Boolean('Activo', default=True) 

    _sql_constraints = [
    
        ('name_unique',
         'UNIQUE(name)',
         "El nombre de marca debe ser único"),
    ]    


