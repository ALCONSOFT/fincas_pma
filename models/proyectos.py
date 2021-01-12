# -*- coding: utf-8 -*-
from odoo import models, fields, api
from openerp import exceptions
# HERENCIA - AMPLIANDO APLICACIONES EXISTENTES
#    AHORA AGREGAREMOS UN CAMPO A UN MODELO EXISTENTE;  EN ESTE CASO SERIA EL MODELO PROYECTO
#    EL CAMPO A AGREGAR ES: fincas_pma EN EL NOMBRE DEL MODELO:  project.project
#    ESTE SE BUSCA EN EL MENU: AJUSTES; OPCIN: TECNICO; SECCION: SECUENCIA E IDENTIFICADRES
    
class FincasProject(models.Model):
    _inherit = 'project.project'
    # PROPIEDADES de la finca y DE LA UBICACION DE LA UP+LOT  PROY
    fincas_pma = fields.Many2one('fincas_pma.fincas_pma', string = 'Finca', tracking=True)
    zafra = fields.Many2one('fincas_pma.zafras', string = 'Periodo Zafra', tracking=True)
    odc = fields.Integer('Orden de Corte.', store=True)
    frente = fields.Many2one('fincas_pma.frentes', string = 'Frente', tracking=True)
    subfinca = fields.Many2one('fincas_pma.subfincas', string = 'Sub Finca', tracking=True)
    up = fields.Many2one('fincas_pma.up', string = 'U.P.', tracking=True)
    lote = fields.Char('LOT', required=True, tracking=True, default='000')
    has = fields.Float('Superficie en HAS.', store=True)
    correg = fields.Many2one('fincas_pma.corregs', string = 'Corregimiento', tracking=True)
    dist = fields.Float('Distancia al Ingenio', digits=(10, 3), tracking=True)
    desr = fields.Float('Distancia entre Surcos', digits=(10, 3), tracking=True)
    ubic = fields.Char('Ubicación', required=True, tracking=True)
    tds = fields.Char('Tipo de Suelo', tracking=True)
    fecha_est_cosecha = fields.Char('Fecha estimada de cosecha', tracking=True)
    # PROPIEDADES DE LA CAÑA
    tipocorte = fields.Many2one('fincas_pma.tiposcortes', string = 'T.D.C.', tracking=True)
    variedad = fields.Many2one('fincas_pma.variedades', string = 'Variedad', tracking=True)
    fdc = fields.Date('Fecha de Cosecha', tracking=True)
    fds = fields.Date('Fecha de Siembra', tracking=True)
    hdc = fields.Datetime('Fecha y Hora de Cosecha', tracking=True)
    hdq = fields.Datetime('Fecha y Hora de Quema', tracking=True)
    hasq = fields.Float('Hectáreas de Caña Quemada', digits=(14, 4), tracking=True)
    tonq = fields.Float('Toneladas de Caña Quemada', digits=(10, 3), tracking=True)
    hasv = fields.Float('Hectáreas de Caña Verde', digits=(14, 4), tracking=True)
    tonv = fields.Float('Toneladas de Caña Verde', digits=(10, 3), tracking=True)
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
    # INDICADORES DE AZUCAR
    are = fields.Float('Azúcar % Rendimiento Estimado', tracking=True)
    bx = fields.Float('Brix', tracking=True)
    sac = fields.Float('Sacarosa', tracking=True)
    pza = fields.Float('Pureza', tracking=True)
    red = fields.Float('Reductores', tracking=True)
    ph = fields.Float('pH', tracking=True)
    # Referencias Historicas de Parametros relevantes de las Zafras por Proyecto
    tch_01 = fields.Float('Tons por Ha Zafra Anterior', tracking=True)
    dif_01 = fields.Float('Diferencia % vs Zafra Anterior', tracking=True)
    tch_02 = fields.Float('Tons por Ha 2da Zafra Anterior', tracking=True)
    dif_02 = fields.Float('Diferencia % vs 2da Zafra Anterior', tracking=True)
    tch_03 = fields.Float('Tons por Ha 3ra Zafra Anterior', tracking=True)
    dif_03 = fields.Float('Diferencia % vs 3ra Zafra Anterior', tracking=True)
    tch_04 = fields.Float('Tons por Ha 4ta Zafra Anterior', tracking=True)
    dif_04 = fields.Float('Diferencia % vs 4ta Zafra Anterior', tracking=True)
    # PROGRaMA DE MADURACION
    dosm = fields.Float('Dosis Madurador', digits=(11, 4), tracking=True)
    mad = fields.Char('Madurador', tracking=True)
    fdam = fields.Date('Fecha de Aplicación de Madurador', tracking=True)
    external_id = fields.Char(string='External Reference', states={'open': [('readonly', False)]}, copy=False, readonly=True, help="Used to hold the reference of the external mean that created this statement (name of imported file, reference of online synchronization...)")
    # CODE REFERENCE - UP+LOT - LLAVE UNICA
    uplote = fields.Char(string='UP.Lote', tracking=True, store=True)

    _sql_constraints = [
        ('uplote_unique',
         'UNIQUE(uplote)',
         "El código de UP+Lote debe ser único")
        ]
    
    @api.depends('up','lote')
    def _calcula_uplote(self):
        lc_uplote = ''
        if not self.up:
            print('Sin UP', self.up)
            return lc_uplote
        else:
            self.uplote = self.up.code_up + '-' + self.lote
            lc_uplote = self.uplote
            print('Con UP:', lc_uplote)
            return lc_uplote

    @api.onchange('up','lote')
    def _onchange_uplote(self):
        lc_uplote = ''
        if not self.up:
            lc_uplote = ''
        else:
            lc_uplote = self.up.code_up + '-' + self.lote
        self.uplote = lc_uplote