---
name: github-pull-requests
description: Estándar de la casa para pull requests en GitHub — PR chico y revisable, título y descripción con plantilla (qué, por qué, cómo probar, evidencia, riesgo), draft PRs, vínculo con issues por palabras clave de cierre, elección de squash/merge/rebase, resolución de conversaciones, PRs apilados y qué NO entra en un PR. Usar al abrir, describir, actualizar o mergear un PR, al partir un cambio grande en varios, o al revisar si un PR está listo para pedir review.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Pull requests en GitHub

Un PR es la unidad de revisión y de reversión. Si no se puede revisar en una sentada ni revertir
de un solo golpe, está mal cortado. El criterio de revisión vive en `code-review-standard`; la
evidencia que acompaña al PR, en `evidence-and-verification`. Esta skill cubre la forma del PR.

## 1. Tamaño y corte

1. **Un PR = un cambio lógico.** Si el título necesita "y", son dos PRs.
2. Apuntá a que se lea en una sentada. No hay número mágico: el límite es la atención del revisor.
   Si el diff es grande por archivos generados, lockfiles o renombres, decilo en la descripción
   y separá esos commits.
3. Separá **mecánico** de **semántico**: renombres, formateo y movimientos de archivos van en un
   PR (o commit) propio; el cambio de comportamiento, en otro. Mezclados, el revisor no ve nada.
4. Refactor previo necesario → PR propio, primero, sin cambio de comportamiento.
5. En cambios full-stack que cruzan repos, un PR por repo, vinculados entre sí
   (ver `github-multirepo-coordination`).

## 2. Rama y título

- Nunca se commitea directo a la rama de integración: rama nueva **antes** del primer commit
  (la protección la impone `github-branch-protection-rulesets`).
- Título en imperativo, específico, ≤ ~70 caracteres, con prefijo Conventional Commits
  (`feat:`, `fix:`, `refactor:`…) porque con squash el título **es** el commit que queda
  en la historia y alimenta el changelog (`github-releases-versioning`).

❌ `Cambios agenda` · `fix` · `WIP`
✅ `fix(agenda): rechazar bloqueos que se solapan con citas confirmadas`

## 3. Descripción — plantilla de la casa

Guardala en `.github/pull_request_template.md` (ver `github-repo-standards`).

```markdown
## Qué
<el cambio, en 1–3 frases; qué ve distinto el usuario o el consumidor de la API>

## Por qué
<problema o requisito; issue/carril vinculado>   Closes #123

## Cómo probar
<pasos reproducibles, datos necesarios, comando exacto>

## Evidencia
<salida literal de tests/typecheck, capturas o trace; qué quedó SIN cubrir>

## Riesgo y reversión
<qué puede romperse, a quién afecta, cómo se revierte; cambios de contrato/esquema>
```

Reglas:
- "Evidencia" lleva **salida literal**, no "tests pasan". Sin evidencia, el PR queda en draft.
- Declarar lo no cubierto es obligatorio: evita que un PASS parcial se lea como total.
- Cambios de UI: captura antes/después (claro y oscuro si existen ambos).
- Cambios de contrato (API, esquema, eventos): decilo arriba y enlazá los PRs hermanos.
- Nada de datos personales ni clínicos reales en descripción, capturas o logs pegados.

## 4. Draft PRs

- Abrí en **draft** cuando querés CI y feedback temprano pero no está para revisión formal.
  Un draft no se puede mergear y no dispara la solicitud automática a code owners hasta
  marcarlo listo.
- `gh pr create --draft` para crearlo; `gh pr ready` para pasarlo a revisión.
- Pasá a "ready" solo cuando: CI verde, descripción completa, auto-revisión hecha (§6).

## 5. Vincular issues

Palabras clave de cierre (en la **descripción del PR** o en un mensaje de commit):
`close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved`.

| Caso | Sintaxis |
|---|---|
| Mismo repo | `Closes #10` |
| Otro repo | `Fixes org/repo#100` |
| Varios | `Resolves #10, resolves #123, resolves org/repo#100` (keyword por cada uno) |

Trampas verificadas en la doc:
- Solo cierra automáticamente si el PR apunta a la **rama por defecto**. Contra cualquier otra
  rama las keywords **se ignoran**: no hay vínculo ni cierre. Si la rama de integración de la
  casa no es la default del repo, vinculá a mano desde el panel del PR (hasta 10 issues).
- Una keyword en un commit cierra el issue al llegar a la default, pero el PR **no** aparece
  como vinculado. Preferí la descripción del PR.
- Si el PR solo avanza el issue sin terminarlo, escribí `Refs #10`: no cierra nada.

## 6. Antes de pedir review

1. Leé tu propio diff completo en la pestaña "Files changed". Lo que te da vergüenza, arreglalo.
2. Sin archivos ajenos al cambio, sin `console.log`, sin código comentado, sin secretos.
3. CI verde. No pidas review con checks rojos "que después arreglo".
4. Rama actualizada contra la base si hay conflicto o si la base cambió el contrato que tocás.
5. Pedí review a quien corresponde; CODEOWNERS lo hace solo para los paths cubiertos.

## 7. Conversaciones

- Respondé **todo** comentario: con un cambio, una explicación, o un issue de seguimiento enlazado.
- Resuelve el hilo **quien lo abrió** (o quien aplicó el cambio, citando el commit). No resuelvas
  en masa para destrabar el merge.
- Cambios tras el review: commits nuevos, **no** force-push que reescriba lo ya revisado; el
  revisor tiene que poder ver qué cambió desde su última pasada. Si hay squash al final, la
  historia intermedia no importa.
- Desacuerdo que no cierra en dos idas y vueltas → conversación sincrónica, y se deja el resumen
  escrito en el hilo.

## 8. Estrategia de merge

| Método | Qué hace | Cuándo |
|---|---|---|
| **Squash and merge** | Todos los commits del PR → un commit en la base | Default de la casa: el PR es un cambio lógico con commits de fixup |
| **Merge commit** (`--no-ff`) | Conserva todos los commits + un commit de merge | Ramas largas o de release; cuando cada commit tiene valor propio y está limpio |
| **Rebase and merge** | Reaplica cada commit sobre la base, historia lineal | Pocos commits, atómicos y todos verdes por separado |

Hechos a recordar:
- Tras un **squash**, no sigas trabajando en la misma rama: los PRs siguientes pueden arrastrar
  commits ya aplastados y repetir conflictos. Rama nueva desde la base actualizada.
- **Rebase and merge** de GitHub siempre reescribe SHAs y el committer; si los commits estaban
  firmados, verificá cómo queda la firma antes de exigirla por regla.
- Un PR puede quedar `merged` **indirectamente** (sus commits llegan a la base por otro camino)
  aunque no haya cumplido las reglas de protección. No empujes a mano commits de un PR abierto.
- Elegí los métodos permitidos a nivel repo y deshabilitá el resto (`github-repo-standards`).
- Auto-merge: `gh pr merge --auto --squash` deja el merge esperando a que pasen los requisitos.
- `--admin` saltea requisitos: **no** lo usa un agente, y un humano solo con registro del porqué.

## 9. PRs apilados

Para un cambio grande que no se puede partir en PRs independientes:
1. Cadena de ramas: `A` ← `B` ← `C`; cada PR apunta a la rama anterior, no a la base final.
2. Cada PR se revisa solo con **su** diff. La descripción dice su posición: "2/3, depende de #41".
3. Se mergea **de abajo hacia arriba**. Al mergear `A`, re-apuntá `B` a la base y actualizalo.
4. Con squash, rebasar los de arriba después de cada merge es inevitable: previsto, no sorpresa.
5. Recordá §5: los PRs intermedios no apuntan a la default, así que sus keywords no cierran issues.

Existe una extensión oficial de `gh` para stacks (`gh-stack`); evaluala antes de automatizar a mano.

## 10. Qué NO va en un PR

- Refactors no pedidos "de paso" (`scope-discipline`).
- Reformateo masivo mezclado con lógica.
- Artefactos de build, `.env`, dumps de base, datos reales de personas.
- Cambios a `.github/workflows/` escondidos en un PR de feature: van aparte y con dueño en CODEOWNERS.
- Tests deshabilitados (`skip`) para poner verde el CI.
- Bumps de dependencias no relacionados (`dependency-management`).

## Anti-patrones

- PR gigante "porque todo está relacionado".
- Descripción vacía o que repite el título.
- "LGTM" sin haber corrido ni leído el "cómo probar".
- Force-push a mitad de review sin avisar.
- Mergear con conversaciones abiertas o checks requeridos salteados con privilegios de admin.
- Rama reutilizada después de un squash.

## Checklist

- [ ] Un solo cambio lógico; mecánico separado de semántico.
- [ ] Rama propia; título imperativo con prefijo convencional.
- [ ] Descripción con las 5 secciones; evidencia literal y "no cubierto" declarado.
- [ ] Issue vinculado con la keyword correcta (o a mano si la base no es la default).
- [ ] Auto-revisión del diff hecha; sin ruido, sin secretos, sin datos reales.
- [ ] CI verde antes de salir de draft.
- [ ] Todas las conversaciones respondidas y resueltas por quien corresponde.
- [ ] Método de merge acorde a la tabla; rama borrada tras el merge.
- [ ] PRs hermanos en otros repos enlazados y con orden de merge explícito.
