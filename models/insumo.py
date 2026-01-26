# -*- coding: utf-8 -*-
"""
Gestión de Insumos Agrícolas
============================
Catálogo de insumos y registro de aplicaciones con trazabilidad completa.

Incluye:
- Fertilizantes (químicos y orgánicos)
- Agroquímicos (herbicidas, fungicidas, insecticidas, etc.)
- Biocontroladores
- Reguladores de crecimiento
- Semillas y material vegetal

Cumple con requisitos de certificaciones:
- GlobalG.A.P.
- Rainforest Alliance
- Orgánico USDA/EU
"""

from odoo import models, fields, api
from datetime import timedelta


class TipoInsumo(models.Model):
    """Clasificación de tipos de insumos agrícolas."""
    _name = 'fincas_pma.tipo_insumo'
    _description = 'Tipo de Insumo Agrícola'
    _order = 'secuencia, name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    secuencia = fields.Integer(string='Secuencia', default=10)
    descripcion = fields.Text(string='Descripción')
    active = fields.Boolean('Activo', default=True)

    # Características del tipo
    requiere_carencia = fields.Boolean(
        string='Requiere Período de Carencia',
        default=True
    )
    requiere_epp = fields.Boolean(
        string='Requiere EPP',
        default=True,
        help='Requiere Equipo de Protección Personal'
    )
    es_fertilizante = fields.Boolean(string='Es Fertilizante')
    es_agroquimico = fields.Boolean(string='Es Agroquímico')
    es_biologico = fields.Boolean(string='Es Biológico/Orgánico')

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)', 'El código debe ser único'),
    ]


class Insumo(models.Model):
    """
    Catálogo de Insumos Agrícolas.
    Gestión completa de productos utilizados en la finca.
    """
    _name = 'fincas_pma.insumo'
    _description = 'Insumo Agrícola'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'tipo_insumo_id, name'

    name = fields.Char(
        string='Nombre Comercial',
        required=True,
        tracking=True
    )
    active = fields.Boolean('Activo', default=True)
    codigo = fields.Char(
        string='Código',
        index=True,
        tracking=True
    )

    # Clasificación
    tipo_insumo_id = fields.Many2one(
        'fincas_pma.tipo_insumo',
        string='Tipo de Insumo',
        required=True,
        tracking=True
    )
    tipo_insumo_codigo = fields.Char(
        related='tipo_insumo_id.codigo',
        store=True
    )

    categoria = fields.Selection([
        # Fertilizantes
        ('fertilizante_quimico', 'Fertilizante Químico'),
        ('fertilizante_organico', 'Fertilizante Orgánico'),
        ('enmienda', 'Enmienda de Suelo'),
        ('foliar', 'Fertilizante Foliar'),
        # Agroquímicos
        ('herbicida', 'Herbicida'),
        ('fungicida', 'Fungicida'),
        ('insecticida', 'Insecticida'),
        ('acaricida', 'Acaricida'),
        ('nematicida', 'Nematicida'),
        ('molusquicida', 'Molusquicida'),
        ('rodenticida', 'Rodenticida'),
        # Otros
        ('regulador', 'Regulador de Crecimiento'),
        ('madurante', 'Madurante'),
        ('coadyuvante', 'Coadyuvante/Surfactante'),
        ('biocontrol', 'Control Biológico'),
        ('semilla', 'Semilla/Material Vegetal'),
        ('otro', 'Otro'),
    ], string='Categoría', required=True)

    # Información del producto
    ingrediente_activo = fields.Char(
        string='Ingrediente Activo',
        help='Principio activo del producto'
    )
    concentracion = fields.Char(
        string='Concentración',
        help='Concentración del ingrediente activo'
    )
    formulacion = fields.Selection([
        ('ec', 'EC - Concentrado Emulsionable'),
        ('sc', 'SC - Suspensión Concentrada'),
        ('sl', 'SL - Concentrado Soluble'),
        ('wp', 'WP - Polvo Mojable'),
        ('wg', 'WG - Gránulos Dispersables'),
        ('gr', 'GR - Granulado'),
        ('sp', 'SP - Polvo Soluble'),
        ('cs', 'CS - Suspensión de Cápsulas'),
        ('me', 'ME - Microemulsión'),
        ('od', 'OD - Dispersión Oleosa'),
        ('solido', 'Sólido'),
        ('liquido', 'Líquido'),
        ('otro', 'Otro'),
    ], string='Formulación')

    fabricante = fields.Char(string='Fabricante')
    distribuidor = fields.Char(string='Distribuidor')
    numero_registro = fields.Char(
        string='Número de Registro',
        help='Registro sanitario/agrícola'
    )
    pais_registro = fields.Char(string='País de Registro')

    # Composición (para fertilizantes)
    nitrogeno_pct = fields.Float(
        string='Nitrógeno N (%)',
        digits=(5, 2)
    )
    fosforo_pct = fields.Float(
        string='Fósforo P2O5 (%)',
        digits=(5, 2)
    )
    potasio_pct = fields.Float(
        string='Potasio K2O (%)',
        digits=(5, 2)
    )
    formula_npk = fields.Char(
        string='Fórmula N-P-K',
        compute='_compute_formula_npk',
        store=True
    )
    calcio_pct = fields.Float(string='Calcio CaO (%)', digits=(5, 2))
    magnesio_pct = fields.Float(string='Magnesio MgO (%)', digits=(5, 2))
    azufre_pct = fields.Float(string='Azufre S (%)', digits=(5, 2))
    otros_elementos = fields.Text(
        string='Otros Elementos',
        help='Microelementos y otros componentes'
    )

    # Toxicidad y seguridad
    categoria_toxicologica = fields.Selection([
        ('Ia', 'Ia - Extremadamente Peligroso'),
        ('Ib', 'Ib - Altamente Peligroso'),
        ('II', 'II - Moderadamente Peligroso'),
        ('III', 'III - Ligeramente Peligroso'),
        ('IV', 'IV - Normalmente No Peligroso'),
        ('na', 'No Aplica'),
    ], string='Categoría Toxicológica', tracking=True)

    color_etiqueta = fields.Selection([
        ('rojo', 'Rojo (Ia/Ib)'),
        ('amarillo', 'Amarillo (II)'),
        ('azul', 'Azul (III)'),
        ('verde', 'Verde (IV)'),
        ('na', 'No Aplica'),
    ], string='Color de Etiqueta')

    pictogramas_seguridad = fields.Text(
        string='Pictogramas de Seguridad',
        help='Códigos de pictogramas GHS'
    )
    epp_requerido = fields.Text(
        string='EPP Requerido',
        help='Equipo de Protección Personal necesario'
    )
    primeros_auxilios = fields.Text(string='Primeros Auxilios')
    antidoto = fields.Char(string='Antídoto')

    # Períodos de carencia y restricciones
    periodo_carencia_dias = fields.Integer(
        string='Período de Carencia (días)',
        help='Días mínimos entre última aplicación y cosecha',
        tracking=True
    )
    periodo_reentrada_horas = fields.Integer(
        string='Período de Reentrada (horas)',
        help='Horas antes de reingresar al área tratada'
    )
    intervalo_aplicacion_dias = fields.Integer(
        string='Intervalo entre Aplicaciones (días)',
        help='Días mínimos entre aplicaciones'
    )
    max_aplicaciones_ciclo = fields.Integer(
        string='Máx. Aplicaciones por Ciclo',
        help='Número máximo de aplicaciones por ciclo de cultivo'
    )

    # Restricciones ambientales
    restriccion_lluvia_horas = fields.Integer(
        string='Horas sin Lluvia Post-Aplicación'
    )
    temp_min_aplicacion = fields.Float(
        string='Temp. Mínima Aplicación (°C)'
    )
    temp_max_aplicacion = fields.Float(
        string='Temp. Máxima Aplicación (°C)'
    )
    humedad_min = fields.Float(string='Humedad Mín. (%)')
    humedad_max = fields.Float(string='Humedad Máx. (%)')
    velocidad_viento_max = fields.Float(
        string='Velocidad Viento Máx. (km/h)'
    )
    no_aplicar_floracion = fields.Boolean(
        string='No Aplicar en Floración',
        help='Restricción de aplicación durante floración (protección abejas)'
    )

    # Certificaciones y restricciones
    permitido_organico = fields.Boolean(
        string='Permitido en Orgánico',
        tracking=True
    )
    lista_omri = fields.Boolean(
        string='Listado OMRI',
        help='Organic Materials Review Institute'
    )
    permitido_rainforest = fields.Boolean(
        string='Permitido Rainforest Alliance',
        tracking=True
    )
    permitido_globalgap = fields.Boolean(
        string='Permitido GlobalG.A.P.',
        tracking=True
    )
    lista_roja = fields.Boolean(
        string='En Lista Roja/Prohibido',
        tracking=True,
        help='Producto en lista de prohibidos'
    )
    restricciones_certificacion = fields.Text(
        string='Restricciones por Certificación',
        help='Restricciones específicas según certificaciones'
    )

    # Dosificación recomendada
    dosis_minima = fields.Float(
        string='Dosis Mínima',
        digits=(10, 4)
    )
    dosis_recomendada = fields.Float(
        string='Dosis Recomendada',
        digits=(10, 4)
    )
    dosis_maxima = fields.Float(
        string='Dosis Máxima',
        digits=(10, 4)
    )
    unidad_dosis_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Dosis',
        help='Unidad de medida para la dosis (kg/ha, L/ha, etc.)'
    )
    volumen_agua_recomendado = fields.Float(
        string='Volumen de Agua (L/ha)',
        help='Litros de agua por hectárea'
    )

    # Cultivos objetivo y compatibilidad
    cultivo_ids = fields.Many2many(
        'fincas_pma.cultivo',
        'insumo_cultivo_rel',
        'insumo_id',
        'cultivo_id',
        string='Cultivos Registrados',
        help='Cultivos para los que está registrado el producto'
    )
    plagas_objetivo = fields.Text(
        string='Plagas/Enfermedades Objetivo',
        help='Lista de plagas o enfermedades que controla'
    )
    modo_accion = fields.Text(
        string='Modo de Acción',
        help='Mecanismo de acción del producto'
    )

    # Almacenamiento
    condiciones_almacenamiento = fields.Text(
        string='Condiciones de Almacenamiento'
    )
    vida_util_meses = fields.Integer(
        string='Vida Útil (meses)'
    )

    # Ficha técnica y documentos
    ficha_tecnica = fields.Binary(string='Ficha Técnica')
    ficha_tecnica_nombre = fields.Char(string='Nombre Ficha Técnica')
    hoja_seguridad = fields.Binary(string='Hoja de Seguridad (MSDS)')
    hoja_seguridad_nombre = fields.Char(string='Nombre Hoja Seguridad')

    # Imagen del producto
    image = fields.Binary(string='Imagen', attachment=True)

    # Notas
    notas = fields.Text(string='Notas')
    descripcion = fields.Text(string='Descripción')

    # Relación con producto de inventario (opcional)
    product_id = fields.Many2one(
        'product.product',
        string='Producto de Inventario',
        help='Producto relacionado en el módulo de inventario'
    )

    @api.depends('nitrogeno_pct', 'fosforo_pct', 'potasio_pct')
    def _compute_formula_npk(self):
        for record in self:
            if record.nitrogeno_pct or record.fosforo_pct or record.potasio_pct:
                record.formula_npk = f"{int(record.nitrogeno_pct or 0)}-{int(record.fosforo_pct or 0)}-{int(record.potasio_pct or 0)}"
            else:
                record.formula_npk = ''

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código del insumo debe ser único'),
    ]


class Aplicacion(models.Model):
    """
    Registro de Aplicación de Insumos.
    Trazabilidad completa de todas las aplicaciones realizadas.
    """
    _name = 'fincas_pma.aplicacion'
    _description = 'Aplicación de Insumo Agrícola'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_aplicacion desc'

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

    # Insumo aplicado
    insumo_id = fields.Many2one(
        'fincas_pma.insumo',
        string='Insumo',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    tipo_insumo_id = fields.Many2one(
        'fincas_pma.tipo_insumo',
        string='Tipo de Insumo',
        related='insumo_id.tipo_insumo_id',
        store=True
    )
    categoria_insumo = fields.Selection(
        related='insumo_id.categoria',
        store=True
    )

    # Fecha y hora
    fecha_aplicacion = fields.Datetime(
        string='Fecha y Hora de Aplicación',
        required=True,
        tracking=True,
        default=fields.Datetime.now
    )
    fecha_carencia = fields.Date(
        string='Fecha Fin Carencia',
        compute='_compute_fecha_carencia',
        store=True,
        help='Fecha a partir de la cual se puede cosechar'
    )
    en_periodo_carencia = fields.Boolean(
        string='En Período de Carencia',
        compute='_compute_en_periodo_carencia'
    )

    # Cantidades
    area_aplicada_ha = fields.Float(
        string='Área Aplicada (ha)',
        digits=(10, 4),
        required=True,
        tracking=True
    )
    dosis_aplicada = fields.Float(
        string='Dosis Aplicada',
        digits=(10, 4),
        required=True,
        tracking=True
    )
    unidad_dosis_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Dosis',
        required=True
    )
    cantidad_total = fields.Float(
        string='Cantidad Total',
        compute='_compute_cantidad_total',
        store=True,
        digits=(10, 4),
        help='Dosis × Área'
    )
    volumen_agua = fields.Float(
        string='Volumen de Agua (L)',
        digits=(10, 2)
    )

    # Trazabilidad del insumo
    lote_insumo = fields.Char(
        string='Lote del Insumo',
        tracking=True,
        help='Número de lote del producto aplicado'
    )
    fecha_fabricacion_insumo = fields.Date(
        string='Fecha Fabricación Insumo'
    )
    fecha_vencimiento_insumo = fields.Date(
        string='Fecha Vencimiento Insumo',
        tracking=True
    )

    # Método de aplicación
    metodo_aplicacion = fields.Selection([
        ('foliar_manual', 'Foliar - Bomba Manual'),
        ('foliar_motor', 'Foliar - Bomba a Motor'),
        ('foliar_tractor', 'Foliar - Tractor'),
        ('foliar_avion', 'Foliar - Aéreo (Avión)'),
        ('foliar_dron', 'Foliar - Aéreo (Dron)'),
        ('suelo_manual', 'Al Suelo - Manual'),
        ('suelo_mecanizado', 'Al Suelo - Mecanizado'),
        ('riego_goteo', 'Fertirrigación - Goteo'),
        ('riego_aspersion', 'Fertirrigación - Aspersión'),
        ('inyeccion_tronco', 'Inyección al Tronco'),
        ('granular', 'Aplicación Granular'),
        ('otro', 'Otro'),
    ], string='Método de Aplicación', required=True, tracking=True)

    equipo_utilizado = fields.Char(
        string='Equipo Utilizado',
        help='Descripción del equipo de aplicación'
    )
    boquilla_tipo = fields.Char(
        string='Tipo de Boquilla',
        help='Para aplicaciones de aspersión'
    )

    # Condiciones climáticas durante aplicación
    temperatura = fields.Float(
        string='Temperatura (°C)',
        digits=(4, 1)
    )
    humedad_relativa = fields.Float(
        string='Humedad Relativa (%)',
        digits=(5, 2)
    )
    velocidad_viento = fields.Float(
        string='Velocidad Viento (km/h)',
        digits=(5, 2)
    )
    condicion_climatica = fields.Selection([
        ('soleado', 'Soleado'),
        ('nublado', 'Nublado'),
        ('parcial', 'Parcialmente Nublado'),
        ('lluvioso', 'Lluvioso'),
    ], string='Condición Climática')

    # Objetivo de la aplicación
    objetivo = fields.Selection([
        ('preventivo', 'Preventivo'),
        ('curativo', 'Curativo'),
        ('nutricion', 'Nutrición'),
        ('control_malezas', 'Control de Malezas'),
        ('maduracion', 'Inducción de Maduración'),
        ('floracion', 'Inducción de Floración'),
        ('otro', 'Otro'),
    ], string='Objetivo', required=True)

    plaga_enfermedad = fields.Char(
        string='Plaga/Enfermedad Objetivo',
        help='Si aplica, especificar la plaga o enfermedad a controlar'
    )

    # Personal
    aplicador_ids = fields.Many2many(
        'hr.employee',
        'aplicacion_aplicador_rel',
        'aplicacion_id',
        'employee_id',
        string='Aplicadores'
    )
    supervisor_id = fields.Many2one(
        'hr.employee',
        string='Supervisor',
        tracking=True
    )
    horas_trabajo = fields.Float(
        string='Horas de Trabajo',
        digits=(5, 2)
    )
    jornales = fields.Float(
        string='Jornales Utilizados',
        digits=(5, 2)
    )

    # Estado
    estado = fields.Selection([
        ('planificada', 'Planificada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='planificada', tracking=True, required=True)

    # Resultados y observaciones
    efectividad = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('pobre', 'Pobre'),
        ('sin_evaluar', 'Sin Evaluar'),
    ], string='Efectividad', default='sin_evaluar')

    fecha_evaluacion = fields.Date(string='Fecha de Evaluación')
    observaciones_efectividad = fields.Text(
        string='Observaciones de Efectividad'
    )
    observaciones = fields.Text(string='Observaciones Generales')

    # Cumplimiento de certificaciones
    cumple_carencia = fields.Boolean(
        string='Cumple Período Carencia',
        compute='_compute_cumple_carencia'
    )
    alerta_certificacion = fields.Boolean(
        string='Alerta Certificación',
        compute='_compute_alerta_certificacion',
        help='Producto puede afectar certificación'
    )

    # Costo
    costo_insumo = fields.Float(
        string='Costo Insumo',
        digits=(12, 2)
    )
    costo_mano_obra = fields.Float(
        string='Costo Mano de Obra',
        digits=(12, 2)
    )
    costo_total = fields.Float(
        string='Costo Total',
        compute='_compute_costo_total',
        store=True,
        digits=(12, 2)
    )

    @api.depends('lote_id', 'insumo_id', 'fecha_aplicacion')
    def _compute_name(self):
        for record in self:
            if record.lote_id and record.insumo_id and record.fecha_aplicacion:
                fecha = record.fecha_aplicacion.strftime('%Y%m%d')
                record.name = f"APL-{record.lote_id.name}-{fecha}"
            else:
                record.name = 'Nueva Aplicación'

    @api.depends('fecha_aplicacion', 'insumo_id.periodo_carencia_dias')
    def _compute_fecha_carencia(self):
        for record in self:
            if record.fecha_aplicacion and record.insumo_id.periodo_carencia_dias:
                record.fecha_carencia = (
                    record.fecha_aplicacion.date() +
                    timedelta(days=record.insumo_id.periodo_carencia_dias)
                )
            else:
                record.fecha_carencia = False

    def _compute_en_periodo_carencia(self):
        today = fields.Date.today()
        for record in self:
            if record.fecha_carencia:
                record.en_periodo_carencia = today < record.fecha_carencia
            else:
                record.en_periodo_carencia = False

    @api.depends('dosis_aplicada', 'area_aplicada_ha')
    def _compute_cantidad_total(self):
        for record in self:
            record.cantidad_total = record.dosis_aplicada * record.area_aplicada_ha

    @api.depends('costo_insumo', 'costo_mano_obra')
    def _compute_costo_total(self):
        for record in self:
            record.costo_total = (record.costo_insumo or 0) + (record.costo_mano_obra or 0)

    def _compute_cumple_carencia(self):
        """Verifica si se respeta el período de carencia con última cosecha"""
        for record in self:
            # Buscar cosechas posteriores en el lote
            cosechas = self.env['fincas_pma.cosecha'].search([
                ('lote_id', '=', record.lote_id.id),
                ('fecha_cosecha', '>', record.fecha_aplicacion),
                ('fecha_cosecha', '<', record.fecha_carencia),
                ('estado', '=', 'completada'),
            ])
            record.cumple_carencia = len(cosechas) == 0

    def _compute_alerta_certificacion(self):
        for record in self:
            insumo = record.insumo_id
            record.alerta_certificacion = (
                insumo.lista_roja or
                (record.lote_id.es_organico and not insumo.permitido_organico)
            )

    @api.onchange('insumo_id')
    def _onchange_insumo_id(self):
        """Carga valores por defecto del insumo"""
        if self.insumo_id:
            self.unidad_dosis_id = self.insumo_id.unidad_dosis_id
            if not self.dosis_aplicada:
                self.dosis_aplicada = self.insumo_id.dosis_recomendada
