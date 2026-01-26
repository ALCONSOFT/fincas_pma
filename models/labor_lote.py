# -*- coding: utf-8 -*-
"""
Gestión de Labores Agrícolas por Lote
=====================================
Registro de todas las actividades realizadas en los lotes.
Integra con el catálogo de labores existente.
"""

from odoo import models, fields, api


class LaborLote(models.Model):
    """
    Registro de labor realizada en un lote específico.
    """
    _name = 'fincas_pma.labor_lote'
    _description = 'Labor Realizada en Lote'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
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
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        related='lote_id.cultivo_id',
        store=True
    )

    # Labor
    labor_id = fields.Many2one(
        'fincas_pma.labores',
        string='Labor',
        required=True,
        tracking=True
    )
    categoria_labor = fields.Selection([
        ('preparacion', 'Preparación de Suelo'),
        ('siembra', 'Siembra'),
        ('fertilizacion', 'Fertilización'),
        ('riego', 'Riego'),
        ('control_malezas', 'Control de Malezas'),
        ('control_plagas', 'Control de Plagas'),
        ('poda', 'Poda'),
        ('cosecha', 'Cosecha'),
        ('post_cosecha', 'Post-Cosecha'),
        ('mantenimiento', 'Mantenimiento'),
        ('otro', 'Otro'),
    ], string='Categoría', required=True)

    descripcion = fields.Text(string='Descripción de la Labor')

    # Fechas
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    hora_inicio = fields.Float(string='Hora Inicio')
    hora_fin = fields.Float(string='Hora Fin')
    duracion_horas = fields.Float(
        string='Duración (horas)',
        compute='_compute_duracion',
        store=True
    )

    # Área y cantidad
    area_trabajada_ha = fields.Float(
        string='Área Trabajada (ha)',
        digits=(10, 4),
        tracking=True
    )
    cantidad = fields.Float(
        string='Cantidad',
        digits=(10, 2),
        help='Cantidad según unidad de medida de la labor'
    )
    unidad_medida_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        related='labor_id.unidad_medida',
        store=True
    )

    # Rendimiento
    rendimiento = fields.Float(
        string='Rendimiento',
        compute='_compute_rendimiento',
        store=True,
        help='Cantidad / Área trabajada'
    )
    rendimiento_hora = fields.Float(
        string='Rendimiento/Hora',
        compute='_compute_rendimiento',
        store=True,
        help='Área trabajada / Horas'
    )

    # Personal
    trabajador_ids = fields.Many2many(
        'hr.employee',
        'labor_lote_trabajador_rel',
        'labor_lote_id',
        'employee_id',
        string='Trabajadores'
    )
    numero_trabajadores = fields.Integer(
        string='Número de Trabajadores',
        compute='_compute_trabajadores',
        store=True
    )
    jornales = fields.Float(
        string='Jornales',
        digits=(8, 2)
    )
    supervisor_id = fields.Many2one(
        'hr.employee',
        string='Supervisor'
    )
    cuadrilla_id = fields.Many2one(
        'fincas_pma.cuadrilla',
        string='Cuadrilla'
    )

    # Equipos
    equipo_ids = fields.Many2many(
        'maintenance.equipment',
        'labor_lote_equipo_rel',
        'labor_lote_id',
        'equipment_id',
        string='Equipos Utilizados'
    )
    horas_maquina = fields.Float(
        string='Horas Máquina',
        digits=(6, 2)
    )
    combustible_litros = fields.Float(
        string='Combustible (L)',
        digits=(8, 2)
    )

    # Insumos utilizados (si aplica)
    insumo_ids = fields.Many2many(
        'fincas_pma.insumo',
        'labor_lote_insumo_rel',
        'labor_lote_id',
        'insumo_id',
        string='Insumos Utilizados'
    )

    # Condiciones climáticas
    condicion_climatica = fields.Selection([
        ('soleado', 'Soleado'),
        ('nublado', 'Nublado'),
        ('lluvioso', 'Lluvioso'),
        ('parcial', 'Parcialmente Nublado'),
    ], string='Clima')
    temperatura = fields.Float(string='Temperatura (°C)')
    interrupciones = fields.Text(
        string='Interrupciones',
        help='Descripción de interrupciones (lluvia, fallas, etc.)'
    )

    # Costos
    costo_mano_obra = fields.Float(
        string='Costo Mano de Obra',
        digits=(12, 2)
    )
    costo_maquinaria = fields.Float(
        string='Costo Maquinaria',
        digits=(12, 2)
    )
    costo_insumos = fields.Float(
        string='Costo Insumos',
        digits=(12, 2)
    )
    costo_total = fields.Float(
        string='Costo Total',
        compute='_compute_costo_total',
        store=True,
        digits=(12, 2)
    )
    costo_por_ha = fields.Float(
        string='Costo por Hectárea',
        compute='_compute_costo_por_ha',
        digits=(10, 2)
    )

    # Estado
    estado = fields.Selection([
        ('planificada', 'Planificada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='completada', tracking=True)

    # Calidad del trabajo
    calidad = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('deficiente', 'Deficiente'),
    ], string='Calidad del Trabajo')

    # Observaciones
    observaciones = fields.Text(string='Observaciones')
    problemas = fields.Text(string='Problemas Encontrados')
    recomendaciones = fields.Text(string='Recomendaciones')

    @api.depends('lote_id', 'labor_id', 'fecha')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.labor_id and record.fecha:
                record.name = f"LAB-{record.lote_id.name}-{record.labor_id.code_labor}-{record.fecha}"
            else:
                record.name = 'Nueva Labor'

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        for record in self:
            if record.hora_fin and record.hora_inicio:
                record.duracion_horas = record.hora_fin - record.hora_inicio
            else:
                record.duracion_horas = 0

    @api.depends('cantidad', 'area_trabajada_ha', 'duracion_horas')
    def _compute_rendimiento(self):
        for record in self:
            if record.area_trabajada_ha:
                record.rendimiento = record.cantidad / record.area_trabajada_ha if record.cantidad else 0
            else:
                record.rendimiento = 0
            if record.duracion_horas:
                record.rendimiento_hora = record.area_trabajada_ha / record.duracion_horas
            else:
                record.rendimiento_hora = 0

    @api.depends('trabajador_ids')
    def _compute_trabajadores(self):
        for record in self:
            record.numero_trabajadores = len(record.trabajador_ids)

    @api.depends('costo_mano_obra', 'costo_maquinaria', 'costo_insumos')
    def _compute_costo_total(self):
        for record in self:
            record.costo_total = (
                (record.costo_mano_obra or 0) +
                (record.costo_maquinaria or 0) +
                (record.costo_insumos or 0)
            )

    def _compute_costo_por_ha(self):
        for record in self:
            if record.area_trabajada_ha:
                record.costo_por_ha = record.costo_total / record.area_trabajada_ha
            else:
                record.costo_por_ha = 0


class Siembra(models.Model):
    """
    Registro específico de siembras.
    Extiende la información de labor para siembras.
    """
    _name = 'fincas_pma.siembra'
    _description = 'Registro de Siembra'
    _inherit = ['mail.thread', 'mail.activity.mixin']
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
        tracking=True
    )
    fecha = fields.Date(
        string='Fecha de Siembra',
        required=True,
        tracking=True
    )

    # Cultivo y variedad
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        required=True,
        tracking=True
    )
    variedad_id = fields.Many2one(
        'fincas_pma.variedad_cultivo',
        string='Variedad',
        required=True,
        tracking=True,
        domain="[('cultivo_id', '=', cultivo_id)]"
    )

    # Tipo de siembra
    tipo_siembra = fields.Selection([
        ('nueva', 'Siembra Nueva'),
        ('renovacion', 'Renovación'),
        ('resiembra', 'Resiembra'),
        ('soca', 'Soca'),
    ], string='Tipo de Siembra', required=True, default='nueva')

    # Material de siembra
    tipo_material = fields.Selection([
        ('semilla', 'Semilla'),
        ('plantula', 'Plántula'),
        ('esqueje', 'Esqueje/Estaca'),
        ('cormo', 'Cormo'),
        ('hijuelo', 'Hijuelo'),
        ('vitro', 'Vitro Planta'),
        ('injerto', 'Injerto'),
    ], string='Tipo de Material')

    procedencia_material = fields.Char(string='Procedencia del Material')
    lote_semilla = fields.Char(string='Lote de Semilla')

    # Cantidades
    area_sembrada_ha = fields.Float(
        string='Área Sembrada (ha)',
        digits=(10, 4),
        required=True,
        tracking=True
    )
    cantidad_material = fields.Float(
        string='Cantidad de Material',
        digits=(10, 2)
    )
    unidad_material_id = fields.Many2one(
        'uom.uom',
        string='Unidad del Material'
    )

    # Densidad
    densidad_plantas_ha = fields.Integer(
        string='Densidad (plantas/ha)'
    )
    distancia_plantas = fields.Float(
        string='Distancia entre Plantas (m)',
        digits=(4, 2)
    )
    distancia_hileras = fields.Float(
        string='Distancia entre Hileras (m)',
        digits=(4, 2)
    )
    sistema_siembra = fields.Selection([
        ('hileras', 'En Hileras'),
        ('cuadrado', 'Cuadrado'),
        ('tresbolillo', 'Tresbolillo'),
        ('contorno', 'En Contorno'),
        ('voleo', 'Al Voleo'),
    ], string='Sistema de Siembra')

    # Condiciones
    preparacion_suelo = fields.Text(string='Preparación del Suelo')
    fertilizacion_base = fields.Text(string='Fertilización Base')
    tratamiento_semilla = fields.Text(string='Tratamiento de Semilla')

    # Personal y costos
    jornales = fields.Float(string='Jornales', digits=(8, 2))
    costo_material = fields.Float(string='Costo Material', digits=(12, 2))
    costo_mano_obra = fields.Float(string='Costo Mano de Obra', digits=(12, 2))
    costo_total = fields.Float(
        string='Costo Total',
        compute='_compute_costo_total',
        store=True
    )

    # Seguimiento
    germinacion_pct = fields.Float(
        string='Germinación (%)',
        digits=(5, 2),
        help='Porcentaje de germinación observado'
    )
    fecha_emergencia = fields.Date(string='Fecha de Emergencia')
    supervivencia_pct = fields.Float(
        string='Supervivencia (%)',
        digits=(5, 2)
    )
    requiere_resiembra = fields.Boolean(string='Requiere Resiembra')

    observaciones = fields.Text(string='Observaciones')

    @api.depends('lote_id', 'fecha')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.fecha:
                record.name = f"SIEMBRA-{record.lote_id.name}-{record.fecha}"
            else:
                record.name = 'Nueva Siembra'

    @api.depends('costo_material', 'costo_mano_obra')
    def _compute_costo_total(self):
        for record in self:
            record.costo_total = (record.costo_material or 0) + (record.costo_mano_obra or 0)

    @api.model
    def create(self, vals):
        """Al crear siembra, actualiza el lote"""
        siembra = super().create(vals)
        if siembra.lote_id:
            siembra.lote_id.write({
                'cultivo_id': siembra.cultivo_id.id,
                'variedad_id': siembra.variedad_id.id,
                'fecha_siembra': siembra.fecha,
                'estado': 'sembrado',
                'densidad_plantas': siembra.densidad_plantas_ha,
                'distancia_entre_plantas': siembra.distancia_plantas,
                'distancia_entre_hileras': siembra.distancia_hileras,
            })
        return siembra
