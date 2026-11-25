---
name: github-releases-versioning
description: Versionado y releases en GitHub — tags anotados, SemVer, Conventional Commits como fuente del changelog, release notes autogeneradas con `.github/release.yml`, pre-releases, versionado coordinado entre repos hermanos y flujo de hotfix. Usar al cortar una versión, al definir el esquema de versiones de un repo nuevo, al configurar las categorías de las release notes, al publicar un release candidate, al sacar un hotfix sobre producción, o al decidir si un cambio es major, minor o patch.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Releases y versionado

Un release es un **punto nombrado, inmutable y reproducible** de la historia, con notas que le
dicen a un humano qué cambió y si le rompe algo. Cómo se despliega y cómo se vuelve atrás:
`release-and-rollback`. Cómo llegan los commits a la rama: `github-pull-requests`.

## 1. SemVer: qué número sube

`MAJOR.MINOR.PATCH` — decide el **contrato público**, no el esfuerzo.

| Cambio | Sube |
|---|---|
| Rompe a un consumidor: endpoint/campo quitado o renombrado, tipo cambiado, campo que pasa a obligatorio, semántica distinta, evento con otra forma | **MAJOR** |
| Agrega capacidad compatible: endpoint nuevo, campo opcional nuevo, valor nuevo que los consumidores toleran | **MINOR** |
| Corrige sin cambiar contrato | **PATCH** |
| Refactor, tests, docs, CI | No requiere release por sí solo |

Reglas:
1. Definí qué es "contrato público" **por repo**: en la API, el OpenAPI y los eventos; en el
   modelo, el esquema que consumen los demás; en web y mobile, normalmente la versión es de
   producto y no hay consumidores de código. Escribilo en el CLAUDE.md del proyecto.
2. Un enum "abierto" que gana un valor es MINOR **solo si** los consumidores están hechos para
   ignorar valores desconocidos. Si no, es MAJOR. Verificalo, no lo asumas.
3. Detección de breaking changes del contrato HTTP: automatizada contra el OpenAPI
   (`api-openapi-docs`), no a ojo.
4. `0.y.z` = todo puede romper. Salí de `0.x` cuando haya un consumidor real en producción.
5. Una versión publicada **no se modifica**. Error en `1.4.0` → `1.4.1`.

## 2. Conventional Commits → changelog

Formato: `tipo(ámbito opcional): descripción`. Con squash merge, el **título del PR** es el
commit que queda (`github-pull-requests` §2): ahí se aplica la convención.

| Tipo | Efecto en versión |
|---|---|
| `feat` | MINOR |
| `fix`, `perf` | PATCH |
| `feat!` / `fix!` o pie `BREAKING CHANGE:` | MAJOR |
| `refactor`, `test`, `docs`, `chore`, `ci`, `build` | Ninguno |

- El `!` o el pie `BREAKING CHANGE:` van acompañados de **qué rompe y cómo migrar**.
- Validá el formato del título del PR en CI; no dependas de la memoria del equipo.
- Si automatizás el bump con una herramienta, su configuración exacta: verificar en su doc oficial.

## 3. Tags

```bash
git tag -a v1.4.0 -m "v1.4.0"      # anotado: autor, fecha y mensaje propios
git push origin v1.4.0
```

- **Siempre anotados** (`-a`), nunca livianos: el anotado es un objeto con autoría y fecha; el
  liviano es solo un puntero. Firmados (`-s`) si la casa exige firma.
- Prefijo `v` consistente en todos los repos.
- **Nunca** muevas ni reuses un tag publicado. Protegé `v*` con un ruleset de tags: restringir
  actualización y borrado (`github-branch-protection-rulesets`).
- El tag se crea sobre un commit **ya mergeado** en la rama de release, con CI verde.

## 4. Release notes autogeneradas

GitHub arma las notas desde los **PRs mergeados** (lista de PRs, contribuyentes y enlace al
changelog completo), agrupados por **labels** según `.github/release.yml`:

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
    authors:
      - dependabot[bot]
  categories:
    - title: Cambios incompatibles
      labels: [riesgo:breaking]
    - title: Funcionalidades
      labels: [tipo:feature]
    - title: Correcciones
      labels: [tipo:bug]
    - title: Seguridad
      labels: [riesgo:seguridad]
    - title: Otros
      labels: ["*"]
```

- Claves: `changelog.exclude.labels`, `changelog.exclude.authors`, y por categoría `title`,
  `labels` (ambas obligatorias) más `exclude.labels` / `exclude.authors`.
- `"*"` es el comodín para lo que no cayó en ninguna categoría anterior: va **último**.
- Consecuencia: **un PR sin label cae en "Otros"**. Las notas son tan buenas como la taxonomía de
  labels (`github-issues-projects` §3) y los títulos de los PRs.

Crear el release:

```bash
gh release create v1.4.0 --verify-tag --generate-notes --notes-start-tag v1.3.0
```

- `--verify-tag` aborta si el tag no existe en el remoto: evita que `gh` cree uno implícito
  desde donde no querías.
- `--notes-start-tag` fija desde qué tag se calculan las notas (imprescindible tras hotfixes o
  con varias líneas de versión).
- `--draft` para revisar antes de publicar; `--target <rama|sha>` si no sale de la default.
- Editá las notas generadas: arriba de todo, un párrafo humano con **qué hay que saber** y los
  pasos de migración si hay breaking. La lista de PRs es el anexo.
- Un fallo de seguridad corregido se anuncia **después** de que el fix esté desplegado, sin
  detalles explotables (`github-security-features`).

## 5. Pre-releases

- Sufijos SemVer: `v2.0.0-rc.1`, `v2.0.0-beta.2`. Ordenan antes que `v2.0.0`.
- `gh release create v2.0.0-rc.1 --prerelease --generate-notes`. Un pre-release no se marca
  "Latest"; `--latest` lo controla explícitamente cuando hay varias líneas vivas.
- El `rc` que pasa QA se **promueve**: mismo commit, tag final nuevo. No se recompila "lo mismo"
  desde otro commit.
- QA firma sobre un tag, no sobre "la rama de hoy" (`qa-orchestration`).

## 6. Versionado coordinado entre repos

Con repos hermanos (API, web, mobile, modelo, landing):

1. **Versión independiente por repo.** No fuerces el mismo número en todos: cada uno tiene su
   ritmo y su contrato.
2. **Matriz de compatibilidad explícita**: qué versión de web/mobile requiere qué mínimo de API,
   y qué versión del modelo genera el esquema de cada API. Vive en un lugar único (repo de
   coordinación o documentación), no en la cabeza de alguien.
3. La API publica su versión en un endpoint o header; los clientes pueden chequear el mínimo.
4. **Mobile manda en compatibilidad hacia atrás**: las versiones viejas de la app siguen
   instaladas semanas. Un MAJOR de la API necesita ventana de convivencia
   (`github-multirepo-coordination`).
5. Un "release de producto" es un **manifiesto**: `{api: v3.2.1, web: v5.0.0, mobile: v2.8.0,
   modelo: v4.1.0}`. Versioná el manifiesto; eso es lo que se despliega y a lo que se vuelve.
6. Builds de stores tienen además su número de build monotónico (`mobile-release-security`).

## 7. Hotfix

```text
v1.4.0 (producción)
   └─ rama hotfix/1.4.1 desde el TAG, no desde la rama de integración
        └─ fix mínimo + test que lo reproduce → PR → CI → tag v1.4.1 → deploy
             └─ llevar el fix a la rama de integración (cherry-pick o merge) — OBLIGATORIO
```

1. Se parte del **tag en producción**: la rama de integración ya tiene cosas no liberadas.
2. Alcance mínimo: solo el fix y su test (`scope-discipline`, `root-cause-debugging`).
3. Mismos gates que un release normal; urgencia no es permiso para saltear CI. Si se usó bypass,
   queda registrado.
4. El paso que más se olvida: **portar el fix hacia adelante**. Sin eso, el próximo release
   reintroduce el bug. Issue de seguimiento abierto hasta que el port esté mergeado.
5. Notas: `--notes-start-tag v1.4.0` para que listen solo el hotfix.
6. Después: postmortem (`incident-response-postmortem`).

## Anti-patrones

- Tags livianos, o tags movidos "porque faltaba un commit".
- Bump de versión a ojo sin mirar el contrato.
- Breaking change escondido en un `fix:`.
- Release notes = lista cruda de commits sin un párrafo humano.
- Release cortado desde un commit con CI rojo o sin mergear.
- Mismo número de versión forzado en repos con ritmos distintos.
- Hotfix que nunca volvió a la rama de integración.
- Recompilar para "promover" un rc en vez de reusar el commit probado.

## Checklist

- [ ] Contrato público de cada repo definido por escrito.
- [ ] Títulos de PR en Conventional Commits, validados en CI.
- [ ] `.github/release.yml` con categorías alineadas a los labels; `"*"` al final.
- [ ] Tag anotado, con prefijo `v`, sobre commit mergeado y verde; tags `v*` protegidos.
- [ ] Release creado con `--verify-tag` y `--notes-start-tag` correcto.
- [ ] Notas con resumen humano y migración si hay MAJOR.
- [ ] Pre-releases marcados; rc promovido sobre el mismo commit.
- [ ] Matriz de compatibilidad y manifiesto de producto actualizados.
- [ ] Hotfix portado a integración, con issue de seguimiento cerrado.
