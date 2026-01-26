# -*- coding: utf-8 -*-
"""
Gestión de Cosechas Multi-Cultivo
=================================
Registro completo de cosechas con métricas específicas por cultivo.

Soporta:
- Café: pergamino, cereza, calidad de taza
- Banano: cajas, calibre, generación
- Piña: peso, brix, corona
- Palma: RFF, extracción
- Caña: toneladas, brix, sacarosa
"""

from odoo import models, fields, api
from datetime import date


class CicloProduccion(models.Model):
    """
    Ciclo de Producción (reemplaza concepto de Zafra).
    Permite gestionar períodos productivos para cualquier cultivo.
    """
    _name = 'fincas_pma.ciclo_produccion'
    _description = 'Ciclo de Producción'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    name = fields.Char(
        string='Nombre del Ciclo',
        required=True,
        tracking=True,
        help='Ej: Cosecha 2024-2025, Zafra 2024'
    )
    codigo = fields.Char(
        string='Código',
        required=True,
        index=True
    )
    active = fields.Boolean('Activo', default=True)

    # Cultivo y finca
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        required=True,
        tracking=True
    )
    finca_id = fields.Many2one(
        'fincas_pma.fincas_pma',
        string='Finca',
        tracking=True,
        help='Dejar vacío para ciclo general de múltiples fincas'
    )

    # Período
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=True,
        tracking=True
    )
    fecha_fin = fields.Date(
        string='Fecha de Fin',
        tracking=True
    )
    anio_fiscal = fields.Char(
        string='Año Fiscal',
        compute='_compute_anio_fiscal',
        store=True
    )

    # Estado
    estado = fields.Selection([
        ('planificacion', 'En Planificación'),
        ('activo', 'Activo'),
        ('cerrado', 'Cerrado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='planificacion', tracking=True, required=True)

    # Objetivos
    area_planificada_ha = fields.Float(
        string='Área Planificada (ha)',
        digits=(10, 2)
    )
    produccion_objetivo = fields.Float(
        string='Producción Objetivo',
        digits=(12, 2)
    )
    unidad_produccion_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Producción'
    )
    rendimiento_objetivo = fields.Float(
        string='Rendimiento Objetivo',
        compute='_compute_rendimiento_objetivo',
        digits=(10, 2)
    )

    # Resultados reales
    area_real_ha = fields.Float(
        string='Área Real (ha)',
        compute='_compute_resultados',
        store=True
    )
    produccion_real = fields.Float(
        string='Producción Real',
        compute='_compute_resultados',
        store=True
    )
    rendimiento_real = fields.Float(
        string='Rendimiento Real',
        compute='_compute_resultados',
        store=True
    )

    # Variaciones
    variacion_area_pct = fields.Float(
        string='Variación Área (%)',
        compute='_compute_variaciones'
    )
    variacion_produccion_pct = fields.Float(
        string='Variación Producción (%)',
        compute='_compute_variaciones'
    )

    # Relaciones
    cosecha_ids = fields.One2many(
        'fincas_pma.cosecha',
        'ciclo_id',
        string='Cosechas'
    )
    lote_ids = fields.Many2many(
        'fincas_pma.lote',
        'ciclo_lote_rel',
        'ciclo_id',
        'lote_id',
        string='Lotes Incluidos'
    )

    # Estadísticas
    total_cosechas = fields.Integer(
        string='Total Cosechas',
        compute='_compute_estadisticas'
    )
    total_lotes = fields.Integer(
        string='Total Lotes',
        compute='_compute_estadisticas'
    )

    descripcion = fields.Text(string='Descripción')
    notas = fields.Text(string='Notas')

    @api.depends('fecha_inicio')
    def _compute_anio_fiscal(self):
        for record in self:
            if record.fecha_inicio:
                # Asume año fiscal igual al año calendario
                record.anio_fiscal = str(record.fecha_inicio.year)
            else:
                record.anio_fiscal = ''

    @api.depends('area_planificada_ha', 'produccion_objetivo')
    def _compute_rendimiento_objetivo(self):
        for record in self:
            if record.area_planificada_ha:
                record.rendimiento_objetivo = (
                    record.produccion_objetivo / record.area_planificada_ha
                )
            else:
                record.rendimiento_objetivo = 0

    @api.depends('cosecha_ids.cantidad_neta', 'cosecha_ids.area_cosechada_ha')
    def _compute_resultados(self):
        for record in self:
            cosechas = record.cosecha_ids.filtered(lambda c: c.estado == 'completada')
            record.area_real_ha = sum(cosechas.mapped('area_cosechada_ha'))
            record.produccion_real = sum(cosechas.mapped('cantidad_neta'))
            if record.area_real_ha:
                record.rendimiento_real = record.produccion_real / record.area_real_ha
            else:
                record.rendimiento_real = 0

    def _compute_variaciones(self):
        for record in self:
            if record.area_planificada_ha:
                record.variacion_area_pct = (
                    (record.area_real_ha - record.area_planificada_ha) /
                    record.area_planificada_ha * 100
                )
            else:
                record.variacion_area_pct = 0
            if record.produccion_objetivo:
                record.variacion_produccion_pct = (
                    (record.produccion_real - record.produccion_objetivo) /
                    record.produccion_objetivo * 100
                )
            else:
                record.variacion_produccion_pct = 0

    def _compute_estadisticas(self):
        for record in self:
            record.total_cosechas = len(record.cosecha_ids)
            record.total_lotes = len(record.lote_ids)

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código del ciclo debe ser único'),
    ]


class Cosecha(models.Model):
    """
    Registro de Cosecha.
    Captura información detallada de cada cosecha realizada.
    """
    _name = 'fincas_pma.cosecha'
    _description = 'Registro de Cosecha'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_cosecha desc'

    name = fields.Char(
        string='Código de Cosecha',
        required=True,
        copy=False,
        index=True,
        tracking=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('fincas_pma.cosecha') or 'Nuevo'
    )

    # Ubicación
    lote_id = fields.Many2one(
        'fincas_pma.lote',
        string='Lote',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    finca_id = fields.Many2one(
        'fincas_pma.fincas_pma',
        string='Finca',
        related='lote_id.finca_id',
        store=True
    )
    up_id = fields.Many2one(
        'fincas_pma.up',
        string='Unidad de Producción',
        related='lote_id.up_id',
        store=True
    )

    # Cultivo
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        related='lote_id.cultivo_id',
        store=True
    )
    variedad_id = fields.Many2one(
        'fincas_pma.variedad_cultivo',
        string='Variedad',
        related='lote_id.variedad_id',
        store=True
    )
    tipo_cultivo = fields.Selection(
        related='cultivo_id.tipo_cultivo',
        store=True
    )

    # Ciclo de producción
    ciclo_id = fields.Many2one(
        'fincas_pma.ciclo_produccion',
        string='Ciclo de Producción',
        tracking=True,
        domain="[('cultivo_id', '=', cultivo_id)]"
    )
    zafra_id = fields.Many2one(
        'fincas_pma.zafras',
        string='Zafra (Legacy)',
        help='Compatibilidad con sistema anterior'
    )

    # Fechas
    fecha_cosecha = fields.Date(
        string='Fecha de Cosecha',
        required=True,
        tracking=True,
        default=fields.Date.today
    )
    fecha_hora_inicio = fields.Datetime(
        string='Inicio de Cosecha'
    )
    fecha_hora_fin = fields.Datetime(
        string='Fin de Cosecha'
    )

    # Cantidades
    area_cosechada_ha = fields.Float(
        string='Área Cosechada (ha)',
        digits=(10, 4),
        tracking=True
    )
    cantidad_bruta = fields.Float(
        string='Cantidad Bruta',
        digits=(12, 2),
        tracking=True,
        help='Cantidad total cosechada antes de descuentos'
    )
    cantidad_descuento = fields.Float(
        string='Descuentos',
        digits=(12, 2),
        help='Descuentos por impurezas, humedad, etc.'
    )
    cantidad_neta = fields.Float(
        string='Cantidad Neta',
        digits=(12, 2),
        compute='_compute_cantidad_neta',
        store=True,
        tracking=True
    )
    unidad_cosecha_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        required=True
    )

    # Rendimiento
    rendimiento = fields.Float(
        string='Rendimiento',
        digits=(10, 2),
        compute='_compute_rendimiento',
        store=True,
        help='Cantidad neta / Área cosechada'
    )
    rendimiento_estimado = fields.Float(
        string='Rendimiento Estimado',
        digits=(10, 2)
    )
    variacion_rendimiento_pct = fields.Float(
        string='Variación vs Estimado (%)',
        compute='_compute_variacion_rendimiento'
    )

    # Calidad general
    grado_calidad = fields.Selection([
        ('premium', 'Premium / Especialidad'),
        ('exportacion', 'Exportación'),
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('rechazo', 'Rechazo / Industrial'),
    ], string='Grado de Calidad', tracking=True)

    porcentaje_exportacion = fields.Float(
        string='% Exportación/Premium',
        digits=(5, 2)
    )
    porcentaje_primera = fields.Float(
        string='% Primera',
        digits=(5, 2)
    )
    porcentaje_segunda = fields.Float(
        string='% Segunda',
        digits=(5, 2)
    )
    porcentaje_rechazo = fields.Float(
        string='% Rechazo',
        digits=(5, 2)
    )

    # === CAMPOS ESPECÍFICOS POR CULTIVO ===

    # --- CAFÉ ---
    cafe_cereza_kg = fields.Float(
        string='[Café] Cereza (kg)',
        digits=(10, 2)
    )
    cafe_pergamino_kg = fields.Float(
        string='[Café] Pergamino (kg)',
        digits=(10, 2)
    )
    cafe_factor_conversion = fields.Float(
        string='[Café] Factor Conversión',
        digits=(4, 2),
        help='kg cereza / kg pergamino'
    )
    cafe_humedad_pct = fields.Float(
        string='[Café] Humedad (%)',
        digits=(4, 2)
    )
    cafe_defectos_pct = fields.Float(
        string='[Café] Defectos (%)',
        digits=(4, 2)
    )
    cafe_puntaje_taza = fields.Float(
        string='[Café] Puntaje de Taza',
        digits=(4, 1),
        help='Puntaje SCA (0-100)'
    )
    cafe_perfil_taza = fields.Text(
        string='[Café] Perfil de Taza',
        help='Notas de cata'
    )
    cafe_proceso = fields.Selection([
        ('lavado', 'Lavado'),
        ('honey', 'Honey'),
        ('natural', 'Natural'),
        ('anaerobico', 'Anaeróbico'),
    ], string='[Café] Proceso')
    cafe_qq_oro = fields.Float(
        string='[Café] Quintales Oro',
        digits=(10, 2),
        help='Quintales de café oro exportable'
    )

    # --- BANANO ---
    banano_racimos = fields.Integer(
        string='[Banano] Racimos Cosechados'
    )
    banano_cajas_total = fields.Integer(
        string='[Banano] Cajas Totales'
    )
    banano_cajas_exportacion = fields.Integer(
        string='[Banano] Cajas Exportación'
    )
    banano_cajas_rechazo = fields.Integer(
        string='[Banano] Cajas Rechazo'
    )
    banano_ratio_exportacion = fields.Float(
        string='[Banano] Ratio Exportación',
        compute='_compute_banano_ratio',
        digits=(5, 2)
    )
    banano_calibre_promedio = fields.Float(
        string='[Banano] Calibre Promedio',
        digits=(4, 1),
        help='Calibre en grados'
    )
    banano_largo_dedo_cm = fields.Float(
        string='[Banano] Largo Dedo (cm)',
        digits=(4, 1)
    )
    banano_manos_promedio = fields.Float(
        string='[Banano] Manos/Racimo Prom',
        digits=(3, 1)
    )
    banano_peso_racimo_kg = fields.Float(
        string='[Banano] Peso Racimo (kg)',
        digits=(4, 1)
    )
    banano_merma_pct = fields.Float(
        string='[Banano] Merma (%)',
        digits=(4, 2)
    )
    banano_semana_cosecha = fields.Integer(
        string='[Banano] Semana de Cosecha'
    )

    # --- PIÑA ---
    pina_frutas_totales = fields.Integer(
        string='[Piña] Frutas Totales'
    )
    pina_peso_promedio_kg = fields.Float(
        string='[Piña] Peso Promedio (kg)',
        digits=(4, 2)
    )
    pina_brix = fields.Float(
        string='[Piña] Brix',
        digits=(4, 1)
    )
    pina_acidez_pct = fields.Float(
        string='[Piña] Acidez (%)',
        digits=(4, 2)
    )
    pina_ratio = fields.Float(
        string='[Piña] Ratio Brix/Acidez',
        compute='_compute_pina_ratio',
        digits=(4, 2)
    )
    pina_corona = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
    ], string='[Piña] Estado Corona')
    pina_color = fields.Selection([
        ('0', '0 - Verde'),
        ('1', '1 - Pintón'),
        ('2', '2 - Medio'),
        ('3', '3 - Maduro'),
        ('4', '4 - Sobremaduro'),
    ], string='[Piña] Color/Madurez')
    pina_cajas_exportacion = fields.Integer(
        string='[Piña] Cajas Exportación'
    )

    # --- PALMA ACEITERA ---
    palma_rff_tons = fields.Float(
        string='[Palma] RFF (Tons)',
        digits=(10, 2),
        help='Racimos de Fruta Fresca'
    )
    palma_racimos = fields.Integer(
        string='[Palma] Número de Racimos'
    )
    palma_peso_racimo_kg = fields.Float(
        string='[Palma] Peso Prom. Racimo (kg)',
        digits=(5, 2)
    )
    palma_aceite_pct = fields.Float(
        string='[Palma] Extracción Aceite (%)',
        digits=(4, 2)
    )
    palma_tons_aceite = fields.Float(
        string='[Palma] Tons Aceite',
        compute='_compute_palma_aceite',
        digits=(10, 2)
    )
    palma_acidez = fields.Float(
        string='[Palma] Acidez (%)',
        digits=(4, 2)
    )
    palma_ciclo_dias = fields.Integer(
        string='[Palma] Días desde Última Cosecha'
    )

    # --- CAÑA DE AZÚCAR ---
    cana_tons_brutas = fields.Float(
        string='[Caña] Tons Brutas',
        digits=(10, 2)
    )
    cana_tons_netas = fields.Float(
        string='[Caña] Tons Netas',
        digits=(10, 2)
    )
    cana_tch = fields.Float(
        string='[Caña] TCH',
        digits=(6, 2),
        help='Toneladas de Caña por Hectárea'
    )
    cana_brix = fields.Float(
        string='[Caña] Brix',
        digits=(4, 2)
    )
    cana_pol = fields.Float(
        string='[Caña] Pol',
        digits=(4, 2)
    )
    cana_pureza = fields.Float(
        string='[Caña] Pureza (%)',
        digits=(5, 2)
    )
    cana_fibra = fields.Float(
        string='[Caña] Fibra (%)',
        digits=(4, 2)
    )
    cana_humedad = fields.Float(
        string='[Caña] Humedad (%)',
        digits=(4, 2)
    )
    cana_sacarosa = fields.Float(
        string='[Caña] Sacarosa (%)',
        digits=(4, 2)
    )
    cana_reductores = fields.Float(
        string='[Caña] Reductores (%)',
        digits=(4, 2)
    )
    cana_arr = fields.Float(
        string='[Caña] ARR',
        digits=(5, 2),
        help='Azúcar Recuperable'
    )
    cana_ph = fields.Float(
        string='[Caña] pH',
        digits=(3, 1)
    )
    cana_trash_pct = fields.Float(
        string='[Caña] Trash (%)',
        digits=(4, 2),
        help='Porcentaje de materia extraña'
    )
    cana_hora_quema = fields.Datetime(
        string='[Caña] Fecha/Hora Quema'
    )
    cana_has_quemadas = fields.Float(
        string='[Caña] Has Quemadas',
        digits=(10, 4)
    )
    cana_tons_quemadas = fields.Float(
        string='[Caña] Tons Quemadas',
        digits=(10, 2)
    )
    cana_has_verde = fields.Float(
        string='[Caña] Has Verde',
        digits=(10, 4)
    )
    cana_tons_verde = fields.Float(
        string='[Caña] Tons Verde',
        digits=(10, 2)
    )
    cana_tipo_corte_id = fields.Many2one(
        'fincas_pma.tiposcortes',
        string='[Caña] Tipo de Corte'
    )
    cana_numero_corte = fields.Integer(
        string='[Caña] Número de Corte'
    )
    cana_orden_corte = fields.Integer(
        string='[Caña] Orden de Corte'
    )

    # Método de cosecha
    metodo_cosecha = fields.Selection([
        ('manual', 'Manual'),
        ('mecanizada', 'Mecanizada'),
        ('semi_mecanizada', 'Semi-Mecanizada'),
    ], string='Método de Cosecha', tracking=True)

    # Personal y equipos
    cuadrilla_id = fields.Many2one(
        'fincas_pma.cuadrilla',
        string='Cuadrilla'
    )
    trabajadores = fields.Integer(string='Número de Trabajadores')
    jornales = fields.Float(
        string='Jornales Utilizados',
        digits=(8, 2)
    )
    horas_trabajo = fields.Float(
        string='Horas de Trabajo',
        digits=(8, 2)
    )
    equipo_ids = fields.Many2many(
        'maintenance.equipment',
        'cosecha_equipo_rel',
        'cosecha_id',
        'equipment_id',
        string='Equipos Utilizados'
    )

    # Transporte
    vehiculo = fields.Char(string='Vehículo/Placa')
    conductor = fields.Char(string='Conductor')
    guia_transporte = fields.Char(string='Guía de Transporte')

    # Destino
    destino = fields.Selection([
        ('planta', 'Planta Procesadora'),
        ('beneficio', 'Beneficio'),
        ('ingenio', 'Ingenio'),
        ('extractora', 'Extractora'),
        ('empacadora', 'Empacadora'),
        ('exportacion', 'Exportación Directa'),
        ('mercado_local', 'Mercado Local'),
        ('almacen', 'Almacén'),
    ], string='Destino', tracking=True)

    destino_partner_id = fields.Many2one(
        'res.partner',
        string='Destino (Cliente/Planta)'
    )
    fecha_entrega = fields.Datetime(string='Fecha/Hora Entrega')
    numero_ticket = fields.Char(string='Número de Ticket/Boleta')

    # Proveedor/Colono
    partner_id = fields.Many2one(
        'res.partner',
        string='Proveedor/Colono',
        related='lote_id.partner_id',
        store=True
    )

    # Estado
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('programada', 'Programada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('verificada', 'Verificada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='borrador', tracking=True, required=True)

    # Costos
    costo_cosecha = fields.Float(
        string='Costo de Cosecha',
        digits=(12, 2)
    )
    costo_transporte = fields.Float(
        string='Costo de Transporte',
        digits=(12, 2)
    )
    costo_total = fields.Float(
        string='Costo Total',
        compute='_compute_costo_total',
        store=True
    )
    costo_por_unidad = fields.Float(
        string='Costo por Unidad',
        compute='_compute_costo_por_unidad'
    )

    # Observaciones
    condiciones_climaticas = fields.Text(string='Condiciones Climáticas')
    incidentes = fields.Text(string='Incidentes/Problemas')
    observaciones = fields.Text(string='Observaciones')

    # Trazabilidad
    lote_cosecha_ids = fields.One2many(
        'fincas_pma.lote_cosecha',
        'cosecha_id',
        string='Lotes de Producto'
    )

    # Referencia externa
    external_id = fields.Char(string='ID Externo')

    @api.depends('cantidad_bruta', 'cantidad_descuento')
    def _compute_cantidad_neta(self):
        for record in self:
            record.cantidad_neta = (record.cantidad_bruta or 0) - (record.cantidad_descuento or 0)

    @api.depends('cantidad_neta', 'area_cosechada_ha')
    def _compute_rendimiento(self):
        for record in self:
            if record.area_cosechada_ha:
                record.rendimiento = record.cantidad_neta / record.area_cosechada_ha
            else:
                record.rendimiento = 0

    def _compute_variacion_rendimiento(self):
        for record in self:
            if record.rendimiento_estimado:
                record.variacion_rendimiento_pct = (
                    (record.rendimiento - record.rendimiento_estimado) /
                    record.rendimiento_estimado * 100
                )
            else:
                record.variacion_rendimiento_pct = 0

    @api.depends('banano_cajas_total', 'banano_cajas_exportacion')
    def _compute_banano_ratio(self):
        for record in self:
            if record.banano_cajas_total:
                record.banano_ratio_exportacion = (
                    record.banano_cajas_exportacion / record.banano_cajas_total * 100
                )
            else:
                record.banano_ratio_exportacion = 0

    @api.depends('pina_brix', 'pina_acidez_pct')
    def _compute_pina_ratio(self):
        for record in self:
            if record.pina_acidez_pct:
                record.pina_ratio = record.pina_brix / record.pina_acidez_pct
            else:
                record.pina_ratio = 0

    @api.depends('palma_rff_tons', 'palma_aceite_pct')
    def _compute_palma_aceite(self):
        for record in self:
            record.palma_tons_aceite = (
                record.palma_rff_tons * (record.palma_aceite_pct or 0) / 100
            )

    @api.depends('costo_cosecha', 'costo_transporte')
    def _compute_costo_total(self):
        for record in self:
            record.costo_total = (record.costo_cosecha or 0) + (record.costo_transporte or 0)

    def _compute_costo_por_unidad(self):
        for record in self:
            if record.cantidad_neta:
                record.costo_por_unidad = record.costo_total / record.cantidad_neta
            else:
                record.costo_por_unidad = 0

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('fincas_pma.cosecha') or 'Nuevo'
        return super().create(vals)


class Cuadrilla(models.Model):
    """Cuadrillas o grupos de trabajo para cosecha."""
    _name = 'fincas_pma.cuadrilla'
    _description = 'Cuadrilla de Cosecha'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código')
    active = fields.Boolean('Activo', default=True)

    responsable_id = fields.Many2one(
        'hr.employee',
        string='Responsable/Capataz'
    )
    miembro_ids = fields.Many2many(
        'hr.employee',
        'cuadrilla_miembro_rel',
        'cuadrilla_id',
        'employee_id',
        string='Miembros'
    )
    finca_id = fields.Many2one(
        'fincas_pma.fincas_pma',
        string='Finca Asignada'
    )

    especialidad = fields.Selection([
        ('general', 'General'),
        ('cafe', 'Café'),
        ('banano', 'Banano'),
        ('pina', 'Piña'),
        ('cana', 'Caña'),
        ('palma', 'Palma'),
    ], string='Especialidad', default='general')

    capacidad_ha_dia = fields.Float(
        string='Capacidad (ha/día)',
        help='Hectáreas que puede cosechar por día'
    )

    notas = fields.Text(string='Notas')


class LoteCosecha(models.Model):
    """
    Lote de Producto Cosechado.
    Permite trazabilidad granular de cada lote de producto.
    """
    _name = 'fincas_pma.lote_cosecha'
    _description = 'Lote de Producto Cosechado (Trazabilidad)'
    _order = 'fecha_creacion desc'

    name = fields.Char(
        string='Código de Lote',
        required=True,
        copy=False,
        index=True
    )

    cosecha_id = fields.Many2one(
        'fincas_pma.cosecha',
        string='Cosecha Origen',
        required=True,
        ondelete='cascade'
    )
    lote_origen_id = fields.Many2one(
        'fincas_pma.lote',
        string='Lote de Campo',
        related='cosecha_id.lote_id',
        store=True
    )

    fecha_creacion = fields.Datetime(
        string='Fecha de Creación',
        default=fields.Datetime.now
    )

    # Cantidades
    cantidad = fields.Float(
        string='Cantidad',
        digits=(12, 2),
        required=True
    )
    unidad_id = fields.Many2one(
        'uom.uom',
        string='Unidad',
        required=True
    )

    # Calidad
    grado_calidad = fields.Selection([
        ('premium', 'Premium'),
        ('exportacion', 'Exportación'),
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('rechazo', 'Rechazo'),
    ], string='Grado de Calidad')

    # Transporte
    vehiculo = fields.Char(string='Vehículo/Placa')
    conductor_id = fields.Many2one('hr.employee', string='Conductor')
    guia_transporte = fields.Char(string='Guía de Transporte')

    # Destino
    destino_id = fields.Many2one(
        'res.partner',
        string='Destino'
    )

    # Fechas
    fecha_despacho = fields.Datetime(string='Fecha Despacho')
    fecha_recepcion = fields.Datetime(string='Fecha Recepción')

    # Estado
    estado = fields.Selection([
        ('creado', 'Creado'),
        ('despachado', 'Despachado'),
        ('en_transito', 'En Tránsito'),
        ('recibido', 'Recibido'),
        ('procesado', 'Procesado'),
    ], string='Estado', default='creado')

    # QR Code
    qr_code = fields.Binary(
        string='Código QR',
        compute='_compute_qr_code'
    )

    observaciones = fields.Text(string='Observaciones')

    def _compute_qr_code(self):
        """Genera código QR para trazabilidad"""
        for record in self:
            # Placeholder - implementar generación de QR
            record.qr_code = False
