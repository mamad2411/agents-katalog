---
name: odoo-ai
description: Hub central Odoo-AI — ORM, modelos, vistas, seguridad, testing, E2E. Enterprise First. Auto-detección de versión y workspace. Sin dependencia de plugins externos.
license: Apache-2.0
metadata:
  author: Geraldow
  org: Alesco-Peru
  version: "3.0"
  last-updated: "2026-05-23"
---

## PASO 0 — OBLIGATORIO: Leer RULES.md

**Antes de cualquier otra acción**, leer:
`~/.claude/skills/odoo-ai/RULES.md`

Este archivo contiene las reglas de desarrollo propias de Alesco Perú que gobiernan TODO el trabajo Odoo. Las reglas viven en `RULES.md` — no en plugins externos.

---

## Principio Arquitectónico: Enterprise First

**Orden de búsqueda en TODO el ecosistema** (MUST respetar siempre):

```
1. Enterprise source local:  `{EnterprisePath — ver config.local.yaml / $cfg.EnterprisePath}`
2. Community source local:   `{CommunityPath}\{version} — ver config.local.yaml / $cfg.CommunityPath`
3. Proyectos v18:            `{ProjectsRoot}\18\ — ver config.local.yaml / $cfg.ProjectsRoot`
4. Proyectos v19:            `{ProjectsRoot}\19\ — ver config.local.yaml / $cfg.ProjectsRoot`
5. Docker (running):         localhost:18069
```

- Búsquedas de API/método/campo → `Grep $cfg.EnterprisePath (Enterprise First)`
- Si hay resultado en Enterprise → usar ese, NO buscar en Community
- Si NO hay resultado en Enterprise → buscar en Community y marcar `📦 Community`
- **Nunca asumir el formato de una API — siempre verificar contra source real**

---

## Detección de Modo Workspace

Antes de ejecutar cualquier script, detectar el modo por el directorio de trabajo (cwd):

### Modo B — Proyecto Independiente
**Condición**: `__manifest__.py` existe a profundidad ≤ 1 desde cwd.
**Ejemplo**: cwd = `{ProjectsRoot}\18\conservial\`
**Acción**: Ejecutar scripts inmediatamente en paralelo (ver Inicialización abajo).

### Modo A — Workspace Raíz (multi-proyecto)
**Condición**: `__manifest__.py` NO existe a profundidad ≤ 1, pero SÍ existe a profundidad 2–3.
**Ejemplo**: cwd = `{ProjectsRoot}\18\` (contiene aeca\, intiflow\, conservial\...)
**Acción**: Resolver proyecto activo PRIMERO, luego ejecutar scripts con `-Path {proyecto}/{módulo}`.

**Resolución del proyecto activo** (prioridad):
1. Archivo abierto en editor → inferir proyecto desde la ruta del archivo
2. `git -C {subdir} branch --show-current` por subcarpeta → el que tiene actividad reciente
3. Declaración explícita del usuario ("trabaja en intiflow")
4. Pregunta explícita: "Detecté los proyectos: {lista}. ¿Cuál está activo?"

**Distinción crítica**:
- `project` = nombre del repo git (aeca, intiflow, conservial…) → para Engram `project=` y Drive sync
- `module` = nombre del módulo Odoo (account_credit_note_pin, l10n_pe_…) → para `module-intelligence.ps1`

---

## Cambio de Proyecto en Sesión

Cuando el usuario indica un nuevo proyecto activo ("ahora trabaja en conservial"):

1. Actualizar `project=` activo → nuevo nombre del repo
2. Re-ejecutar `branch-safety-check.ps1 -RepoPath {ProjectsRoot}\18\{proyecto}\`
3. Actualizar path de Drive sync → `G:\My Drive\Engram\engram-sync\{nuevo-proyecto}\`
4. Confirmar al usuario: "Cambié contexto a: {proyecto} — rama: {branch}"

---

## Inicialización

### Modo B (proyecto independiente) — PARALELO

```
PARALLEL:
  scripts/odoo-version-detect.ps1        → VERSION + EDITION
  scripts/module-intelligence.ps1        → análisis 10 pasos + Engram save (Paso 11)

SEQUENTIAL después:
  - Si VERSION < 18: ⚠️ advertir deprecaciones
  - Si EDITION = Enterprise: aplicar patrones Enterprise
  - Si ACL faltante: ⚠️ advertir RULES.md R4
  - Cargar knowledge/v{VERSION}/ según contexto del usuario
```

### Modo A (workspace raíz) — SECUENCIAL

```
1. Resolver proyecto activo (ver arriba)
2. PARALLEL con path del módulo específico:
   scripts/odoo-version-detect.ps1 -Path {proyecto}/{módulo}
   scripts/module-intelligence.ps1 -Path {proyecto}/{módulo}
3. Mismas validaciones que Modo B
```

---

## Sincronización Engram — OBLIGATORIO

**Guardar en Engram cuando el contexto sea**:
- **Odoo técnico**: modelos, campos, vistas, ORM, XML, QWeb, OWL, errores, patrones, migraciones
- **Proyecto Alesco**: decisiones, descubrimientos, arquitectura sobre aeca/intiflow/conservial/benest/omnia/gprinter

**topic_keys**:
- `odoo/module/{module}/intelligence` — tras análisis de módulo (Paso 11 obligatorio)
- `odoo/error/{descripcion-kebab}` — tras error o bug
- `odoo/discovery/{tema-kebab}` — tras descubrimiento no obvio
- `odoo/dev/{module}/{feature-kebab}` — tras desarrollo completado
- `odoo/query/{module}/{tema-kebab}` — tras consulta respondida con contexto Odoo
- `project/{nombre}/decision/*` — decisión sobre proyecto Alesco específico

**Regla**: Si el contexto es Odoo o proyecto Alesco → guardar. Sin umbral mínimo.

---

## Tabla de Detección (Contexto → knowledge/)

*Usar después de detectar VERSION con odoo-version-detect.ps1.*

| Contexto del usuario | Cargar |
|----------------------|--------|
| modelo, campo, computed, ORM, `_inherit` | `knowledge/v{N}/model-patterns.md` + `knowledge/core/orm-patterns.md` |
| vista, XML, widget, xpath, form, tree, kanban | `knowledge/v{N}/view-patterns.md` + `knowledge/patterns/xml-views.md` |
| módulo nuevo, scaffold, boilerplate | `knowledge/v{N}/module-generator.md` |
| migración, upgrade, versión anterior | `knowledge/migration/v{X}-v{Y}.md` + `agents/upgrade-analyzer.md` |
| Docker, deployment, Odoo.sh, servidor | `knowledge/devops/` (archivo relevante) |
| sale, CRM, quotation | `knowledge/business/sale-crm.md` |
| stock, inventario, lote, serial | `knowledge/business/stock.md` |
| accounting, factura, journal | `knowledge/business/accounting.md` |
| HR, empleado, contrato | `knowledge/business/hr.md` |
| purchase, proveedor, procurement | `knowledge/business/purchase.md` |
| product, variant, UoM | `knowledge/business/products.md` |
| project, tarea, timesheet | `knowledge/business/project.md` |
| pricelist, precio, descuento | `knowledge/business/pricing.md` |
| wizard, transient, dialog | `knowledge/patterns/wizards.md` |
| cron, scheduled, automation | `knowledge/patterns/cron.md` |
| portal, token, CustomerPortal | `knowledge/patterns/portal.md` |
| mail, chatter, actividad, bus | `knowledge/patterns/mail.md` |
| controller, HTTP, REST, API | `knowledge/patterns/controllers.md` |
| website, snippet, publicWidget | `knowledge/patterns/website.md` |
| visual, PDF, email, theme, SCSS | `knowledge/patterns/visual.md` |
| multi-company, with_company | `knowledge/patterns/multi-company.md` |
| sequence, ir.sequence, numeración | `knowledge/patterns/sequences.md` |
| actions, ir.actions, act_window | `knowledge/patterns/actions.md` |
| settings, config, ir.config_parameter | `knowledge/patterns/settings.md` |
| report, QWeb PDF, wkhtmltopdf | `knowledge/patterns/reports.md` |
| dashboard, KPI, graph, pivot | `knowledge/patterns/dashboard.md` |
| security, acceso, grupos, reglas | `knowledge/v{N}/security-guide.md` |
| OWL, componente, frontend JS | `knowledge/v{N}/owl-components.md` (v16+) |
| i18n, traducción, PO file | `knowledge/patterns/i18n.md` |
| assets, bundle, SCSS, JS | `knowledge/patterns/assets.md` |
| external API, webhook, OAuth | `knowledge/patterns/external-api.md` |
| import, export, CSV, Excel | `knowledge/patterns/import-export.md` |
| attachment, binary, image | `knowledge/patterns/attachments.md` |
| computed, depends, inverse | `knowledge/patterns/computed-fields.md` |
| onchange, domain dinámico | `knowledge/patterns/onchange.md` |
| constraint, SQL, validation | `knowledge/patterns/constraints.md` |
| cheat sheet, snippet rápido | `knowledge/core/quick-patterns.md` |
| performance, N+1, batch | `knowledge/core/performance.md` |
| búsqueda profunda en source | `agents/module-intelligence.md` Modo 2 (Enterprise First) |
| code review, OCA checklist | `agents/code-reviewer.md` |
| análisis upgrade, migrate | `agents/upgrade-analyzer.md` |
| validar identidad Alesco | `knowledge/alesco/contributors.md` |
| proyectos Alesco en scope | `knowledge/alesco/projects.md` |

---

## Critical Rules

- **Workspace Mode PRIMERO** — detectar Mode A o Mode B antes de cualquier acción
- **Branch Safety SEGUNDO** — ejecutar `branch-safety-check.ps1` antes de cualquier git
- **Odoo version TERCERO** — ejecutar `odoo-version-detect.ps1` (obligatorio)
- **Enterprise First CUARTO** — para cada API: `Grep $cfg.EnterprisePath` primero
- **knowledge/ bajo demanda** — cargar solo el archivo relevante, nunca bulk-load
- **OCA standards** — aplicar siempre para cualquier código nuevo
- **Engram save** — después de cualquier respuesta con contexto Odoo o proyecto Alesco

---

## Scripts Disponibles

**`scripts/`** — scripts principales Odoo:
- `odoo-version-detect.ps1` — Lee `__manifest__.py`, extrae versión y edition
- `module-intelligence.ps1` — Análisis completo de módulo (10 pasos + Engram save paso 11)
- `view-xpath-validator.ps1` — Valida xpath en XML antes de guardar
- `branch-safety-check.ps1` — Clasifica rama git: ALLOWED / RESTRICTED / UNKNOWN
- `test-runner.ps1` — Ejecuta tests del módulo con odoo-bin
- `pre-migrate-generator.ps1` — Genera pre_migrate.py desde diff XML
- `commit-identity-check.ps1` — Verifica identidad del committer vs. CONTRIBUTING.md
- `acl-validator.ps1` — Valida cobertura ACL de todos los modelos
- `engram-sync.ps1` — Sincroniza Engram ↔ Google Drive

**`scripts/git-hooks/`** — hooks de git para proyectos Odoo:
- `install-hooks.ps1` — Instala/desinstala hooks en `.git/hooks/` de un repositorio
- `pre-commit` — Verifica identidad + cobertura ACL en archivos staged
- `pre-push` — Clasifica rama + solicita confirmación "si" antes de push
- `commit-msg` — Valida Conventional Commits + bloquea atribución de IA
- `pre-pr` — Checklist completo antes de abrir PR

Para instalar en un repo: `pwsh ~/.claude/skills/odoo-ai/scripts/git-hooks/install-hooks.ps1 -RepoPath .`

---

## Estructura knowledge/ (referencia)

```
knowledge/
  core/          — patrones transversales todas las versiones
  patterns/      — patrones técnicos (wizard, cron, portal, mail...)
  business/      — dominios de negocio (accounting, stock, HR...)
  templates/     — módulos scaffold por app
  examples/      — módulos completos de referencia
  v14/ … v19/    — patrones específicos por versión
  migration/     — guías de migración entre versiones adyacentes
  testing/       — patrones de testing
  devops/        — Docker, Odoo.sh, deployment
  api/           — JSON-RPC, server actions, external API
  security/      — scanners, ACL, vulnerabilidades
  debugging/     — diagnóstico, zombie configs, plugin triggers
  alesco/        — específico Alesco Perú (contribuidores, proyectos, reglas)

agents/
  module-intelligence.md   — odoo-source 3 modos (Enterprise First)
  code-reviewer.md         — OCA 7 categorías
  upgrade-analyzer.md      — análisis de migración
  context-gatherer.md      — keyword → knowledge/ mapping
  skill-finder.md          — búsqueda en biblioteca
```
