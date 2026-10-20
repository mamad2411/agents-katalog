---
name: confluence-publish
description: >
  Publica la documentación de un proyecto en Confluence Cloud con un ASISTENTE
  GUIADO pensado para personas NO técnicas, reutilizando el conector oficial de
  Atlassian (Rovo MCP) — no reimplementa la integración. Acompaña al usuario paso
  a paso: elige el espacio y el punto de anclaje (raíz del espacio o bajo una
  página existente) mostrando nombres y árbol reales (nunca IDs), previsualiza qué
  se va a publicar, pide confirmación antes de tocar nada y espeja el árbol de
  docs/ de forma idempotente (crea o actualiza, sin duplicar). Guarda las
  preferencias en .claude/confluence.json para que la próxima vez sea de un clic.
  Úsala cuando el usuario diga "publica en Confluence", "sube la doc a Confluence",
  "sincroniza con Confluence", "crea el espacio/árbol del proyecto en Confluence".
user-invokable: true
---

# confluence-publish — publicar en Confluence con asistente guiado

Espeja la documentación local de un proyecto (`docs/…`) como un árbol de páginas en
**Confluence Cloud**, usando el **conector oficial de Atlassian (Rovo MCP)**. No hay motor
propio ni instalación: las operaciones usan las herramientas del conector.

**Esta skill la usarán personas NO técnicas.** El objetivo es que nadie tenga que conocer
IDs, claves de espacio ni editar ficheros. Tú (el agente) haces de asistente: preguntas
en lenguaje natural, ofreces opciones por su **nombre**, previsualizas y **confirmas antes
de escribir nada**. Los tecnicismos (cloudId, spaceId, parentId, pageId) se resuelven y se
guardan **por debajo**, sin exponerlos.

## Principios de interacción (obligatorios)

- **Una pregunta a la vez**, en lenguaje llano. Nunca sueltes un cuestionario largo.
- **Opciones numeradas por nombre.** Muestra "1) Marketing  2) Ingeniería  3) …", no claves ni UUIDs.
- **Nada de jerga.** Di "dónde quieres que aparezca", no "introduce el parentId". Evita cloudId/spaceKey/pageId en lo que ve el usuario.
- **Valores por defecto sensatos** y recomendados: propón la opción más común y deja cambiarla ("Por defecto lo pongo como página nueva dentro de 'Proyectos'. ¿Te vale? [Sí / elegir otro sitio]").
- **Previsualiza y confirma** antes de crear/actualizar: enseña un resumen de qué páginas se crearán y dónde, y espera un "sí" explícito.
- **Sin callejones sin salida:** si algo falla (sin conexión, sin permisos), explícalo en una frase clara y di el siguiente paso, sin volcar errores técnicos crudos.
- **Recuerda las decisiones:** guarda todo en `.claude/confluence.json` para que la próxima vez no haya que preguntar (solo confirmar).

## Requisitos

- **Conector Atlassian (Rovo MCP) conectado** en Claude (Jira & Confluence). Si no lo está,
  díselo al usuario con naturalidad ("Necesito permiso para conectarme a vuestro Confluence;
  actívalo en los conectores y volvemos") y **detente**; no intentes otra vía.
- Permiso de escritura del usuario en el espacio de destino.
- Herramientas del conector (por su función; el prefijo `mcp__…__` puede variar):
  `getAccessibleAtlassianResources`, `getConfluenceSpaces`, `getPagesInConfluenceSpace`,
  `getConfluencePage`, `getConfluencePageAncestors`, `getConfluencePageDescendants`,
  `createConfluencePage`, `updateConfluencePage` y la búsqueda (CQL) si está disponible.

## Paso 0 — opt-in (¿sincronizar con Confluence?) — SIEMPRE primero

La sincronización con Confluence es **opcional** y se decide **una vez por proyecto**. Antes de
nada, localiza la config y mira el flag `enabled` de `.claude/confluence.json`:

```bash
CFG="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*confluence.json' 2>/dev/null | head -1)"
```

- **`enabled: true`** → sincronización activada; sigue el flujo normal (conexión → espacio → árbol → subir).
- **`enabled: false`** → el usuario dijo que NO. **No hagas nada** y **no vuelvas a preguntar**.
- **No hay config** (primera vez) → **pregunta una sola vez**:
  > "¿Quieres sincronizar la documentación de este proyecto con Confluence? [Sí / No]"
  - **Sí** → crea `.claude/confluence.json` con `"enabled": true` y continúa con la conexión (Paso 1) y el asistente (espacio → árbol → subir), tal como está descrito.
  - **No** → crea `.claude/confluence.json` con `"enabled": false` (para no volver a preguntar) y termina sin sincronizar.

Este opt-in aplica igual cuando la skill se invoca a mano y cuando la llaman otros agentes
(modo sincronización): si `enabled` es `false` o el usuario dice que no, no se sincroniza nada.

## Cómo funciona por dentro (una sola idea)

Al crear una página, **si se pasa `parentId` es hija de ese nodo; si se omite, va a la raíz
del espacio.** Todo el "dónde aparece" se reduce a eso. El usuario nunca ve `parentId`: elige
un sitio por su nombre y tú traduces.

## El flujo, de un vistazo

El asistente encadena estos pasos, cada uno alimenta al siguiente:

1. **Conectar con Confluence** (interactivo) → 2. **Buscar y elegir espacio** → 3. **Ver el árbol del espacio y elegir dónde** → 4. **Nombrar la página del proyecto** → 5. **Confirmar y subir el contenido**.

Si el proyecto ya se configuró antes (`.claude/confluence.json`), se salta directo a una confirmación de una línea (**Modo rápido**, Paso 3-bis).

> **Lectura bajo demanda (token-diet).** Este fichero es el mapa: cada paso trae su regla en 1-3 líneas
> y remite a `references/<tema>.md` para los guiones y la casuística completa. **Abre una referencia
> solo cuando llegues al paso que la cita** (tabla al final); no las cargues todas al arrancar.

---

## Paso 1 — conectar con Confluence (interactivo)

`getAccessibleAtlassianResources`; si no conecta, guía en llano y **reintenta** cuando el usuario confirme
(no sigas sin conexión). Varios sites → elige por nombre (el `cloudId` se guarda por debajo). Luego localiza
`.claude/confluence.json`: **si existe → Modo rápido (Paso 3-bis)**; si no → Paso 2. → `references/wizard.md`.

## Paso 2 — buscar y elegir espacio

Permite **buscar por nombre** (`getConfluenceSpaces`), muestra coincidencias numeradas por nombre y, al
elegir, pasa directamente a mostrar el árbol del espacio (Paso 3). → `references/wizard.md`.

## Paso 3 — ver el árbol del espacio y elegir dónde

Detecta el entorno: **Paso 3-A** navegador de árbol como artefacto (plantilla
`assets/tree-browser.template.html`, nunca un HTML improvisado) o **Paso 3-B** navegación conversacional
(CLI/VS Code: abrir · subir · elegir). Resultado en ambos: `{mode: existing|child|root-child, parentPageId,
name}`. → `references/wizard.md`.

## Paso 4 — confirmar el nombre (si procede)

Solo si se crea página nueva (`child` / `root-child`); en `existing` no hay página nueva. → `references/wizard.md`.

## Paso 5 — confirmar y subir

Previsualiza (bloque «Confirmación»), espera el "sí", aplica el `mode` (existing → sin home; child /
root-child → crea la página `name`) y sube espejando `docs/` («Publicar»). Al terminar guarda
`.claude/confluence.json` con lo elegido. → `references/wizard.md`.

## Confirmación (SIEMPRE, antes de escribir)

Resumen humano: espacio · ubicación · página principal · nº de páginas → **espera un sí**; "cambiar algo"
vuelve a la pregunta correspondiente. → `references/wizard.md`.

## Paso 3-bis — modo rápido (config ya existe)

Confirma en una línea («Publico la doc en **A › B › C** como la última vez. ¿Actualizo?») y publica;
"cambiar destino" reusa los Pasos 2-3. → `references/wizard.md`.

## Publicar (idempotente; por debajo)

Orden fijo: (0) regenerar el **staging** si `publish.staging: true` (`confluence-scope.py --stage --root
"$PWD"`; si falla, degrada a `publish.source = "docs"` sin bloquear) → (1) espacio → (2) anclaje
(`parentId` debe ser una **página**) → (3) página principal idempotente → (4) árbol `mirror-tree`
(nunca espejes `_STAGING-LEEME.md`) → (5) **idempotencia por manifiesto** `.claude/confluence-state.json`
(hash igual → nada; distinto → `updateConfluencePage`; ausente → `createConfluencePage`; respaldo: buscar
por título antes de crear). **Nunca dupliques.** → `references/publish-and-sync.md`.

## Cierre (en lenguaje humano)

Resumen sin tecnicismos + **enlace clicable** a la página principal; lo omitido o fallido, por página y
en una frase. → `references/wizard.md`.

## Modo sincronización (invocada por otros agentes, sin interacción)

Aplica el opt-in (Paso 0); con `enabled: true` sincroniza en silencio **solo lo que cambió según el
manifiesto** (crear / modificar / sin cambios / eliminar → marcar obsoleta y listar, el conector no borra).
Antes de comparar: regenera `docs/roadmap/dashboard.md` (skill `roadmap-dashboard`) si hay cambios bajo
`docs/roadmap/`, y después el staging (D5). **Exclusión obligatoria: nunca publiques
`docs/security-scan/**`.** → `references/publish-and-sync.md`.

## Estado de sincronización — manifiesto `.claude/confluence-state.json` (sin git)

Mapa `ruta → {hash, pageId}` por contenido, sin git ni fechas; clasifica crear / modificar / sin cambios /
eliminados y se actualiza al final de cada ejecución. Marca opcional `.claude/.confluence-pending` del
hook `PostToolUse` (disparador, no publicador). → `references/publish-and-sync.md`.

## Config `.claude/confluence.json` (gestión interna, no la pide el usuario)

Formato en `assets/confluence.example.json`: `cloudId`, `spaceKey`, `anchor`, `home`, `publish`
(`staging: true`, `source`, `layout: mirror-tree`, `include: ["**/*.md"]`, `exclude`, `onConflict`).
`SKILL.md`/referencias y `confluence.example.json` van siempre sincronizados. → `references/config-and-policy.md`.

## Qué sube y qué no (política de publicación — normativa)

Política **opt-out** (`include: ["**/*.md"]` + `exclude`). Fuera: `docs/security-scan/**` (**invariante no
negociable**, `confluence-scope.py --check`), `docs/en/**`, `docs/examples/**`, `docs/agents/**`,
`atlassian-connector-notes.md`, `improvement-plan.md`/`tasks.md`/`test-plan.md` (D1), `docs/knowledge/journal/**` (bitácora de sesión, no decisión), `**/testing/**` (D4),
`docs/confluence/**` (staged, D5), `**/node_modules/**`. **Dentro:** `spec.md`, `evaluation.md`,
`design.md` (decisión de arquitectura, `architect`), `retro.md` y `docs/knowledge/**` (menos `journal/`). Tabla completa con razones, consecuencias y el contrato de la carpeta
staged → `references/config-and-policy.md`.

## Reglas

- **Guiado y humano:** una pregunta a la vez, opciones por nombre, sin jerga, con defaults recomendados.
- **Confirma antes de escribir:** siempre previsualiza destino + nº de páginas y espera el "sí".
- **No reimplementes la API:** todo por el conector Atlassian. Si no está conectado, detente y pide conectarlo (en llano).
- **Idempotente siempre:** buscar → actualizar o crear; reejecutar no duplica.
- **La config es memoria, no un requisito del usuario:** se rellena sola la primera vez y luego solo se confirma.
- **`parentId` = ubicación** (oculto al usuario): presente → hija; ausente → raíz. Debe apuntar a una página.
- **Un proyecto → una página principal.** Todo cuelga de ella; usa el id guardado como caché para no duplicarla.
- **Errores en llano:** sin conexión / sin permiso / página fallida → una frase clara y el siguiente paso, no un volcado técnico.

## Qué NO hace

- No reimplementa la API de Confluence ni instala nada: solo el conector Atlassian (Rovo MCP).
- No escribe nada sin opt-in (`enabled: true`) ni sin el "sí" a la previsualización.
- No publica `docs/security-scan/**` bajo ninguna configuración, ni el ledger `tasks.md` salvo `include` manual.
- No baja contenido de Confluence a `docs/` (eso es `confluence-pull`) ni edita `docs/confluence/` a mano.

## Referencias (lectura bajo demanda)

| Fichero | Léelo SOLO cuando… | Contiene |
|---|---|---|
| `references/wizard.md` | el opt-in sea `true` y acompañes al usuario (**Pasos 1-5**, Confirmación, **3-bis**, Cierre) | guiones literales de cada pregunta, navegador de árbol 3-A (plantilla + marcadores) y modo conversacional 3-B |
| `references/publish-and-sync.md` | vayas a escribir en Confluence (**Publicar**), te invoque otro agente (**Modo sincronización**) o toques el manifiesto / dashboard / staging | algoritmo idempotente completo, regla por tipo de cambio, regeneración del dashboard y del staging (D5), formato del manifiesto y marca de pendiente |
| `references/config-and-policy.md` | tengas que crear/explicar la config o decidir si un fichero entra en el espejo (**Qué sube y qué no**) | campos y defaults de `publish`, tabla normativa de exclusiones con razones, `docs/knowledge/**` y stubs, contrato de `docs/confluence/` |
| `assets/confluence.example.json` | escribas `.claude/confluence.json` | formato con `_comment_exclude` por patrón |
| `skills/confluence-pull/SKILL.md` | el usuario quiera el sentido inverso (Confluence → `docs/`) | la skill pareja; no mezcles sentidos en la misma pasada |
