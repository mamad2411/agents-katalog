---
name: changelog-sync
description: >
  Genera las entradas `[Unreleased]` (EN) y `[Sin publicar]` (ES) del CHANGELOG a partir de los
  ledgers CERRADOS del roadmap (`docs/roadmap/*/tasks.md` con `estado: completado`), de forma
  DETERMINISTA e idempotente: un bullet por tarea `T-XX` con su título, un resumen de UNA o DOS
  frases y sus ficheros clave, con la categoría `Added|Changed|Fixed` deducida (o declarada en el
  frontmatter). El resumen sale de una ESCALERA: el campo `- **Changelog**:` de la tarea si está
  (la vía buena, lo escribe quien la cerró) → la primera frase de la `Descripción` si cabe en el
  tope → su oración principal → solo el título con puntero al ledger. Nunca trunca una frase con
  `…`. No crea la sección de versión (eso es el script de release del proyecto) ni inventa
  alcance. Úsala cuando el usuario diga "escribe el changelog", "sincroniza el CHANGELOG",
  "genera las notas de la release", "actualiza [Unreleased]", o al cerrar una iniciativa.
---

# changelog-sync — el CHANGELOG sale del ledger, no de la memoria

Al cerrar una iniciativa hay que dejar constancia en el CHANGELOG. Escribirlo «de memoria» al
final del día es justo cuando se olvidan tareas y se inventa alcance (pasó en la v1.15.0: las
notas se redactaron a mano cuatro veces — [`LES-012`](../../docs/knowledge/lessons/)). Aquí la
fuente es el **ledger canónico**, que ya tiene el título, la descripción y los ficheros de cada
tarea; el script solo los traslada.

**El resumen lo escribe quien cierra la tarea, no lo adivina el script** ([`ADR-012`](../../docs/knowledge/adr/ADR-012-resumen-del-changelog-lo-escribe-quien-cierra-la-tarea.md)).
La `Descripción` del ledger está escrita para el implementador: medida sobre los **13 ledgers
cerrados** de este repo (**63 tareas**),<!--m:base_ledgers=13,base_tareas=63--> su primera frase
tenía **mediana 447 y máximo 1.944 caracteres** (la foto del 2026-09-04, con el script de
`a7a11b0`)<!--m@2026-09-04:a7a11b0_frase_mediana=447,a7a11b0_frase_max=1944--> — inusable
como nota de release (por eso las notas de la v1.16.0 se escribieron a mano). El campo opcional
`- **Changelog**: <una o dos frases>` de cada `### T-XX` pone el resumen donde lo sabe una persona.

Resolución de rutas (regla 5 de CONVENTIONS — nunca rutas fijas):

```bash
CLS="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*skills/changelog-sync/scripts/changelog-sync.py' 2>/dev/null | head -1)"
```

## Cuándo usarla

- **Al cerrar una iniciativa** (`/dev-cycle` Fase 6, `quick-implement`): su ledger acaba de pasar
  a `completado`, así que ya hay entrada que generar.
- **Antes de un release**: el script de release del plugin (`release.py`) ejecuta `--check` en sus precondiciones y
  **avisa** si falta alguna entrada (no bloquea: se puede publicar deuda de notas a sabiendas).
- **A demanda**, cuando el CHANGELOG se ha quedado atrás respecto al roadmap.

## Cómo se ejecuta

```bash
python3 "$CLS" --check              # exit 1 si hay ledgers cerrados sin entrada (no escribe)
python3 "$CLS" --dry-run            # imprime lo que escribiría, sin tocar nada
python3 "$CLS"                      # escribe en CHANGELOG.md y CHANGELOG.es.md
python3 "$CLS" --only <slug>        # una sola iniciativa
python3 "$CLS" --check --json       # para consumo por script
python3 "$CLS" --medicion           # las cifras que la doc afirma, medidas (`--json` para script)
```

Exit: `0` ok o nada pendiente · `1` solo con `--check` y entradas pendientes · `2` uso
(falta un CHANGELOG, `--only` con un slug que no está cerrado).

## Qué produce

Una subsección por iniciativa, insertada bajo la cabecera de la sección abierta y ordenada por
fecha (la más reciente arriba):

```markdown
### Added — `mi-iniciativa` initiative (2026-09-03)

- **T-01 — Título de la tarea** Resumen de una o dos frases. (`a.py`, `b.md`, `c.json`)
- **T-02 — Tarea sin resumen en el ledger** ([ledger](docs/roadmap/2026-09-03-mi-iniciativa/tasks.md))
```

### La escalera del resumen (determinista, en este orden)

| # | Camino | Cuándo | Qué sale |
|---|---|---|---|
| 1 | `changelog` | la tarea trae `- **Changelog**: …` con texto (un `{{…}}` de plantilla o el campo vacío **no** cuentan) | **tal cual**, con la continuación indentada absorbida. Más de 2 frases → avisa y usa las dos primeras; más de `RESUMEN_MAX` → avisa y lo respeta igual (no trunca lo que escribió una persona) |
| 2 | `frase` | la **1.ª frase** de la `Descripción` cabe en `RESUMEN_MAX` | esa frase (comportamiento clásico) |
| 3 | `corte` | la **oración principal** cabe y se lee como una idea | lo anterior al primer `:`, `;`, `—` o `(` de nivel superior (fuera de `código`, paréntesis y «comillas»), con ≥ `CORTE_MIN_PALABRAS` palabras de prosa |
| 4 | `titulo` | nada de lo anterior cabe | **solo el título** + `([ledger](docs/roadmap/<fecha>-<slug>/tasks.md))` |

Topes (constantes del script, no números repartidos): `RESUMEN_MAX = 200` · `RESUMEN_FRASES_MAX = 2`
· `ARCHIVOS_MAX = 3` · `ARCHIVOS_MAX_TOCADOS = 6` · `CORTE_MIN_PALABRAS = 5`.<!--m:resumen_max=200,resumen_frases_max=2,archivos_max=3,archivos_max_tocados=6,corte_min_palabras=5-->
**Cada uno se eligió midiendo los 13 ledgers cerrados reales (63 tareas)**<!--m:base_ledgers=13,base_tareas=63--> — la medición, con lo que sale a 160/200/240,
por qué el paso 3 rescata poco en este repo y el desglose de longitud POR CAMINO, está en [`references/medicion-escalera.md`](references/medicion-escalera.md)
(**léela solo** si vas a mover un tope).

**Nunca trunca con `…`.** Degradar al título es honesto; cortar una frase técnica por la mitad no lo
es. Si un bullet sale pobre, la respuesta es escribir el campo `Changelog:` de esa tarea, no aflojar
el tope.

`RESUMEN_MAX` acota **el resumen, no el bullet**: el resto lo ponen el título del ledger y la lista
de ficheros. Techo real medido el 2026-09-12 con los títulos y rutas de este repo: **467
caracteres**.<!--m@2026-09-12:bullet_max=467--> Y el camino que se promueve es, medido, el que
produce los bullets más LARGOS (`changelog` mediana 342 · `titulo` mediana 115)<!--m@2026-09-12:changelog_mediana=342,titulo_mediana=115--> — es el precio de que el bullet diga algo. `RESUMEN_FRASES_MAX` es un tope
**tipográfico**: `FIN_FRASE` reconoce «punto + espacio + apertura de frase», con una guarda de
abreviaturas (`p. ej.`, `vs.`, `etc.`, `Sr.`, `pág.`, `EE. UU.`…), así que un texto cuyas frases
empiecen en minúscula no se recorta. El aviso solo sale cuando de verdad se ha recortado.

- **Ficheros**: hasta `ARCHIVOS_MAX` (3) entre paréntesis, y **ninguno** si la tarea toca más de
  `ARCHIVOS_MAX_TOCADOS` (6): con 20 ficheros tocados, enseñar 3 hace creer que son todos.
- **Categoría**: `fix|corrige|corrección|saldar|bug|regresión` → `Fixed`;
  `cambia|retira|renombra|migra|sustituye|reemplaza` → `Changed`; resto `Added`. Para fijarla a
  mano, añade `changelog: Added|Changed|Fixed` al frontmatter del ledger — el override manda.
- **Idempotencia**: si el slug ya aparece entre acentos graves en el CHANGELOG, no se vuelve a
  escribir. Puedes reescribir el texto generado sin miedo: no se regenera.
- **Empuje del campo**: `--check` nombra las tareas sin `Changelog:` de las iniciativas **realmente
  pendientes** (en las ya publicadas escribirlo no cambiaría la salida: `pendientes()` las salta
  para siempre), más UNA línea con el total de la deuda. Es **aviso**: no cambia el exit code (el
  `1` sigue siendo solo por «entradas pendientes»). El detalle por camino, sobre TODO ledger
  cerrado, está en `--check --json` → `degradacion.caminos`, y el POR QUÉ falta el campo en
  `degradacion.sin_campo_por_motivo` (`ausente` · `vacio` · `placeholder`): un campo vacío o que ES
  todavía el `{{…}}` de la plantilla cuenta como NO escrito en la deuda, porque el bullet degrada
  igual.
  `agent-kits/shared/ledger-lint.py` también avisa, y solo en **adopción parcial** (una tarea del
  ledger lo trae y otra no), con el campo vacío o con un `{{…}}` sin sustituir: el campo es opcional
  por diseño y los ledgers antiguos validan igual. Los dos comparten UN patrón
  (`CHANGELOG_FIELD_PATTERN`, replicado literal y comparado byte a byte por la suite), para que lo
  que valida el linter y lo que publica el generador sea el mismo campo.

## Cómo afinar el texto generado

El bullet automático es un **punto de partida honesto**, no la nota final:

0. Lo primero, **antes** de tocar el CHANGELOG: si un bullet degradó al título, escribe el campo
   `- **Changelog**:` en esa tarea del ledger y vuelve a generar. Así el arreglo queda en la
   fuente y sirve para el siguiente release, en vez de perderse en una edición manual.
1. Reescribe la redacción para que hable del **valor** («los hooks informan del progreso»), no de
   la tarea («T-02 hooks»). Puedes fundir varios bullets en uno.
2. Quita los ficheros que no aporten y añade el enlace al ADR/lección si la iniciativa lo tiene.
3. **Nunca amplíes el alcance**: si el bullet no lo dice, no pasó. Lo que falte, está en el
   ledger; lo que no esté en el ledger, no va al CHANGELOG.

## Qué NO hace

- **No crea la sección de versión** ni mueve `[Unreleased]` → `[X.Y.Z]`: eso es el script de
  release del plugin, `release.py` (que además comprueba árbol limpio, versión creciente y tag libre).
- **No traduce con modelo**: el ledger está en español, así que el bullet ES y EN salen del mismo
  texto. Traducir la versión EN es trabajo humano (o de un turno del agente) posterior.
- **No inventa alcance ni cifras**, no lee la conversación y no toca ledgers (el campo
  `Changelog:` lo escribe el implementador al cerrar la tarea, no este script).
- **No resume con modelo ni trunca con `…`**: la escalera es determinista y, cuando no hay
  material que quepa, dice el título y apunta al ledger.

## Referencias

| Fichero | Léelo cuando |
|---|---|
| [`references/medicion-escalera.md`](references/medicion-escalera.md) | vayas a mover `RESUMEN_MAX`, `ARCHIVOS_MAX*` o `CORTE_MIN_PALABRAS`: trae la medición sobre los 13 ledgers cerrados (63 tareas), el antes/después y el desglose de longitud por camino. **Sus cifras las imprime `--medicion`** y las compara `tests/test_cifras_medidas.py`: no se escriben a mano |
