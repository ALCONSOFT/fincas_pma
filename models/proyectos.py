# -*- coding: utf-8 -*-
from odoo import models, fields, api
# HERENCIA - AMPLIANDO APLICACIONES EXISTENTES
#    AHORA AGREGAREMOS UN CAMPO A UN MODELO EXISTENTE;  EN ESTE CASO SERIA EL MODELO PROYECTO
#    EL CAMPO A AGREGAR ES: fincas_pma EN EL NOMBRE DEL MODELO:  project.project
#    ESTE SE BUSCA EN EL MENU: AJUSTES; OPCIN: TECNICO; SECCION: SECUENCIA E IDENTIFICADRES
    
class FincasProject(models.Model):
    _inherit = 'project.project'
    
    fincas_pma = fields.Many2one('fincas_pma.fincas_pma', string = 'Finca', tracking=True)
    zafra = fields.Many2one('fincas_pma.zafras', string = 'Zafra', tracking=True)
    frente = fields.Many2one('fincas_pma.frentes', string = 'Frente', tracking=True)
    subfinca = fields.Many2one('fincas_pma.subfincas', string = 'Sub Finca', tracking=True)
    unidadproduccion = fields.Many2one('fincas_pma.unidadproducion', string = 'U.P.', tracking=True)
    lote = fields.Char('LOT', required=True, tracking=True, default='000')
    tipocorte = fields.Many2one('fincas_pma.tiposcortes', string = 'T.D.C.', tracking=True)

    