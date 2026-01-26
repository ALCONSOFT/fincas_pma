# -*- coding: utf-8 -*-
"""
Catálogo de Cultivos Multi-Región
=================================
Soporta: Café, Banano, Piña, Palma Aceitera, Caña de Azúcar y otros cultivos
importantes para Panamá, Centro América y Colombia.

Basado en mejores prácticas internacionales de gestión agrícola:
- GlobalG.A.P.
- Rainforest Alliance
- UTZ Certified
- RSPO (Palma)
- Bonsucro (Caña)
"""

from odoo import models, fields, api


class Cultivo(models.Model):
    """
    Catálogo principal de cultivos agrícolas.
    Permite gestionar múltiples cultivos en una misma finca.
    """
    _name = 'fincas_pma.cultivo'
    _description = 'Catálogo de Cultivos Agrícolas'
    _order = 'name'

    name = fields.Char(
        string='Nombre del Cultivo',
        required=True,
        help='Nombre común del cultivo (ej: Café, Banano, Caña)'
    )
    active = fields.Boolean('Activo', default=True)
    codigo = fields.Char(
        string='Código',
        required=True,
        index=True,
        help='Código único del cultivo (ej: CAF, BAN, CAN, PIN, PAL)'
    )
    nombre_cientifico = fields.Char(
        string='Nombre Científico',
        help='Nombre científico (ej: Coffea arabica, Musa acuminata)'
    )
    familia_botanica = fields.Char(
        string='Familia Botánica',
        help='Familia botánica (ej: Rubiaceae, Musaceae, Poaceae)'
    )

    # Clasificación del cultivo
    tipo_cultivo = fields.Selection([
        ('perenne', 'Perenne'),           # Café, Palma, Cacao, Frutales
        ('semipermanente', 'Semi-permanente'),  # Caña, Piña, Banano
        ('anual', 'Anual'),               # Maíz, Arroz, Frijol
        ('hortalizas', 'Hortalizas'),     # Tomate, Pimiento, etc.
    ], string='Tipo de Cultivo', required=True, default='perenne')

    # Características productivas
    ciclo_dias = fields.Integer(
        string='Ciclo Productivo (días)',
        help='Días desde siembra/floración hasta cosecha'
    )
    vida_util_anios = fields.Integer(
        string='Vida Útil (años)',
        help='Años de producción económica del cultivo'
    )
    meses_primera_cosecha = fields.Integer(
        string='Meses hasta Primera Cosecha',
        help='Meses desde siembra hasta primera cosecha'
    )
    cosechas_por_anio = fields.Float(
        string='Cosechas por Año',
        help='Número de cosechas anuales (ej: Banano = 52 semanas)'
    )

    # Requerimientos agroecológicos
    temp_min = fields.Float(
        string='Temperatura Mínima (°C)',
        help='Temperatura mínima tolerable'
    )
    temp_optima_min = fields.Float(
        string='Temp. Óptima Mín (°C)',
        help='Temperatura óptima mínima'
    )
    temp_optima_max = fields.Float(
        string='Temp. Óptima Máx (°C)',
        help='Temperatura óptima máxima'
    )
    temp_max = fields.Float(
        string='Temperatura Máxima (°C)',
        help='Temperatura máxima tolerable'
    )
    precipitacion_min = fields.Float(
        string='Precipitación Mínima (mm/año)',
        help='Precipitación anual mínima requerida'
    )
    precipitacion_optima = fields.Float(
        string='Precipitación Óptima (mm/año)',
        help='Precipitación anual óptima'
    )
    precipitacion_max = fields.Float(
        string='Precipitación Máxima (mm/año)',
        help='Precipitación anual máxima tolerable'
    )
    altitud_min = fields.Integer(
        string='Altitud Mínima (msnm)',
        help='Altitud mínima para el cultivo'
    )
    altitud_optima_min = fields.Integer(
        string='Altitud Óptima Mín (msnm)'
    )
    altitud_optima_max = fields.Integer(
        string='Altitud Óptima Máx (msnm)'
    )
    altitud_max = fields.Integer(
        string='Altitud Máxima (msnm)',
        help='Altitud máxima para el cultivo'
    )

    # Requerimientos de suelo
    ph_min = fields.Float(string='pH Mínimo', digits=(3, 1))
    ph_optimo_min = fields.Float(string='pH Óptimo Mín', digits=(3, 1))
    ph_optimo_max = fields.Float(string='pH Óptimo Máx', digits=(3, 1))
    ph_max = fields.Float(string='pH Máximo', digits=(3, 1))

    tipos_suelo_recomendados = fields.Text(
        string='Tipos de Suelo Recomendados',
        help='Tipos de suelo aptos para el cultivo'
    )

    # Rendimientos de referencia
    rendimiento_min = fields.Float(
        string='Rendimiento Mínimo',
        help='Rendimiento mínimo esperado'
    )
    rendimiento_promedio = fields.Float(
        string='Rendimiento Promedio',
        help='Rendimiento promedio de la región'
    )
    rendimiento_optimo = fields.Float(
        string='Rendimiento Óptimo',
        help='Rendimiento óptimo alcanzable'
    )
    unidad_rendimiento_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Rendimiento',
        help='Unidad de medida del rendimiento (qq/ha, tons/ha, cajas/ha)'
    )

    # Imagen/Icono del cultivo
    image = fields.Binary(string='Imagen', attachment=True)

    # Descripción y notas técnicas
    description = fields.Text(string='Descripción General')
    notas_tecnicas = fields.Text(
        string='Notas Técnicas',
        help='Información técnica adicional del cultivo'
    )

    # Relaciones
    variedad_ids = fields.One2many(
        'fincas_pma.variedad_cultivo',
        'cultivo_id',
        string='Variedades'
    )
    fenologia_ids = fields.One2many(
        'fincas_pma.fenologia',
        'cultivo_id',
        string='Etapas Fenológicas'
    )
    parametro_calidad_ids = fields.One2many(
        'fincas_pma.parametro_calidad',
        'cultivo_id',
        string='Parámetros de Calidad'
    )

    # Campos computados
    variedad_count = fields.Integer(
        string='# Variedades',
        compute='_compute_variedad_count'
    )

    @api.depends('variedad_ids')
    def _compute_variedad_count(self):
        for record in self:
            record.variedad_count = len(record.variedad_ids)

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código del cultivo debe ser único'),
        ('name_unique', 'UNIQUE(name)',
         'El nombre del cultivo debe ser único'),
    ]


class VariedadCultivo(models.Model):
    """
    Variedades específicas de cada cultivo.
    Permite registrar características únicas por variedad.
    """
    _name = 'fincas_pma.variedad_cultivo'
    _description = 'Variedades de Cultivo'
    _order = 'cultivo_id, name'

    name = fields.Char(
        string='Nombre de la Variedad',
        required=True,
        help='Nombre comercial o técnico de la variedad'
    )
    active = fields.Boolean('Activo', default=True)
    codigo = fields.Char(
        string='Código',
        index=True,
        help='Código único de la variedad'
    )
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        required=True,
        ondelete='restrict'
    )

    # Origen y genética
    origen = fields.Char(
        string='País/Región de Origen',
        help='Origen geográfico de la variedad'
    )
    ano_liberacion = fields.Integer(
        string='Año de Liberación',
        help='Año en que fue liberada comercialmente'
    )
    obtentor = fields.Char(
        string='Obtentor/Desarrollador',
        help='Institución o empresa que desarrolló la variedad'
    )
    parentales = fields.Char(
        string='Parentales',
        help='Variedades parentales (cruce genético)'
    )

    # Características productivas
    rendimiento_esperado = fields.Float(
        string='Rendimiento Esperado',
        help='Rendimiento típico de la variedad'
    )
    unidad_rendimiento_id = fields.Many2one(
        'uom.uom',
        string='Unidad Rendimiento'
    )
    ciclo_dias = fields.Integer(
        string='Ciclo (días)',
        help='Días hasta cosecha (puede variar del cultivo base)'
    )

    # Resistencias (escala: alta, media, baja, susceptible)
    resistencia_sequia = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='Resistencia a Sequía')

    resistencia_plagas = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='Resistencia a Plagas')

    resistencia_enfermedades = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='Resistencia a Enfermedades')

    tolerancia_frio = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='Tolerancia al Frío')

    # Calidad del producto
    calidad_general = fields.Selection([
        ('premium', 'Premium/Especialidad'),
        ('primera', 'Primera'),
        ('estandar', 'Estándar'),
    ], string='Calidad General', default='estandar')

    # === CAMPOS ESPECÍFICOS POR CULTIVO ===

    # --- CAFÉ ---
    cafe_perfil_taza = fields.Text(
        string='[Café] Perfil de Taza',
        help='Notas de cata: acidez, cuerpo, aroma, sabor'
    )
    cafe_puntaje_taza_tipico = fields.Float(
        string='[Café] Puntaje Taza Típico',
        digits=(4, 1),
        help='Puntaje SCA típico (0-100)'
    )
    cafe_altitud_recomendada = fields.Char(
        string='[Café] Altitud Recomendada',
        help='Rango de altitud óptimo para esta variedad'
    )
    cafe_porte = fields.Selection([
        ('alto', 'Alto (>3m)'),
        ('medio', 'Medio (2-3m)'),
        ('bajo', 'Bajo/Compacto (<2m)'),
    ], string='[Café] Porte de Planta')
    cafe_resistencia_roya = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Café] Resistencia a Roya')
    cafe_resistencia_cbd = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Café] Resistencia a CBD',
        help='Coffee Berry Disease')

    # --- BANANO ---
    banano_grupo_genomico = fields.Selection([
        ('aaa', 'AAA (Cavendish, Gros Michel)'),
        ('aab', 'AAB (Plátano, Seda)'),
        ('abb', 'ABB (Pelipita, Saba)'),
        ('aa', 'AA (Diploides)'),
    ], string='[Banano] Grupo Genómico')
    banano_ciclo_semanas = fields.Integer(
        string='[Banano] Ciclo (semanas)',
        help='Semanas desde siembra hasta cosecha'
    )
    banano_calibre_tipico = fields.Char(
        string='[Banano] Calibre Típico',
        help='Calibre típico en grados (ej: 39-46)'
    )
    banano_manos_por_racimo = fields.Char(
        string='[Banano] Manos por Racimo',
        help='Rango típico de manos (ej: 8-12)'
    )
    banano_peso_racimo = fields.Float(
        string='[Banano] Peso Racimo (kg)',
        help='Peso promedio del racimo'
    )
    banano_resistencia_sigatoka = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Banano] Resistencia a Sigatoka')
    banano_resistencia_fusarium = fields.Selection([
        ('alta', 'Alta (TR4 tolerante)'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Banano] Resistencia a Fusarium',
        help='Resistencia a Fusarium oxysporum (Mal de Panamá)')

    # --- PIÑA ---
    pina_grupo = fields.Selection([
        ('cayena', 'Cayena Lisa'),
        ('queen', 'Queen'),
        ('espanola', 'Española'),
        ('md2', 'MD2/Gold'),
        ('otro', 'Otro'),
    ], string='[Piña] Grupo')
    pina_peso_fruta = fields.Float(
        string='[Piña] Peso Fruta (kg)',
        help='Peso promedio de la fruta'
    )
    pina_brix_tipico = fields.Float(
        string='[Piña] Brix Típico',
        help='Grados Brix típicos'
    )
    pina_acidez_tipica = fields.Float(
        string='[Piña] Acidez Típica (%)',
        help='Porcentaje de acidez'
    )
    pina_ratio_tipico = fields.Float(
        string='[Piña] Ratio Brix/Acidez',
        help='Relación Brix/Acidez típica'
    )
    pina_color_pulpa = fields.Selection([
        ('amarillo_intenso', 'Amarillo Intenso'),
        ('amarillo', 'Amarillo'),
        ('amarillo_palido', 'Amarillo Pálido'),
        ('blanco', 'Blanco'),
    ], string='[Piña] Color de Pulpa')

    # --- PALMA ACEITERA ---
    palma_tipo = fields.Selection([
        ('dura', 'Dura'),
        ('pisifera', 'Pisífera'),
        ('tenera', 'Tenera (D x P)'),
    ], string='[Palma] Tipo')
    palma_produccion_rff = fields.Float(
        string='[Palma] Producción RFF (tons/ha/año)',
        help='Toneladas de Racimos de Fruta Fresca por hectárea/año'
    )
    palma_extraccion_aceite = fields.Float(
        string='[Palma] Extracción Aceite (%)',
        help='Porcentaje típico de extracción de aceite'
    )
    palma_altura_tronco = fields.Float(
        string='[Palma] Crecimiento Tronco (cm/año)',
        help='Crecimiento anual del tronco'
    )
    palma_resistencia_pc = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Palma] Resistencia a PC',
        help='Resistencia a Pudrición del Cogollo')

    # --- CAÑA DE AZÚCAR ---
    cana_contenido_sacarosa = fields.Float(
        string='[Caña] Sacarosa (%)',
        help='Contenido típico de sacarosa'
    )
    cana_contenido_fibra = fields.Float(
        string='[Caña] Fibra (%)',
        help='Contenido típico de fibra'
    )
    cana_maduracion = fields.Selection([
        ('temprana', 'Temprana'),
        ('media', 'Media'),
        ('tardia', 'Tardía'),
    ], string='[Caña] Maduración')
    cana_floracion = fields.Selection([
        ('nula', 'Nula/Muy baja'),
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ], string='[Caña] Tendencia a Floración')
    cana_tch_tipico = fields.Float(
        string='[Caña] TCH Típico',
        help='Toneladas de caña por hectárea típico'
    )
    cana_resistencia_carbon = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Caña] Resistencia a Carbón')
    cana_resistencia_roya = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('susceptible', 'Susceptible'),
    ], string='[Caña] Resistencia a Roya')

    # Imagen de la variedad
    image = fields.Binary(string='Imagen', attachment=True)

    # Descripción
    description = fields.Text(string='Descripción')
    notas = fields.Text(string='Notas Técnicas')

    _sql_constraints = [
        ('codigo_cultivo_unique', 'UNIQUE(codigo, cultivo_id)',
         'El código de variedad debe ser único por cultivo'),
    ]


class Fenologia(models.Model):
    """
    Etapas fenológicas por cultivo.
    Define las fases de desarrollo del cultivo para seguimiento.
    """
    _name = 'fincas_pma.fenologia'
    _description = 'Etapas Fenológicas del Cultivo'
    _order = 'cultivo_id, secuencia'

    name = fields.Char(
        string='Nombre de la Etapa',
        required=True,
        help='Nombre de la etapa fenológica'
    )
    codigo = fields.Char(string='Código', index=True)
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        required=True,
        ondelete='cascade'
    )
    secuencia = fields.Integer(
        string='Secuencia',
        default=10,
        help='Orden de la etapa en el ciclo'
    )

    # Duración
    dias_inicio = fields.Integer(
        string='Día Inicio',
        help='Día de inicio desde siembra/evento base'
    )
    dias_fin = fields.Integer(
        string='Día Fin',
        help='Día de finalización desde siembra/evento base'
    )
    duracion_dias = fields.Integer(
        string='Duración (días)',
        compute='_compute_duracion',
        store=True
    )

    # Características de la etapa
    descripcion = fields.Text(string='Descripción')
    indicadores_visuales = fields.Text(
        string='Indicadores Visuales',
        help='Características visibles para identificar la etapa'
    )
    labores_recomendadas = fields.Text(
        string='Labores Recomendadas',
        help='Actividades agrícolas recomendadas en esta etapa'
    )

    # Requerimientos hídricos y nutricionales
    requerimiento_agua = fields.Selection([
        ('critico', 'Crítico (Alta demanda)'),
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    ], string='Requerimiento de Agua')

    requerimiento_nutrientes = fields.Selection([
        ('critico', 'Crítico (Alta demanda)'),
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    ], string='Requerimiento Nutricional')

    # Susceptibilidad a plagas/enfermedades
    susceptibilidad_plagas = fields.Selection([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ], string='Susceptibilidad a Plagas')

    plagas_comunes = fields.Text(
        string='Plagas Comunes',
        help='Plagas frecuentes en esta etapa'
    )

    color = fields.Char(
        string='Color',
        default='#3498db',
        help='Color para visualización en Gantt/Timeline'
    )

    @api.depends('dias_inicio', 'dias_fin')
    def _compute_duracion(self):
        for record in self:
            if record.dias_fin and record.dias_inicio:
                record.duracion_dias = record.dias_fin - record.dias_inicio
            else:
                record.duracion_dias = 0


class ParametroCalidad(models.Model):
    """
    Parámetros de calidad específicos por cultivo.
    Define los KPIs de calidad que se medirán en la cosecha.
    """
    _name = 'fincas_pma.parametro_calidad'
    _description = 'Parámetros de Calidad por Cultivo'
    _order = 'cultivo_id, secuencia'

    name = fields.Char(
        string='Nombre del Parámetro',
        required=True,
        help='Nombre del parámetro de calidad'
    )
    codigo = fields.Char(string='Código', index=True)
    cultivo_id = fields.Many2one(
        'fincas_pma.cultivo',
        string='Cultivo',
        required=True,
        ondelete='cascade'
    )
    secuencia = fields.Integer(string='Secuencia', default=10)

    # Tipo y unidad
    tipo_dato = fields.Selection([
        ('float', 'Numérico Decimal'),
        ('integer', 'Numérico Entero'),
        ('percentage', 'Porcentaje'),
        ('selection', 'Selección'),
        ('boolean', 'Sí/No'),
    ], string='Tipo de Dato', required=True, default='float')

    unidad = fields.Char(
        string='Unidad',
        help='Unidad de medida (%, °Brix, mm, etc.)'
    )

    # Rangos de aceptación
    valor_minimo = fields.Float(string='Valor Mínimo Aceptable')
    valor_optimo_min = fields.Float(string='Valor Óptimo Mín')
    valor_optimo_max = fields.Float(string='Valor Óptimo Máx')
    valor_maximo = fields.Float(string='Valor Máximo Aceptable')

    # Opciones para tipo selección
    opciones_seleccion = fields.Text(
        string='Opciones (Selección)',
        help='Opciones separadas por coma para tipo selección'
    )

    # Importancia
    es_critico = fields.Boolean(
        string='Es Crítico',
        help='Indica si este parámetro es crítico para la calidad'
    )
    peso_calidad = fields.Float(
        string='Peso en Calidad (%)',
        default=10.0,
        help='Peso porcentual en el cálculo de calidad general'
    )

    # Método de medición
    metodo_medicion = fields.Text(
        string='Método de Medición',
        help='Protocolo para medir este parámetro'
    )
    equipo_requerido = fields.Char(
        string='Equipo Requerido',
        help='Equipo necesario para la medición'
    )

    descripcion = fields.Text(string='Descripción')

    _sql_constraints = [
        ('codigo_cultivo_unique', 'UNIQUE(codigo, cultivo_id)',
         'El código del parámetro debe ser único por cultivo'),
    ]
