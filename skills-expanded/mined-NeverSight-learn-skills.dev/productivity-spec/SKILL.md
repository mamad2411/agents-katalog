---
name: productivity-spec
description: Guía al usuario a través de un proceso estructurado para transformar una historia de usuario en una especificación técnica completa. Incluye Fase 0 de clasificación de stack (carga automática de dev-kits), identificación de suposiciones, validación iterativa con detección de contradicciones, y generación de especificación final con estructura de proyecto y checklist de pendientes. Usar cuando el usuario proporcione una historia de usuario o necesite crear una especificación técnica a partir de requisitos ambiguos.
requires-devkits: auto-detect
---

# Productivity Spec — Historia de Usuario a Especificación Técnica

## Propósito

Guiar al usuario a través de un proceso estructurado para transformar una historia de usuario en una especificación técnica completa, mediante la identificación de suposiciones, validación iterativa y refinamiento colaborativo.

---

## Instrucciones del Agente

### Fase 0: Clasificación del Stack

Antes de hacer suposiciones técnicas, identifica el stack del proyecto:

1. Pregunta al usuario en un solo mensaje:
   - **Stack**: ¿Qué tecnologías usarán? (ej: "React + Node.js + PostgreSQL", ".NET + SQL Server + React + Ant Design")
   - **Plataforma**: ¿Web, móvil (Flutter), o ambos?
   - **Infraestructura**: ¿On-premise, Azure, AWS, GCP?

2. Carga los dev-kits relevantes según la respuesta:
   - Backend .NET → `dotnet-core`, `dotnet-api`, `dotnet-ef-core`
   - Backend Node.js → `nodejs-core`, `nodejs-express`, `nodejs-database`
   - Backend Python → `python-core`, `python-fastapi`, `python-database`
   - Frontend React + Ant Design → `react-core`, `react-antdesign`
   - Frontend React + Tailwind → `react-core`, `react-components`
   - SQL Server → `sql-server-core`
   - PostgreSQL → `postgresql-core`
   - DevOps → `devops-core`, `devops-cicd`

3. Las suposiciones técnicas (autenticación, API design, esquema de BD) se basan en el dev-kit cargado.
   Ej: si el stack es .NET + SQL Server, las suposiciones sobre auth usan `dotnet-security` (JWT Bearer con OAuth2).
   Si es Node.js + PostgreSQL, usan `nodejs-security` (JWT con jsonwebtoken).

### Fase 1: Recepción de la Historia de Usuario

Cuando el usuario te proporcione una historia de usuario:

1. Analiza la historia en profundidad.
2. Identifica todos los espacios en blanco (requisitos funcionales y no funcionales no definidos explícitamente).
3. Completa los espacios en blanco con suposiciones razonables basadas en contexto estándar de la industria.
4. Genera la primera versión de la especificación con los espacios rellenos.

### Fase 2: Listado de Suposiciones

Presenta al usuario un **listado numerado** de todas las suposiciones **no técnicas o no funcionales** que hayas asumido para rellenar los espacios en blanco. Por ejemplo:

- Suposiciones sobre audiencia objetivo
- Suposiciones sobre flujos de trabajo preferidos
- Suposiciones sobre prioridades de negocio
- Suposiciones sobre restricciones regulatorias o de marca
- Suposiciones sobre comportamiento esperado del usuario final

**Formato obligatorio:**

```markdown
## Suposiciones Asumidas (No Técnicas / No Funcionales)

1. [Descripción clara de la suposición]
2. [Descripción clara de la suposición]
...
N. [Descripción clara de la suposición]
```

### Fase 3: Selección y Refinamiento Iterativo

**Principio de eficiencia:** Si dos o más suposiciones son de dominios independientes (ej: una sobre UX y otra sobre BD), pueden preguntarse juntas en el mismo turno para reducir rounds.

El usuario te indicará qué números de suposiciones no le gustaron. Para cada una:

1. **Muestra una barra de progreso** indicando:
   - Preguntas respondidas hasta el momento
   - Preguntas totales pendientes

2. **Formula UNA pregunta a la vez** para clarificar esa suposición específica.

3. **Presenta 4 opciones de asunciones alternativas** + 1 opción "Otra":
   - Opción A: [Alternativa 1]
   - Opción B: [Alternativa 2]
   - Opción C: [Alternativa 3]
   - Opción D: [Alternativa 4]
   - Opción E: **Otra** (el usuario especificará su respuesta)

4. Espera la respuesta del usuario antes de pasar a la siguiente pregunta.

**Detección de contradicciones:** Después de cada respuesta, verifica consistencia con respuestas previas. Si detectas conflicto (ej: pregunta 1 eligió "sin autenticación" y pregunta 5 pide "dashboard por usuario"), alerta: "⚠️ Esta respuesta contradice tu elección anterior en la pregunta 1 (sin autenticación). ¿Quieres revisar alguna de las dos?"

**Formato de la barra de progreso:**

```markdown
[████░░░░░░] Progreso: X de Y preguntas completadas
```

### Fase 5: Generación de la Especificación

Al confirmar el usuario, genera la especificación final con:

1. **Resumen funcional**: qué hace el sistema, para quién, flujo principal.
2. **Stack tecnológico**: tecnologías elegidas con referencia a los dev-kits cargados.
3. **Estructura de proyecto sugerida**: árbol de directorios basado en la arquitectura del dev-kit:
   - .NET → estructura Clean Architecture (`dotnet-architecture`)
   - Node.js → estructura Vertical Slices (`nodejs-architecture`)
   - React → estructura feature-based Next.js o Vite (`react-architecture`)
   - Python → estructura FastAPI (`python-core`)
4. **Especificación técnica**: endpoints, modelos de datos, componentes, flujos.
5. **Lo que queda por definir**: checklist de temas no cubiertos en las preguntas (rate limiting, i18n, a11y, backups, CI/CD, monitoreo).

**Formato de salida**: markdown estructurado listo para copiar a un README o documento de arquitectura.

---

## Restricciones

- Solo se presenta **UNA pregunta por turno**.
- Las alternativas deben ser **mutuamente excluyentes y concretas**.
- Nunca generes la especificación final sin confirmación explícita del usuario.
- Si el usuario selecciona "Otra", espera su definición específica antes de continuar.

---

## Ejemplo de Flujo

**Usuario:** "Como usuario quiero poder registrarme en la plataforma"

**Agente:**

```markdown
## Especificación Preliminar
[...espacios rellenos...]

## Suposiciones Asumidas (No Técnicas / No Funcionales)
1. El registro será mediante email y contraseña
2. No se requiere verificación de correo inmediata
3. El usuario debe ser mayor de 18 años
4. Se permiten caracteres especiales en la contraseña
5. El flujo es de un solo paso (no wizard)
```

**Usuario:** "No me gustan la 1, la 3 y la 5"

**Agente:**

```markdown
[░░░░░░░░░░] Progreso: 0 de 3 preguntas completadas

Pregunta 1 de 3: ¿Qué métodos de registro debería soportar la plataforma?

A. Email y contraseña únicamente
B. Email/contraseña + Google OAuth
C. Email/contraseña + Google + GitHub
D. Solo redes sociales (sin email)
E. Otra (especifica tu respuesta)
```

**Usuario:** "B"

**Agente:**

```markdown
[████░░░░░░] Progreso: 1 de 3 preguntas completadas

Pregunta 2 de 3: ¿Qué restricción de edad debería aplicarse?

A. Mayor de 18 años
B. Mayor de 13 años (COPPA)
C. Mayor de 16 años
D. Sin restricción de edad
E. Otra (especifica tu respuesta)
```

...y así sucesivamente hasta completar las 3 preguntas.

---

## Notas de Implementación

- Mantén el tono profesional y colaborativo.
- Si el usuario no selecciona ninguna suposición para corregir, salta directamente a la Fase 4.
- Las alternativas deben cubrir el espectro más probable de respuestas para minimizar la selección de "Otra".
- Documenta cada respuesta del usuario para construir la especificación final.
