from odoo import models, fields, api
# HERENCIA - AMPLIANDO APLICACIONES EXISTENTES
#    AHORA AGREGAREMOS UN CAMPO A UN MODELO EXISTENTE;  EN ESTE CASO SERIA EL MODELO PROYECTO
#    EL CAMPO A AGREGAR ES: fincas_pma EN EL NOMBRE DEL MODELO:  project.project
#    ESTE SE BUSCA EN EL MENU: AJUSTES; OPCIN: TECNICO; SECCION: SECUENCIA E IDENTIFICADRES
    
class FincasEmpleados(models.Model):
    _inherit = 'hr.employee'
    
    nempl = fields.Char('Numero de Empleado', required=True, tracking=True)
    fincas_pma = fields.Many2one('fincas_pma.fincas_pma', string = 'Finca', tracking=True)
    salario = fields.Char('Salario por horas', required=True, tracking=True)
    fecha_ingreso = fields.Date('Fecha de ingreso', tracking=True)
    cod_hora = fields.Char('Codigo de hora', tracking=True)
    t_sangre = fields.Char('Tipo de sangre',  tracking=True)
    t_salario = fields.Char('Tipo de salario',  tracking=True)
    hora_regular = fields.Float('Hora regular',  tracking=True)
    salario_pactado = fields.Float('Salario pactado', tracking=True)

    _sql_constraints = [
        ('code_identification_unique',
         'UNIQUE(identification_id)',
         "El código de Identificación debe ser único"),

        ('nempl_unique',
         'UNIQUE(nempl)',
         "El Número de Empleado debe ser único"),
    ]    
