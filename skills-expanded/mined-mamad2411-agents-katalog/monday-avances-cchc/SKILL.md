---
name: monday-avances-cchc
description: Gestiona requerimientos y avances del proyecto Tienda Deportiva CCHC en Monday.com via MCP. Use cuando el usuario pida crear, actualizar, completar o reportar requerimientos, avance por modulo, o estado de entregables.
disable-model-invocation: true
---

# Monday Avances CCHC

## Objetivo
Usar Monday.com via MCP para llevar control operativo del proyecto: requerimientos creados, en progreso, bloqueados y completados, con trazabilidad a modulo, commit y PR.

## Contexto obligatorio del repo
Antes de registrar o cambiar estados:
1. Leer `CLAUDE.md` para restricciones de arquitectura y orden de trabajo.
2. Leer `spec.md` para modulo activo y Definition of Done (DoD).
3. Leer `data.md` y `docs/arquitectura-datos.md` si el requerimiento toca datos.

Reglas clave:
- M0-M6 ya entregado.
- M7+ solo despues de validaciones de arquitectura pendientes.
- No crear alcance fuera del modulo activo definido en `spec.md`.

## Pre-chequeo MCP Monday
1. Verificar que el servidor MCP de Monday.com este disponible en la sesion.
2. Si no existe conexion, pedir al usuario configurar MCP de Monday y detener la ejecucion.
3. No inventar IDs de board, grupo, item o columna.

## Estructura recomendada en Monday
Si el board no existe, crear un board llamado: `CCHC - Tienda Deportiva - Avances`.

Grupos:
- Backlog
- En progreso
- Bloqueado
- Completado

Columnas sugeridas:
- `req_id` (texto corto, unico)
- `titulo` (texto)
- `modulo` (estado o dropdown: M0..M12)
- `estado` (status: Backlog, En progreso, Bloqueado, Completado)
- `prioridad` (status)
- `owner` (personas)
- `fecha_inicio` (date)
- `fecha_cierre` (date)
- `fuente` (status: spec, bug, mejora, deuda_tecnica)
- `criterio_dod` (texto largo)
- `evidencia` (texto largo con commit/PR/test)
- `bloqueo` (texto largo)

## Flujo operativo
### 1) Crear requerimiento
Al crear un requerimiento:
1. Validar que pertenezca al modulo activo.
2. Generar `req_id` con formato `M{N}-{slug}`. Ejemplo: `M7-variantes-sku-basico`.
3. Crear item en grupo `Backlog` con campos minimos: `req_id`, `titulo`, `modulo`, `fuente`, `criterio_dod`.
4. Confirmar al usuario el ID creado y el estado inicial.

### 2) Marcar en progreso
1. Mover item a `En progreso`.
2. Cambiar columna `estado` a `En progreso`.
3. Completar `owner` y `fecha_inicio` si faltan.

### 3) Marcar bloqueado
1. Mover item a `Bloqueado`.
2. Cambiar `estado` a `Bloqueado`.
3. Registrar causa en `bloqueo` con accion requerida.

### 4) Marcar completado
Solo completar cuando exista evidencia verificable:
- commit o PR asociado
- validacion local (tests o checks aplicables)
- cumplimiento de DoD del modulo

Acciones:
1. Mover item a `Completado`.
2. Cambiar `estado` a `Completado`.
3. Setear `fecha_cierre`.
4. Completar `evidencia` con links o referencias concretas.

## Reglas de calidad
- No cerrar requerimientos sin evidencia.
- No crear requerimientos duplicados: buscar por `req_id` y titulo similar antes de crear.
- Mantener consistencia de nombres de modulo (M0..M12).
- Si hay ambiguedad de alcance, pedir confirmacion antes de crear o mover.

## Plantillas de respuesta al usuario
### Alta creada
`Requerimiento creado: {req_id} - {titulo}. Estado: Backlog. Modulo: {modulo}.`

### Cambio de estado
`Requerimiento {req_id} actualizado a {estado}.`

### Cierre
`Requerimiento {req_id} completado. Evidencia: {evidencia}.`

### Bloqueo
`Requerimiento {req_id} bloqueado. Motivo: {bloqueo}. Accion sugerida: {accion}.`

## Prompt unico recomendado
Usa este prompt tal cual cuando quieras operar el tablero desde este skill:

"Usa el skill monday-avances-cchc para sincronizar Monday.com via MCP con este repositorio: crea los requerimientos faltantes del modulo activo segun spec.md, marca en progreso los que esten implementandose, bloquea los impedidos con causa, y completa solo los que tengan evidencia (commit/PR/tests). Devuelveme un resumen con: creados, actualizados, bloqueados y completados, incluyendo req_id y modulo."