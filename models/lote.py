# -*- coding: utf-8 -*-
"""
Lotes de Producción Agrícola
============================
Modelo independiente para gestionar lotes/parcelas de producción.
Separa la gestión de lotes del módulo project.project para mayor flexibilidad.

Soporta geolocalización, trazabilidad completa y multi-cultivo.
"""

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class Lote(models.Model):
    """
    Lote de Producción Agrícola.
    Unidad mínima de gestión productiva con trazabilidad completa.
    """
    _name = 'fincas_pma.lote'
    _description = 'Lote de Producción Agrícola'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'finca_id, up_id, codigo'

    name = fields.Char(
        string='Nombre del Lote',
        compute='_compute_name',
        store=True,
        help='Nombre completo: UP-Código'
    )
    codigo = fields.Char(
        string='Código de Lote',
        required=True,
        index=True,
        tracking=True,
        help='Código único dentro de la UP (ej: 001, A1, etc.)'
    )
    active = fields.Boolean('Activo', default=True)

    # Jerarquía organizacional
    finca_id = fields.Many2one(
        'fincas_pma.fincas_pma',
        string='Finca',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    subfinca_id = fields.Many2one(
        'fincas_pma.subfincas',
        string='Sub-Finca',
        tracking=True
    )
    up_id = fields.Many2one(
        'fincas_pma.up',
        string='Unidad de Producción',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    frente_id = fields.Many2one(
        'fincas_pma.frentes',
        string='Frente de Cosecha',
        tracking=True,
        help='Frente asignado durante zafra/cosecha'
    )

    # Ubicación geográfica
    correg_id = fields.Many2one(
        'fincas_pma.corregs',
        string='Corregimiento',
        tracking=True
    )
    distrito_id = fields.Many2one(
        'fincas_pma.distritos',
        string='Distrito',
        related='correg_id.distrito',
        store=True
    )
    provincia_id = fields.Many2one(
        'fincas_pma.provincias',
        string='Provincia',
        related='correg_id.distrito.provincia',
        store=True
    )
    ubicacion_texto = fields.Char(
        string='Ubicación (Texto)',
        tracking=True,
        help='Descripción textual de la ubicación'
    )

    # Geolocalización
    latitud = fields.Float(
        string='Latitud',
        digits=(10, 6),
        help='Coordenada de latitud (centroide del lote)'
    )
    longitud = fields.Float(
        string='Longitud',
        digits=(10, 6),
        help='Coordenada de longitud (centroide del lote)'
    )
    altitud_msnm = fields.Integer(
        string='Altitud (msnm)',
        help='Altitud sobre el nivel del mar'
    )
    poligono_geojson = fields.Text(
        string='Polígono GeoJSON',
        help='Geometría del lote en formato GeoJSON para mapas'
    )

    # Áreas
    area_total_ha = fields.Float(
        string='Área Total (ha)',
        digits=(10, 4),
        tracking=True,
        help='Área total del lote en hectáreas'
    )
    area_efectiva_ha = fields.Float(
        string='Área Efectiva (ha)',
        digits=(10, 4),
        tracking=True,
        help='Área efectivamente cultivada'
    )
    area_infraestructura_ha = fields.Float(
        string='Área Infraestructura (ha)',
        digits=(10, 4),
        compute='_compute_area_infraestructura',
        store=True,
        help='Área ocupada por caminos, canales, etc.'
    )
    porcentaje_efectivo = fields.Float(
        string='% Área Efectiva',
        compute='_compute_porcentaje_efectivo',
        store=True,
        digits=(5, 2)
    )

    # Cultivo actual
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo Actual',
        tracking=True,
        help='Cultivo actualmente sembrado'
    )
    variedad_id = fields.Many2one(
        'fincas_pma.variedad_cultivo',
        string='Variedad',
        tracking=True,
        domain="[('cultivo_id', '=', cultivo_id)]"
    )

    # Características del suelo
    tipo_suelo = fields.Selection([
        ('arcilloso', 'Arcilloso'),
        ('arenoso', 'Arenoso'),
        ('franco', 'Franco'),
        ('franco_arcilloso', 'Franco Arcilloso'),
        ('franco_arenoso', 'Franco Arenoso'),
        ('limoso', 'Limoso'),
        ('organico', 'Orgánico/Turba'),
    ], string='Tipo de Suelo', tracking=True)

    textura_suelo = fields.Char(
        string='Textura del Suelo',
        help='Descripción detallada de la textura'
    )
    ph_suelo = fields.Float(
        string='pH del Suelo',
        digits=(3, 1),
        tracking=True
    )
    materia_organica_pct = fields.Float(
        string='Materia Orgánica (%)',
        digits=(4, 2)
    )
    pendiente_pct = fields.Float(
        string='Pendiente (%)',
        digits=(5, 2),
        help='Pendiente promedio del terreno'
    )
    orientacion = fields.Selection([
        ('norte', 'Norte'),
        ('sur', 'Sur'),
        ('este', 'Este'),
        ('oeste', 'Oeste'),
        ('noreste', 'Noreste'),
        ('noroeste', 'Noroeste'),
        ('sureste', 'Sureste'),
        ('suroeste', 'Suroeste'),
        ('plano', 'Plano'),
    ], string='Orientación')
    drenaje = fields.Selection([
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('moderado', 'Moderado'),
        ('deficiente', 'Deficiente'),
        ('muy_deficiente', 'Muy Deficiente'),
    ], string='Drenaje', tracking=True)

    # Sistema de riego
    sistema_riego = fields.Selection([
        ('secano', 'Secano (Sin riego)'),
        ('gravedad', 'Gravedad/Surcos'),
        ('aspersion', 'Aspersión'),
        ('goteo', 'Goteo'),
        ('microaspersion', 'Microaspersión'),
        ('pivot', 'Pivote Central'),
        ('inundacion', 'Inundación'),
    ], string='Sistema de Riego', tracking=True)
    fuente_agua = fields.Char(string='Fuente de Agua')

    # Estado del lote
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('preparacion', 'En Preparación'),
        ('sembrado', 'Sembrado'),
        ('desarrollo', 'En Desarrollo'),
        ('produccion', 'En Producción'),
        ('cosecha', 'En Cosecha'),
        ('post_cosecha', 'Post-Cosecha'),
        ('renovacion', 'En Renovación'),
        ('descanso', 'En Descanso'),
        ('inhabilitado', 'Inhabilitado'),
    ], string='Estado', default='disponible', tracking=True, required=True)

    # Fechas del ciclo actual
    fecha_preparacion = fields.Date(
        string='Fecha de Preparación',
        tracking=True
    )
    fecha_siembra = fields.Date(
        string='Fecha de Siembra',
        tracking=True
    )
    fecha_primera_cosecha = fields.Date(
        string='Primera Cosecha',
        tracking=True
    )
    fecha_ultima_cosecha = fields.Date(
        string='Última Cosecha',
        tracking=True
    )

    # Edad y ciclo
    edad_meses = fields.Integer(
        string='Edad (meses)',
        compute='_compute_edad',
        store=True,
        help='Meses desde la siembra'
    )
    numero_ciclo = fields.Integer(
        string='Número de Ciclo/Corte',
        default=1,
        tracking=True,
        help='Para cultivos con múltiples ciclos (ej: socas de caña)'
    )

    # Densidad de siembra
    densidad_plantas = fields.Integer(
        string='Plantas por Hectárea',
        help='Densidad de siembra'
    )
    distancia_entre_plantas = fields.Float(
        string='Distancia entre Plantas (m)',
        digits=(5, 2)
    )
    distancia_entre_hileras = fields.Float(
        string='Distancia entre Hileras (m)',
        digits=(5, 2)
    )

    # Proveedor/Colono (para caña y otros)
    partner_id = fields.Many2one(
        'res.partner',
        string='Proveedor/Colono',
        tracking=True,
        help='Propietario o proveedor del lote'
    )

    # Certificaciones
    certificacion_ids = fields.Many2many(
        'fincas_pma.certificacion',
        'lote_certificacion_rel',
        'lote_id',
        'certificacion_id',
        string='Certificaciones'
    )
    es_organico = fields.Boolean(
        string='Es Orgánico',
        tracking=True
    )
    en_transicion_organica = fields.Boolean(
        string='En Transición Orgánica'
    )
    fecha_inicio_transicion = fields.Date(
        string='Inicio Transición Orgánica'
    )

    # === CAMPOS ESPECÍFICOS POR CULTIVO ===

    # --- CAFÉ ---
    cafe_sombra_pct = fields.Float(
        string='[Café] Sombra (%)',
        digits=(5, 2),
        help='Porcentaje de cobertura de sombra'
    )
    cafe_especie_sombra = fields.Char(
        string='[Café] Especie de Sombra',
        help='Especies usadas para sombra'
    )
    cafe_sistema_produccion = fields.Selection([
        ('sol', 'Pleno Sol'),
        ('sombra_baja', 'Sombra Baja (<30%)'),
        ('sombra_media', 'Sombra Media (30-50%)'),
        ('sombra_alta', 'Sombra Alta (>50%)'),
        ('agroforestal', 'Sistema Agroforestal'),
    ], string='[Café] Sistema de Producción')

    # --- BANANO ---
    banano_generacion = fields.Integer(
        string='[Banano] Generación',
        help='Número de generación desde siembra inicial'
    )
    banano_tipo_semilla = fields.Selection([
        ('cormo', 'Cormo'),
        ('vitro', 'Vitro Planta'),
        ('hijo', 'Hijo de Agua'),
    ], string='[Banano] Tipo de Semilla')
    banano_sistema_cable = fields.Boolean(
        string='[Banano] Tiene Cable-vía'
    )

    # --- PIÑA ---
    pina_ciclo_produccion = fields.Selection([
        ('planta', 'Planta (1er ciclo)'),
        ('soca1', 'Soca 1'),
        ('soca2', 'Soca 2'),
    ], string='[Piña] Ciclo de Producción')
    pina_tipo_semilla = fields.Selection([
        ('corona', 'Corona'),
        ('hijuelo', 'Hijuelo'),
        ('eslabon', 'Eslabón'),
        ('vitro', 'Vitro Planta'),
    ], string='[Piña] Tipo de Semilla')

    # --- PALMA ---
    palma_ano_siembra = fields.Integer(
        string='[Palma] Año de Siembra',
        help='Año de establecimiento del lote'
    )
    palma_fase_produccion = fields.Selection([
        ('improductiva', 'Improductiva (<3 años)'),
        ('creciente', 'Producción Creciente (3-7 años)'),
        ('plena', 'Plena Producción (8-20 años)'),
        ('decreciente', 'Producción Decreciente (>20 años)'),
    ], string='[Palma] Fase de Producción')

    # --- CAÑA ---
    cana_numero_corte = fields.Integer(
        string='[Caña] Número de Corte',
        help='Número de corte/soca'
    )
    cana_edad_cepa = fields.Integer(
        string='[Caña] Edad de Cepa (años)'
    )
    cana_tipo = fields.Many2one(
        'fincas_pma.tipo_cane',
        string='[Caña] Tipo de Caña'
    )
    cana_orden_corte = fields.Integer(
        string='[Caña] Orden de Corte',
        help='Orden en la programación de cosecha'
    )
    cana_distancia_ingenio = fields.Float(
        string='[Caña] Distancia al Ingenio (km)',
        digits=(6, 2)
    )
    cana_distancia_surcos = fields.Float(
        string='[Caña] Distancia entre Surcos (m)',
        digits=(4, 2)
    )

    # Notas y observaciones
    notas = fields.Text(string='Notas')

    # Relaciones de historial
    siembra_ids = fields.One2many(
        'fincas_pma.siembra',
        'lote_id',
        string='Historial de Siembras'
    )
    cosecha_ids = fields.One2many(
        'fincas_pma.cosecha',
        'lote_id',
        string='Historial de Cosechas'
    )
    aplicacion_ids = fields.One2many(
        'fincas_pma.aplicacion',
        'lote_id',
        string='Aplicaciones de Insumos'
    )
    monitoreo_ids = fields.One2many(
        'fincas_pma.monitoreo_sanitario',
        'lote_id',
        string='Monitoreos Sanitarios'
    )
    labor_ids = fields.One2many(
        'fincas_pma.labor_lote',
        'lote_id',
        string='Labores Realizadas'
    )
    analisis_suelo_ids = fields.One2many(
        'fincas_pma.analisis_suelo',
        'lote_id',
        string='Análisis de Suelo'
    )

    # Campos computados para resumen
    total_cosechas = fields.Integer(
        string='Total Cosechas',
        compute='_compute_estadisticas'
    )
    produccion_total = fields.Float(
        string='Producción Total',
        compute='_compute_estadisticas'
    )
    rendimiento_promedio = fields.Float(
        string='Rendimiento Promedio',
        compute='_compute_estadisticas'
    )

    # Referencia externa
    external_id = fields.Char(
        string='ID Externo',
        help='Referencia de sistema externo'
    )

    # Proyecto relacionado (compatibilidad con sistema actual)
    project_id = fields.Many2one(
        'project.project',
        string='Proyecto Relacionado',
        help='Proyecto de Odoo asociado (para compatibilidad)'
    )

    @api.depends('up_id', 'codigo')
    def _compute_name(self):
        for record in self:
            if record.up_id and record.codigo:
                record.name = f"{record.up_id.code_up}-{record.codigo}"
            else:
                record.name = record.codigo or 'Nuevo Lote'

    @api.depends('area_total_ha', 'area_efectiva_ha')
    def _compute_area_infraestructura(self):
        for record in self:
            record.area_infraestructura_ha = (
                (record.area_total_ha or 0) - (record.area_efectiva_ha or 0)
            )

    @api.depends('area_total_ha', 'area_efectiva_ha')
    def _compute_porcentaje_efectivo(self):
        for record in self:
            if record.area_total_ha:
                record.porcentaje_efectivo = (
                    (record.area_efectiva_ha or 0) / record.area_total_ha * 100
                )
            else:
                record.porcentaje_efectivo = 0

    @api.depends('fecha_siembra')
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if record.fecha_siembra:
                delta = relativedelta(today, record.fecha_siembra)
                record.edad_meses = delta.years * 12 + delta.months
            else:
                record.edad_meses = 0

    def _compute_estadisticas(self):
        for record in self:
            cosechas = record.cosecha_ids.filtered(lambda c: c.estado == 'completada')
            record.total_cosechas = len(cosechas)
            record.produccion_total = sum(cosechas.mapped('cantidad_neta'))
            if record.total_cosechas > 0 and record.area_efectiva_ha:
                record.rendimiento_promedio = (
                    record.produccion_total / record.total_cosechas / record.area_efectiva_ha
                )
            else:
                record.rendimiento_promedio = 0

    @api.onchange('cultivo_id')
    def _onchange_cultivo_id(self):
        """Limpia la variedad si cambia el cultivo"""
        if self.cultivo_id != self.variedad_id.cultivo_id:
            self.variedad_id = False

    _sql_constraints = [
        ('codigo_up_unique', 'UNIQUE(codigo, up_id)',
         'El código de lote debe ser único dentro de la UP'),
        ('name_unique', 'UNIQUE(name)',
         'El nombre del lote (UP-Código) debe ser único'),
    ]


class AnalisisSuelo(models.Model):
    """
    Registro de análisis de suelo por lote.
    Permite seguimiento histórico de la fertilidad del suelo.
    """
    _name = 'fincas_pma.analisis_suelo'
    _description = 'Análisis de Suelo'
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
    )
    lote_id = fields.Many2one(
        'fincas_pma.lote',
        string='Lote',
        required=True,
        ondelete='cascade'
    )
    fecha = fields.Date(
        string='Fecha de Muestreo',
        required=True,
        default=fields.Date.today
    )
    laboratorio = fields.Char(string='Laboratorio')
    numero_muestra = fields.Char(string='Número de Muestra')

    # Propiedades físicas
    ph = fields.Float(string='pH', digits=(3, 1))
    conductividad_electrica = fields.Float(
        string='CE (dS/m)',
        digits=(5, 2),
        help='Conductividad Eléctrica'
    )
    materia_organica = fields.Float(string='Materia Orgánica (%)', digits=(4, 2))
    textura = fields.Char(string='Textura')

    # Macronutrientes
    nitrogeno = fields.Float(string='Nitrógeno (N) %', digits=(5, 3))
    fosforo = fields.Float(string='Fósforo (P) ppm', digits=(6, 2))
    potasio = fields.Float(string='Potasio (K) meq/100g', digits=(5, 2))
    calcio = fields.Float(string='Calcio (Ca) meq/100g', digits=(5, 2))
    magnesio = fields.Float(string='Magnesio (Mg) meq/100g', digits=(5, 2))
    azufre = fields.Float(string='Azufre (S) ppm', digits=(6, 2))

    # Micronutrientes
    hierro = fields.Float(string='Hierro (Fe) ppm', digits=(6, 2))
    manganeso = fields.Float(string='Manganeso (Mn) ppm', digits=(6, 2))
    cobre = fields.Float(string='Cobre (Cu) ppm', digits=(6, 2))
    zinc = fields.Float(string='Zinc (Zn) ppm', digits=(6, 2))
    boro = fields.Float(string='Boro (B) ppm', digits=(6, 2))

    # Relaciones catiónicas
    ca_mg = fields.Float(
        string='Relación Ca/Mg',
        compute='_compute_relaciones',
        digits=(4, 2)
    )
    mg_k = fields.Float(
        string='Relación Mg/K',
        compute='_compute_relaciones',
        digits=(4, 2)
    )
    ca_k = fields.Float(
        string='Relación Ca/K',
        compute='_compute_relaciones',
        digits=(4, 2)
    )

    # CIC
    cic = fields.Float(
        string='CIC (meq/100g)',
        digits=(5, 2),
        help='Capacidad de Intercambio Catiónico'
    )
    saturacion_bases = fields.Float(
        string='Saturación de Bases (%)',
        digits=(5, 2)
    )

    # Aluminio (importante para trópicos)
    aluminio = fields.Float(string='Aluminio (Al) meq/100g', digits=(5, 2))
    saturacion_aluminio = fields.Float(
        string='Saturación de Al (%)',
        digits=(5, 2)
    )

    # Recomendaciones
    recomendaciones = fields.Text(string='Recomendaciones')
    documento = fields.Binary(string='Documento Adjunto')
    documento_nombre = fields.Char(string='Nombre del Documento')

    @api.depends('lote_id', 'fecha')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.fecha:
                record.name = f"AS-{record.lote_id.name}-{record.fecha}"
            else:
                record.name = 'Nuevo Análisis'

    @api.depends('calcio', 'magnesio', 'potasio')
    def _compute_relaciones(self):
        for record in self:
            record.ca_mg = record.calcio / record.magnesio if record.magnesio else 0
            record.mg_k = record.magnesio / record.potasio if record.potasio else 0
            record.ca_k = record.calcio / record.potasio if record.potasio else 0
