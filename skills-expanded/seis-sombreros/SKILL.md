---
name: seis-sombreros
description: Análisis estructurado por Seis Sombreros de De Bono con sistema anti-ancla integrado y aislamiento estricto entre fases. Úsala cuando el usuario quiera analizar una funcionalidad compleja, evaluar una decisión difícil, desbloquear un conflicto de equipo, validar una propuesta técnica o comercial, hacer un pre-mortem, salir de un bloqueo de pensamiento, o pida "seis sombreros", "six hats", "6 sombreros", "análisis multi-perspectiva", "ayúdame a pensar", "rompe el ancla", "pros y contras en serio". Activar también ante "¿debería hacer X?" o tensión emocional+técnica+estratégica mezcladas.
---

# seis-sombreros

Implementación operativa del método de Edward de Bono con dos capas:

1. **Sistema anti-ancla** — ruptura obligatoria del sesgo antes de pensar.
2. **Seis sombreros secuenciales con aislamiento estricto** — un modo a la vez, sin contaminación cruzada.

## Cuándo NO usar esta skill

- Preguntas factuales simples.
- Tareas de ejecución pura (escribir código, redactar un email).
- Decisiones triviales o reversibles de bajo coste.
- Cuando el usuario pide opinión rápida sin querer proceso.

Si el problema cabe en 3 líneas, no lances esta skill.

---

## Fase 0 — Sistema Anti-Ancla (obligatoria)

Se ejecuta ANTES de los sombreros, siempre. No saltarla aunque haya prisa.

### 0.1 Detección de ancla

Evaluar si el usuario viene con solución pre-elegida. Señales:
- Verbaliza solución ("voy a hacer X", "creo que lo mejor es Y")
- Lleva 3+ turnos iterando sobre el mismo enfoque
- Vocabulario de compromiso ("ya decidí", "solo necesito confirmación")
- Pattern-matching propio del modelo (la primera idea que vino a la cabeza)

Si se detecta ancla, declararlo: "Detecto que vienes anclado en [X]. Voy a romper esa ancla antes de analizar."

Si no se detecta ancla, declararlo también: "No detecto ancla clara. Ejecuto la ruptura igualmente como medida preventiva."

### 0.2 Ruptura del ancla — 4 movimientos en orden

**Movimiento 1 — Re-formulación pura:**
Reescribir el problema SIN asumir el enfoque actual. Solo objetivo + restricciones. Prohibido incluir la solución implícita. Test: ¿alguien que lea la reformulación podría llegar a una solución completamente distinta? Si no, reescribir.

**Movimiento 2 — Asunción fundacional:**
Identificar la creencia invisible que sostiene el enfoque del usuario. Formular test de falsación: "Esta asunción sería falsa si...".

**Movimiento 3 — Steel-man del opuesto:**
Construir el mejor argumento posible a favor de NO hacer lo propuesto, o de hacer lo contrario. Versión fuerte, no caricatura. Test: ¿alguien inteligente que defendiera esa posición se sentiría representado?

**Movimiento 4 — Pre-mortem rápido:**
Imaginar que el enfoque ha fracasado en 6-12 meses. Identificar los 3 modos de fallo más probables.

### 0.3 Clasificación del problema

Determinar variante de sombreros según tipo. Ver `references/variants.md`:
- Funcionalidad de producto → Variante 2
- Conflicto de personas → Variante 3
- Pre-mortem → Variante 4
- Desbloqueo creativo → Variante 5
- Decisión irreversible de alto coste → Variante 6
- General → Variante 1

---

## Reglas de aislamiento (no negociables)

1. **Un sombrero a la vez.** Nunca mezclar dos modos en la misma sección.
2. **Aislamiento estricto.** Mientras se lleva un sombrero, el resto NO existen. Si aparece contenido de otro sombrero, descartarlo o guardarlo para su fase. Cada sombrero debe ser monolítico.
3. **El Azul abre y cierra siempre.** Sin Azul de apertura no se empieza.
4. **Sin justificación en el Rojo.** Si aparece "porque..." en el Rojo, la frase es inválida.
5. **El Negro es lógica negativa, no pesimismo.** Solo riesgos verificables. No "no me gusta" (eso es Rojo).
6. **El Amarillo exige respaldo lógico.** Cada beneficio debe poder defenderse con un argumento.
7. **El Verde usa marcos divergentes.** Ver `references/divergence-frameworks.md`. Mínimo 3 marcos distintos, mínimo 1 provocación radical.
8. **No cambiar de sombrero a mitad de fase.** Si una fase queda corta, se cierra y se pasa.
9. **Si no hay material para una fase, declararlo.** "No encuentro riesgos sólidos" es información valiosa. No rellenar con contenido falso.

---

## Sombrero Azul (apertura)

Definir:
- **Pregunta exacta** reformulada por la skill (no copiada del usuario).
- **Restricciones** conocidas.
- **Criterio de éxito**: ¿cómo sabremos que la conclusión es buena?
- **Orden de sombreros** elegido y por qué.

Fase corta (4-8 líneas). Si falta contexto, parar y preguntar.

---

## Sombrero Blanco

Solo hechos, en dos categorías:
- **Hechos verificados** (datos, métricas, restricciones objetivas del contexto del usuario).
- **Hechos creídos pero no verificados** (asunciones no demostradas).

Listar **vacíos de información** si faltan datos críticos. No rellenar con suposiciones. Todo lo que no esté en el contexto explícito del usuario va en "creídos" o en "vacíos".

---

## Sombrero Amarillo

Beneficios con respaldo lógico:

> **Beneficio:** [descripción] — **Por qué es plausible:** [razonamiento]

Mínimo 3, máximo 7. Si no hay 3 defendibles, declararlo. PROHIBIDO mencionar riesgos, matizar con "aunque..." o añadir advertencias. Eso pertenece al Negro.

---

## Sombrero Negro

Riesgos concretos con evaluación:

> **Riesgo:** [descripción] — **Probabilidad/impacto:** [bajo/medio/alto] — **Por qué:** [razonamiento]

Mínimo 3, máximo 7. Sé severo. Este es el sombrero más valioso y el que más se diluye por instinto de complacencia. PROHIBIDO suavizar con condicional ("podría quizá..."). Enunciar con seguridad: "Esto fallará cuando...". PROHIBIDO mencionar beneficios u oportunidades.

---

## Sombrero Verde

Alternativas creativas usando marcos divergentes de `references/divergence-frameworks.md`.

Reglas:
- Mínimo **5 alternativas ejecutivamente distintas** (cambian el qué o el cómo fundamental, no solo el stack o el color del botón).
- Usar mínimo **3 marcos diferentes** del catálogo de 10.
- Al menos **1 provocación radical** (inversión total, eliminación del problema, constraint shock extremo).
- **No pre-juzgar.** La crítica no es trabajo del Verde. PROHIBIDO decir "esta no es viable" o "esta es la mejor".
- Test de distinción: ¿el coste y el resultado de dos alternativas son distintos? Si no, son la misma. Eliminar duplicados.

Formato por alternativa:
> **Alt N — [Nombre corto]** *(Marco: [letra+nombre])* — [2-3 líneas de descripción] — Insight clave: [1 línea].

---

## Sombrero Rojo

Reacciones emocionales e intuitivas sin justificación. Frases cortas, directas, viscerales.

Ejemplos válidos:
- "Esto huele a trampa."
- "Algo en la opción 3 me entusiasma sin saber por qué."
- "Cansancio anticipado solo de leer el scope."
- "No me fío."

**Prohibido escribir "porque..." en esta fase.** Si aparece, la frase es inválida. Máximo 8 frases.

---

## Sombrero Azul (síntesis) — Convergencia con matriz

Estructura fija:

### 1. Mapa del terreno
3-5 líneas resumiendo lo que sabemos tras los 6 sombreros.

### 2. Tensiones detectadas
Dónde el Negro y el Amarillo chocan. Dónde el Rojo no encaja con la lógica.

### 3. Matriz de decisión
Definir 3-5 criterios **específicos del problema** (no genéricos como "viabilidad"). Puntuar las alternativas del Verde:

| Alternativa | Criterio 1 | Criterio 2 | Criterio 3 | Trade-off principal |
|---|---|---|---|---|
| Alt 1 | Alto | Medio | Bajo | [trade-off] |

Test de criterios: ¿puedes asignar Alto/Medio/Bajo con justificación verificable? Si no, operacionaliza mejor el criterio.

### 4. Recomendación accionable
UNA opción priorizada + pasos concretos siguientes. No tres opciones. Una. Si no puedes elegir, declara qué dato te falta.

### 5. Plan B
Segunda opción + condición de activación ("activar Plan B si...").

### 6. Métricas de revisión
Evidencia concreta que haría revisar la elección en 1-3 meses.

### 7. Vacíos pendientes
Información del Blanco que sigue faltando y debería conseguirse antes de ejecutar.

---

## Formato de salida

```
## Fase 0 — Anti-Ancla
[detección + 4 movimientos de ruptura]

## Sombrero Azul (apertura)
[definición del problema]

## Sombrero Blanco
[hechos]

## Sombrero Amarillo
[beneficios]

## Sombrero Negro
[riesgos]

## Sombrero Verde
[alternativas con marcos]

## Sombrero Rojo
[emociones]

## Sombrero Azul (síntesis)
[mapa + tensiones + matriz + recomendación + plan B + métricas]
```

El orden de presentación varía según la variante elegida (ver `references/variants.md`).

---

## Output empaquetado e integración con el OS

Si el análisis es relevante para guardar (decisión importante, análisis que se va a compartir con socio/equipo/cliente):

- **Guardar** en `projects/seis-sombreros/<YYYY-MM-DD>-<tema-corto>.md` con el análisis completo.
- **Si el usuario lo va a compartir** (con socio, equipo, asesor), invocar `tool-visual-explainer` para empaquetar en HTML compartible.
- **Si cierra con una decisión efectiva**, append en `context/decisions-log.md` con la decisión final.
- **Si la sesión enseñó algo no obvio** sobre cómo el usuario piensa (preferencias, sesgos, valores), append en `context/learnings.md` bajo `## seis-sombreros`.

## Skills relacionadas

- **`tool-visual-explainer`** (opcional) — empaquetar análisis en HTML compartible.
- **`decisions-log`** (opcional) — registrar decisión final append-only.
- **`metodo-ias`** — si durante la fase I del método I.A.S. aparece una decisión grande, invocar seis-sombreros antes de congelarla.

---

## Checklist antes de entregar

- [ ] ¿Fase 0 (anti-ancla) ejecutada con los 4 movimientos?
- [ ] ¿Ancla detectada y declarada (o ausencia declarada)?
- [ ] ¿Las 7+ secciones presentes y en el orden correcto de la variante?
- [ ] ¿El Negro tiene al menos 3 riesgos reales y no diluidos?
- [ ] ¿El Verde tiene al menos 5 alternativas con 3+ marcos distintos?
- [ ] ¿El Verde incluye al menos 1 provocación radical?
- [ ] ¿El Rojo está libre de "porque..."?
- [ ] ¿La síntesis incluye matriz con criterios operacionalizables?
- [ ] ¿La síntesis da UNA recomendación + Plan B?
- [ ] ¿Hay contaminación cruzada entre sombreros? Si la hay, reescribir esa sección.

Si algún punto falla, reescribir antes de entregar.

---

## Edge cases

- **Pregunta demasiado vaga** ("¿qué hago con mi vida?"): aplicar primero el sombrero Azul para acotar. Si no se acota, sugerir mentoría, no análisis.
- **Pregunta puramente operativa** ("¿qué color de botón uso?"): los 6 sombreros son overkill. Sugerir decidir directamente o usar A/B test.
- **Usuario emocionalmente cargado** (acaba de perder cliente, contrato roto): NO aplicar inmediatamente. Pedir 24h de cooldown — el sombrero Rojo en caliente sesga el resto.
- **Decisión ya tomada**: el usuario quiere validación, no análisis. Aplicar solo Variante 4 (pre-mortem) en lugar del flujo completo.
- **Tiempo limitado** (<5 min disponibles): usar Variante 7 (condensada) con aviso explícito de qué se sacrifica.

---

## Referencias

- `references/variants.md` — 7 órdenes alternativos según tipo de problema.
- `references/divergence-frameworks.md` — Catálogo de 10 marcos para el Sombrero Verde.
- `references/anti-patterns.md` — Errores comunes (ancla + sombreros).
- `references/examples.md` — Ejemplos completos de aplicación.
