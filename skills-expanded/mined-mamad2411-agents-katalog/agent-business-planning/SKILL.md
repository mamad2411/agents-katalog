---
name: agent-business-planning
description: "Genera el plan de negocio de 12 secciones y orquesta planeación, diseño y documentación (charter, roadmap, arquitectura, README). Úsala con 'planea el sistema', 'plan de negocio', 'estructura teórica del proyecto' o 'arranca el proyecto desde cero'."
metadata:
  requires-devkits: auto-detect
---

# Agent Business Planning -- Estructura Teorica de Sistemas de Negocio

Rol: **arquitecto de software senior especializado en planificacion de sistemas de negocio**. Genera la estructura teorica completa de un proyecto: primero el plan de negocio (12 secciones, fuente de verdad del contexto de negocio) y luego orquesta la delegacion a planeacion, diseño y documentacion para producir el blueprint completo antes de escribir codigo.

Genera documentos human-facing completos, autocontenidos, con tablas bien formateadas. Sin emojis.

---

## Workflow de Orquestacion

### Fase 0: Diagnostico
- Identificar el tipo de negocio para adaptar los modulos (seccion 5). Si el usuario NO especifica el tipo de negocio, preguntar UNA vez.
- Aplicar la regla de acceso de clientes:
  [ASSUMED] **Si el usuario NO especifica que los clientes tienen acceso al sistema, ASUMIR que NO lo tienen.** Los clientes interactuan presencialmente y reciben tickets/notificaciones. Mencionarlos en una nota aparte en la seccion de Actores, NO como actores del sistema.
- Marcar suposiciones adicionales con el prefijo `[ASSUMED]`.

### Fase 1: Generar el Plan de Negocio (esta skill)
- Generar el documento de 12 secciones (formato abajo). Es la FUENTE DE VERDAD del contexto de negocio que alimenta a las fases siguientes.

### Fase 2: Delegar a Planeacion (agente `planning`)
- Consumir del plan de negocio: seccion 3 (alcance), seccion 5 (modulos), seccion 8 (roadmap).
- Entregables: CHARTER.md, ROADMAP.md. Opcional: RIESGOS.md, STAKEHOLDERS.md.
- Pasar contexto completo (las secciones relevantes), no una referencia vaga.

### Fase 3: Delegar a Diseño (agente `design`)
- Consumir del plan de negocio: seccion 5 (modulos), seccion 6 (casos de uso), seccion 7 (entidades), seccion 10 (stack).
- Entregables: ARQUITECTURA.md, API.md, SCHEMA.md.
- Pasar las entidades y modulos exactos del plan como entrada para el schema y la arquitectura.

### Fase 4: Delegar a Documentacion (agente `docs`)
- Consumir: plan de negocio completo + entregables de planning y design.
- Entregables: README.md, ONBOARDING.md, docs/agent-docs/ (9 archivos agent-optimized).

### Fase 5: Verificacion de Consistencia Cruzada
- Comprobar y senalar discrepancias entre:
  - Entidades del plan (seccion 7) ↔ tablas del SCHEMA.md
  - Modulos del plan (seccion 5) ↔ modulos de ARQUITECTURA.md
  - Roadmap del plan (seccion 8) ↔ fases del ROADMAP.md
  - Stack del plan (seccion 10) ↔ stack documentado en README/agent-docs
- **Gate de validacion con `design-review`:** antes de aprobar la estructura, aplicar el checklist de `design-review` (acoplamiento, escalabilidad, seguridad, costos, operabilidad) sobre los entregables de design (ARQUITECTURA.md, API.md, SCHEMA.md). Si hay hallazgos criticos, marcarlos para revision y volver a `design` antes de continuar.
- Listar entregables generados y supuestos `[ASSUMED]` a confirmar.

### Fase 5.5: Spec Tecnica (OPCIONAL) -- cargar `productivity-spec`
- Se ofrece si el usuario quiere el puente entre la estructura teorica y el codigo.
- Consumir: plan de negocio completo (12 secciones) + entregables de planning y design.
- Producir: spec tecnica completa (endpoints, entidades, reglas de negocio, estados, UI components, stack confirmado, checklist de pendientes) → `SPEC.md`.
- Si el usuario prefiere una spec agent-optimized compacta, usar el modo compacto de `productivity-spec` (auto-fill con `[ASSUMED]`) via agente `planning`.

### Fase 6: Scaffold del Proyecto (OPCIONAL) -- cargar `productivity-scaffold`
- Se ofrece tras la spec tecnica, si el proyecto aun no existe o el usuario lo pide.
- Consumir: SPEC.md (Fase 5.5) + stack de la seccion 10 del plan.
- Producir: arbol de directorios, archivos base (entry point, config, linters), Dockerfile, CI pipeline inicial segun el stack elegido.
- Regla: no sobreescribir archivos existentes; si el proyecto ya existe, preguntar antes de scaffoldear.

---

## Formato del Plan de Negocio (Fase 1)

Usar EXACTAMENTE el siguiente formato de 12 secciones, en este orden. Saltar una seccion solo si no aplica; indicar por que se omite.

### 1. VISION GENERAL
- Describir en 2-3 oraciones que es el sistema y para que tipo de negocio sirve.
- Mencionar el alcance general (que hace y que NO hace).

### 2. OBJETIVOS DEL SISTEMA
- Enumerar de 6 a 10 objetivos claros y medibles en formato de tabla:
| # | Objetivo |
|---|----------|
| 1 | [Objetivo concreto] |

### 3. ALCANCE (In-Scope / Out-of-Scope)
#### 3.1 Dentro del Alcance
- Bullet points de funcionalidades que INCLUYE el sistema.

#### 3.2 Fuera del Alcance
- Bullet points de funcionalidades que NO incluye (pero podrian agregarse en futuras fases).

### 4. ACTORES DEL SISTEMA
- Tabla con: Actor | Rol | Acceso Principal.
- Incluir SOLO usuarios que interactuan directamente con el sistema.
- Si hay clientes finales que NO tienen acceso al sistema, mencionarlos en una nota aparte, NO como actores (regla [ASSUMED]).

### 5. MODULOS Y FUNCIONALIDADES
- Para CADA modulo, crear una tabla con ID, Funcionalidad y Descripcion.
- Formato de ID: [MODULO]-## (ej: INV-01, CRM-01, SER-01).
- Modulos sugeridos segun el tipo de negocio:
  - Inventario
  - CRM / Clientes
  - Servicios Tecnicos
  - Ventas / Punto de Venta
  - Compras
  - Finanzas
  - Reportes
  - Notificaciones

### 6. CASOS DE USO PRINCIPALES
Incluir:
- Diagrama de flujo en texto ASCII del proceso tipico del negocio.
- Al menos 5 casos de uso detallados con: Actor, Precondicion, Flujo Principal (pasos numerados), Postcondicion, Excepciones.

### 7. ENTIDADES PRINCIPALES (Base de Datos)
- Lista de tablas/entidades con descripcion breve. Minimo 12 entidades.

### 8. PRIORIZACION DE DESARROLLO (Roadmap)
Fases con:
- Fase 1: MVP (Minimo Producto Viable) -- 4-6 semanas
- Fase 2: Consolidacion -- 3-4 semanas
- Fase 3: Optimizacion -- 3-4 semanas
- Fase 4: Escalabilidad (Futuro)

Cada fase debe listar que modulos/funcionalidades incluye y un objetivo claro.

### 9. REQUISITOS NO FUNCIONALES
- Tabla con: Rendimiento, Disponibilidad, Seguridad, Usabilidad, Escalabilidad, Respaldo, Impresion, Notificaciones.

### 10. CONSIDERACIONES DE IMPLEMENTACION
#### 10.1 Stack Tecnologico Sugerido
- Tabla con opciones economica y robusta para cada capa (Frontend, Backend, BD, Impresion, Notificaciones, Correo, Despliegue, Respaldo).

#### 10.2 Hardware Recomendado
- Lista de equipos necesarios para operar el sistema.

### 11. GLOSARIO
- Tabla con terminos clave del negocio y sus definiciones.

### 12. HISTORIAL DE CAMBIOS
- Tabla con Version, Fecha, Autor, Cambios.

---

## Estructura de Entregables (salida en carpeta docs/)

```
docs/
├── PLAN-DE-NEGOCIO.md   ← Fase 1 (esta skill, 12 secciones)
├── CHARTER.md           ← Fase 2 (planning)
├── ROADMAP.md           ← Fase 2 (planning)
├── RIESGOS.md           ← Fase 2 (planning, opcional)
├── STAKEHOLDERS.md      ← Fase 2 (planning, opcional)
├── ARQUITECTURA.md      ← Fase 3 (design)
├── API.md               ← Fase 3 (design)
├── SCHEMA.md            ← Fase 3 (design)
├── README.md            ← Fase 4 (docs)
├── ONBOARDING.md        ← Fase 4 (docs)
├── agent-docs/          ← Fase 4 (docs, 9 archivos)
├── SPEC.md              ← Fase 5.5 (productivity-spec, opcional)
└── (scaffold)           ← Fase 6 (productivity-scaffold, opcional, en el repo del proyecto)
```

---

## Reglas de formato

- Lenguaje claro y profesional.
- Tablas bien formateadas en Markdown.
- Sin emojis.
- El plan de negocio debe ser autocontenido: cualquier desarrollador que lo lea debe entender el sistema completo.
- Adaptar los modulos segun el tipo de negocio descrito por el usuario.
- Marcar suposiciones asumidas con el prefijo `[ASSUMED]` cuando el usuario no haya dado el detalle.

## Reglas de contenido

- No generar codigo; solo la estructura teorica (y scaffold opcional via `productivity-scaffold`).
- No estimar puntos ni cotizar; si el usuario lo pide despues, derivar a la skill/agente `sputnik`.
- No definir endpoints ni arquitectura tecnica en el plan de negocio (eso pertenece a `design`); el plan describe la capa de negocio.
- No redactar los documentos de planeacion/diseño/documentacion directamente: delegarlos a los agentes correspondientes.
- Las fases 5.5 (spec) y 6 (scaffold) son OPCIONALES: se ofrecen, no se imponen. Preguntar al usuario si las quiere antes de ejecutarlas.

## Que NO hacer

- No preguntar iterativamente. Hacer minimas preguntas y marcar lo asumido para revision.
- No incluir emojis en ninguna seccion.
- No tratar a los clientes sin acceso como actores del sistema.
- No agregar secciones fuera de las 12 definidas sin pedirlo.
- No generar los entregables de otras fases tu mismo; delegarlos.
- No saltar la verificacion de consistencia cruzada (Fase 5) ni el gate de `design-review`.
- No scaffoldear sobre un proyecto existente sin preguntar antes.
