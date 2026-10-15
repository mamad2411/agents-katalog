---
name: planning-status
description: "Genera reporte de estado del proyecto: avance por fase/módulo, tareas completadas vs pendientes, bloqueantes, desvíos de cronograma, riesgos materializados, y decisiones pendientes. Lee del código, git log y issues/Jira. Actívala cuando el usuario diga 'estado del proyecto', 'status report', 'qué falta', 'qué sobra', 'avance', 'project health', 'cómo vamos'."
---

# Planning Status — Reporte de Estado

Una página. Lo que importa y nada más.

---

## Estructura del reporte

```markdown
# 📊 Status Report — [Proyecto]
> **Fecha:** [YYYY-MM-DD] | **Período:** [sprint/fase actual]

---

## 🟢🟡🔴 Salud General: [Verde / Amarillo / Rojo]

[Razón en 1 línea. Ej: "Amarillo: 1 semana de atraso por bloqueante en API de pagos."]

---

## 📈 Avance

| Fase/Módulo | % Completado | Entregables terminados | Pendiente |
|-------------|-------------|----------------------|-----------|
| Auth | 100% | Login, registro, JWT | — |
| Órdenes | 70% | Crear, listar órdenes | Cancelar, filtros |
| Pagos | 30% | Integración iniciada | Flujo completo, reembolsos |
| Notificaciones | 0% | — | Email transaccional |

**Total proyecto:** 55% completado

---

## ✅ Completado este período

- Endpoint POST /api/orders con validación (PR #42)
- Pantalla de creación de orden (PR #45)
- Índice para búsqueda de órdenes por fecha (migración #12)

---

## 🔄 En progreso

| Qué | Quién | Bloqueado? |
|-----|-------|-----------|
| Integración Stripe | Ana | ⚠️ Sí — esperando credenciales sandbox |
| Listado de órdenes con paginación | Carlos | No |
| Diseño de email transaccional | Diseño (externo) | No |
| Endpoint GET /api/orders?status=X | Backend | No |

---

## 🚫 Bloqueantes

| # | Bloqueante | Impacto | Acción | Dueño |
|---|-----------|---------|--------|-------|
| 1 | Sin credenciales sandbox Stripe | Detiene módulo de pagos | Solicitar a finanzas, ETA 2 días | Ana |
| 2 | Endpoint del banco devuelve 503 intermitente | Pruebas de pago inconsistentes | Escalar al proveedor, ticket #887 | Carlos |

---

## ⚠️ Desvíos

| Hito | Fecha original | Nueva fecha | Desvío | Razón |
|------|---------------|-------------|--------|-------|
| Demo MVP | 15/jul | 22/jul | +1 semana | Bloqueante Stripe + ausencia Carlos 3 días |
| Release Beta | 01/ago | 01/ago | Sin cambio | — |

---

## 🔴 Riesgos materializados

| Riesgo | Impacto real | Mitigación aplicada |
|--------|-------------|-------------------|
| API del banco sin sandbox (identificado en planning) | 3 días de atraso en pagos | Mock temporal para avanzar frontend |

---

## 🧠 Decisiones pendientes

- [ ] ¿Soporte multi-moneda en MVP o post-MVP? — PO debe decidir (sin decisión desde 10/jun)
- [ ] ¿Proveedor de email (SendGrid vs Resend)? — Tech Lead investigando

---

## 📊 Burndown / Avance del sprint

```
Sprint actual: 15/20 story points completados (75%)
Días restantes: 3

[████████░░] 75%
```

---

## 🔜 Próximo período (qué se hará)

1. Terminar integración Stripe (si se libera el bloqueante)
2. Completar cancelación de órdenes (backend + frontend)
3. Iniciar envío de emails transaccionales
4. Demo al sponsor (viernes 22/jul)

---
```

---

## Cómo obtener los datos

### Del código
```bash
# Archivos creados/modificados en el último sprint
git diff --stat $(git tag --sort=-v:refname | head -1)..HEAD

# Endpoints implementados
rg "Map(Get|Post|Put|Delete)" src/  # .NET
rg "router\.(get|post|put|delete)" src/  # Express
rg "@router\.(get|post|put|delete)" src/  # FastAPI
```

### De issues (si hay Jira)
Usar `search_jira_issues` con JQL:
```
project = PROJ AND sprint in openSprints()
project = PROJ AND status = "In Progress"
project = PROJ AND status = Blocked
```

### Del git log reciente
```bash
git log --oneline --since="2 weeks ago" --no-merges
```

---

## Workflow

1. **Detecta el stack** automáticamente (lee `package.json`, `*.csproj`, `pyproject.toml`, etc.)
2. **Escanea el código** para determinar qué está implementado:
   - Endpoints/Routes existentes (qué módulos tienen código real, no stubs)
   - Migraciones de BD aplicadas
   - Archivos con contenido significativo (>20 líneas, no solo placeholders)
3. **Revisa git log** del período relevante (último sprint, últimas 2 semanas, desde último tag)
4. **Si hay acceso a Jira**, consulta issues del sprint actual
5. **Genera el reporte** con todas las secciones.
6. **Marca gaps** donde no hay datos suficientes: `[Sin datos — no se encontró X]`

---

## Diagnóstico automático

La skill infiere "qué falta" y "qué sobra" automáticamente:

### Qué falta
- **Endpoints definidos en spec pero sin implementar en código** (si hay spec disponible)
- **Migraciones no aplicadas** (`dotnet ef migrations list` vs BD actual)
- **Issues en "To Do" del sprint actual**
- **Archivos stub** (menos de 20 líneas, puros placeholders)

### Qué sobra
- **Endpoints huérfanos** (implementados pero no referenciados en spec/sin ruta mapeada)
- **Archivos sin imports entrantes** (no usados por nadie)
- **Código comentado grande** (>5 líneas)
- **Issues en sprint sin actividad en 2+ semanas** (probablemente mal priorizados o innecesarios)

---

## Lo que NO debe hacer

- No requiere acceso a Jira. Si no hay, trabaja solo con git y código.
- No inventar porcentajes. Si no puedes medir avance real de un módulo, escribe "Sin estimar" en vez de un número falso.
- No generar reporte de más de 1 página. Si el proyecto es grande, una sección por módulo con 1-2 líneas cada una.
- No reemplazar la daily. Este reporte es para stakeholders, no para el equipo.
