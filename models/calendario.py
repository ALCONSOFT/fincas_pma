# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta

class calendario(models.Model):
    _name = "fincas_pma.calendario"
    _description = "Calendario de Zafra y Cultivo"

    name = fields.Char('Nombre del Periodo Zafra-Cultivo', required=True)
    active = fields.Boolean('Activo', default=True)
    code_zafra = fields.Many2one('fincas_pma.zafras', string = 'Zafra_Cultivo', tracking=True, required=True)
    description = fields.Text(string='Descripción', tracking=True, required=True)
    fecha_hora_inicio = fields.Datetime(string='Fecha Hora Inicio Zafra', tracking=True, required=True)
    fecha_hora_fin = fields.Datetime(string='Fecha Hora Fin Zafra', tracking=True, required=True)
    fecha_hora_cultivo_i = fields.Datetime(string='Fecha Hora Inicio Cultivo', tracking=True, required=True)
    fecha_hora_cultivo_f = fields.Datetime(string='Fecha Hora Fin Cultivo', tracking=True, required=True)
    periodo_actual = fields.Boolean('Periodo Corriente', default=False, tracking=True, required=True)
    ahora = fields.Datetime(string='Ahora:', compute="_devuelve_ahora", store=True)
 
    @api.onchange('fecha_hora_inicio')
    def _devuelve_ahora(self):
        for record in self:
            self.ahora = datetime.now()
