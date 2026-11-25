---
name: briefing-asunto
description: "Genera un briefing ejecutivo de un asunto procesal para reunión con socio o cliente"
argument-hint: "<referencia-del-asunto>"
---

## Propósito

Esta skill genera un briefing ejecutivo sobre un asunto procesal activo. Sintetiza el estado actual, los riesgos, las opciones estratégicas y los próximos pasos. Diseñada para preparar reuniones con socios, clientes o comités de dirección.

## Instrucciones

### Paso 1 — Cargar datos del asunto

1. Leer la ficha del asunto (generada por la skill de intake o proporcionada).
2. Leer la actividad reciente: últimos escritos, resoluciones, comunicaciones.
3. Leer la cronología actualizada si está disponible.
4. Identificar la audiencia del briefing: socio, cliente, comité.

### Paso 2 — Sintetizar estado actual

- Fase procesal actual.
- Última actuación relevante y su fecha.
- Próxima actuación prevista.
- Días transcurridos desde la última actividad.

### Paso 3 — Evaluar riesgos y opciones

**Riesgos:**
- Riesgo de resolución desfavorable (con justificación).
- Riesgo económico (cuantía + costas).
- Riesgo reputacional (si aplica).
- Riesgos procesales (prescripción, caducidad, litispendencia).

**Opciones estratégicas:**
- Continuar con la estrategia actual.
- Modificar la estrategia (indicar alternativas).
- Explorar transacción / mediación.
- Desistir (con valoración de costas).

### Paso 4 — Adaptar al público

- **Para socio/partner**: énfasis en riesgo, coste y decisiones pendientes.
- **Para cliente**: lenguaje accesible, opciones claras, implicaciones económicas.
- **Para comité**: visión de portfolio, impacto en la empresa, recomendación.

## Formato de salida

```markdown
## Briefing de asunto

**Asunto:** [nombre] — Ref.: [código]
**Cliente:** [nombre]
**Preparado para:** [socio/cliente/comité]
**Fecha:** [fecha]
**Preparado por:** [equipo]

---

### Resumen ejecutivo

[3-5 frases que resuman el asunto, su estado y la recomendación principal]

### Datos clave

| Campo | Valor |
|-------|-------|
| Posición | [demandante/demandado] |
| Jurisdicción | [tipo] |
| Procedimiento | [tipo] — Nº autos: [número] |
| Cuantía | [importe] |
| Fase actual | [fase] |
| Última actuación | [acción — fecha] |
| Próxima actuación | [acción — fecha] |

### Estado y evolución reciente

[Narración breve de los últimos desarrollos significativos]

### Análisis de riesgo

| Tipo de riesgo | Nivel | Detalle |
|----------------|-------|---------|
| Resolución desfavorable | [A/M/B] | [justificación] |
| Económico (condena + costas) | [rango EUR] | [desglose] |
| Reputacional | [A/M/B] | [detalle] |
| Procesal | [A/M/B] | [detalle] |

### Opciones estratégicas

| Opción | Descripción | Probabilidad de éxito | Coste estimado | Tiempo |
|--------|-------------|----------------------|----------------|--------|
| [opción 1] | [detalle] | [%] | [EUR] | [meses] |
| [opción 2] | [detalle] | [%] | [EUR] | [meses] |

### Recomendación

[Recomendación concreta del equipo con justificación]

### Próximos pasos

| Acción | Responsable | Plazo | Prioridad |
|--------|-------------|-------|-----------|
| [acción] | [nombre] | [fecha] | [alta/media/baja] |

### Presupuesto y facturación

| Concepto | Importe |
|----------|---------|
| Honorarios devengados a fecha | [EUR] |
| Estimación hasta resolución | [EUR] |
| Provisión para costas | [EUR] |
```

## Referencias normativas

- Aplicables según la materia y jurisdicción del asunto concreto.
- **LEC**: procedimiento civil.
- **LRJS**: procedimiento laboral.
- **LJCA**: procedimiento contencioso-administrativo.
- **LECrim**: procedimiento penal.

## Guardrails

- **NO** predice el resultado del procedimiento — proporciona análisis de riesgo orientativo.
- **NO** toma decisiones estratégicas — presenta opciones para que decida el letrado/cliente.
- **NO** revela información confidencial del despacho al preparar briefings para clientes.
- **NO** garantiza la exactitud de las probabilidades de éxito — son estimaciones.
- **ESCALAR** si el asunto lleva más de 90 días sin actividad (stale matter).
- **ESCALAR** si el riesgo económico supera umbrales del despacho.
- **AVISAR** si la información disponible está desactualizada (última actualización > 30 días).
- **AVISAR** si faltan datos para completar alguna sección del briefing.
