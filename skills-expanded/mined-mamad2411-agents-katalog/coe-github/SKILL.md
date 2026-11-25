---
name: coe-github
description: Flujo Git/GitHub obligatorio del proyecto. Aplicar SIEMPRE antes de crear una rama, commitear, pushear, sincronizar o abrir un Pull Request. Cubre las dos ramas permanentes (dev y main), main protegido sin push directo, nombres de rama tipo/slug, commits Conventional Commits, la plantilla obligatoria de PR, el security review previo a cada PR y la auditoría previa a cada release, los checks que corre el hook reglas-pr en la sesión y en CI, squash & merge del coordinador, semver vX.Y.Z y las reglas de secretos y datos sensibles.
---

# Git & GitHub — flujo del proyecto

> *"Primero disciplina, luego automatización. Automatizar el desorden solo produce
> caos más rápido."*

Este flujo es deliberadamente simple: **dos ramas permanentes**, `dev`
(integración) y `main` (producción / lo que se despliega), y todo lo demás pasa por
Pull Request. No depende de ninguna herramienta externa al repo: se puede
transferir el repositorio a otro equipo u otra empresa tal cual.

## Reglas inviolables

Estas no se negocian, ni siquiera en un hotfix.

- **Nunca `git push` a `main`.** `main` es producción. Nadie trabaja directo sobre
  `main` — tampoco el coordinador ni los administradores. El hook `reglas-pr`
  deniega cualquier push cuyo destino sea `main` (o `master`) y, donde el plan de
  GitHub lo permite (repos públicos, o privados en Pro/Team), la branch protection
  lo rechaza del otro lado. En un repo privado de un plan Free esa protección no
  existe: la regla se sostiene en el hook y en la revisión del coordinador, y
  `init`/`upgrade` lo avisan en una línea sin que haya nada que arreglar.
- **`main` solo recibe merges desde `dev`.** Las ramas de trabajo nacen de `dev` y su
  PR apunta a `dev`; el paso `dev` → `main` es el release, también por PR. Ninguna
  rama de trabajo mergea directo a `main`.
- **Nunca hacer merge de un PR propio.** El autor del cambio no mergea. El squash &
  merge lo hace el coordinador o el aprobador suplente.
- **Nunca aprobar un PR propio.** Nadie aprueba lo suyo.
- **Nunca `git push --force` ni `-f` ni refspecs con `+`.** El hook los deniega.
  `--force-with-lease` solo sobre rama propia, nunca sobre `dev` ni `main`, y
  siempre con confirmación explícita del usuario. Con la política por defecto
  (merge, no rebase) no hace falta nunca.
- **Nunca `git push --all` ni `--mirror`**: suben `main` y ramas que nadie revisó.
- **Solo se pushea a `origin`.** El hook deniega cualquier push a otro remoto o
  a una URL; si de verdad hace falta, lo hace el usuario a mano.
- **El `git push` va solo, en su propio comando, en su forma canónica.** Nada de
  `git commit … && git push` ni `git switch … && git push`: el hook escanea los
  commits que existen cuando corre y ensaya el push con la rama actual, así que un
  commit o un cambio de rama en el mismo comando lo dejan ciego y pide
  confirmación. Primero el commit (o el cambio de rama), después `git push -u
  origin <rama>` a secas (si hace falta, `cd <ruta literal> && git push -u origin
  <rama>` o `git -C <ruta> push -u origin <rama>`), sin `-q`, sin variables de
  entorno delante, sin opciones abreviadas, sin envoltorios (`env`, `sh -c`,
  `timeout`), sin variables en lugar del subcomando (`git $s`), sin alias de git y
  sin rutas con `$PWD`: nada de eso se puede analizar y pide confirmación.
- **Si el hook pide confirmación, no confirmes a ciegas.** Lo hace cuando no
  puede resolver con certeza a dónde va el push ni qué lleva (caracteres que
  expande el shell, `git -c`, variables de entorno, `--no-verify`, opciones
  desconocidas o abreviadas, un comando previo que cambia la rama o los
  commits, o git no pudo ensayarlo porque no hay upstream o red): reescribe el
  comando en su forma simple, `git push -u origin <rama>`, y vuelve a intentar.
- **Nunca commitear secretos**: `.env`, `*.pem`, `*.key`, `*.pfx`, `credentials.json`,
  `secrets.json`, tokens, contraseñas, llaves privadas, connection strings.
- **Nunca subir datos de la organización sin autorización previa**: datos
  personales de empleados o clientes, nóminas, documentos de identidad, datos
  bancarios, listados, volcados, infraestructura interna. Ver skill
  `datos-sensibles`.
- **Nunca crear una rama sin nombre descriptivo.** Formato `tipo/descripcion-corta`.
  Si el trabajo tiene un ID rastreable de un tracker externo, va como prefijo del
  slug (`feature/ABC-123-captura-lead`); si no lo hay, el slug solo. **No inventes
  IDs.**
- **Nunca crear repositorios** ni borrarlos. Eso es del coordinador.
- **Un hotfix NO es un bypass.** Aun en máxima criticidad: rama + Pull Request.
- **Nunca crear workflows de GitHub Actions ni checks adicionales.** Los únicos
  workflows del repo son los que instala y actualiza el harness (`reglas-pr.yml`,
  `tag-release.yml`); no se agregan otros en `.github/workflows/` por proyecto ni
  por funcionalidad (tests, lint, build, deploy) ni se editan a mano. Si el
  proyecto necesita CI propia, se acuerda con el coordinador.
- **Security review antes de cada PR, auditoría antes de cada release.** Ver
  "Pull Request" y "Release".

## Antes de tocar código

```bash
git checkout dev
git pull origin dev           # siempre partir de dev actualizado
git checkout -b tipo/descripcion-corta
```

Chequeo previo: ¿leíste el README? ¿tienes el `.env` local configurado (copiado de
`.env.example`, nunca commiteado)?

## Nombre de rama

```
tipo/descripcion-corta          # o tipo/ID-descripcion-corta si hay ID rastreable
```

| Tipo | Uso |
|---|---|
| `feature/` | Nueva funcionalidad |
| `fix/` | Corrección de error no crítico |
| `hotfix/` | Corrección urgente sobre producción |
| `docs/` | Documentación |
| `chore/` | Mantenimiento, dependencias o configuración |
| `refactor/` | Mejora interna sin cambiar comportamiento |
| `experiment/` | Pruebas, POC, IA o laboratorio |

```
feature/captura-lead
feature/ABC-123-captura-lead     # con ID del tracker del proyecto
fix/error-integracion-erp
hotfix/correccion-produccion
refactor/mejorar-estructura-api
experiment/prueba-modelo-rag
```

**Prohibidos**: `cambios`, `prueba`, `final`, `final-final`, `arreglo`, o el nombre de
una persona. Un nombre de rama tampoco lleva datos sensibles (nada de
`fix/cliente-juan-perez`).

Una rama vive lo que vive el cambio: nace de `dev`, recibe sus commits y PRs, y se
borra tras el merge del último PR. Desde la misma rama se pueden abrir varios PRs a
`dev` (uno abierto a la vez); tras cada merge, `git fetch origin && git merge
origin/dev` y se sigue en la misma rama.

## Commits

```
tipo: descripción breve del cambio
```

Sin scope. Sin ID en el título (el ID, si existe, va en la rama y en el PR; si
quieres dejar rastro de la tarea que cierra un commit, va en el **cuerpo** del
mensaje). Descripciones en el idioma del proyecto.

| | | |
|---|---|---|
| `feat` | `fix` | `docs` |
| `chore` | `refactor` | `test` |
| `style` | `build` | `ci` |
| `perf` | `revert` | |

```
feat: agregar endpoint de consulta de órdenes
fix: corregir error de autenticación con el ERP
refactor: reorganizar servicio de conexión a BD
```

**Ojo**: no existe el tipo de commit `hotfix`. Un hotfix **se commitea como `fix:`**.

**Prohibidos**: `update`, `fix`, `cosas`, `ya`, `ahora sí`.
*Git tiene memoria; no le demos material para novela de misterio.*

Un mensaje de commit tampoco lleva credenciales ni datos de personas.

## Sincronizar con dev

**Por defecto, merge.** Simple, no reescribe historia, no requiere force-push.

```bash
git fetch origin
git merge origin/dev
# resolver conflictos si los hay
git push origin <tu-rama>
```

Rebase es opcional y solo para uso avanzado: nunca sobre rama compartida, y con
`--force-with-lease` confirmado por el usuario. Como el squash & merge descarta el
historial granular de la rama igual, el rebase es esencialmente cosmético.

## Pull Request

**El PR se abre solo con el visto bueno del usuario.** Terminar un cambio no
implica abrir el PR: el agente lo crea únicamente cuando el usuario lo pide
("abre el PR"), dice que quiere mergear/integrar el trabajo o responde que sí a
tu pregunta. **El agente pregunta una sola vez, cuando ya es hora de cerrar** (el
feature está terminado y verificado), si abre el PR; no lo menciona antes ni lo
repite en cada avance. Sin esa respuesta no lo abre. Mientras tanto: commit y push
a la rama. Esto evita PRs de features a medio terminar.

Antes de pedir revisión:
- El proyecto corre localmente.
- El flujo afectado está probado.
- No hay `.env`, credenciales ni datos de la organización en los commits (ni en
  las capturas de la evidencia).
- El README está actualizado si aplica.
- El PR indica si requiere versión/release.

### Security review antes de abrir el PR

**Siempre, antes de abrir cualquier PR, delegar el security review a un subagente**
(`Agent`, tipo `general-purpose`) en vez de correr `/security-review` inline.
Instrúyelo a fondo: que corra `/security-review` sobre el diff de la rama contra
`origin/dev` y devuelva los hallazgos (o la ausencia de ellos) en un resumen claro,
con severidad, archivo y evidencia, sin pegar valores sensibles. Mientras corre, el
agente principal puede seguir armando el resto del PR (plantilla, checklist).

Esto no es un capricho de estilo: correr el review en el mismo hilo hace que, tras
un volcado largo de resultados, el agente principal pierda el hilo y no retome el
PR. Delegarlo a un subagente convierte el resultado en un tool-result concreto que
exige una reacción explícita.

Al recibir el resultado del subagente:
- **Documentar** los hallazgos (o su ausencia) en la sección "Security review" de
  la plantilla del PR: casilla marcada y la línea "Hallazgos:" con contenido real
  (`ninguno` también es contenido real). El check `pr-metadata` falla si la casilla
  no está marcada o la línea sigue con el texto de la plantilla.
- **Sin hallazgos bloqueantes**: seguir directo con push/PR. El security review es
  un paso intermedio del mismo pedido, no un punto de checkpoint.
- **Con hallazgos Critical o High**: parar y preguntar al usuario si quiere
  remediarlos antes de continuar. No abrir el PR con hallazgos sin remediar salvo
  que el usuario decida explícitamente continuar así — en ese caso, dejarlo
  registrado en el PR (quién aceptó el riesgo).

### La plantilla

**Completa `.github/pull_request_template.md` de verdad.** Checkboxes tildadas
porque se hizo, no por rellenar. Nada de "N/A" genéricos: si una sección no aplica,
se **omite entera** (título incluido). **Excepción: "Descripción del cambio",
"Evidencia", "Impacto / Riesgos", "Security review", "Datos sensibles" y "Requiere
versión / release" van siempre** — las valida el check `pr-metadata`, que da FAIL si
faltan, están vacías, dicen "N/A" o conservan el texto guía de la plantilla.

En "Datos sensibles" se marca **exactamente una** casilla: el PR no incluye datos
de la organización, o los incluye **con autorización previa** registrada en
`.datos-autorizados` (y entonces se dice quién autorizó y cuándo). Marcar la
primera cuando el PR sí lleva datos es una falsedad, no un atajo.

**La plantilla no se aplica sola al abrir el PR por CLI.** Solo la web de GitHub la
precarga; `gh pr create` deja el cuerpo que le pases y nada más. El flujo correcto:
escribir la plantilla ya completada en un archivo temporal y abrir el PR con
`gh pr create --base dev --body-file <archivo>`.

### Los checks de PR

Los checks de `scripts/check-pr-rules.mjs` corren en dos lugares, con las mismas
reglas:

- **En la sesión, con el hook `reglas-pr` de Claude Code** (`.claude/hooks/reglas-pr.mjs`,
  no es un git hook):
  - **Antes de cada `git push`** (de todos los del comando, no solo el primero):
    deniega el push si va a `main`/`master` (o los borra), si es
    `--force`/`-f`/`+refspec`, `--all`/`--mirror` o el refspec `:`, si el remoto
    no es `origin`, y corre el grupo `secretos` (archivos de credenciales, llaves
    y tokens en el contenido, datos personales o de nómina) sobre cada commit que
    el push subiría, merges incluidos. Después le pide a git que **ensaye** el
    push (`--dry-run`) y deniega si el destino real es `main` aunque el texto no
    lo diga (upstream, `push.default`). Si falla el check, el push queda denegado
    con el motivo: sigue sus instrucciones (sacar el archivo o el contenido de
    los commits sin pushear; si ya se había pusheado, avisar al usuario para
    rotar la credencial o tratar la filtración). Si no pudo verificar —o se
    quedó sin tiempo—, pide confirmación: no la des por él.
  - **Al crear el PR o editar su body o su base**: los tres grupos contra el PR
    (`rama-commits` es informativo; `secretos` y `pr-metadata` bloquean). El
    resultado se publica como comentario en el PR — la evidencia para el revisor —
    y te vuelve como contexto.
- **En CI**, con `.github/workflows/reglas-pr.yml` (un solo job, check requerido
  `reglas-pr` en la protección de `main`): la segunda línea, para lo que llega
  desde fuera de la sesión.

No lo rodees: nada de `bash -c`, `node -e`, scripts ni otra tool para pushear o
crear el PR por fuera. Los PRs se crean y editan **solo** con `gh pr create` y
`gh pr edit`: el hook no ve el MCP de GitHub ni `gh api`. Si tras crear o editar
el PR no te llegó el resultado de `reglas-pr`, córrelo a mano:
`node .claude/hooks/reglas-pr.mjs --pr <url>`.

**Apenas creas el PR, el hook `reglas-pr` te devuelve el resultado de los
checks.** Con un FAIL en `secretos` o `pr-metadata`, el PR no está listo:
corrígelo en ese momento.

- Body o base: `gh pr edit <url> --body-file <archivo>` o
  `gh pr edit <url> --base dev` (cada edición vuelve a disparar el check y deja
  un comentario nuevo en el PR).
- Conflictos: `git fetch origin && git merge origin/dev`, push, y después
  `node .claude/hooks/reglas-pr.mjs --pr <url>` — un push no vuelve a disparar
  el check del PR.
- Secreto o dato sensible: sácalo en un commit nuevo (`git rm --cached` o edita
  el contenido) y avisa al usuario: ya se pusheó, hay que rotar la credencial o
  tratar la filtración. Un falso positivo (fixture sintético, ejemplo de la
  documentación) lo resuelve **el usuario** registrando la ruta en
  `.datos-autorizados` o marcando la línea con `coe:no-secreto`; el agente nunca
  lo hace por su cuenta.
- `rama-commits` es informativo: no reescribas commits ya pusheados por su
  formato.

Si el FAIL no se arregla desde el body o la base (por ejemplo, `gh` sin
autenticar), o sigue tras dos rondas de corrección, **para y repórtalo al
usuario** — no reintentes en bucle.

Si piden correcciones: **pushear a la misma rama.** El PR se actualiza solo. Crear un
PR nuevo por cada corrección rompe la trazabilidad y duplica el ruido.

**Al editar el body de un PR a pedido del usuario, re-lanza en el mismo paso los
jobs de CI fallidos de ese PR.** Cambiar la descripción no re-dispara todos los
checks, y un PR suele arrastrar checks en rojo por fallos transitorios que
conviene reintentar. Detecta los fallidos con `gh pr checks <pr>` y relánzalos con
`gh run rerun <run-id> --failed` — solo los jobs en estado `failure`, no el run
completo. Si no hay jobs fallidos, edita el body y no hagas nada más.

Integración: **squash & merge**, y la hace el coordinador. Para un `refactor/`
grande o una migración, el coordinador puede optar por merge commit y lo registra
en el PR.

Después del merge (esto sí lo puedes hacer):
```bash
git checkout dev && git pull origin dev && git branch -d <tu-rama>
```

## Release: `dev` → `main`

El release es un PR de `dev` a `main`. Antes de abrirlo:

1. **Corre la skill `security-audit`** sobre lo que entra en el release (alcance
   `diff` entre `main` y `dev`, o `full` si el coordinador lo pide). Su estado
   (`READY FOR REVIEW` o `READY WITH CONDITIONS`) y la ruta del informe en
   `docs/security/` van en la sección "Security review" del PR; el check
   `pr-metadata` lo exige en los PRs con base `main`. Con estado `NOT READY`, el
   release no se abre: se remedia primero.
2. **Propón la versión** editando `version` en `package.json` (o la fuente de
   versión del stack) como parte del PR de release. Ese bump se commitea
   **directo en `dev`** — nunca en una rama `chore` aparte solo para el bump.
3. Abre el PR con `gh pr create --base main --head dev --body-file <archivo>`, con
   la sección "Requiere versión / release" marcada en `Sí` y la versión sugerida.

Tras el merge, el workflow `tag-release.yml` lee esa versión del commit de merge y
crea/pushea el tag inmutable `vX.Y.Z` y el tag móvil de la serie (`v1`) — es
idempotente. En repos sin Actions, el agente los crea y pushea en el mismo
momento:

```bash
git fetch origin && node scripts/tag-release.mjs --ref origin/main
```

`--ref` lee la versión del `package.json` de `origin/main` y taggea ese commit, sin
cambiar de rama ni tocar tu árbol de trabajo. En repos sin `scripts/tag-release.mjs`
(stack no Node), usa el script de tags del stack (skill `harness-upgrade`) o créalos
a mano: `vX.Y.Z` anotado y el móvil `vX` movido al mismo commit. Los releases de
GitHub siguen siendo del coordinador.

## Versionamiento

SemVer con prefijo `v`: `v1.2.3`.

| Cambio | Regla |
|---|---|
| Corrección menor | PATCH · `v1.0.0 → v1.0.1` |
| Funcionalidad compatible | MINOR · `v1.0.1 → v1.1.0` |
| Cambio incompatible | MAJOR · `v1.1.0 → v2.0.0` |

## Secretos y datos sensibles

Nunca en el repo. `.env.example` sin valores. Datos de prueba sintéticos. Si una
credencial se expone por accidente: **rotarla**, no solo borrar el commit. Si se
expone un dato de personas: avisar al usuario y al coordinador; limpiar el
historial es decisión del coordinador. El detalle completo está en la skill
`datos-sensibles`.

## Lo que esta guía NO define

No lo inventes. Si hace falta, pregunta:

- Formato del **título** del PR.
- **Scopes** de commit (`feat(api):`) — el formato es solo `tipo: descripción`.
- **Trailers** de commit (`Co-Authored-By`, `Signed-off-by`).
- `CHANGELOG.md` — el changelog es el `git log` de `main`, salvo que el proyecto
  decida llevar uno.
- Ramas `release/*` — no existen.
- `BREAKING CHANGE` / `!` de Conventional Commits.
- Git hooks, `--no-verify` (el hook `reglas-pr` es de Claude Code, no de git).
- Commits firmados: **no** son obligatorios hoy.
