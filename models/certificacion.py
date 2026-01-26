# -*- coding: utf-8 -*-
"""
Gestión de Certificaciones de Sostenibilidad
=============================================
Manejo de certificaciones agrícolas internacionales.

Certificaciones soportadas:
- Rainforest Alliance / UTZ (fusionadas)
- GlobalG.A.P.
- Orgánico (USDA, EU, JAS)
- Fairtrade
- RSPO (Palma Sostenible)
- Bonsucro (Caña Sostenible)
- 4C (Café)
- C.A.F.E. Practices (Starbucks)
- Bird Friendly (Smithsonian)
"""

from odoo import models, fields, api
from datetime import date, timedelta


class TipoCertificacion(models.Model):
    """Tipos de certificaciones disponibles."""
    _name = 'fincas_pma.tipo_certificacion'
    _description = 'Tipo de Certificación'
    _order = 'secuencia, name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    secuencia = fields.Integer(string='Secuencia', default=10)
    active = fields.Boolean('Activo', default=True)

    descripcion = fields.Text(string='Descripción')
    sitio_web = fields.Char(string='Sitio Web')
    logo = fields.Binary(string='Logo', attachment=True)

    # Cultivos aplicables
    cultivo_ids = fields.Many2many(
        'fincas_pma.cultivo',
        'tipo_cert_cultivo_rel',
        'tipo_cert_id',
        'cultivo_id',
        string='Cultivos Aplicables'
    )

    # Características
    es_sostenibilidad = fields.Boolean(string='Es de Sostenibilidad')
    es_organico = fields.Boolean(string='Es Orgánico')
    es_comercio_justo = fields.Boolean(string='Es Comercio Justo')
    es_calidad = fields.Boolean(string='Es de Calidad')

    # Requisitos
    requiere_auditoria_anual = fields.Boolean(
        string='Requiere Auditoría Anual',
        default=True
    )
    vigencia_meses = fields.Integer(
        string='Vigencia (meses)',
        default=12
    )
    periodo_transicion_meses = fields.Integer(
        string='Período de Transición (meses)',
        help='Meses requeridos de transición para nuevas certificaciones'
    )

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código debe ser único'),
    ]


class Certificacion(models.Model):
    """
    Certificación otorgada a una finca o grupo de lotes.
    """
    _name = 'fincas_pma.certificacion'
    _description = 'Certificación'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_vencimiento'

    name = fields.Char(
        string='Nombre/Referencia',
        required=True,
        tracking=True
    )
    tipo_id = fields.Many2one(
        'fincas_pma.tipo_certificacion',
        string='Tipo de Certificación',
        required=True,
        tracking=True
    )
    codigo_tipo = fields.Char(
        related='tipo_id.codigo',
        store=True
    )
    active = fields.Boolean('Activo', default=True)

    # Alcance
    finca_id = fields.Many2one(
        'fincas_pma.fincas_pma',
        string='Finca',
        tracking=True
    )
    lote_ids = fields.Many2many(
        'fincas_pma.lote',
        'lote_certificacion_rel',
        'certificacion_id',
        'lote_id',
        string='Lotes Certificados'
    )
    area_certificada_ha = fields.Float(
        string='Área Certificada (ha)',
        digits=(10, 2)
    )

    # Número y organismo
    numero_certificado = fields.Char(
        string='Número de Certificado',
        tracking=True
    )
    certificador_id = fields.Many2one(
        'res.partner',
        string='Organismo Certificador',
        tracking=True
    )
    auditor = fields.Char(string='Auditor Principal')

    # Fechas
    fecha_solicitud = fields.Date(string='Fecha de Solicitud')
    fecha_auditoria = fields.Date(
        string='Fecha de Auditoría',
        tracking=True
    )
    fecha_emision = fields.Date(
        string='Fecha de Emisión',
        tracking=True
    )
    fecha_vencimiento = fields.Date(
        string='Fecha de Vencimiento',
        tracking=True
    )
    dias_para_vencer = fields.Integer(
        string='Días para Vencer',
        compute='_compute_dias_para_vencer'
    )

    # Estado
    estado = fields.Selection([
        ('solicitada', 'Solicitada'),
        ('en_proceso', 'En Proceso de Auditoría'),
        ('aprobada', 'Aprobada/Vigente'),
        ('condicionada', 'Aprobada con Condiciones'),
        ('suspendida', 'Suspendida'),
        ('vencida', 'Vencida'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='solicitada', tracking=True, required=True)

    estado_semaforo = fields.Selection([
        ('verde', 'Verde (OK)'),
        ('amarillo', 'Amarillo (Por Vencer)'),
        ('rojo', 'Rojo (Vencida/Problema)'),
    ], string='Semáforo', compute='_compute_estado_semaforo')

    # Resultados de auditoría
    puntaje_auditoria = fields.Float(
        string='Puntaje de Auditoría',
        digits=(5, 2)
    )
    nivel_certificacion = fields.Selection([
        ('oro', 'Oro/Platinum'),
        ('plata', 'Plata'),
        ('bronce', 'Bronce'),
        ('basico', 'Básico'),
    ], string='Nivel de Certificación')

    # No conformidades
    no_conformidad_ids = fields.One2many(
        'fincas_pma.no_conformidad',
        'certificacion_id',
        string='No Conformidades'
    )
    total_nc_mayores = fields.Integer(
        string='NC Mayores',
        compute='_compute_no_conformidades'
    )
    total_nc_menores = fields.Integer(
        string='NC Menores',
        compute='_compute_no_conformidades'
    )
    nc_pendientes = fields.Integer(
        string='NC Pendientes',
        compute='_compute_no_conformidades'
    )

    # Auditorías
    auditoria_ids = fields.One2many(
        'fincas_pma.auditoria',
        'certificacion_id',
        string='Historial de Auditorías'
    )

    # Documentos
    certificado_pdf = fields.Binary(
        string='Certificado PDF',
        attachment=True
    )
    certificado_nombre = fields.Char(string='Nombre Certificado')

    # Costos
    costo_certificacion = fields.Float(
        string='Costo de Certificación',
        digits=(10, 2)
    )
    costo_auditoria = fields.Float(
        string='Costo de Auditoría',
        digits=(10, 2)
    )

    notas = fields.Text(string='Notas')

    def _compute_dias_para_vencer(self):
        today = date.today()
        for record in self:
            if record.fecha_vencimiento:
                delta = record.fecha_vencimiento - today
                record.dias_para_vencer = delta.days
            else:
                record.dias_para_vencer = 0

    def _compute_estado_semaforo(self):
        for record in self:
            if record.estado in ['vencida', 'suspendida', 'rechazada']:
                record.estado_semaforo = 'rojo'
            elif record.estado == 'aprobada':
                if record.dias_para_vencer <= 30:
                    record.estado_semaforo = 'amarillo'
                elif record.dias_para_vencer <= 0:
                    record.estado_semaforo = 'rojo'
                else:
                    record.estado_semaforo = 'verde'
            elif record.estado == 'condicionada':
                record.estado_semaforo = 'amarillo'
            else:
                record.estado_semaforo = 'verde'

    @api.depends('no_conformidad_ids.tipo', 'no_conformidad_ids.estado')
    def _compute_no_conformidades(self):
        for record in self:
            nc = record.no_conformidad_ids
            record.total_nc_mayores = len(nc.filtered(lambda n: n.tipo == 'mayor'))
            record.total_nc_menores = len(nc.filtered(lambda n: n.tipo == 'menor'))
            record.nc_pendientes = len(nc.filtered(
                lambda n: n.estado not in ['cerrada', 'verificada']
            ))

    @api.model
    def _cron_verificar_vencimientos(self):
        """Cron job para verificar certificaciones próximas a vencer"""
        fecha_limite = date.today() + timedelta(days=60)
        certificaciones = self.search([
            ('estado', '=', 'aprobada'),
            ('fecha_vencimiento', '<=', fecha_limite),
            ('fecha_vencimiento', '>=', date.today()),
        ])
        for cert in certificaciones:
            # Crear actividad de recordatorio
            cert.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=cert.fecha_vencimiento - timedelta(days=30),
                summary=f'Renovar certificación {cert.name}',
                note=f'La certificación {cert.name} vence el {cert.fecha_vencimiento}'
            )


class Auditoria(models.Model):
    """
    Registro de auditorías de certificación.
    """
    _name = 'fincas_pma.auditoria'
    _description = 'Auditoría de Certificación'
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
    )
    certificacion_id = fields.Many2one(
        'fincas_pma.certificacion',
        string='Certificación',
        required=True,
        ondelete='cascade'
    )
    tipo_certificacion = fields.Many2one(
        'fincas_pma.tipo_certificacion',
        related='certificacion_id.tipo_id',
        store=True
    )

    # Tipo de auditoría
    tipo = fields.Selection([
        ('inicial', 'Inicial'),
        ('seguimiento', 'Seguimiento'),
        ('renovacion', 'Renovación'),
        ('no_anunciada', 'No Anunciada'),
        ('especial', 'Especial'),
    ], string='Tipo de Auditoría', required=True)

    # Fechas
    fecha = fields.Date(
        string='Fecha de Auditoría',
        required=True
    )
    fecha_inicio = fields.Datetime(string='Inicio')
    fecha_fin = fields.Datetime(string='Fin')
    duracion_dias = fields.Float(string='Duración (días)')

    # Equipo auditor
    certificador_id = fields.Many2one(
        'res.partner',
        string='Organismo Certificador'
    )
    auditor_lider = fields.Char(string='Auditor Líder')
    equipo_auditor = fields.Text(string='Equipo Auditor')

    # Alcance
    lotes_auditados = fields.Many2many(
        'fincas_pma.lote',
        'auditoria_lote_rel',
        'auditoria_id',
        'lote_id',
        string='Lotes Auditados'
    )
    areas_evaluadas = fields.Text(string='Áreas/Criterios Evaluados')

    # Resultados
    resultado = fields.Selection([
        ('aprobada', 'Aprobada'),
        ('aprobada_condiciones', 'Aprobada con Condiciones'),
        ('rechazada', 'Rechazada'),
        ('pendiente', 'Pendiente de Decisión'),
    ], string='Resultado', tracking=True)

    puntaje = fields.Float(
        string='Puntaje Obtenido',
        digits=(5, 2)
    )
    puntaje_maximo = fields.Float(
        string='Puntaje Máximo',
        digits=(5, 2)
    )
    porcentaje_cumplimiento = fields.Float(
        string='% Cumplimiento',
        compute='_compute_porcentaje',
        digits=(5, 2)
    )

    # No conformidades encontradas
    no_conformidad_ids = fields.One2many(
        'fincas_pma.no_conformidad',
        'auditoria_id',
        string='No Conformidades'
    )
    total_nc = fields.Integer(
        string='Total NC',
        compute='_compute_total_nc'
    )

    # Fortalezas y oportunidades
    fortalezas = fields.Text(string='Fortalezas Identificadas')
    oportunidades_mejora = fields.Text(string='Oportunidades de Mejora')
    observaciones = fields.Text(string='Observaciones del Auditor')

    # Documentos
    informe_pdf = fields.Binary(
        string='Informe de Auditoría',
        attachment=True
    )
    informe_nombre = fields.Char(string='Nombre del Informe')
    checklist_pdf = fields.Binary(
        string='Checklist Completado',
        attachment=True
    )

    # Próxima auditoría
    fecha_proxima_auditoria = fields.Date(string='Próxima Auditoría')

    @api.depends('certificacion_id', 'fecha', 'tipo')
    def _compute_name(self):
        for record in self:
            if record.certificacion_id and record.fecha:
                tipo_corto = dict(record._fields['tipo'].selection).get(record.tipo, '')[:3].upper()
                record.name = f"AUD-{record.certificacion_id.name}-{tipo_corto}-{record.fecha}"
            else:
                record.name = 'Nueva Auditoría'

    @api.depends('puntaje', 'puntaje_maximo')
    def _compute_porcentaje(self):
        for record in self:
            if record.puntaje_maximo:
                record.porcentaje_cumplimiento = (
                    record.puntaje / record.puntaje_maximo * 100
                )
            else:
                record.porcentaje_cumplimiento = 0

    @api.depends('no_conformidad_ids')
    def _compute_total_nc(self):
        for record in self:
            record.total_nc = len(record.no_conformidad_ids)


class NoConformidad(models.Model):
    """
    No conformidades detectadas en auditorías.
    """
    _name = 'fincas_pma.no_conformidad'
    _description = 'No Conformidad'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_deteccion desc'

    name = fields.Char(
        string='Código',
        required=True,
        copy=False,
        index=True
    )
    certificacion_id = fields.Many2one(
        'fincas_pma.certificacion',
        string='Certificación',
        required=True,
        ondelete='cascade'
    )
    auditoria_id = fields.Many2one(
        'fincas_pma.auditoria',
        string='Auditoría',
        ondelete='set null'
    )

    # Clasificación
    tipo = fields.Selection([
        ('mayor', 'Mayor'),
        ('menor', 'Menor'),
        ('observacion', 'Observación'),
    ], string='Tipo', required=True, tracking=True)

    categoria = fields.Selection([
        ('ambiental', 'Ambiental'),
        ('social', 'Social/Laboral'),
        ('calidad', 'Calidad'),
        ('trazabilidad', 'Trazabilidad'),
        ('documentacion', 'Documentación'),
        ('infraestructura', 'Infraestructura'),
        ('seguridad', 'Seguridad'),
        ('otro', 'Otro'),
    ], string='Categoría')

    criterio = fields.Char(
        string='Criterio/Requisito',
        help='Número del criterio o requisito incumplido'
    )

    # Descripción
    descripcion = fields.Text(
        string='Descripción del Hallazgo',
        required=True
    )
    evidencia = fields.Text(string='Evidencia')
    causa_raiz = fields.Text(string='Causa Raíz')

    # Fechas
    fecha_deteccion = fields.Date(
        string='Fecha de Detección',
        default=fields.Date.today
    )
    fecha_limite = fields.Date(
        string='Fecha Límite de Corrección',
        tracking=True
    )
    fecha_correccion = fields.Date(
        string='Fecha de Corrección',
        tracking=True
    )
    fecha_verificacion = fields.Date(
        string='Fecha de Verificación'
    )

    # Plan de acción
    accion_correctiva = fields.Text(
        string='Acción Correctiva',
        help='Acción para corregir la no conformidad'
    )
    accion_preventiva = fields.Text(
        string='Acción Preventiva',
        help='Acción para prevenir recurrencia'
    )
    responsable_id = fields.Many2one(
        'hr.employee',
        string='Responsable'
    )
    recursos_requeridos = fields.Text(string='Recursos Requeridos')

    # Verificación
    verificado_por = fields.Char(string='Verificado Por')
    evidencia_cierre = fields.Text(string='Evidencia de Cierre')

    # Estado
    estado = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('corregida', 'Corregida'),
        ('verificada', 'Verificada'),
        ('cerrada', 'Cerrada'),
    ], string='Estado', default='abierta', tracking=True, required=True)

    # Documentos
    documento_evidencia = fields.Binary(
        string='Documento de Evidencia',
        attachment=True
    )
    documento_nombre = fields.Char(string='Nombre del Documento')

    observaciones = fields.Text(string='Observaciones')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fincas_pma.no_conformidad') or 'NC-001'
        return super().create(vals)
