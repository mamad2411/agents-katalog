---
name: project-research
description: Use when necesitas investigar una librería, framework, API o herramienta de pentest antes de adoptarla, comparar alternativas tecnológicas, verificar precios/límites/ToS de un servicio externo, o buscar mejores prácticas — produce una tabla de alternativas y documenta la decisión como ADR en plans/DECISIONS.md.
---

# Skill: Project Research

> Habilidad para investigar features, librerías, APIs, herramientas de pentest y mejores prácticas via web, y cerrar con una decisión documentada (ADR).

## Cuándo usar esta skill

Cuando el PM Coordinator (o cualquier agente con acceso web) necesite:

- Investigar una nueva librería o framework Python antes de adoptarlo (ej: httpx vs requests; pydantic v1 vs v2).
- Comparar alternativas tecnológicas (ej: SQLite vs DuckDB para findings; Ollama vs llama.cpp local; qwen3:8b vs mistral).
- Buscar mejores prácticas para implementar una feature (ej: fuzzing con ffuf vs gobuster; parsing de resultados nmap en Python).
- Investigar herramientas de pentest de terceros (nmap, sqlmap, nuclei, nikto, feroxbuster).
- **Verificar licencias, límites de uso y — CRÍTICO — los Terms of Service de cada herramienta** antes de integrarla.
- Buscar documentación oficial de herramientas del stack.

## Workflow de investigación (5 pasos)

### 1. Definir el objetivo
Antes de buscar, clarificar en una frase:
- Qué problema queremos resolver.
- Qué restricciones tenemos (stack Python, lab local, un solo dev, uso educativo/personal).
- Qué criterios de evaluación usaremos (licencia permisiva, mantenimiento activo, integrable como subprocess o librería).

### 2. Buscar información
Usar `WebSearch` para encontrar, en este orden de preferencia:
- Documentación oficial de la herramienta/librería.
- Artículos comparativos recientes (preferir 2025-2026; descartar lo anterior a 2023 salvo specs estables).
- Repositorios GitHub con estrellas y commits recientes (mantenimiento activo).
- Opiniones de la comunidad (Reddit, HN, Stack Overflow) como señal secundaria.

Para herramientas de pentest: localiza explícitamente la **licencia** y los **términos de uso**. Si la herramienta sólo permite uso ético/autorizado (casi todas), documenta que el uso es en lab aislado. Si no encuentras términos claros, eso es por sí mismo un hallazgo (riesgo).

### 3. Analizar alternativas
Para cada alternativa, rellenar la tabla:

| Criterio | Alternativa A | Alternativa B | Alternativa C |
|----------|---------------|---------------|---------------|
| Pros | ... | ... | ... |
| Contras | ... | ... | ... |
| Licencia | ... | ... | ... |
| Integración Python | librería/subprocess/API | ... | ... |
| Mantenimiento (último release) | ... | ... | ... |
| Dependencias extra | ... | ... | ... |
| Complejidad integración | baja/media/alta | ... | ... |
| Compatibilidad con stack | ... | ... | ... |

### 4. Recomendar
Proponer la mejor opción con justificación clara:
- Por qué es la mejor para nuestro caso (licencia permisiva, integrable en Python, mantenimiento activo).
- Qué riesgos tiene (dependencias pesadas, output parsing frágil, cambios de CLI entre versiones).
- Cómo se integraría en el proyecto (nueva tool en `src/nexus/tools/`, wrapper subprocess, o librería directa).
- Estimación de esfuerzo (S/M/L).

### 5. Documentar
Guardar los hallazgos en `plans/DECISIONS.md` como un ADR. **Antes de escribir, comprueba el último ADR-NNN existente y usa el siguiente número (IDs únicos — nunca reutilices un número).**

```markdown
## ADR-NNN: Elección de {tecnología/herramienta} para {propósito}
- **Fecha**: YYYY-MM-DD
- **Estado**: Propuesta
- **Contexto**: [problema a resolver]
- **Opciones**:
  1. {Opción A} — [pros/contras]
  2. {Opción B} — [pros/contras]
- **Decisión**: {opción elegida} porque {justificación}
- **Licencia verificada**: si/no — [url]
- **Consecuencias**: {qué implica para el proyecto}
```

## Herramientas disponibles
- **WebSearch**: Búsquedas web generales.
- **WebFetch**: Leer contenido de URLs específicas (docs, licencias, páginas de releases).
- **Read**: Leer archivos del proyecto para contexto.

## Contexto del proyecto (stack actual)
Al investigar, ten en cuenta el stack de Nexus:
- **Lenguaje**: Python 3.12+; proyecto con `pyproject.toml`.
- **Agentes**: Agent Framework (Microsoft) con Ollama (`qwen3:8b` por defecto).
- **Tools**: `src/nexus/tools/<tool>/{core.py,tool.py,rules.py}` — patrón httpx + timeout + fallback gracioso.
- **Findings**: modelo `Finding` persistido en SQLite via `src/nexus/storage/`.
- **Lab**: Docker local con Juice Shop (:3000), DVWA (:8081), WebGoat (:8082), DVNA (:9091).
- **Presupuesto**: proyecto personal, preferir herramientas gratuitas/open-source/locales.
- **Equipo**: 1 desarrollador + agentes IA.

## Regla anti-duplicación
La metodología de investigación exploratoria más amplia y la fase de diseño viven en `superpowers:brainstorming` y en la skill local `design-doc`. Esta skill es el paso concreto **investigar opción → tabla → ADR**; no recrees aquí un flujo de brainstorming completo.
