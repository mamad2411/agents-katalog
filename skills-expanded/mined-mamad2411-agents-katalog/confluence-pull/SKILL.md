---
name: confluence-pull
description: >
  Trae a local (docs/) el estado actual de Confluence — el sentido INVERSO de
  confluence-publish — para que una persona NO técnica (p. ej. un PM sin git)
  tenga su copia al día sin clonar ni hacer pull de git. Reutiliza el conector
  oficial de Atlassian (Rovo MCP) y el mismo mapeo página↔fichero del manifiesto
  .claude/confluence-state.json. Es un asistente guiado: comprueba conexión,
  previsualiza qué se va a crear/actualizar, avisa de conflictos y pide
  confirmación antes de escribir nada en local. Preserva el frontmatter local.
  Úsala cuando el usuario diga "actualiza mis docs desde Confluence", "baja/trae
  la doc de Confluence", "sincroniza desde Confluence", "ponme al día el roadmap".
user-invokable: true
---

# confluence-pull — traer la doc desde Confluence (sentido inverso)

Espeja **de Confluence a `docs/` local** las páginas del proyecto, usando el **conector oficial de
Atlassian (Rovo MCP)**. Es la pareja inversa de `confluence-publish`: donde aquella sube
`docs/ → Confluence`, ésta baja `Confluence → docs/`. Sirve para que quien **no usa git** (típico
de un PM) tenga en su carpeta el estado real que otros han ido actualizando, y pueda leer/editar
sin herramientas de desarrollo.

**Pensada para personas NO técnicas.** Mismo estilo que `confluence-publish`: una pregunta a la
vez, lenguaje llano, previsualiza y **confirma antes de escribir en local**. Nada de IDs ni jerga.

## Requisitos

- **Conector Atlassian (Rovo MCP) conectado** (Jira & Confluence). Si no lo está, dilo en llano
  ("Necesito conectarme a vuestro Confluence; actívalo en los conectores y volvemos") y **detente**.
- El proyecto ya debe estar **sincronizado alguna vez** (`.claude/confluence.json` con
  `enabled: true` y, idealmente, `.claude/confluence-state.json`). Si no existe config, esto es un
  proyecto que nunca publicó: remite a `confluence-publish` para el alta y **no** inventes destino.
- Herramientas del conector (por su función; el prefijo `mcp__…__` puede variar):
  `getAccessibleAtlassianResources`, `getConfluenceSpaces`, `getPagesInConfluenceSpace`,
  `getConfluencePage` (cuerpo de la página), `getConfluencePageDescendants`.

## Idea en una frase

El manifiesto `.claude/confluence-state.json` ya mapea **cada fichero local ↔ su `pageId`**. El
pull recorre ese mapa (y el árbol bajo el anclaje para descubrir páginas nuevas), lee el cuerpo de
cada página y lo escribe en su fichero local — **solo si cambió** y **sin pisar** trabajo local no
publicado.

## Flujo

### Paso 0 — opt-in y conexión
1. Igual que `confluence-publish`: localiza la config y respeta el flag `enabled`.
   ```bash
   CFG="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*confluence.json' 2>/dev/null | head -1)"
   STATE="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*confluence-state.json' 2>/dev/null | head -1)"
   ```
   - `enabled: false` → no hagas nada. Sin config → remite a `confluence-publish` (alta) y termina.
2. Comprueba la conexión con `getAccessibleAtlassianResources`; si no está, guía a conectarla y detente. Resuelve `cloudId`/espacio/anclaje desde `confluence.json`.

### Paso 1 — construir el conjunto remoto
1. A partir del **anclaje** guardado (página raíz del proyecto), recorre el subárbol con `getConfluencePageDescendants` para obtener todas las páginas del proyecto (título, `pageId`, jerarquía).
2. Cruza con el **manifiesto**: cada `pageId` conocido → su **fichero local**. Las páginas del árbol que **no** estén en el manifiesto son "**nuevas en Confluence**" (creadas allí directamente): propón una ruta local coherente con el árbol (carpeta por página con hijos, `.md` por hoja), pero **márcalas aparte** para que el usuario confirme dónde van.
3. **Simetría con `confluence-publish` (misma política, mismo alcance).** El pull aplica el **mismo** `include`/`exclude` de `.claude/confluence.json` que usa `confluence-publish` para decidir qué se sube (fuente de la lista vigente: `assets/confluence.example.json` — no la dupliques aquí). Una página remota cuyo destino local caería **fuera** del alcance actual (p. ej. porque la política cambió después de publicarla) se trata como "**no gestionada por el circuito**": no se recrea ni se sobrescribe sin más — se lista aparte y se pregunta antes de tocar nada. Con el **staging activo** (D5), el destino de escritura de cada página se resuelve con el **mapeo inverso staged → canónico** de `confluence-scope.py` — nunca lo reimplementes con tus propios cálculos de ruta:
   ```bash
   SCOPE="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*skills/confluence-publish/scripts/confluence-scope.py' 2>/dev/null | head -1)"
   python3 "$SCOPE" --map "docs/confluence/<ruta-de-la-pagina>.md" --root "$PWD"
   ```
   Exit 0 + la ruta canónica por stdout → escribe **ahí** (nunca bajo `docs/confluence/`). Exit 1 (página huérfana, sin fichero canónico correspondiente) → avisa y **no escribas nada**. Si el script no está disponible, degrada a `docs/` directamente (staging desactivado) sin bloquear el pull.

### Paso 2 — leer y clasificar (sin escribir aún)
Para cada página mapeada, obtén su cuerpo con `getConfluencePage`. **Pide el cuerpo en el formato
más fiel a Markdown que ofrezca el conector**; si solo hay formato de almacenamiento (XHTML),
conviértelo a Markdown lo más limpio posible. Luego clasifica comparando **tres versiones**: el
fichero **local**, el **hash del manifiesto** (última vez sincronizado) y el **remoto** recién leído:

| Local vs manifiesto | Remoto vs manifiesto | Acción |
|---|---|---|
| igual (sin cambios locales) | distinto | **Actualizar** el fichero local con lo remoto |
| igual | igual | **Sin cambios**, no tocar |
| distinto (hay edición local sin publicar) | igual | **Conservar local** (nada que traer) |
| distinto | distinto | **⚠️ Conflicto**: ambos cambiaron. No sobrescribas: lista el fichero y ofrece opciones (ver Reglas) |
| no existe en local | existe | **Crear** en local (página nueva o fichero borrado localmente) |
| existe en local | ya no existe remoto | **Solo informar**: la página se borró/movió en Confluence; no borres el local por tu cuenta |

### Paso 3 — preservar el frontmatter local (clave)
Confluence **no** conserva de forma fiable el frontmatter YAML (`--- estado / evaluacion / plan
---`) ni todos los matices de tablas/paneles. Por eso, al **actualizar** un fichero que ya existe
en local: **mantén intacto su bloque de frontmatter** y reemplaza solo el cuerpo por lo traído de
Confluence. Así no se pierde el estado máquina del que dependen `roadmap-dashboard` y `/pm-backlog`.
Para ficheros **nuevos** (no existían en local) no hay frontmatter que preservar: créalo con el
cuerpo y **avisa** de que su estado/enlaces habrá que fijarlos (o correr el agente correspondiente).

### Paso 4 — previsualizar y confirmar
Enseña un resumen humano y **espera un "sí"** antes de escribir nada en local:

> "Desde Confluence traería:
> • Actualizar **3** documentos (login-sso, export-pdf, README)
> • Crear **1** nuevo (panel-metricas)
> • **1 conflicto** (roadmap/notas.md cambió aquí y allí) → lo dejo como está y te lo enseño
> • Sin cambios: 5
> ¿Aplico los cambios en tu carpeta? [Sí / Ver detalle / Cancelar]"

### Paso 5 — aplicar y actualizar el manifiesto
Con el "sí": escribe los ficheros (creando carpetas si hace falta), **actualiza
`.claude/confluence-state.json`** con el nuevo hash y `pageId` de cada uno, y **regenera la vista
local** del dashboard si existe roadmap:
```bash
DASH="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*skills/roadmap-dashboard/scripts/build_dashboard.py' 2>/dev/null | head -1)"
[ -d docs/roadmap ] && python3 "$DASH" --root docs/roadmap --html docs/roadmap/dashboard.html --md docs/roadmap/dashboard.md
```
Cierra en llano: "Listo ✅ Actualicé 3 y creé 1. Tienes conflicto en 1, te lo enseño para que decidas."

## Reglas

- **Nunca pises trabajo local sin avisar.** Si el fichero local difiere del manifiesto, hay edición sin publicar: no la sobrescribas en silencio.
- **Conflictos (ambos lados cambiaron):** no elijas por el usuario. Ofrece: (1) quedarte con lo local, (2) traer lo remoto (guardando antes una copia `.local.bak` del local), o (3) ver ambos y decidir. Por defecto, **conserva lo local** y lístalo.
- **Preserva el frontmatter local** al actualizar; solo reemplaza el cuerpo (ver Paso 3).
- **No borres local** porque una página desaparezca en Confluence: solo informa (el borrado es una decisión del usuario).
- **Solo lectura del lado Confluence.** Esta skill **no** publica ni modifica Confluence; para eso está `confluence-publish`. No mezcles los dos sentidos en la misma pasada.
- **Nunca traigas `docs/security-scan/**`** (datos sensibles de nemesis), ni nada excluido en `confluence.json`.
- **Sin config → no inventes.** Si el proyecto nunca publicó, remite a `confluence-publish` para el alta; no adivines espacio ni anclaje.
- **Fidelidad honesta.** La conversión Confluence→Markdown puede no ser idéntica al original (tablas complejas, paneles, imágenes/adjuntos). Si detectas pérdida, dilo en el cierre; no afirmes fidelidad perfecta.

## Qué sube y qué no (política — resumen; fuente en confluence-publish)

El pull respeta la misma política que `confluence-publish` (resumen en `skills/confluence-publish/SKILL.md`,
sección "qué sube y qué no"; detalle normativo y tabla completa en
`skills/confluence-publish/references/config-and-policy.md`): lo que no está en el espejo
por `exclude` (doc interna del plugin, plan/ledger del roadmap, `**/testing/**`, `docs/en/**`,
`docs/security-scan/**`…) tampoco puede "bajar" de Confluence, porque nunca subió. La regla que
sí es propia del pull: **el destino de escritura es SIEMPRE el fichero canónico de `docs/`**, con
staging activo o sin él — `docs/confluence/` es una salida de `confluence-publish`, nunca una
entrada de `confluence-pull` (ver Paso 1, punto 3).

## Relación con confluence-publish

Comparten `.claude/confluence.json` (destino, y su `include`/`exclude` — mismo alcance en los dos
sentidos, ver Paso 1) y `.claude/confluence-state.json` (mapa + hashes). `publish` sube y `pull`
baja; el manifiesto es la memoria común que hace ambos idempotentes. Un PM típico: `pull` al
empezar (traer lo último) → trabaja/crea specs con `/pm-cycle` → `publish` (o lo hace el hook) al
terminar. Con staging activo, `pull` **siempre** escribe en el fichero canónico de `docs/`, nunca
en `docs/confluence/` (esa carpeta es una salida derivada de `publish`, no una entrada del pull).
