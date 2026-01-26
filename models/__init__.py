# -*- coding: utf-8 -*-
"""
Fincas PMA - Gestión de Fincas Agrícolas Multi-Cultivo
======================================================
Módulo completo para gestión de fincas agrícolas en Panamá,
Centro América y Colombia.

Cultivos soportados:
- Café
- Banano
- Piña
- Palma Aceitera
- Caña de Azúcar
- Otros cultivos tropicales
"""

# Modelos base existentes
from . import models
from . import proyectos
from . import labores
from . import calendario
from . import equiposymq
from . import tipo_activo
from . import tipo_equipo
from . import marca
from . import empleados
from . import tipo_cultivo

# ========================================
# NUEVOS MODELOS MULTI-CULTIVO
# ========================================

# Catálogo de cultivos y variedades
from . import cultivo

# Lotes de producción (separado de project.project)
from . import lote

# Gestión de insumos y aplicaciones
from . import insumo

# Ciclos de producción y cosechas
from . import cosecha

# Sanidad vegetal (plagas, monitoreo, tratamientos)
from . import sanidad

# Certificaciones de sostenibilidad
from . import certificacion

# Labores agrícolas por lote
from . import labor_lote
