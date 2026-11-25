---
name: claims
description: >
  Checker de claims de marketing — analiza afirmaciones publicitarias de un
  producto o servicio e identifica cuáles necesitan sustanciación, cuáles son
  potencialmente engañosas y cuáles deben eliminarse. Cubre publicidad engañosa
  (LCD art. 5), comparativa (LCD art. 10), influencers y prácticas comerciales
  desleales. Usar cuando el usuario diga "revisa estos claims", "¿podemos
  decir esto?", "copy del producto" o "publicidad".
argument-hint: "[pegar los claims o adjuntar material publicitario]"
---

# /claims

1. Cargar `~/.claude/plugins/config/claude-para-abogados/consumo/CLAUDE.md` → sector, tolerancia al riesgo, historial de claims.
2. Obtener el material publicitario o los claims.
3. Analizar claim por claim.
4. Generar tabla con clasificación y acción requerida.

```
/consumo:claims
"Nuestro producto es el más vendido de España"
"Ingredientes 100% naturales"
"Resultados garantizados en 30 días"
```

---

## Propósito

Los claims publicitarios son la primera línea de riesgo de consumo. Un claim sin sustanciación es publicidad engañosa (LCD art. 5). Un claim comparativo sin cumplir los requisitos es publicidad ilícita (LCD art. 10). Un influencer sin etiquetar la publicidad es práctica comercial desleal. Este skill revisa cada afirmación y clasifica el riesgo.

---

## Tipos de claims y marco legal

### Publicidad engañosa (LCD art. 5)

Es desleal la conducta que contenga información falsa o que, siendo veraz, por su contenido o presentación induzca o pueda inducir a error a los destinatarios. Se evalúa:
- Existencia, naturaleza y características del producto
- Precio o modo de cálculo
- Servicio posventa y garantía
- Necesidad de servicio o pieza
- Naturaleza, cualificación y derechos del empresario

### Publicidad comparativa (LCD art. 10)

Lícita solo si:
- No es engañosa
- Compara bienes o servicios que satisfacen las mismas necesidades
- Compara objetivamente características esenciales, pertinentes, verificables y representativas
- No desacredita ni denigra al competidor
- No se aprovecha indebidamente de la reputación del competidor
- No presenta el bien como imitación o réplica

### Prácticas comerciales con consumidores

- **Prácticas engañosas por acción** (LCD art. 5) — información falsa o que induce a error
- **Prácticas engañosas por omisión** (LCD art. 7) — ocultar información sustancial
- **Prácticas agresivas** (LCD art. 8) — coacción, acoso, influencia indebida

### Influencers y publicidad encubierta

- Toda publicidad debe ser identificable como tal (LCD art. 26)
- El influencer debe etiquetar el contenido patrocinado de forma clara y visible
- Código de conducta de Autocontrol sobre publicidad con influencers

---

## Análisis claim por claim

Para cada claim, evaluar:

| Campo | Pregunta |
|---|---|
| **Literalidad** | ¿Qué dice exactamente el claim? |
| **Tipo** | ¿Es objetivo (verificable) o subjetivo (opinión)? |
| **Sustanciación** | ¿Tiene respaldo documental/científico? |
| **Veracidad** | ¿Es verdad? ¿Puede demostrarse? |
| **Impresión global** | ¿Qué entiende el consumidor medio? |
| **Superlativos** | ¿Usa "el mejor", "el más", "el único"? → Necesita prueba |
| **Comparación** | ¿Compara con competidores? → Requisitos LCD art. 10 |
| **Salud/medio ambiente** | ¿Alega beneficios de salud o sostenibilidad? → Normativa sectorial |

---

## Clasificación de claims

| Clasificación | Significado | Acción |
|---|---|---|
| **CONFORME** | Claim veraz, sustanciado y lícito | Mantener |
| **MODIFICAR** | Necesita ajuste de redacción para evitar inducir a error | Reformular |
| **SUSTANCIAR** | Claim plausible pero sin documentación de respaldo | Aportar prueba o retirar |
| **RETIRAR** | Claim falso, no sustanciable o contrario a norma | Eliminar |

---

## Formato de salida

```markdown
# Revisión de claims: [Producto/Campaña]

**Fecha:** [fecha]
**Material revisado:** [descripción del material]
**Sector:** [alimentación / cosmética / tecnología / servicios / etc.]

---

## Resumen

**Claims revisados:** [N]
**Conformes:** [N] | **Modificar:** [N] | **Sustanciar:** [N] | **Retirar:** [N]

---

## Tabla de claims

| # | Claim | Tipo | Clasificación | Base legal | Acción requerida |
|---|---|---|---|---|---|
| 1 | "El más vendido de España" | Superlativo objetivo | SUSTANCIAR | LCD art. 5 | Aportar datos de ventas o reformular a "uno de los más vendidos" |
| 2 | "100% natural" | Objetivo | SUSTANCIAR | Rto. (CE) 1924/2006 si alimentación | Verificar que todos los ingredientes son naturales; definir "natural" |
| 3 | "Resultados garantizados" | Promesa de resultado | RETIRAR | LCD art. 5 | Promesa absoluta de resultado es engañosa si no se puede garantizar |

---

## Recomendaciones generales

[Observaciones transversales sobre el material publicitario]
```

---

## Claims de especial atención

| Tipo de claim | Normativa específica | Requisito |
|---|---|---|
| Alegaciones nutricionales/salud | Rto. (CE) 1924/2006 | Solo alegaciones autorizadas; base científica |
| Claims medioambientales (greenwashing) | Directiva (UE) 2024/825 | Sustanciación específica; sin genéricos ("ecológico", "verde") |
| "Gratis" / "gratuito" | LCD art. 5; LGDCU | Solo si realmente no hay coste para el consumidor |
| Testimonios | LCD art. 5 | Deben ser reales y representativos |
| Precios tachados / descuentos | Directiva Ómnibus (UE) 2019/2161 | Precio anterior = precio más bajo en los 30 días previos |

---

## Legislación de referencia

- LCD (Ley 3/1991) — arts. 4-8, 10, 26 (competencia desleal y publicidad)
- LGDCU (RDL 1/2007) — arts. 18-20 (publicidad e información)
- LSSI-CE (Ley 34/2002) — art. 20 (comunicaciones comerciales electrónicas)
- Reglamento (CE) 1924/2006 — alegaciones nutricionales y de salud
- Directiva (UE) 2024/825 — contra el greenwashing
- Directiva (UE) 2019/2161 — Ómnibus (precios tachados)

---

## Lo que este skill NO hace

- No valida claims sectoriales regulados (dispositivos médicos, medicamentos, productos financieros) — marca cuándo se necesita especialista.
- No diseña la campaña publicitaria — revisa el material existente.
- No sustituye el dictamen de Autocontrol — recomienda cuándo solicitarlo.
