---
name: calculadora-plazos
description: "Calcula plazos procesales en días hábiles considerando agosto inhábil y festivos"
argument-hint: "<tipo-procedimiento> <fecha-notificación> [jurisdicción]"
---

## Propósito

Esta skill calcula plazos procesales en el orden jurisdiccional civil, social, contencioso-administrativo y penal. Aplica las reglas de cómputo de la LEC y LOPJ: días hábiles, exclusión de sábados y festivos, inhabilidad de agosto (con excepciones) y reglas especiales por jurisdicción.

## Instrucciones

### Paso 1 — Recopilar datos de entrada

1. **Tipo de procedimiento**: ordinario, verbal, monitorio, ejecución, laboral, contencioso, penal.
2. **Fecha de notificación**: fecha en que se recibe la comunicación.
3. **Jurisdicción**: civil, social, contencioso-administrativo, penal.
4. **Localidad/CCAA**: para identificar festivos locales y autonómicos.
5. **Acción procesal**: contestación, recurso, oposición, etc.

### Paso 2 — Identificar plazo aplicable

**Jurisdicción civil (LEC):**

| Acción | Plazo | Base legal |
|--------|-------|------------|
| Contestación demanda ordinario | 20 días | Art. 404 |
| Contestación verbal | 10 días | Art. 438 |
| Recurso reposición | 5 días | Art. 452 |
| Recurso apelación (preparación) | 20 días | Art. 458 |
| Oposición monitorio | 20 días | Art. 815 |
| Oposición ejecución | 10 días | Art. 556 |
| Recurso extraordinario infracción procesal | 20 días | Art. 470 |
| Recurso de casación | 20 días | Art. 479 |

**Jurisdicción social (LRJS):**

| Acción | Plazo | Base legal |
|--------|-------|------------|
| Recurso de suplicación | 5 días (anuncio) + 10 días (formalización) | Arts. 194-195 |
| Recurso de casación | 5 días (preparación) + 10 días (formalización) | Arts. 206-210 |
| Conciliación previa | Sin plazo fijo — antes de demanda | Art. 63 |

### Paso 3 — Aplicar reglas de cómputo

1. **Dies a quo**: el día de la notificación NO cuenta (art. 133.1 LEC).
2. **Días hábiles**: se excluyen sábados, domingos y festivos (art. 130.2 LEC).
3. **Agosto inhábil**: todo el mes de agosto es inhábil en jurisdicción civil (art. 183.1 LOPJ).
   - **Excepciones** (art. 183.2 LOPJ): medidas cautelares, diligencias urgentes, procedimientos sobre guarda y custodia, alimentos, internamiento.
4. **Jurisdicción social**: agosto es hábil para actos de conciliación y juicio (art. 43.4 LRJS) pero inhábil para plazos de recurso.
5. **Jurisdicción penal**: todos los días son hábiles.
6. **Si el último día es inhábil**: se prorroga al siguiente día hábil (art. 133.4 LEC).
7. **Presentación telemática**: hasta las 15:00 del día hábil siguiente al vencimiento (art. 135 LEC).

### Paso 4 — Calcular y presentar resultado

## Formato de salida

```markdown
## Cálculo de plazo procesal

### Datos de entrada

| Concepto | Valor |
|----------|-------|
| Procedimiento | [tipo] |
| Jurisdicción | [civil/social/contencioso/penal] |
| Acción procesal | [tipo] |
| Fecha de notificación | [fecha] |
| Plazo aplicable | [n] días [hábiles/naturales] |
| Base legal | [artículo] |

### Cómputo

- Dies a quo (no cuenta): [fecha notificación]
- Primer día del cómputo: [fecha]
- Días inhábiles en el período: [lista de fechas con motivo]
- Agosto inhábil: [SÍ/NO — motivo]
- Último día del plazo: [fecha]
- Si cae en inhábil, prórroga a: [fecha]

### Resultado

| Fecha límite | Hora límite | Forma |
|--------------|-------------|-------|
| **[fecha]** | Hasta las 15:00 del [fecha+1] si presentación telemática | LexNET/Sede judicial electrónica |

### Advertencias

- [Verificar festivos locales de [localidad] no incluidos en este cálculo]
- [Este cálculo es orientativo — verificar con el calendario oficial del partido judicial]
```

## Referencias normativas

- **LEC art. 130**: Días y horas hábiles.
- **LEC art. 131**: Habilitación de días y horas.
- **LEC art. 132**: Plazos y términos — carácter improrrogable.
- **LEC art. 133**: Cómputo de los plazos.
- **LEC art. 134**: Improrrogabilidad y consecuencias.
- **LEC art. 135**: Presentación de escritos — hasta las 15:00 del día siguiente.
- **LOPJ art. 182**: Días y horas hábiles.
- **LOPJ art. 183**: Mes de agosto inhábil — excepciones.
- **LOPJ arts. 184-185**: Habilitación.
- **LRJS art. 43**: Días hábiles en jurisdicción social.

## Guardrails

- **NO** garantiza la exactitud del cómputo — es orientativo y debe verificarse.
- **NO** tiene acceso al calendario oficial del partido judicial ni festivos locales.
- **NO** presenta escritos ni gestiona plazos en LexNET.
- **AVISAR** siempre: "Este cálculo es orientativo. Verifique con el calendario oficial del órgano judicial."
- **AVISAR** si el plazo puede verse afectado por agosto y hay duda sobre la excepción.
- **ESCALAR** si el plazo vence en menos de 3 días hábiles.
- **ESCALAR** si hay duda sobre si agosto es hábil o inhábil para el caso concreto.
