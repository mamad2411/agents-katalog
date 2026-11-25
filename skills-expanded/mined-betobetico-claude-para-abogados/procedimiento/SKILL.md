---
name: procedimiento
description: >
  Triaje de procedimiento tributario — analiza la situación procesal
  tributaria del usuario e identifica el tipo de procedimiento, plazos,
  opciones y estrategia. Cubre: comprobación limitada, inspección,
  sancionador, reclamación ante TEA y recurso contencioso-administrativo.
  Usar cuando el usuario diga "me ha llegado una notificación de Hacienda",
  "inspección", "requerimiento", "sanción tributaria", "recurso TEA".
argument-hint: "[describir la situación o pegar la notificación]"
---

# /procedimiento

1. Cargar `~/.claude/plugins/config/claude-para-abogados/fiscal/CLAUDE.md` → tipo de entidad, historial de procedimientos, asesores.
2. Identificar el tipo de procedimiento.
3. Analizar la situación procesal (plazos, fase, opciones).
4. Generar informe con opciones y estrategia.

```
/fiscal:procedimiento
Hemos recibido una comunicación de inicio de procedimiento de comprobación
limitada respecto del IVA del ejercicio 2024.
```

---

## Propósito

Recibir una notificación de la AEAT genera incertidumbre. ¿Qué tipo de procedimiento es? ¿Cuánto tiempo tienen? ¿Qué opciones tengo? ¿Debo recurrir o aceptar? Este skill triaja la situación, identifica plazos y opciones, y propone una estrategia procesal.

---

## Tipos de procedimiento tributario

### 1. Procedimiento de verificación de datos (arts. 131-133 LGT)

| Aspecto | Detalle |
|---|---|
| **Qué es** | Comprobación de errores materiales, aritméticos o discrepancias con datos declarados por terceros |
| **Plazo máximo** | 6 meses desde notificación de inicio |
| **Resultado** | Liquidación provisional o archivo |
| **Recurso** | Reposición (1 mes) o reclamación ante TEA (1 mes) |

### 2. Comprobación limitada (arts. 136-140 LGT)

| Aspecto | Detalle |
|---|---|
| **Qué es** | Comprobación de declaraciones sin acceso a contabilidad completa |
| **Plazo máximo** | 6 meses desde notificación de inicio |
| **Actuaciones** | Requerimientos documentales, acceso a registros, comprobación de datos |
| **Límites** | No puede examinar la contabilidad mercantil (salvo excepciones) |
| **Resultado** | Liquidación provisional o confirmación |
| **Recurso** | Reposición (1 mes) o reclamación ante TEA (1 mes) |

### 3. Procedimiento de inspección (arts. 141-159 LGT)

| Aspecto | Detalle |
|---|---|
| **Qué es** | Comprobación e investigación completa — acceso a toda la documentación |
| **Plazo máximo** | 18 meses (27 meses en casos de especial complejidad: volumen de operaciones >5,7M EUR, grupo consolidado, etc. — art. 150 LGT) |
| **Inicio** | Comunicación de inicio de actuaciones inspectoras |
| **Actas** | De conformidad (art. 156), de disconformidad (art. 157), con acuerdo (art. 155) |
| **Recurso** | Contra la liquidación: reposición o TEA (1 mes) |

**Actas según conformidad:**

| Tipo de acta | Efecto | Reducción de sanción |
|---|---|---|
| **Con acuerdo** (art. 155) | Liquidación firme salvo nulidad/lesividad | 50% reducción sanción |
| **De conformidad** (art. 156) | Liquidación provisional; firmeza si no se recurre en 1 mes | 30% reducción sanción |
| **De disconformidad** (art. 157) | Se abre plazo de alegaciones (15 días) | Sin reducción por conformidad |

### 4. Procedimiento sancionador (arts. 207-212 LGT)

| Aspecto | Detalle |
|---|---|
| **Inicio** | Separado de la liquidación; notificación de inicio |
| **Plazo** | 6 meses desde notificación de inicio (art. 211 LGT) |
| **Clasificación** | Leve (art. 191-195), grave (art. 191-195), muy grave (art. 191-195) |
| **Reducción por conformidad** | 30% (art. 188.1 LGT) |
| **Reducción por pronto pago** | 25% adicional si no se recurre y se paga en período voluntario (art. 188.3 LGT) |
| **Total reducción posible** | Hasta 50% acumulando conformidad + pronto pago; hasta 65% si acta con acuerdo + pronto pago |

### 5. Reclamación económico-administrativa (arts. 226-249 LGT)

| Aspecto | Detalle |
|---|---|
| **Órgano** | TEAR (regional) o TEAC (central, si >150.000 EUR o determinados actos) |
| **Plazo de interposición** | 1 mes desde notificación del acto |
| **Plazo de resolución TEAR** | 1 año (art. 240 LGT); silencio negativo |
| **Plazo de resolución TEAC** | 1 año |
| **Recurso de alzada ante TEAC** | 1 mes desde notificación de resolución TEAR |
| **Recurso extraordinario de alzada para unificación de criterio** | Directores generales del Ministerio |

### 6. Recurso contencioso-administrativo (LJCA 29/1998)

| Aspecto | Detalle |
|---|---|
| **Plazo** | 2 meses desde notificación de la resolución del TEA |
| **Órgano** | TSJ (actos de CCAA y TEAR) o AN (actos del TEAC y determinados actos estatales) |
| **Casación** | Recurso de casación ante el TS (interés casacional objetivo) |

---

## Árbol de decisión procesal

```
Notificación recibida
├── ¿Qué tipo de acto es?
│   ├── Requerimiento de información → Atender en plazo
│   ├── Inicio de comprobación limitada → Analizar alcance y plazo
│   ├── Inicio de inspección → Evaluar riesgos y estrategia
│   ├── Propuesta de liquidación → Alegaciones (15 días)
│   ├── Liquidación definitiva → ¿Recurrir?
│   │   ├── Reposición (1 mes) — ante el mismo órgano
│   │   └── Reclamación TEA (1 mes) — ante TEAR/TEAC
│   ├── Resolución sancionadora → ¿Aceptar + pronto pago o recurrir?
│   └── Resolución TEA → ¿Contencioso? (2 meses)
```

---

## Formato de salida

```markdown
# Triaje de procedimiento tributario

**Tipo de procedimiento:** [verificación / comprobación limitada / inspección / sancionador / TEA / contencioso]
**Fecha de notificación:** [fecha]
**Plazo para actuar:** [fecha límite — CRÍTICO]
**Órgano actuante:** [AEAT / TEAR / TEAC / TSJ / AN]

---

## Situación procesal

[Resumen: en qué fase estamos, qué ha pasado, qué viene]

---

## Plazos

| Concepto | Plazo | Fecha límite | Estado |
|---|---|---|---|
| [Ej., Alegaciones] | 15 días | [fecha] | [Pendiente] |
| [Ej., Recurso de reposición] | 1 mes | [fecha] | [Pendiente] |

---

## Opciones

| Opción | Ventajas | Inconvenientes | Recomendación |
|---|---|---|---|
| 1. [Ej., Firmar conformidad] | [Reducción 30% sanción] | [Renuncia a recurrir] | [Para importes bajos con poca defensa] |
| 2. [Ej., Alegar en disconformidad] | [Mantiene opciones] | [Sin reducción] | [Si hay argumentos sólidos] |
| 3. [Ej., Recurrir ante TEA] | [Revisión por órgano independiente] | [Plazo largo; suspensión requiere garantía] | [Si liquidación >X EUR] |

---

## Estrategia recomendada

[Análisis razonado de la mejor opción según las circunstancias]

---

## Suspensión

**¿Procede solicitar la suspensión?** [Sí/No]
**Tipo:** [Automática con garantía (art. 233 LGT) / Sin garantía / Parcial]
**Garantía necesaria:** [tipo y cuantía estimada]
```

---

## Legislación de referencia

- LGT (Ley 58/2003) — arts. 131-159 (procedimientos de aplicación), arts. 207-212 (sanciones), arts. 226-249 (reclamaciones económico-administrativas)
- RGRVA (RD 520/2005) — Reglamento de revisión en vía administrativa
- LJCA (Ley 29/1998) — recurso contencioso-administrativo
- RGIT (RD 1065/2007) — Reglamento de gestión e inspección

---

## Lo que este skill NO hace

- No redacta el escrito de alegaciones o recurso — identifica la estrategia. Para redacción, indicar que se necesita el escrito.
- No presenta recurso ante ningún órgano — genera el análisis para decisión del profesional.
- No sustituye al abogado tributarista en procedimientos complejos de inspección — recomienda cuándo acudir a especialista.
