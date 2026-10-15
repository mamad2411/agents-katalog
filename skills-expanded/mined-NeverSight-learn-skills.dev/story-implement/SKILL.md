---
name: story-implement
description: Usar al pedir implementar, desarrollar o ejecutar trabajo referenciado por una historia de usuario o tarea. Solo debe usarse si la historia o tarea se encuentra en estado `Ready`. Activar tambien cuando el usuario mencione "ejecutar tareas", "codificar", "desarrollar la US", "trabajar en el TK" o cualquier variante que implique escribir codigo para una historia o tarea ya especificada.
license: MIT
---

# Skill: Implementar historia de usuario

Guia para **ejecutar en codigo** el trabajo especificado en historias `US-XXX` y tareas `TK-XXX` bajo `docs/specs/user-stories/`.

> **Alcance:** consume especificaciones ya redactadas por **story-plan**. No reescribe ni reestructura tareas - solo las implementa. Correcciones menores acordadas con el usuario son la unica excepcion.
>
> **Ritmo obligatorio - una tarea por confirmacion:** implementar una TK, actualizar `progress.md`, ejecutar lint, y **esperar confirmacion explicita del usuario antes de arrancar la siguiente**. Sin excepcion.
>
> **Solo implementacion:** no modifica documentacion de producto (`README.md` de US, `TK-XXX`, ADRs, technical-docs) - solo `progress.md`. Si se detecta un conflicto en la documentacion que pueda afectar el resultado, **parar inmediatamente y notificar al usuario** antes de continuar.
>
> **Handoffs:** Entrada minima: US y TK en `Ready`; salida: `progress.md` en `Done` y working tree limpio => **`story-integrate`**.

---

## Agentes condicionales

| Condicion | Agente / Skill requerido |
| --------- | ------------------------ |
| La tarea genera o modifica archivos de UI (HTML, CSS, componentes) | Ejecutar bajo el agente `ui-specialist` |
| La referencia de diseno es un enlace o archivo de Figma | Usar el **MCP de Figma** para obtener el contexto del diseno antes y durante la implementacion |
| Fase final de pruebas (Paso 4) aceptada por el usuario | Ejecutar bajo el agente **`quality-specialist`** - no escribir tests desde este skill |

Ambas condiciones pueden aplicar a la vez. Si la tarea no involucra UI, implementar directamente sin delegar.

---

## Ubicacion de archivos

| Artefacto | Ruta |
| --------- | ---- |
| Historia de usuario | `docs/specs/user-stories/US-XXX-[nombre-corto]/README.md` |
| Tareas | `docs/specs/user-stories/US-XXX-[nombre-corto]/TK-XXX-[nombre].md` |
| Progreso | `docs/specs/user-stories/US-XXX-[nombre-corto]/progress.md` |
| Unidades de trabajo | `docs/specs/work-units.md` |
| Glosario | `docs/specs/glossary.md` |

---

## Informacion requerida antes de implementar

| Dato | Como obtenerlo | Si no esta disponible |
| ---- | -------------- | --------------------- |
| **US padre** | Indicada por el usuario o inferida de la ruta | Preguntar a que `US-XXX` pertenece; no implementar hasta tenerla |
| **Alcance** | Del mensaje del usuario: toda la US, una lista de TK, o un TK concreto | Preguntar si hay ambiguedad |
| **Unidad de trabajo** | Campo `Unidad de trabajo` de cada TK; complementar con `work-units.md` si no es claro | Preguntar al usuario; no asumir |
| **Working tree limpio** | `git status --porcelain` | Si hay cambios pendientes no resueltos: parar y avisar al usuario |
| **Rama de la US** | `feature/US-XXX-[nombre-corto]` | Crear con `git checkout -b feature/US-XXX-[nombre-corto]` desde la rama base acordada |
| **Usuario asignado** | Campo `Asignado a` del TK; si no: `git config user.name` | Aplicar como filtro salvo instruccion explicita del usuario |

> Si el usuario indica una lista concreta de TK, un implementador distinto o pide implementar sin filtro, esa instruccion explicita prevalece sobre los filtros automaticos.

---

## Validacion antes de implementar

Verificar las siguientes condiciones. Si alguna falla, **parar** - informar al usuario y resolver primero.

- **Working tree limpio:** `git status --porcelain` sin cambios pendientes no resueltos.
- **Rama correcta:** estar en `feature/US-XXX-[nombre-corto]` (o crearla). No implementar en `main` ni en ramas de otras historias sin instruccion explicita.
- **US padre con README.md:** la carpeta de la US existe, tiene `README.md` con metadato `Estado: Ready`.
- **TK en estado Ready:** solo encolar tareas con `Estado: Ready`. Las `Draft` o `Done` en `progress.md` no son ejecutables por defecto.
- **Solapamiento de progreso:** leer `progress.md` si existe; respetar tareas ya en `Done`; si hay alguna `In Progress`, revisar notas y estado real antes de continuar.

Si hay conflicto:

```
WARNING No es posible continuar:
- <razon concreta>
```

---

## Flujo de implementacion

### Paso 1 - Preparar repositorio y rama

1. Verificar working tree limpio; si no, parar y avisar.
2. Resolver nombre de rama: `feature/US-XXX-[nombre-corto]` (el segmento tras `feature/` debe coincidir con la carpeta de la US).
3. `git checkout feature/US-XXX-[nombre-corto]` si la rama existe; si no, `git checkout -b feature/US-XXX-[nombre-corto]` desde la rama base acordada con el usuario (no asumir `main`/`develop`).
4. Leer o crear `progress.md` (desde `assets/progress-template.md` si no existe). Al crearlo, anadir **una entrada por cada TK del alcance acordado** con `Estado: Pending` salvo las ya `Done`.

### Paso 2 - Filtrar y presentar cola

1. Leer `README.md` de la US y todos los `TK-*.md` del alcance indicado.
2. Consultar `docs/specs/work-units.md` si el alcance de alguna unidad no es claro.
3. Construir dos listas:
   - **Implementables:** TK con `Estado: Ready` que pasen los filtros de unidad y usuario asignado, no marcadas como `Done` en `progress.md`.
   - **Excluidas:** el resto, con su estado entre parentesis - p. ej. `TK-002 - Ajuste de permisos (Draft)`, `TK-004 - Exportacion CSV (Done)`.
4. Mostrar ambas listas al usuario en orden numerico. **No ejecutar codigo en este turno.**
5. Preguntar explicitamente si se desea continuar y **esperar confirmacion** antes de implementar.

### Paso 3 - Implementar tarea a tarea

> IMPORTANTE **Regla de oro - una TK por turno:** implementar exactamente **una tarea por turno**. Al terminar cada TK, detenerse y **preguntar al usuario si desea continuar con la siguiente**. No avanzar sin confirmacion explicita. Esta regla no tiene excepciones, aunque el usuario haya aprobado la cola completa en el Paso 2.

Por cada tarea aprobada, en orden numerico salvo dependencias obvias en el texto:

1. Implementar segun la especificacion del TK.
2. Si la tarea genera o modifica archivos de UI: ejecutar bajo el agente `ui-specialist`. Si ademas la referencia de diseno es Figma: usar el MCP de Figma.
3. Al terminar, ejecutar lint, typecheck o build del paquete afectado. Si falla, corregir antes de continuar. **No** ejecutar suites de tests en esta fase.
4. Actualizar `progress.md`: `Pending` => `In Progress` => `Done`; anadir notas si quedan aspectos parciales. Registrar en `Decisiones adicionales` **toda decision tomada durante la sesion de chat** que no este ya documentada en el TK — cambios de enfoque, alternativas descartadas, restricciones descubiertas, acuerdos con el usuario. Si no hubo decisiones nuevas, omitir la seccion.
5. **Detenerse y preguntar** al usuario (con herramienta de preguntas estructuradas):
   - Mensaje: "TK-XXX completada. Continuo con TK-YYY - [titulo]?"
   - Opciones: [Si, continuar] / [No, detener aqui]
6. Esperar respuesta. Solo si el usuario confirma: pasar a la siguiente TK. Si detiene, registrar nota en `progress.md` y pasar al Paso 4.

### Paso 4 - Cierre

1. Cuando no queden tareas pendientes (o el usuario detenga la ejecucion), ofrecer la fase de pruebas: delegar a **`quality-specialist`** para escribir tests basados en los `SC-XX` y `BR-XX` del `README.md`.
2. Si el usuario acepta: invocar **`quality-specialist`** con el contexto de la US, la rama `feature/US-XXX-*` y los TK en `Done`. No escribir tests desde este skill.
3. Si el usuario rechaza: registrar nota en `progress.md`.
4. **Handoff:** si todo el alcance esta en `Done`, working tree limpio y commits hechos (`git-commit`), sugerir: (1) **`git-pr`** si el equipo revisa por PR; (2) **`story-integrate`** para merge local. Si quedan TK en `Pending`/`In Progress`, indicar que falta cerrar.

---

## Flujo: TK indicada sin US explicita

Un `TK-XXX` siempre vive bajo la carpeta de una US. Si el usuario indica solo el numero de tarea sin mencionar la US:

1. **Preguntar** a que `US-XXX` pertenece antes de continuar.
2. Una vez recibida la US, **validar** que el archivo `TK-XXX-[nombre].md` existe dentro de `docs/specs/user-stories/US-XXX-[nombre-corto]/`.
3. Si la tarea no pertenece a esa US o el archivo no se encuentra, **parar** e informar:

```
WARNING No es posible continuar con la implementacion:
- TK-XXX no pertenece a US-XXX o no se encontro en su carpeta.
- Motivo: <archivo no encontrado / TK en carpeta de otra US>
- Verificar el numero de tarea y la historia indicada antes de continuar.
```

4. **No** implementar hasta que la relacion TK => US este confirmada.

---

## Checklist antes de implementar

**Repositorio:**
- Working tree limpio (`git status --porcelain` sin cambios pendientes)
- Rama `feature/US-XXX-[nombre-corto]` activa o creada
- `progress.md` leido o creado

**Cola:**
- `README.md` de la US leido
- Todos los `TK-*.md` del alcance leidos
- `work-units.md` consultado si algun alcance de unidad no era claro
- Lista de implementables y excluidas presentada al usuario
- Confirmacion del usuario recibida antes del primer cambio de codigo

**Por cada tarea:**
- TK con `Estado: Ready`
- No marcada como `Done` en `progress.md`
- Si la tarea genera o modifica UI: ejecutado bajo `ui-specialist`
- Si la referencia de diseno es Figma: MCP de Figma usado
- Lint/build ejecutado tras la implementacion
- `progress.md` actualizado a `Done`
- Decisiones tomadas en la sesion registradas en `Decisiones adicionales` del TK en `progress.md`
- **Confirmacion explicita del usuario recibida antes de pasar a la siguiente TK**

**Cierre (fase de pruebas):**
- Usuario preguntado sobre fase final de pruebas
- Si acepta: tests delegados a **`quality-specialist`**, no escritos desde este skill

---

## Ejemplos

**Ejemplo 1 - US completa con filtro de unidad**
- *Entrada:* "Implementa lo Ready de la US-042; estoy en el paquete `@acme/web-app`."
- *Salida:* Rama limpia y checkout a `feature/US-042-[nombre-corto]`; mensaje con TK Ready en cola y excluidas; tras confirmacion del usuario, implementa **solo la primera TK Ready**, ejecuta lint/build, actualiza `progress.md`, y **pausa para preguntar si continuar con la siguiente**.

**Ejemplo 2 - TK indicada sin US**
- *Entrada:* "Implementa TK-003."
- *Comportamiento:* Preguntar a que `US-XXX` pertenece. Validar que el archivo existe. Si existe, continuar con el flujo normal. Si no, parar con mensaje de error.

**Ejemplo 3 - TK en Draft**
- *Entrada:* "Ejecuta TK-005 de la US-042" y TK-005 esta en Draft.
- *Salida:* Lista de excluidas: `TK-005 - ... (Draft)`. No implementa TK-005 hasta que este en Ready.

**Ejemplo 4 - Confirmacion entre tareas (caso clave)**
- *Entrada:* Hay tres TK Ready aprobadas en la cola.
- *Comportamiento:* Implementa TK-001, actualiza `progress.md`, ejecuta lint. Luego **pausa y pregunta** con opciones tappables: "TK-001 completada. Continuo con TK-002 - [titulo]?" [Si, continuar] / [No, detener aqui]. No avanza sin respuesta afirmativa. Mismo ciclo tras TK-002 antes de TK-003.

**Ejemplo 5 - Usuario pide "implementar todo de corrido"**
- *Entrada:* "Implementa todas las tareas de una vez sin preguntar."
- *Comportamiento:* Informar que el skill opera con **una tarea por confirmacion** y que no es posible omitir las pausas entre tareas. Explicar el beneficio: detectar errores temprano y mantener control del alcance. Ofrecer continuar con el flujo estandar.

---

## Anti-patterns

- Implementar mas de una TK por turno sin confirmacion intermedia del usuario.
- Codificar con working tree sucio sin avisar y pausar.
- Implementar en `main` u otra rama que no sea `feature/US-XXX-[nombre-corto]` sin instruccion explicita.
- Omitir el mensaje de cola y confirmacion e ir directo al codigo.
- Tratar tareas en Draft como ejecutables por defecto.
- Arrancar la siguiente TK sin confirmacion explicita (aunque el usuario haya aprobado la cola completa en el Paso 2).
- Ejecutar suites de tests durante el ciclo de tareas sin que el usuario haya aceptado la fase final.
- Escribir tests en la fase final sin delegar a **`quality-specialist`**.
- Ignorar `progress.md` o usar identificadores distintos a `TK-XXX`.
- Omitir la seccion `Decisiones adicionales` cuando durante la sesion se tomaron decisiones no documentadas en el TK.
- Implementar archivos de UI sin usar el agente `ui-specialist`.
- Implementar UI con referencia Figma sin usar el MCP de Figma.
- Modificar `README.md` de la US, archivos `TK-XXX`, ADRs o `technical-docs/` durante la implementacion.
- Continuar cuando se detecta un conflicto en la documentacion sin notificar al usuario primero.
- Escribir `Skipped` u otro estado no definido en `progress.md`; estados validos: `Pending`, `In Progress`, `Done`.
- Lanzar preguntas como prosa libre cuando el cliente expone herramienta de preguntas estructuradas.
- Aceptar como confirmacion una respuesta ambigua ("ok", "dale") sin opciones explicitas; si hay duda, repreguntar.

---

## Notas

### Handoffs del ciclo

Posicion: **implementacion** - entre `story-plan` e `story-integrate`.

| | |
|--|--|
| **Entrada** | US `Estado: Ready`; TK del alcance con `Estado: Ready`; rama `feature/US-XXX-[nombre-corto]` activa o creada desde la rama base acordada con el usuario. |
| **Salida** | Codigo commiteado; `progress.md` con cada TK del alcance en `Done`; working tree limpio. |
| **Siguiente paso** | `git-commit` si hay cambios pendientes => `git-pr` (opcional, abrir desde `feature/US-XXX-*` antes de mergear) => **`story-integrate`** cuando `progress.md` este integro en `Done`. |
| **Regreso desde plan** | TK en Draft o conflicto tecnico => volver a **`story-plan`** para completar o corregir el TK antes de continuar. |
| **Regreso desde integrate** | TK no `Done` detectada al intentar mergear => completar la implementacion aqui y actualizar `progress.md` antes de reintentar. |

### Estados de `progress.md`

Estados validos por tarea: **`Pending`**, **`In Progress`**, **`Done`**. No usar `Skipped` ni otros valores.

| Situacion | Que hacer |
|-----------|-----------|
| Posponer una TK | Mantener `Pending` y registrar el motivo en `Notas`. |
| Sacar una TK del alcance | Parar; alinear con `story-define` o `story-plan`; eliminar la entrada de `progress.md` si ya no aplica. |
| TK completada | `Done`. |

### Orden de implementacion

Respetar orden numerico `TK-001`, `TK-002`, ... salvo dependencias obvias en el texto de las tareas. Si hay conflicto de orden, preguntar al usuario antes de implementar.

### Relacion con otros skills

- **story-plan** especifica el formato y contenido de los TK; este skill los consume (solo TK `Ready`).
- **story-define** define la US y sus criterios de aceptacion (`BR-XX`, `SC-XX`).
- **quality-specialist** escribe tests en el cierre cuando el usuario acepta la fase final.
- **story-integrate** cierra la US tras este skill; requiere `progress.md` completo en `Done` y working tree limpio.
- **git-commit** prepara commits antes del handoff a integrate.
- **MCP de Figma:** obligatorio para tareas de UI con referencia Figma.