---
name: roadmap-manager
description: Use when necesitas leer, añadir, completar o repriorizar tareas del roadmap (plans/ROADMAP.md) o registrar/consultar decisiones arquitectónicas (plans/DECISIONS.md, ADR con IDs únicos), o generar un resumen de progreso con barra. Es la skill que gestiona el file-blackboard de planificación.
---

# Skill: Roadmap Manager

> Habilidad para leer, actualizar y gestionar el roadmap del proyecto en `plans/ROADMAP.md` y el log de decisiones en `plans/DECISIONS.md`.

## Cuándo usar esta skill

Cuando necesites:
- Ver el estado actual del roadmap.
- Añadir nuevas tareas o features al roadmap.
- Marcar tareas como completadas.
- Repriorizar tareas existentes.
- Registrar o consultar una decisión arquitectónica (ADR).
- Generar un resumen de progreso.

## Archivos gestionados

### `plans/ROADMAP.md`
Fuente de verdad del roadmap. Estructura:

```markdown
# Nexus - Roadmap de Desarrollo

## Estado del Proyecto: [Mes Año]

Progreso global: ████████░░ 80% (16/20 tareas)

### Completado
- [x] Feature A — descripción breve — (YYYY-MM-DD)
- [x] Feature B — descripción breve — (YYYY-MM-DD)

### En Progreso
- [ ] Feature C — [ALTA] [M] — descripción — @agente

### Backlog (priorizado)
- [ ] Feature D — [ALTA] — descripción
- [ ] Feature E — [MEDIA] — descripción
- [ ] Feature F — [BAJA] — descripción

### Mejoras Técnicas
- [ ] Mejora X — descripción

### Métricas
| Métrica | Valor |
|---------|-------|
| Tools activas | N |
| Agentes implementados | N |
| Cobertura de tests | N% |
| Findings en lab | N |
```

### `plans/DECISIONS.md`
Log de decisiones arquitectónicas (ADR). Estructura:

```markdown
# Nexus - Decisions Log (ADR)

## ADR-001: [Título]
- **Fecha**: YYYY-MM-DD
- **Estado**: Propuesta | Aceptada | Rechazada | Superada por ADR-NNN
- **Contexto**: ...
- **Opciones**: ...
- **Decisión**: ...
- **Consecuencias**: ...
```

ADR semilla recomendados para Nexus:
- **ADR-001**: stack Python + Agent Framework + Ollama (`qwen3:8b`) + SQLite de findings.
- **ADR-002**: patrón de tools `core.py` / `tool.py` / `rules.py` — lógica pura separada del wrapper del agente.
- **ADR-003**: lab Docker local (Juice Shop, DVWA, WebGoat, DVNA) como único scope de pentest.
- **ADR-004**: pentest-safety como guardrail obligatorio: allowlist + HITL para acciones intrusivas.

## Operaciones disponibles

### Ver roadmap
1. Leer `plans/ROADMAP.md`.
2. Presentar resumen al usuario con estado actual y barra de progreso.

### Añadir tarea
1. Determinar sección (En Progreso / Backlog / Mejoras Técnicas).
2. Asignar prioridad (ALTA / MEDIA / BAJA).
3. Estimar esfuerzo (S/M/L) si es posible.
4. Escribir la tarea en el formato del roadmap.
5. Registrar en `agent-comms.md` si afecta a otros agentes.

### Completar tarea
1. Mover la tarea de "En Progreso" / "Backlog" a "Completado".
2. Añadir fecha de completado.
3. Actualizar la barra de progreso y las métricas si aplica.
4. Registrar en `agent-comms.md` con `[STATUS] DONE`.

### Repriorizar
1. Leer roadmap actual.
2. Proponer nuevo orden al usuario con justificación.
3. Aplicar cambios tras aprobación.
4. Documentar la decisión de repriorizar en `plans/DECISIONS.md` si es significativo.

### Registrar un ADR
1. **Lint de IDs únicos**: localiza el último `ADR-NNN` y usa el siguiente número. Nunca reutilices un número (evita el bug del ADR duplicado).
2. Rellena el bloque ADR completo (fecha, estado, contexto, opciones, decisión, consecuencias).
3. Si un ADR sustituye a otro, marca el viejo como `Superada por ADR-NNN` — nunca lo borres.

### Generar resumen de progreso
1. Contar tareas completadas vs pendientes.
2. Identificar bloqueadores en `agent-comms.md` (líneas `[BLOCKED]`).
3. Calcular velocidad de progreso (tareas/semana aprox).
4. Presentar resumen visual:

```
Progreso: ████████░░ 80% (16/20 tareas)
Bloqueadores: 1 (timeout en tool sqli_probe)
Próxima entrega: agente de web pentest
```

## Reglas
- **Nunca borres tareas completadas** — son historial del proyecto.
- **Nunca reutilices un ID de ADR** — IDs estrictamente únicos.
- **Siempre justifica repriorizar** — documenta por qué cambió el orden.
- **Consulta con el usuario** antes de cambiar prioridades ALTA.
- **Sincroniza con agent-comms.md** — cualquier cambio que afecte a agentes.
- **Sólo el PM escribe en DECISIONS.md** — los especialistas proponen, el PM registra.
- **Actualiza la barra y las métricas** cuando se completen tareas significativas.
