# -*- coding: utf-8 -*-
"""
Gestión de Sanidad Vegetal
==========================
Control fitosanitario: plagas, enfermedades y monitoreo.

Basado en protocolos de Manejo Integrado de Plagas (MIP):
- Monitoreo sistemático
- Umbrales de acción
- Registros de tratamientos
- Evaluación de efectividad
"""

from odoo import models, fields, api


class Plaga(models.Model):
    """
    Catálogo de Plagas y Enfermedades.
    Base de conocimiento para identificación y manejo.
    """
    _name = 'fincas_pma.plaga'
    _description = 'Plaga o Enfermedad'
    _order = 'tipo, name'

    name = fields.Char(
        string='Nombre Común',
        required=True
    )
    nombre_cientifico = fields.Char(
        string='Nombre Científico',
        help='Nombre científico del agente causal'
    )
    codigo = fields.Char(string='Código', index=True)
    active = fields.Boolean('Activo', default=True)

    # Clasificación
    tipo = fields.Selection([
        ('insecto', 'Insecto'),
        ('acaro', 'Ácaro'),
        ('hongo', 'Hongo'),
        ('bacteria', 'Bacteria'),
        ('virus', 'Virus'),
        ('nematodo', 'Nematodo'),
        ('maleza', 'Maleza'),
        ('roedor', 'Roedor'),
        ('ave', 'Ave'),
        ('molusco', 'Molusco'),
        ('otro', 'Otro'),
    ], string='Tipo', required=True)

    categoria = fields.Selection([
        ('plaga', 'Plaga'),
        ('enfermedad', 'Enfermedad'),
        ('maleza', 'Maleza'),
        ('otro', 'Otro Agente'),
    ], string='Categoría', required=True)

    # Cultivos afectados
    cultivo_ids = fields.Many2many(
        'fincas_pma.cultivo',
        'plaga_cultivo_rel',
        'plaga_id',
        'cultivo_id',
        string='Cultivos Afectados'
    )

    # Importancia económica
    importancia = fields.Selection([
        ('alta', 'Alta (Plaga Clave)'),
        ('media', 'Media (Plaga Secundaria)'),
        ('baja', 'Baja (Ocasional)'),
    ], string='Importancia Económica')

    es_cuarentenaria = fields.Boolean(
        string='Es Cuarentenaria',
        help='Plaga de importancia cuarentenaria'
    )

    # Biología y comportamiento
    ciclo_vida = fields.Text(
        string='Ciclo de Vida',
        help='Descripción de las etapas del ciclo biológico'
    )
    hospederos = fields.Text(
        string='Hospederos',
        help='Plantas hospederas conocidas'
    )
    condiciones_favorables = fields.Text(
        string='Condiciones Favorables',
        help='Condiciones que favorecen su desarrollo'
    )
    epocas_mayor_incidencia = fields.Char(
        string='Épocas de Mayor Incidencia',
        help='Meses o estaciones de mayor presencia'
    )

    # Daños
    parte_afectada = fields.Selection([
        ('raiz', 'Raíz'),
        ('tallo', 'Tallo'),
        ('hoja', 'Hoja'),
        ('flor', 'Flor'),
        ('fruto', 'Fruto'),
        ('semilla', 'Semilla'),
        ('planta_completa', 'Planta Completa'),
    ], string='Parte Afectada')

    sintomas = fields.Text(
        string='Síntomas',
        help='Síntomas visibles de la afectación'
    )
    danos = fields.Text(
        string='Daños',
        help='Descripción de los daños causados'
    )

    # Umbrales de acción
    umbral_economico = fields.Char(
        string='Umbral Económico',
        help='Nivel de infestación que justifica control'
    )
    umbral_accion = fields.Char(
        string='Umbral de Acción',
        help='Nivel para iniciar tratamiento'
    )
    metodo_muestreo = fields.Text(
        string='Método de Muestreo',
        help='Protocolo para monitoreo'
    )

    # Control
    control_cultural = fields.Text(
        string='Control Cultural',
        help='Prácticas culturales para manejo'
    )
    control_biologico = fields.Text(
        string='Control Biológico',
        help='Enemigos naturales y biocontroladores'
    )
    control_quimico = fields.Text(
        string='Control Químico',
        help='Productos y recomendaciones químicas'
    )

    # Insumos recomendados
    insumo_ids = fields.Many2many(
        'fincas_pma.insumo',
        'plaga_insumo_rel',
        'plaga_id',
        'insumo_id',
        string='Insumos Recomendados'
    )

    # Imágenes para identificación
    imagen_1 = fields.Binary(string='Imagen 1', attachment=True)
    imagen_2 = fields.Binary(string='Imagen 2', attachment=True)
    imagen_3 = fields.Binary(string='Imagen 3', attachment=True)

    descripcion = fields.Text(string='Descripción General')
    referencias = fields.Text(string='Referencias Bibliográficas')

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código de la plaga debe ser único'),
    ]


class MonitoreoSanitario(models.Model):
    """
    Registro de Monitoreo Fitosanitario.
    Seguimiento sistemático de plagas y enfermedades.
    """
    _name = 'fincas_pma.monitoreo_sanitario'
    _description = 'Monitoreo Fitosanitario'
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
        tracking=True
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

    # Fecha y tipo
    fecha = fields.Date(
        string='Fecha de Monitoreo',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    hora_inicio = fields.Float(string='Hora Inicio')
    hora_fin = fields.Float(string='Hora Fin')

    tipo_monitoreo = fields.Selection([
        ('rutinario', 'Rutinario'),
        ('alerta', 'Por Alerta/Reporte'),
        ('post_tratamiento', 'Post-Tratamiento'),
        ('pre_cosecha', 'Pre-Cosecha'),
        ('certificacion', 'Para Certificación'),
    ], string='Tipo de Monitoreo', required=True, default='rutinario')

    # Metodología
    metodologia = fields.Selection([
        ('visual', 'Inspección Visual'),
        ('trampas', 'Revisión de Trampas'),
        ('muestreo_plantas', 'Muestreo de Plantas'),
        ('muestreo_suelo', 'Muestreo de Suelo'),
        ('conteo_directo', 'Conteo Directo'),
    ], string='Metodología')

    plantas_muestreadas = fields.Integer(
        string='Plantas Muestreadas'
    )
    area_muestreada_ha = fields.Float(
        string='Área Muestreada (ha)',
        digits=(6, 2)
    )

    # Condiciones climáticas
    temperatura = fields.Float(string='Temperatura (°C)')
    humedad_relativa = fields.Float(string='Humedad Relativa (%)')
    precipitacion_reciente = fields.Boolean(string='Lluvia Reciente (24h)')

    # Estado fenológico del cultivo
    etapa_fenologica = fields.Char(
        string='Etapa Fenológica',
        help='Etapa de desarrollo del cultivo'
    )

    # Hallazgos
    hallazgo_ids = fields.One2many(
        'fincas_pma.hallazgo_monitoreo',
        'monitoreo_id',
        string='Hallazgos'
    )

    # Resumen
    hay_hallazgos = fields.Boolean(
        string='Hay Hallazgos',
        compute='_compute_hay_hallazgos'
    )
    requiere_tratamiento = fields.Boolean(
        string='Requiere Tratamiento',
        tracking=True
    )
    urgencia = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ], string='Urgencia')

    # Recomendaciones
    recomendaciones = fields.Text(
        string='Recomendaciones',
        help='Acciones recomendadas basadas en el monitoreo'
    )
    fecha_siguiente_monitoreo = fields.Date(
        string='Próximo Monitoreo'
    )

    # Personal
    monitor_id = fields.Many2one(
        'hr.employee',
        string='Monitor/Evaluador',
        tracking=True
    )
    verificado_por_id = fields.Many2one(
        'hr.employee',
        string='Verificado Por'
    )

    # Fotos de evidencia
    foto_ids = fields.One2many(
        'fincas_pma.foto_monitoreo',
        'monitoreo_id',
        string='Fotos de Evidencia'
    )

    # Estado
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('completado', 'Completado'),
        ('verificado', 'Verificado'),
    ], string='Estado', default='borrador', tracking=True)

    observaciones = fields.Text(string='Observaciones Generales')

    @api.depends('lote_id', 'fecha')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.fecha:
                record.name = f"MON-{record.lote_id.name}-{record.fecha}"
            else:
                record.name = 'Nuevo Monitoreo'

    @api.depends('hallazgo_ids')
    def _compute_hay_hallazgos(self):
        for record in self:
            record.hay_hallazgos = bool(record.hallazgo_ids)


class HallazgoMonitoreo(models.Model):
    """
    Hallazgo individual en un monitoreo.
    Registra cada plaga/enfermedad detectada.
    """
    _name = 'fincas_pma.hallazgo_monitoreo'
    _description = 'Hallazgo de Monitoreo'

    monitoreo_id = fields.Many2one(
        'fincas_pma.monitoreo_sanitario',
        string='Monitoreo',
        required=True,
        ondelete='cascade'
    )

    # Plaga/Enfermedad
    plaga_id = fields.Many2one(
        'fincas_pma.plaga',
        string='Plaga/Enfermedad',
        required=True
    )
    tipo_plaga = fields.Selection(
        related='plaga_id.tipo',
        store=True
    )

    # Nivel de incidencia
    nivel_incidencia = fields.Selection([
        ('nulo', 'Nulo (0%)'),
        ('trazas', 'Trazas (<1%)'),
        ('bajo', 'Bajo (1-10%)'),
        ('medio', 'Medio (11-30%)'),
        ('alto', 'Alto (31-60%)'),
        ('severo', 'Severo (>60%)'),
    ], string='Nivel de Incidencia', required=True)

    incidencia_pct = fields.Float(
        string='Incidencia (%)',
        digits=(5, 2),
        help='Porcentaje de plantas/área afectada'
    )
    severidad = fields.Selection([
        ('leve', 'Leve'),
        ('moderada', 'Moderada'),
        ('severa', 'Severa'),
    ], string='Severidad del Daño')

    # Área afectada
    area_afectada_ha = fields.Float(
        string='Área Afectada (ha)',
        digits=(6, 2)
    )
    plantas_afectadas = fields.Integer(string='Plantas Afectadas')

    # Ubicación dentro del lote
    ubicacion_en_lote = fields.Selection([
        ('generalizado', 'Generalizado'),
        ('focalizado', 'Focalizado'),
        ('bordes', 'En Bordes'),
        ('centro', 'En Centro'),
        ('parches', 'En Parches'),
    ], string='Distribución')

    ubicacion_detalle = fields.Char(
        string='Detalle de Ubicación',
        help='Descripción específica de la ubicación'
    )

    # Estado de desarrollo (para plagas)
    estado_desarrollo = fields.Selection([
        ('huevo', 'Huevo'),
        ('larva', 'Larva/Ninfa'),
        ('pupa', 'Pupa'),
        ('adulto', 'Adulto'),
        ('todos', 'Todos los Estados'),
    ], string='Estado de Desarrollo')

    # Comparación
    tendencia = fields.Selection([
        ('aumento', 'En Aumento'),
        ('estable', 'Estable'),
        ('disminucion', 'En Disminución'),
        ('nuevo', 'Nueva Detección'),
    ], string='Tendencia')

    # Evaluación vs umbral
    supera_umbral = fields.Boolean(
        string='Supera Umbral',
        help='Indica si el nivel supera el umbral de acción'
    )

    # Tratamiento
    requiere_tratamiento = fields.Boolean(string='Requiere Tratamiento')
    tratamiento_sugerido = fields.Text(string='Tratamiento Sugerido')

    observaciones = fields.Text(string='Observaciones')


class FotoMonitoreo(models.Model):
    """Fotos de evidencia de monitoreos."""
    _name = 'fincas_pma.foto_monitoreo'
    _description = 'Foto de Monitoreo'

    monitoreo_id = fields.Many2one(
        'fincas_pma.monitoreo_sanitario',
        string='Monitoreo',
        required=True,
        ondelete='cascade'
    )

    image = fields.Binary(
        string='Imagen',
        required=True,
        attachment=True
    )
    descripcion = fields.Char(string='Descripción')
    fecha_captura = fields.Datetime(
        string='Fecha de Captura',
        default=fields.Datetime.now
    )

    # Geolocalización de la foto
    latitud = fields.Float(string='Latitud', digits=(10, 6))
    longitud = fields.Float(string='Longitud', digits=(10, 6))

    plaga_id = fields.Many2one(
        'fincas_pma.plaga',
        string='Plaga/Enfermedad Mostrada'
    )


class Tratamiento(models.Model):
    """
    Registro de tratamientos fitosanitarios.
    Vincula monitoreo con aplicación de insumos.
    """
    _name = 'fincas_pma.tratamiento'
    _description = 'Tratamiento Fitosanitario'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
    )

    # Origen
    monitoreo_id = fields.Many2one(
        'fincas_pma.monitoreo_sanitario',
        string='Monitoreo Origen',
        help='Monitoreo que generó este tratamiento'
    )
    lote_id = fields.Many2one(
        'fincas_pma.lote',
        string='Lote',
        required=True,
        tracking=True
    )

    # Objetivo
    plaga_ids = fields.Many2many(
        'fincas_pma.plaga',
        'tratamiento_plaga_rel',
        'tratamiento_id',
        'plaga_id',
        string='Plagas/Enfermedades Objetivo'
    )
    objetivo = fields.Selection([
        ('preventivo', 'Preventivo'),
        ('curativo', 'Curativo'),
        ('erradicacion', 'Erradicación'),
    ], string='Tipo de Tratamiento', required=True)

    # Planificación
    fecha_planificada = fields.Date(string='Fecha Planificada')
    fecha = fields.Date(
        string='Fecha de Tratamiento',
        tracking=True
    )

    # Aplicaciones realizadas
    aplicacion_ids = fields.One2many(
        'fincas_pma.aplicacion',
        'tratamiento_id',
        string='Aplicaciones'
    )
    numero_aplicaciones = fields.Integer(
        string='Número de Aplicaciones',
        compute='_compute_numero_aplicaciones'
    )

    # Evaluación de efectividad
    fecha_evaluacion = fields.Date(string='Fecha de Evaluación')
    efectividad = fields.Selection([
        ('excelente', 'Excelente (>90% control)'),
        ('buena', 'Buena (70-90% control)'),
        ('regular', 'Regular (50-70% control)'),
        ('pobre', 'Pobre (<50% control)'),
        ('sin_efecto', 'Sin Efecto'),
    ], string='Efectividad', tracking=True)

    reduccion_incidencia_pct = fields.Float(
        string='Reducción de Incidencia (%)',
        digits=(5, 2)
    )

    # Estado
    estado = fields.Selection([
        ('planificado', 'Planificado'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('evaluado', 'Evaluado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='planificado', tracking=True)

    observaciones = fields.Text(string='Observaciones')
    recomendaciones_futuras = fields.Text(
        string='Recomendaciones Futuras',
        help='Lecciones aprendidas y recomendaciones'
    )

    @api.depends('lote_id', 'fecha')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.fecha:
                record.name = f"TRAT-{record.lote_id.name}-{record.fecha}"
            else:
                record.name = 'Nuevo Tratamiento'

    def _compute_numero_aplicaciones(self):
        for record in self:
            record.numero_aplicaciones = len(record.aplicacion_ids)


# Agregar campo al modelo de aplicación para vincular con tratamiento
class AplicacionTratamiento(models.Model):
    _inherit = 'fincas_pma.aplicacion'

    tratamiento_id = fields.Many2one(
        'fincas_pma.tratamiento',
        string='Tratamiento Relacionado',
        help='Tratamiento fitosanitario al que pertenece esta aplicación'
    )
