---
name: prompt-validator
description: Validar prompts dirigidos a agentes de IA (Claude Code, Cursor, Copilot, etc.) contra reglas de redacción efectiva. Calcular un porcentaje de efectividad del prompt y devolver sugerencias de mejora concretas, más una propuesta de prompt reescrito. Cubre verbos no imperativos, lenguaje conversacional, acciones vagas, términos subjetivos, alcance difuso, prohibiciones implícitas, intenciones múltiples y nombres genéricos. Las reglas de detalle técnico (alcance, nombres exactos) se aplican solo a prompts de implementación; en prompts funcionales (user stories, descripciones de comportamiento) se marcan N/A. Usar siempre que el usuario pida validar, revisar, auditar, mejorar, corregir o "pulir" un prompt antes de enviarlo a un agente, o cuando pegue un prompt y pida feedback sobre cómo está redactado.
license: MIT
---

# Skill: Validador de Prompts

Validar y mejorar prompts dirigidos a agentes de IA aplicando un conjunto fijo de **11 reglas de redacción imperativa**.

El skill **no** ejecuta el prompt ni produce el código pedido; **solo** audita la redacción y devuelve un informe accionable.

---

## Seguridad

- En todo el informe (transcripción, "Texto actual", prompt reescrito), **enmascarar** credenciales: API keys, PAT, contraseñas, tokens de sesión, claves privadas y valores tras `=` en variables de entorno → `[REDACTED]`.
- **Nunca** reproducir en el chat valores secretos que el usuario haya pegado en su prompt, aunque la cita sea para localizar un fragmento.
- Conservar el resto del texto del prompt tal cual (estructura, rutas, nombres de clase) para que el usuario pueda ubicar las sugerencias.

---

## Propósito

Auditar un prompt recibido del usuario y devolver:

1. Un **porcentaje de efectividad** del prompt (0–100%), basado en cuántas reglas evaluables cumple.
2. Una lista de **sugerencias de mejora** concretas, con: texto actual, propuesta de reemplazo y motivo. La regla aplicada se muestra como referencia discreta, no como acusación.
3. Una **propuesta de prompt reescrito** que aplique todas las sugerencias.

Usar cuando el usuario pida revisar, validar, mejorar o auditar un prompt; o cuando pegue un prompt en el chat y pida feedback sobre su redacción.

---

## Alcance

**Incluye:**

- Análisis de prompts dirigidos a agentes de código (Claude Code, Cursor, Copilot, Cline, etc.).
- Detección de las 11 oportunidades de mejora tipificadas en [Reglas](#reglas).
- Sugerencia concreta de reemplazo para cada oportunidad detectada.
- Cálculo del porcentaje de efectividad del prompt.
- Generación de un prompt reescrito final que integre todas las sugerencias.

**No incluye:**

- Ejecutar o cumplir el prompt (no escribir el código, middleware, refactor, etc. que el prompt pide).
- Evaluar la *corrección técnica* del contenido del prompt (si la solución pedida tiene sentido en el stack del usuario). El skill audita **redacción**, no **arquitectura**.
- Reglas distintas de las 11 listadas (estilo de redacción literaria, ortografía, gramática general).
- Validar prompts para imagen, audio o tareas no-código (el skill está calibrado a prompts de desarrollo).

---

## Entradas

Para ejecutar bien el skill, el agente necesita:

- **Obligatorio:** el **texto del prompt** a auditar, completo. Si el usuario pega secretos, el agente los trata internamente pero **no** los vuelca en la salida (ver [Seguridad](#seguridad)).
- **Opcional:**
  - **`type`** — declara explícitamente el tipo de prompt. Valores permitidos:
    - `Funcional` — describe comportamiento, criterios de aceptación (`BR-XX`, `SC-XX`), reglas de negocio o necesidad del usuario (p. ej. user stories, descripciones de feature, especificaciones de comportamiento). No requiere detalles técnicos como rutas, nombres de clase o archivos. **Las reglas de delimitar alcance y usar nombres exactos se marcan N/A.**
    - `Técnico` — solicita implementación, refactor o cambios concretos de código (p. ej. "crea AuthService", "refactoriza /features/auth"). **Las reglas de delimitar alcance y usar nombres exactos aplican plenamente.**

    El usuario puede declararlo de varias formas: `type: Funcional`, `type=Funcional`, `tipo=Funcional`, o en lenguaje natural ("es un prompt funcional", "este es técnico"). El agente reconoce ambas formas y normaliza variantes sin acento (`tecnico` → `Técnico`).

    Si **no se declara**, el agente lo **infiere** — ver paso 0 de [Ejecución del análisis](#ejecución-del-análisis).

  - Lenguaje/stack del proyecto (ayuda a juzgar si un nombre es "exacto" o genérico, p. ej. `AuthService` vs `un servicio`).
  - Si el usuario quiere **solo las sugerencias** o **también el prompt reescrito** (por defecto: ambos).
  - Si el prompt es **un fragmento** de uno mayor o **independiente** (un fragmento puede legítimamente referirse a contexto ya establecido).

Si el prompt llega como captura, imagen o referencia indirecta (p. ej. "el prompt que te pasé ayer"), **pedir** el texto del prompt antes de auditar. No inventar el contenido.

---

## Salidas

El skill **siempre** responde con esta estructura:

```
## Análisis del prompt

**Prompt analizado:**
> [transcripción del prompt; secretos como `[REDACTED]`]

**Tipo detectado:** Funcional | Técnico

**Efectividad: XX%**

**Reglas no evaluables:** [descripciones, ver reglas de formato abajo]

**Reglas cumplidas:** [descripciones, ver reglas de formato abajo]

### Sugerencias de mejora

**1. [Título corto de la mejora]**
- Texto actual: "<fragmento citado; secretos como `[REDACTED]`>"
- Propuesta: "<reemplazo concreto>"
- Por qué mejora: <explicación en 1 línea>
- *Regla: [nombre de la regla]*

[... una entrada por cada sugerencia, numeradas en orden de regla ...]

### Prompt reescrito (propuesta)

> [prompt completo aplicando todas las sugerencias]
```

Si el prompt **no tiene oportunidades de mejora**, omitir la sección "Sugerencias de mejora" y la propuesta reescrita; el bloque de cabecera (Tipo, Efectividad, Reglas no evaluables, Reglas cumplidas) se mantiene seguido de:

```
Sin sugerencias.
```

Si el usuario pidió **solo sugerencias** o **solo prompt reescrito**, devolver únicamente esa sección manteniendo el bloque de cabecera arriba.

### Reglas de formato para listas de reglas

Aplicar a `Reglas no evaluables`, `Reglas cumplidas` y a la cita `Regla:` dentro de cada sugerencia:

- **No mostrar códigos** (`R-1`, `R-2`, …): usar siempre el **nombre/descripción** de la regla (p. ej. `Usar verbos imperativos directos`).
- **No numerar** los elementos (sin `1.`, `2.`, …): el orden no aporta valor.
- **Siempre presentar como lista con viñetas**, una regla por línea, independientemente de la cantidad de elementos.
- **Separar cada bloque de cabecera con una línea en blanco** (`Tipo detectado`, `Efectividad`, `Reglas no evaluables`, `Reglas cumplidas`): sin línea en blanco el renderizador los fusiona en un mismo párrafo.
- En `Reglas no evaluables` se puede añadir un paréntesis breve aclarando el motivo cuando sea no obvio: p. ej. `Delimitar el alcance (N/A en prompt funcional)`.
- **R-9** se reporta siempre como bloque aparte `Mejora opcional · refinamiento de exclusividad` (no en `Reglas cumplidas` ni en `Sugerencias de mejora`), sin afectar el porcentaje.

**Ejemplo de formato:**

> **Reglas no evaluables:**
> - Delimitar el alcance (N/A en prompt funcional)
> - Usar nombres exactos (N/A en prompt funcional)
>
> **Reglas cumplidas:**
> - Usar verbos imperativos directos
> - Evitar lenguaje conversacional
> - Usar acciones específicas
> - Evitar términos subjetivos
> - Usar "NO" explícitos
> - Evitar instrucciones implícitas
> - Una intención por frase
> - Usar formato checklist para listas de tareas

### Cálculo de efectividad

- **Efectividad = (Reglas cumplidas / Reglas evaluables) × 100**, redondeado al entero más cercano.
- **Reglas evaluables** = de las 11, las que aplican al prompt. Descontar las marcadas como **N/A**:
  - R-5 y R-10 son **N/A** si el tipo de prompt es **Funcional**.
  - R-11 es **N/A** si el prompt no enumera ≥2 acciones.
  - Cualquier regla cuyo patrón no aplica al contenido del prompt.
- **R-9** (refinamiento opcional) **no entra** en el cálculo del porcentaje. Si aplica, se muestra como sugerencia separada bajo el título `Mejora opcional · refinamiento de exclusividad`, sin afectar la efectividad.

---

## Reglas

Las 11 reglas de auditoría. Cada una incluye el patrón a detectar y ejemplos MAL → BIEN.

### R-1 · Usar verbos imperativos directos

Detectar verbos en modo no-imperativo dirigidos al agente (`puedes`, `podrías`, `deberías`, `sería bueno que`, `tendrías que`).

- MAL: `Puedes crear un middleware`
- BIEN: `Crea un middleware`

### R-2 · Evitar lenguaje conversacional

Detectar fórmulas de cortesía o desiderativas dirigidas al agente (`me gustaría que`, `te pido que`, `necesito que por favor`, `quisiera`, `por favor`).

- MAL: `Me gustaría que implementes refresh tokens`
- BIEN: `Implementa refresh tokens`

### R-3 · Usar acciones específicas

Detectar verbos genéricos sin objeto concreto: `mejorar`, `optimizar`, `arreglar`, `pulir`, `revisar` cuando no van acompañados de **qué exactamente** y **cómo**.

- MAL: `Mejora la autenticación`
- BIEN: `Implementa refresh token con expiración automática a los 15 minutos`

### R-4 · Evitar términos subjetivos

Lista cerrada de términos ambiguos para un agente. Detectar:

`limpio`, `bonito`, `elegante`, `robusto`, `escalable`, `profesional`, `moderno`, `bien hecho`, `de calidad`, `idiomático`.

- MAL: `Hazlo limpio y moderno`
- BIEN: `Usa componentes pequeños (<150 líneas) y separación feature-based bajo /features`

Cada término subjetivo detectado **debe** convertirse en una restricción observable concreta en la sugerencia.

### R-5 · Delimitar el alcance

**Solo aplica a prompts de tipo Técnico.** En prompts **Funcionales** (descripciones de comportamiento, user stories, criterios de aceptación), la falta de ruta o módulo concreto no es una oportunidad de mejora: marcar la regla como **N/A** y excluirla del cálculo de efectividad.

Detectar instrucciones globales sin ruta, módulo o entidad concreta: `refactoriza el proyecto`, `revisa todo el código`, `actualiza el sistema`.

- MAL: `Refactoriza el proyecto`
- BIEN: `Refactoriza únicamente /features/auth`

### R-6 · Usar "NO" explícitos

Detectar prohibiciones tibias o sugeridas: `preferiblemente no`, `evita en lo posible`, `trata de no`, `intenta no usar`.

- MAL: `Preferiblemente no usar Redux`
- BIEN: `No uses Redux`

### R-7 · Evitar instrucciones implícitas

Detectar apelaciones a estándares no especificados: `buenas prácticas`, `código de calidad`, `como debe ser`, `siguiendo las convenciones`, `código limpio`, `SOLID` (sin más detalle).

- MAL: `Hazlo siguiendo buenas prácticas`
- BIEN (checklist explícito):
  - Evita lógica en componentes
  - Usa hooks para estado
  - Separa dominio e infraestructura

Cada apelación implícita debe convertirse en una lista de reglas explícitas en la sugerencia (con tu mejor inferencia razonable del contexto, marcando claramente que son suposiciones a confirmar).

### R-8 · Una intención por frase

Detectar frases que mezclan múltiples objetivos con `y aprovecha para`, `y de paso`, `y también`, `mientras tanto`, `además optimiza`.

- MAL: `Implementa autenticación y aprovecha para mejorar el routing y optimizar el código`
- BIEN (descompuesto):
  - `Implementa autenticación.`
  - `No modifiques routing global.`
  - `No optimices módulos no relacionados.`

### R-9 · Usar "solo / únicamente / exclusivamente"

Detectar instrucciones de alcance que **podrían** ser absolutas pero no llevan el cuantificador exclusivo. Aplicar **solo** cuando R-5 ya está cumplida (hay un alcance concreto) pero falta el refuerzo de exclusividad.

- ACEPTABLE: `Modifica archivos dentro de /auth`
- MEJOR: `Modifica únicamente archivos dentro de /auth`

Esta regla es de **refinamiento**: marcarla como `Mejora opcional · refinamiento de exclusividad` en el output y **no incluirla** en el cálculo del porcentaje de efectividad.

### R-10 · Usar nombres exactos

**Solo aplica a prompts de tipo Técnico.** En prompts **Funcionales** se usa lenguaje de dominio ("el flujo de autenticación", "el usuario", "la solicitud"), no nombres de clase, archivo o función: marcar la regla como **N/A** y excluirla del cálculo de efectividad.

Detectar sustantivos genéricos cuando el contexto permitiría un nombre específico: `un servicio`, `el componente`, `una clase`, `un método`.

- MAL: `Crea un servicio`
- BIEN: `Crea AuthService`

Si el prompt no contiene el contexto suficiente para sugerir un nombre exacto, marcar la sugerencia como `Crea <Nombre>Service` y pedir al usuario que rellene el nombre.

### R-11 · Usar formato checklist para listas de tareas

Detectar prompts que enumeran ≥2 acciones en una sola línea separadas por comas o `y` sin formato de lista.

- MAL: `Implementa middleware auth, hook useAuth y redirect a /login`
- BIEN:

  ```
  Implementa:
  - middleware auth
  - hook useAuth
  - redirect a /login
  ```

---

## Ejecución del análisis

Para cada prompt recibido, el agente debe:

0. **Determinar el tipo de prompt**:
   - **Si el usuario declaró `type` explícitamente** (p. ej. `type: Funcional`, `type=Tecnico`, `tipo=Funcional`, o en lenguaje natural como "este es un prompt funcional"), usar ese valor. Normalizar variantes sin acento (`tecnico` → `Técnico`, `funcional` → `Funcional`).
   - **Si no se declaró**, inferirlo:
     - **Funcional** si el prompt: usa lenguaje de comportamiento (`el sistema debe`, `el usuario puede`, `como ... quiero ... para ...`), describe criterios de aceptación (p. ej. `BR-XX`, `SC-XX`, Gherkin), casos de uso o reglas de negocio, y **no** menciona archivos, rutas, clases, funciones ni verbos de codificación.
     - **Técnico** si el prompt: pide implementar / refactorizar / crear / modificar / corregir código, menciona archivos, rutas, clases, funciones, endpoints, o usa verbos de codificación (`implementa`, `crea`, `refactoriza`, `migra`, `optimiza`, `arregla`).
     - Si es **ambiguo**, asumir **Técnico** (criterio más estricto: aplica más reglas).
   - **Declarar el tipo en el output**. Si fue **inferido** (no declarado), añadir la nota: *"Tipo inferido; declara `type: Funcional` o `type: Técnico` si quieres cambiarlo."*. Si fue **declarado**, no añadir nota.
1. **Leer el prompt completo** y separarlo en frases u oraciones.
2. **Aplicar las 11 reglas en orden**, frase por frase. Una misma frase puede activar varias sugerencias (p. ej. `Me gustaría que mejores el código de forma elegante` activa R-1, R-2, R-3 y R-4). Si el tipo es Funcional, **omitir** R-5 y R-10 (marcar N/A).
3. **Citar el fragmento** en el campo "Texto actual" de cada sugerencia, con la misma redacción que en el prompt salvo secretos (`[REDACTED]`). No parafrasear el fragmento original; sí parafrasear/reescribir en la propuesta.
4. **Producir la propuesta más concreta posible**. Si falta contexto (p. ej. para nombrar `AuthService`), proponer un placeholder explícito y pedir confirmación.
5. **Calcular la efectividad** según la fórmula en [Salidas › Cálculo de efectividad](#cálculo-de-efectividad).
6. **Generar el prompt reescrito** integrando todas las sugerencias, manteniendo la intención original del usuario. No añadir requisitos nuevos que el prompt no contemplaba. Aplicar la misma redacción de secretos que en [Seguridad](#seguridad).

---

## Antipatrones

Evitar al ejecutar este skill:

- **Cumplir el prompt** en lugar de auditarlo (p. ej. el usuario pega `Crea un middleware` y el agente crea el middleware).
- **Inventar sugerencias** que no derivan de las 11 reglas (no es un skill de estilo libre).
- **Aplicar R-5 o R-10 a un prompt Funcional**: en descripciones de comportamiento o user stories, la ausencia de rutas y nombres de clase es esperada, no una oportunidad de mejora. Marcar **N/A** y excluir del cálculo.
- **Penalizar el refinamiento opcional en la efectividad**: la regla de exclusividad (`solo`/`únicamente`) es refinamiento, no entra en el porcentaje.
- **Reescribir la intención** del prompt en la propuesta final (añadir features, cambiar el stack, decidir por el usuario decisiones de arquitectura no implicadas).
- **Parafrasear el "Texto actual"** de forma que el usuario no pueda localizar el fragmento en su prompt (salvo redacción de `[REDACTED]` en credenciales).
- **Reproducir credenciales** del prompt del usuario en la transcripción, en "Texto actual" o en el prompt reescrito.
- **Devolver solo la propuesta reescrita** sin las sugerencias (perdería valor pedagógico). Excepción: el usuario lo pide explícitamente.
- **Omitir la versión reescrita** salvo si el usuario lo pidió.
- **Omitir la efectividad** o sustituirla por `X/N`: el porcentaje es la métrica principal y debe aparecer siempre.
- **Auditar un prompt cuyo texto no se ha recibido** (no inferir, pedir).
- **Formular las sugerencias como acusaciones** ("incumples la regla X"): redactarlas como mejoras propuestas ("reemplaza ... por ...; reduce ambigüedad para el agente").
- **Mostrar códigos de regla (`R-1`, `R-2`, …) al usuario**: en el output usar el nombre/descripción de la regla, no el código. Los códigos son referencia interna de este documento.
- **Numerar `Reglas cumplidas` o `Reglas no evaluables`**: usar siempre viñetas, una regla por línea; no usar `1.`, `2.`, … ni separación por coma.
- **Mostrar el desglose `(X de N reglas evaluables cumplidas)`** junto a la efectividad: el porcentaje basta; la información de cuáles reglas se evaluaron ya está en `Reglas no evaluables` y `Reglas cumplidas`.

---

## Notas

### Cómo contar "reglas evaluables"

No todas las 11 reglas aplican a todos los prompts. En el bloque de efectividad:

- **Evaluables (N)** = reglas que aplican al prompt (entre 1 y 10, ya que R-9 nunca cuenta).
- **Cumplidas (X)** = evaluables sin sugerencia.
- **Efectividad** = `round((X / N) × 100)`.

Reglas que pueden ser **N/A** (y se excluyen de N):

- **R-5** y **R-10** si el tipo de prompt es **Funcional**.
- **R-11** si el prompt no enumera ≥2 acciones.
- Cualquier regla cuyo patrón no aparece en el contenido del prompt.

**R-9** nunca cuenta en N ni en X; si aplica, se reporta como sugerencia separada bajo `Mejora opcional · refinamiento de exclusividad` sin afectar el porcentaje.

### Tono de las sugerencias

Redactar cada sugerencia en clave de mejora, no de fallo:

- BIEN: *"Reemplaza el texto conversacional por un imperativo directo: reduce ambigüedad para el agente."*
- MAL: *"Incumples R-2 porque usas lenguaje conversacional."*

### Orden de presentación

Las sugerencias se numeran en el orden de las reglas (R-1 → R-11), no por severidad. R-9, si aplica, va al final como `Mejora opcional`.

### Detección del tipo de prompt

El parámetro `type` (`Funcional` o `Técnico`) lo declara el usuario. Solo si **no** lo declara, el agente lo infiere con esta heurística:

| Señal | Tipo |
|---|---|
| `como ... quiero ... para ...`, criterios de aceptación, "el sistema debe", "el usuario puede" | Funcional |
| Verbos imperativos de código (`implementa`, `crea`, `refactoriza`, `migra`), referencias a rutas/archivos/clases | Técnico |
| Mezcla ambigua o muy corto | Asumir Técnico |

Si el tipo fue **inferido**, declararlo en el output y ofrecer al usuario corregirlo en una nueva pasada con `type: Funcional` o `type: Técnico`.

### Prompts muy cortos

Para prompts ≤10 palabras (p. ej. `arregla esto`), priorizar R-3 (acción específica) y R-5 (alcance, si es Técnico) en las sugerencias; las demás reglas pueden ser N/A.

### Cuándo pedir contexto adicional

Pedir contexto al usuario **solo** si:

- El prompt referencia archivos, módulos o nombres que el agente no puede ver y la sugerencia depende de ellos (R-10, solo aplica a Técnico).
- El prompt apela a "buenas prácticas" (R-7) y el stack/dominio cambia radicalmente lo que esas prácticas son (p. ej. React vs Quarkus).
- El prompt llega indirectamente (captura, "el de ayer") y no se tiene el texto del prompt.

En el resto de casos, auditar con lo recibido y marcar suposiciones en las sugerencias.