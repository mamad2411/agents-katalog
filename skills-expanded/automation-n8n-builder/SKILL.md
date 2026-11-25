---
name: automation-n8n-builder
description: Crea, valida y despliega workflows de n8n desde Claude Code usando el MCP n8n-mcp. Úsala cuando el usuario diga "crea un workflow en n8n", "monta un n8n que haga X", "convierte esta idea en automatización", "diseña un flujo n8n", o describa una secuencia de pasos automatizables (recibir webhook → procesar → enviar a Slack, scheduler diario que lee de Google Sheets, etc.). Activable también con frases como "auto­matización", "n8n", "workflow", "trigger". NO uses esta skill para migrar workflows existentes de n8n a Claude — para eso usa automation-n8n-to-claude.
author: IA Masters Academy
version: 1.0.0
tags: [n8n, mcp, automatizacion, workflow, builder, claude-code]
---

# automation-n8n-builder — Constructor de workflows n8n desde Claude

> Esta skill convierte una descripción en lenguaje natural ("quiero que cuando llegue un lead por formulario lo meta en Sheets y avise por Slack") en un workflow n8n funcional, validado y desplegado.

---

## Prerequisitos

1. **MCP `n8n-mcp` instalado y configurado** en `.mcp.json` del repo o en `~/.claude/.mcp.json`.
   Si no lo tiene, sugerir al usuario: `/install-mcp n8n-mcp`.
2. **Acceso a una instancia n8n** (self-hosted o cloud) con API key en variable de entorno `N8N_API_KEY` y `N8N_BASE_URL`.
3. **Permisos**: el MCP requiere que el operador pueda crear/editar/desplegar workflows.

Si falta cualquiera de los tres, la skill explica al usuario qué falta antes de continuar.

---

## Flujo de trabajo

### Paso 1 · Entender el caso de uso

Antes de tocar n8n, hacer 3-5 preguntas para clarificar:

- ¿Cuál es el **trigger**? (webhook, schedule, evento de app, manual…)
- ¿Qué **fuentes de datos** intervienen? (Google Sheets, Notion, base de datos, API…)
- ¿Qué **transformaciones** son necesarias? (filtrar, enriquecer, formatear…)
- ¿Cuál es el **destino**? (Slack, email, Notion, otra app…)
- ¿Hay **manejo de errores** necesario? (reintentos, notificaciones de fallo…)

Si la idea es vaga, proponer 2-3 versiones concretas y dejar al usuario elegir.

### Paso 2 · Diseño visual del flujo

Antes de pedir nada al MCP, mostrar al usuario un **diagrama en texto** del workflow propuesto:

```
[Webhook: form-submission]
    ↓
[Filter: si email contiene @empresa.com]
    ↓
[Sheets: append row con {nombre, email, fuente, fecha}]
    ↓
[Slack: notify #leads con "Nuevo lead: {nombre}"]
    ↓
[Error branch: si Slack falla, email a admin]
```

Pedir confirmación al usuario antes de construir.

### Paso 3 · Construir vía MCP

Usar las herramientas del MCP `n8n-mcp`:

- `search_nodes` para encontrar nodos relevantes
- `get_node` para inspeccionar parámetros de un nodo concreto
- `n8n_create_workflow` para crear el workflow vacío
- `n8n_update_partial_workflow` para añadir nodos uno a uno con sus conexiones
- `n8n_validate_workflow` para verificar que el grafo es válido

Construir el workflow incrementalmente, no de golpe. Tras cada nodo añadido, mostrar progreso al usuario.

### Paso 4 · Validar antes de desplegar

Ejecutar `n8n_validate_workflow` y revisar:

- Todos los nodos tienen credenciales asignadas (o aviso si faltan)
- Las conexiones entre nodos son coherentes
- Los expressions (`{{$json.field}}`) referencian campos que existen
- El trigger está configurado correctamente

Si hay errores → mostrarlos al usuario, proponer fixes, no desplegar todavía.

### Paso 5 · Test en modo prueba

Antes de activar:

- `n8n_test_workflow` con un payload de ejemplo
- Mostrar al usuario el resultado de cada nodo
- Si algún nodo falla, proponer fix o ajustar el diseño

### Paso 6 · Activar y entregar

Una vez validado:

- Activar el workflow (`active: true`)
- Devolver al usuario:
  - URL del workflow en n8n
  - Resumen de qué hace y cuándo se dispara
  - Cómo monitorizar las ejecuciones (`n8n_executions`)
  - Sugerencia de mejoras futuras (logs, alertas, etc.)

---

## Patrones comunes

### Patrón 1 — Webhook → Procesar → Notificar

Para captación de leads, formularios, integraciones de CRM ligeras.

Nodos clave: `Webhook` (trigger) → `Code` / `Set` (transformar) → `Slack` / `Email` (notificar) → `Respond to Webhook` (200 OK).

### Patrón 2 — Schedule → Leer → Reportar

Para reportes diarios/semanales, recordatorios, backups.

Nodos clave: `Schedule Trigger` → `HTTP Request` / `Database` (leer datos) → `Code` (formatear) → `Slack` / `Email` (entregar).

### Patrón 3 — Evento de app → Enriquecer → Persistir

Para mantener bases de datos en sync, enriquecer leads con datos externos.

Nodos clave: `Trigger de app` (Notion, Airtable, etc.) → `HTTP Request` (Clearbit, BORME, etc.) → `Set` (componer) → `Sheets` / `Postgres` (escribir).

### Patrón 4 — Multi-canal con fallback

Para mensajería crítica que NO puede fallar.

Nodos clave: `IF` (rama principal) → `Try` (canal A: Slack) → `On error` (canal B: email) → `On error` (canal C: WhatsApp).

---

## Coordinación con otras skills

- **Si el usuario tiene un workflow ya en n8n y quiere migrar a Claude** → usar `automation-n8n-to-claude` en su lugar.
- **Si el usuario describe la automatización en términos de marketing** (envíos masivos, secuencias) → recomendar primero `marketing-email-sequence` para diseñar la secuencia, luego esta skill para construirla en n8n.
- **Si la automatización requiere scraping** → combinar con `tool-firecrawl-scraper` antes de meterlo en n8n (puede tener sentido hacerlo todo en Claude en lugar de n8n).

---

## Cuándo NO usar n8n

Antes de construir el workflow, valorar honestamente si **n8n es la herramienta adecuada**. Casos en los que conviene plantear alternativa:

- **El usuario quiere "una skill que haga X cada día"** → mejor un cron job + skill Claude directa (más simple, no requiere infra n8n).
- **El flujo es 100% texto** (resumir, reescribir, traducir) → Claude lo hace nativo, no necesita orquestador.
- **El usuario solo quiere conectar 2 SaaS conocidos** (Sheets ↔ Slack) → Zapier o Make pueden ser más rápidos de configurar.

Decir honestamente *"esto se puede montar en n8n, pero te recomendaría X porque…"* es parte del trabajo de la skill. No empujar n8n por inercia.

---

## Output esperado

Al cerrar:

- Workflow n8n desplegado y activo
- Documentación mínima del workflow en `projects/automations/<fecha>-<nombre>/README.md` con:
  - Diagrama del flujo
  - Trigger y schedule (si aplica)
  - Credenciales que requiere
  - Cómo testarlo
  - Cómo monitorizar
