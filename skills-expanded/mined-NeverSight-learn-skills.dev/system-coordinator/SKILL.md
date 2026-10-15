---
name: system-coordinator
description: Mantiene la integridad y coherencia del sistema Brain OS v2.0. Ejecuta auditorías técnicas, valida alineación con Flujo Maestro v2, gestiona riesgos, genera reportes con puntuación, y sincroniza componentes. Usar cuando se diga "Verifica el sistema", "Auditoría completa", "Reconciliar diferencias", o después de cambios significativos.
trigger_conditions:
  - "Verifica el sistema"
  - "Auditoría completa"
  - "Reconciliar diferencias"
  - "Buenos días (activación matutina)"
  - "Estado del sistema Brain OS"
  - "Después de cambios significativos en la arquitectura"
usage_constraints: "No usar para tareas de usuario (estudio, escritura, investigación). Solo para operaciones de mantenimiento, auditoría y coordinación interna del sistema Brain OS."
category: "Sistema"
parameters:
  mode: "Tipo de verificación: quick | full | reconcile (default: quick)"
---

# 🔗 System Coordinator v2.0

> Cerebro operativo de Brain OS. Garantiza que todos los componentes funcionen como un sistema cohesivo.

## Cuándo Se Activa

| Trigger | Comando |
|---------|---------|
| Verificación estándar | "Verifica el sistema" |
| Auditoría completa + Flujo v2 | "Verifica el sistema completo" |
| Check rápido (Modo Crisis) | "Verifica conexiones críticas" |
| Análisis semanal | "Auditoría de uso semanal" |
| Sync bidireccional | "Reconciliar diferencias" |
| Automático | Después de instalar skills, agregar cursos, o cambios en config |

---

## Arquitectura del Sistema

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Aula Virtual│────▶│  Brain OS   │◀───▶│   Notion    │
│   (Moodle)  │     │  (Central)  │     │ BD_TAREAS   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │NotebookLM│ │ Pomodoro │ │ Skills   │
       │ (7+books)│ │  Timer   │ │  (30)    │
       └──────────┘ └──────────┘ └──────────┘
```

### Componentes Monitoreados

| Componente | Archivos Clave | Qué Verificar |
|------------|---------------|---------------|
| Config | `brain_config.md` | IDs, cronotipo, semestre, cursos |
| Dashboard | `INICIO.md` | Conteos, timestamps, secciones Flujo v2 |
| Pomodoro | `tools/pomodoro/config.json` | Modos, Active Recall, Notion sync |
| NotebookLM | `config/notebooklm_registry.json` | Notebooks ↔ cursos ↔ IDs |
| Aula Virtual | `skills/aula-virtual/` | Scripts, pending sync, token |
| Workflows | `.agent/workflows/*.md` | Buenos días, brain-os-study |
| Flujo Maestro | `Flujo_Maestro_BrainOS_v2.md` | Fases, modos, protocolos |
| Hemingway Bridge | `config/hemingway_bridge.json` | Último hilo, fecha |
| Backups | `backups/` | JSONs de BD_TAREAS, frescura |
| Sync Status | `config/sync_status.json` | Timestamps de último sync |
| **Semantic Memory** | `config/semantic_memory.json` | Gists presentes, último entry < 7 días 🆕 |
| **Memory Governance** | `brain_config.md → MEMORY_GOVERNANCE` | Parámetros activos y valores válidos 🆕 |

---

## Flujo de Ejecución por Comando

### 1. "Verifica el sistema" (Estándar)

```
PASO 1 → Leer brain_config.md
PASO 2 → Escanear skills/ → Contar (actual: 29)
PASO 3 → Verificar IDs Notion cruzados (config ↔ registry ↔ workflows)
PASO 4 → Verificar Pomodoro (config.json → modos, Active Recall)
PASO 5 → Verificar INICIO.md (conteos, timestamps, secciones)
PASO 6 → Reportar con formato estándar
```

**Formato de reporte estándar:**

```markdown
## ✅ Verificación del Sistema — [FECHA]

| Componente | Estado | Detalle |
|------------|:------:|---------|
| Notion IDs | 🟢/🟡/🔴 | ... |
| Skills | 🟢/🟡/🔴 | X directorios |
| Pomodoro | 🟢/🟡/🔴 | X modos |
| Dashboard | 🟢/🟡/🔴 | Timestamp: ... |
| NotebookLM | 🟢/🟡/🔴 | X notebooks |
```

### 2. "Verifica el sistema completo" (Auditoría + Flujo v2)

Ejecuta **todos los pasos del comando estándar** más:

```
PASO 7  → Validar Fase BOOT
          - ¿Workflow buenos-dias.md existe y es coherente?
          - ¿Comando "Buenos días" en INICIO.md?
          - ¿Hemingway Bridge tiene persistencia? (config/hemingway_bridge.json)

PASO 8  → Validar Fase EJECUCIÓN
          - ¿Selector de 6 modos documentado en INICIO.md?
          - ¿5 modos Pomodoro en config.json? (default, intensive, light, exam_prep, ultradian)
          - ¿Active Recall habilitado? (questions_per_session, bloom_levels)
          - ¿Ventanas Bear correctas? (brain_config.md → cronobiología)

PASO 9  → Validar Fase CIERRE
          - ¿Sección Hemingway Bridge en INICIO.md?
          - ¿Comando "Mañana sigo por [X]" documentado?
          - ¿Directorio sesiones/ con logs?

PASO 10 → Auditar Gestión de Riesgos
          - ¿Existen backups JSON en backups/?
          - ¿Config/sync_status.json presente? → indicador de frescura
          - ¿Scripts de sync tienen manejo de errores offline?

PASO 11 → Verificar Skills Extendidas (16 core)
          system-coordinator, dashboard-sync, aula-virtual, notebooklm,
          pomodoro, library-manager, research-engineer, doc-coauthoring,
          copy-editing, brainstorming, plan-writing, cleanup-manager,
          elite-skill-architect, architecture, skill-creator, pdf,
          autonomous-agent-patterns, agent-memory-systems, skill-orchestrator


PASO 12 → Generar Reporte de 5 Secciones con Puntuación /30
```

**Formato de reporte completo (6 secciones):**

```markdown
# 🔍 AUDITORÍA INTEGRAL — Brain OS v2.0
> Fecha: [FECHA] | Ejecutada por: system-coordinator

## 1. Verificación Técnica
[Tabla de IDs, conexiones, estructura, Pomodoro, Dashboard]

## 2. Alineación con Flujo Maestro v2.0
[3 fases: BOOT, EJECUCIÓN, CIERRE — cada componente con 🟢/🟡/🔴]
[Gestión de riesgos + Skills 11/11]

## 3. Brechas Críticas (Priorizadas)
[Tabla: #, Brecha, Impacto, Prioridad 🔴/🟡/⚪]

## 4. Plan de Acción (3-5 pasos)
[Pasos concretos y accionables]

## 5. Puntuación General
| Categoría       | Máx | Obtenido |
|-----------------|:---:|:--------:|
| Salud Técnica   |  10 |    X     |
| Alineación v2   |  10 |    X     |
| Completitud     |  10 |    X     |
| **TOTAL**       |  30 |   XX     |

## 6. Higiene del Sistema 🧹
| Métrica | Valor | Estado |
|---------|:-----:|:------:|
| __pycache__ | XX dirs (XX MB) | 🟢/🟡/🔴 |
| Archivos temporales | XX | 🟢/🟡/🔴 |
| Browser cache | XX MB | 🟢/🟡/🔴 |
| Última limpieza | FECHA | 🟢/🟡/🔴 |
| Espacio recuperable | XX MB | — |

Criterios: <10MB → 🟢 | 10-50MB → 🟡 | >50MB → 🔴
💡 Ejecutar: python skills/cleanup-manager/scripts/cleanup.py --scan
```

### 3. "Verifica conexiones críticas" (Modo Crisis — Rápido)

Para cuando hay poco tiempo. Solo verifica lo esencial:

```
PASO 1 → Notion API: GET /v1/users/me → ¿Responde?
PASO 2 → BD_TAREAS: Query → ¿Hay tareas pendientes?
PASO 3 → Pomodoro: state.json → ¿Timer idle o activo?
PASO 4 → Reportar en 3 líneas
```

**Formato:**
```
✅ Notion: Conectado (bot: Prueba_Integracion)
✅ Tareas: X pendientes
✅ Pomodoro: idle/activo (modo: X)
```

### 4. "Auditoría de uso semanal"

Analiza logs y sesiones de la semana:

```
PASO 1 → Leer sesiones/ del período (últimos 7 días)
PASO 2 → Leer Pomodoro history.json → Contar sesiones/modos/temas
PASO 3 → Verificar Hemingway Bridges registrados
PASO 4 → Calcular métricas:
          - Sesiones totales
          - Horas de estudio estimadas
          - Modo más usado
          - Curso más trabajado
          - Bridges completados vs días
PASO 5 → Leer cleanup_history.json → Stats de limpieza:
          - Operaciones de limpieza esta semana
          - Espacio recuperado (MB)
          - Tendencia: 📉/📈 vs semana anterior
          - Archivos en cleanup_archive/ pendientes de purga
PASO 6 → Generar reporte semanal con recomendaciones
```

### 5. "Reconciliar diferencias"

Sync bidireccional Notion ↔ Local:

```
PASO 1 → Leer BD_TAREAS de Notion (query MCP)
PASO 2 → Leer backups/tareas_latest.json (local)
PASO 3 → Comparar: ¿Hay tareas en Notion que no están en local? ¿Vice versa?
PASO 4 → Leer BD_RECURSOS de Notion
PASO 5 → Comparar con archivos locales en carpetas de cursos
PASO 6 → Reportar diferencias con acción sugerida (sincronizar / ignorar / alertar)
```

---

## Reglas de Puntuación (0-30)

### Salud Técnica (0-10)

| Puntos | Criterio |
|:------:|----------|
| +2 | Notion API responde correctamente |
| +2 | Todos los IDs cruzados coinciden (config ↔ registry ↔ workflows) |
| +2 | Estructura de carpetas completa (7 cursos + sesiones + config) |
| +2 | Pomodoro config válido (5 modos + Active Recall) |
| +1 | Dashboard actualizado (timestamp < 24h) |
| +1 | History.json con sesiones recientes (< 7 días) |

### Alineación Flujo v2 (0-10)

| Puntos | Criterio |
|:------:|----------|
| +2 | Fase BOOT completa (workflow buenos-dias + 5 pasos) |
| +2 | Fase EJECUCIÓN (selector de modos + BRAC/Pomodoro + Active Recall) |
| +2 | Fase CIERRE (registro + Hemingway Bridge con persistencia) |
| +2 | Gestión de riesgos operativa (backups + offline + frescura) |
| +1 | Ventanas Bear documentadas y correctas |
| +1 | Flujo Maestro v2 visible en dashboard |

### Completitud Skills (0-10)

| Puntos | Criterio |
|:------:|----------|
| +1 cada | 11 skills core presentes y con SKILL.md válido |
| -1 cada | Skill referenciada en INICIO.md pero sin directorio |

---

## Archivos Obligatorios a Sincronizar

Al detectar cambios, el coordinator debe actualizar:

| Archivo | Qué Sincronizar |
|---------|-----------------|
| `INICIO.md` | Conteo skills, timestamps, Hemingway Bridge, tareas, estado |
| `README.md` | Conteo skills, integraciones |
| `brain_config.md` | IDs Notion, cursos, cronobiología |
| `config/notebooklm_registry.json` | Notebooks ↔ cursos |
| `tools/pomodoro/config.json` | Modos, Active Recall, Notion sync |
| `config/hemingway_bridge.json` | Último hilo dejado |
| `config/sync_status.json` | Timestamps de sincronización |

---

## Gestión de Riesgos

### Detección de Modo Offline

```
SI Notion API falla (timeout > 5s o error 4xx/5xx):
  → Mostrar: "⚠️ Modo offline detectado — trabajando con cache local"
  → Usar backups/tareas_latest.json como fuente de verdad temporal
  → Marcar sync_status.json → "offline_since": timestamp

SI Moodle no responde:
  → Mostrar: "⚠️ Aula Virtual sin conexión"
  → Continuar con datos locales de aula-virtual/scripts/downloaded_files.json
```

### Indicador de Frescura

```
config/sync_status.json:
{
  "notion_last_sync": "2026-02-12T23:37:00",
  "moodle_last_sync": "2026-02-12T05:15:00",
  "dashboard_last_sync": "2026-02-12T23:37:00",
  "backup_last_created": null,
  "offline_since": null
}

Reglas de frescura:
  < 4h  → 🟢 Datos frescos
  < 24h → 🟡 Datos recientes
  > 24h → 🔴 Datos obsoletos — recomendar sync
```

### Backups Automáticos

```
Al ejecutar "Buenos días" o "Verifica el sistema":
  1. Query BD_TAREAS → Guardar en backups/tareas_YYYY-MM-DD.json
  2. Actualizar backups/tareas_latest.json (symlink o copia)
  3. Retener últimos 7 backups, eliminar más antiguos
```

---

## Alertas Visuales

| Símbolo | Significado | Acción |
|:-------:|-------------|--------|
| 🟢 | Todo operativo | Ninguna |
| 🟡 | Funcional con advertencias | Revisar cuando sea posible |
| 🔴 | Falla crítica | Resolver antes de continuar |
| ⚪ | No verificado / no aplica | Informativo |
| ⏱️ | Indicador de frescura | Mostrar antigüedad de datos |

---

## Auto-Actualización

Esta skill se auto-actualiza cuando detecta cambios:

### Triggers de Auto-Update
- Nueva skill instalada → Actualizar conteo y categorías
- Nuevo curso agregado → Verificar IDs, carpeta, NotebookLM
- Cambio en brain_config.md → Re-validar todo
- Nuevo workflow creado → Registrar en arquitectura
- Cambio en Flujo Maestro → Re-validar alineación

### Última Auto-Actualización
- **Fecha**: 2026-03-14
- **Skills activas**: 32 (+ `skill-orchestrator` purgando skills falsas y añadiendo Flow Dinámico)
- **Skills archivadas**: 4 (`concise-planning`, `plan-writing`, `writing-plans`, `skill-creator`)
- **Descriptions**: 100% en español (19 skills traducidas)
- **Skills Elite (≥90)**: `cleanup-manager`, `system-coordinator`, `elite-skill-architect`
- **Herramientas**: pomodoro/
- **Integraciones**: Notion, NotebookLM, Aula Virtual, Pomodoro Timer, Flujo Maestro v2
- **Estado**: ✅ Post-mejora integral — Partes 1-4 completadas

---

## Troubleshooting

| Problema | Diagnóstico | Solución |
|----------|------------|----------|
| Skills count no coincide | `ls skills/ \| wc -l` | Actualizar INICIO.md y README.md |
| Notion IDs desincronizados | Comparar brain_config ↔ registry | Corregir fuente de verdad (brain_config) |
| Pomodoro no registra | Verificar state.json y history.json | Resetear state.json a idle |
| Hemingway Bridge vacío | Verificar config/hemingway_bridge.json | Crear archivo si no existe |
| Dashboard obsoleto | Verificar timestamp en INICIO.md | Ejecutar dashboard-sync |
| Backups inexistentes | Verificar carpeta backups/ | Crear y ejecutar primer backup |
| Query Notion falla | Verificar formato UUID del database_id | Usar formato con guiones |
| Modo offline no detectado | Verificar sync_status.json | Crear archivo si no existe |

---

## 📋 Log de Auditoría

Cada verificación del sistema se registra en `config/audit_log.json`:

```json
{
  "audits": [
    {
      "date": "2026-02-26T23:35:00",
      "type": "full",
      "score": "24/30",
      "components": {
        "skills": "🟢 29 activas",
        "notion": "🟢 Conectado",
        "dashboard": "🟡 Desactualizado (>24h)",
        "pomodoro": "🟢 Operativo",
        "cleanup": "🟢 <10MB basura",
        "hemingway": "🟡 Vacío"
      },
      "actions_taken": ["dashboard-sync ejecutado"],
      "next_audit": "2026-03-05"
    }
  ]
}
```

> **Regla**: Cada `"Verifica el sistema"` genera una nueva entrada. Historial se preserva indefinidamente.

---

## 🧪 Escenarios de Prueba

### Test 1: Verificación completa — sistema sano

```
Input:    "Verifica el sistema completo"
Espera:   Tabla con 6 secciones, todos 🟢
Verifica: Score ≥27/30, cero 🔴
Output:   Tabla + "Sistema en estado óptimo ✅"
```

### Test 2: Verificación rápida — respuesta concisa

```
Input:    "Verifica conexiones críticas"
Espera:   Resumen en ≤3 líneas con estado de Notion + Skills + Dashboard
Verifica: Respuesta NO supera 5 líneas
Output:   "Notion: 🟢 | Skills: 29 activas 🟢 | Dashboard: 🟡 (>24h)"
```

### Test 3: Detección de modo offline

```
Input:    "Verifica el sistema" (con Notion no alcanzable)
Espera:   Detecta Notion offline, cambia a modo offline
Verifica: - Sección Notion muestra 🔴
          - Recomienda "Verificar token de Notion"
          - NO falla del todo — resto del sistema se verifica
Output:   Score reducido, nota de degradación graceful
```

### Test 4: Skills count desincronizado

```
Input:    INICIO.md dice "32 skills" pero hay 29 activas
Espera:   Detecta discrepancia en sección "Skills"
Verifica: Mensaje de divergencia explícito
Output:   "🟡 INICIO.md reporta 32, pero hay 29 activas → ejecutar dashboard-sync"
```

### Test 5: Hemingway Bridge vacío

```
Input:    "Verifica el sistema" (hemingway_bridge.json vacío o inexistente)
Espera:   Sección 5 muestra 🟡 o 🔴
Verifica: Sugiere ejecutar cierre diario
Output:   "🟡 Hemingway Bridge vacío → ejecutar 'Cierre diario' antes de terminar"
```

### Test 6: Auto-actualización post-cambio

```
Input:    Nueva skill instalada + "Verifica el sistema"
Espera:   Detecta nueva skill, actualiza conteo
Verifica: - "Última Auto-Actualización" se actualiza a fecha actual
          - Conteo de skills es correcto
Output:   "Auto-actualización: 29 → 30 skills detectadas"
```
