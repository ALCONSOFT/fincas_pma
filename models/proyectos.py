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
    up = fields.Many2one('fincas_pma.up', string = 'U.P.', tracking=True)
    lote = fields.Char('LOT', required=True, tracking=True, default='000')
    tipocorte = fields.Many2one('fincas_pma.tiposcortes', string = 'T.D.C.', tracking=True)
    has = fields.Float('Superficie en HAS.', store=True)
    variedad = fields.Many2one('fincas_pma.variedades', string = 'Variedad', tracking=True)
    correg = fields.Many2one('fincas_pma.corregs', string = 'Corregimiento', tracking=True)
    fdc = fields.Date('Fecha de Cosecha', tracking=True)
    fds = fields.Date('Fecha de Siembra', tracking=True)
    hdc = fields.Datetime('Fecha y Hora de Cosecha', tracking=True)
    hdq = fields.Datetime('Fecha y Hora de Quema', tracking=True)
    hasq = fields.Float('Hectáreas de Caña Quemada', digits=(14, 4), tracking=True)
    tonq = fields.Float('Toneladas de Caña Quemada', digits=(10, 3), tracking=True)
    tche1 = fields.Float('Tons por Ha Estim 1', digits=(10, 3), tracking=True)
    tche2 = fields.Float('Tons por Ha Estim 2', digits=(10, 3), tracking=True)
    tche3 = fields.Float('Tons por Ha Estim 3', digits=(10, 3), tracking=True)
    hasc = fields.Float('Hectáreas Cosechadas', digits=(14, 4), tracking=True)
    toncos = fields.Float('Toneladas Producidas', digits=(10, 3), tracking=True)
    tonme = fields.Float('Toneladas Merma', digits=(10, 3), tracking=True)
    tonrt = fields.Float('Toneladas Total', digits=(10, 3), tracking=True)
    tchr = fields.Float('Tons por Ha Real', digits=(10, 3), tracking=True)
    difton = fields.Float('Diferencia Tons vs Estim', digits=(10, 3), tracking=True)
    difprc = fields.Float('Diferencia % vs Estim', tracking=True)
    dist = fields.Float('Distancia al Ingenio', digits=(10, 3), tracking=True)
    tds = fields.Char('Tipo de Suelo', tracking=True)
    are = fields.Float('Azúcar % Rendimiento Estimado', tracking=True)
    bx = fields.Float('Brix', tracking=True)
    sac = fields.Float('Sacarosa', tracking=True)
    pza = fields.Float('Pureza', tracking=True)
    red = fields.Float('Reductores', tracking=True)
    ph = fields.Float('pH', tracking=True)
    # Referencias Historicas de Parametros relevantes de las Zafras por Proyecto
    tch20 = fields.Float('Tons por Ha Zafra Anterior 2020', tracking=True)
    dif20 = fields.Float('Diferencia % vs Zafra Anterior 2020', tracking=True)