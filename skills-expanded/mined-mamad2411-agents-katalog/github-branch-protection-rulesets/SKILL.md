---
name: github-branch-protection-rulesets
description: Protección de ramas en GitHub con rulesets y reglas clásicas — checks y reviews requeridos, CODEOWNERS (ubicación, sintaxis y precedencia), historial lineal, commits firmados, merge queue, bloqueo de force-push y borrado, y bypass controlado. Usar al configurar un repo nuevo, al endurecer la rama de integración o la de producción, al escribir o depurar un CODEOWNERS, al decidir quién puede saltear una regla, o cuando un PR queda bloqueado por un check que nunca reporta.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Protección de ramas: rulesets y CODEOWNERS

Regla de la casa, sin excepciones: **nadie —persona ni agente— commitea directo a la rama de
integración ni a la de producción.** Todo entra por PR (`github-pull-requests`). Esta skill es
el candado que lo hace cumplir en la plataforma, en vez de depender de la buena voluntad.

## 1. Rulesets vs branch protection clásica

| | Branch protection clásica | Rulesets |
|---|---|---|
| Reglas por rama | Una sola aplica | **Varios** rulesets se superponen |
| Apagar sin borrar | No | Sí: estado *Active* / *Disabled* |
| Visibilidad | Solo admins | Cualquiera con lectura ve los rulesets activos |
| Alcance | Un repo | Repo u organización (según plan) |
| Metadatos de commit | No | Sí: mensaje, email del autor |
| Tags | No | Sí |

- Preferí **rulesets** para todo lo nuevo. Disponibilidad según plan: verificar en la doc oficial
  antes de prometer una regla en un repo privado.
- **Superposición**: cuando varios rulesets (o un ruleset y una regla clásica) cubren la misma
  rama, las reglas se **agregan** y gana la versión **más restrictiva**. No podés "aflojar" con
  un segundo ruleset.
- La API expone `enforcement` con valores `active`, `disabled` y `evaluate` (probar la regla sin
  aplicarla). Disponibilidad de `evaluate` según plan: verificar en la doc oficial.
- **Push rulesets** (restringir paths, extensiones, tamaño de archivo) aplican a toda la red de forks.

## 2. Reglas disponibles y postura de la casa

| Regla (nombre en la UI) | Rama de integración | Rama de producción |
|---|---|---|
| Require a pull request before merging | Sí | Sí |
| └ aprobaciones requeridas | ≥ 1 | ≥ 1 (≥ 2 en módulos sensibles) |
| └ descartar aprobaciones ante commits nuevos | Sí | Sí |
| └ review de Code Owners | Sí | Sí |
| └ resolver conversaciones antes de mergear | Sí | Sí |
| Require status checks to pass | Sí | Sí |
| └ rama actualizada antes de mergear | Si no hay merge queue | Sí |
| Block force pushes | Sí | Sí |
| Restrict deletions | Sí | Sí |
| Require linear history | Si la casa usa squash/rebase | Ídem |
| Require signed commits | Evaluar (§5) | Evaluar |
| Require deployments to succeed | — | Si hay staging |
| Require code scanning results | Si está habilitado | Sí |
| Restrict creations / updates | Para patrones `release/*` | Sí |

"Módulos sensibles" en un producto de salud: datos clínicos, consentimiento, autenticación,
autorización, contabilidad, esquema de datos, workflows de CI. Ver `data-privacy-sensitive`.

## 3. Checks requeridos — trampas

1. Un check requerido se identifica por el **nombre del job** (o del contexto de estado).
   Renombrar un job rompe el requisito en silencio: el PR queda esperando un check que ya no existe.
2. Un workflow filtrado por `paths:` que **no corre** deja el check requerido en "Expected"
   para siempre. Solución: un job que siempre reporte (y decida adentro si hay trabajo),
   no sacar el requisito.
3. Con matrix, cada combinación es un check distinto. Requerí un job "resumen" que dependa
   (`needs:`) de toda la matrix, no cada celda.
4. Con **merge queue**, los workflows requeridos deben dispararse también con `merge_group`
   (`github-actions-ci`); si no, la cola nunca avanza.
5. Requerí solo checks **deterministas**. Un check flaky requerido enseña al equipo a
   re-ejecutar hasta verde (`regression-suite-management`).

## 4. CODEOWNERS

**Ubicación** — GitHub busca en este orden y usa el **primero** que encuentra:
`.github/CODEOWNERS` → `CODEOWNERS` (raíz) → `docs/CODEOWNERS`. Cada rama tiene el suyo: vale el
de la rama **base** del PR.

**Sintaxis** — patrones estilo gitignore, con excepciones que **no** funcionan:
negación con `!`, rangos con `[ ]`, y escapar `#` con `\`. Los paths distinguen mayúsculas.
Una línea inválida se **saltea** (la UI del repo la resalta). Tope de tamaño: 3 MB.

**Precedencia** — gana el **último** patrón que matchea. Lo general arriba, lo específico abajo.

```text
# Default: todo
*                           @mi-org/plataforma

# Por área
/src/modules/clinical/      @mi-org/clinico @mi-org/seguridad
/src/modules/accounting/    @mi-org/contable
*.sql                       @mi-org/datos

# El CI y este archivo siempre tienen dueño
/.github/                   @mi-org/plataforma
/.github/workflows/         @mi-org/plataforma @mi-org/seguridad
/.github/CODEOWNERS         @mi-org/plataforma
```

Hechos verificados:
- Dueños como `@usuario`, `@org/equipo` o email. Varios dueños van **en la misma línea**; si los
  partís en dos líneas, solo cuenta la última.
- Usuarios y equipos necesitan acceso de **escritura explícito** al repo, aunque ya lo tengan
  por otra vía. Si no, no se les pide review y la regla no se cumple como esperás.
- Con "Require review from Code Owners", alcanza la aprobación de **cualquiera** de los dueños
  del path, no de todos. Si necesitás dos áreas, exigí el número de aprobaciones además.
- Preferí **equipos** a personas: las personas se van de vacaciones y de la empresa.

❌ Patrón específico arriba y `*` abajo: el `*` final pisa todo.
❌ Equipo sin permiso de escritura: aparece en el archivo, nunca recibe el review.
✅ `CODEOWNERS` protegido por sí mismo, para que nadie se quite como dueño en el mismo PR.

## 5. Historial lineal y commits firmados

- **Require linear history** prohíbe commits de merge: obliga a squash o rebase. Coherente con
  squash por defecto; incompatible con "merge commit" en esa rama.
- **Require signed commits** exige commits firmados y verificados. Antes de activarlo: todas las
  personas **y bots** que pushean a la rama tienen que poder firmar, y el método de merge
  elegido debe producir commits verificados (el rebase desde la UI reescribe los commits:
  probalo en un repo de prueba). Activarlo sin ese ensayo bloquea al equipo entero.

## 6. Merge queue

Sirve cuando hay muchos PRs compitiendo por la misma rama: valida cada PR **sobre el estado
que va a tener la base** y evita el "verde por separado, rojo juntos".

- Se exige con la opción "Require merge queue" de la protección de la rama base.
- Configurable: método de merge, concurrencia de builds, tamaño mínimo/máximo de grupo y espera,
  timeout de checks, si solo se mergean grupos sin fallas.
- Requisito duro: workflows con trigger `merge_group`.
- `gh pr merge` contra una rama con cola no necesita estrategia: encola el PR (o activa
  auto-merge si faltan checks). `--admin` la saltea: ver §7.
- Disponibilidad por plan y tipo de repo: verificar en la doc oficial.

## 7. Bypass controlado

1. La lista de bypass admite **roles** (p. ej. admin del repo), **equipos** y **GitHub Apps**.
   Mantenela mínima; nunca "todos los maintainers".
2. Bypass es para **emergencias con registro**: quién, cuándo, por qué, y el PR de regularización.
3. Un bot de release que necesita pushear tags o bumps: dale bypass a **esa App**, acotado a ese
   ruleset, no a una persona con un token personal.
4. **Agentes**: jamás usan `--admin`, ni force-push a ramas protegidas, ni editan rulesets.
   Si una regla bloquea, reportan BLOCKED con la regla exacta (`evidence-and-verification`).
5. "Incluir administradores" activado: si los admins pueden saltear todo, la regla es decorativa.

## Anti-patrones

- Proteger solo la rama de producción y dejar abierta la de integración.
- Requerir un check por nombre y después renombrar el job.
- CODEOWNERS con personas individuales y sin cubrir `.github/`.
- Aprobaciones que no se descartan ante commits nuevos: se aprueba una cosa y se mergea otra.
- Desactivar el ruleset "un ratito" para destrabar un merge, sin registro.
- Dar bypass a un equipo amplio para no discutir un check flaky.

## Evidencia / DoD

Para afirmar "la rama está protegida", pegá la salida literal de:

```bash
gh api repos/{owner}/{repo}/rulesets --jq '.[] | {name, enforcement, target}'
gh api repos/{owner}/{repo}/rules/branches/<rama> --jq '.[].type'
```

(en PowerShell, los `{owner}` `{repo}` van entre comillas) y además:
- CODEOWNERS sin errores en la vista del repo, y un PR de prueba que **sí** pidió review al equipo esperado.
- Un intento de push directo a la rama protegida **rechazado** (salida del `git push`).
- Lista de bypass actual, con justificación de cada entrada.

Sin esas salidas, el estado es "configurado, no verificado".

## Checklist

- [ ] Ruleset activo sobre integración y producción; superposiciones entendidas (gana lo más restrictivo).
- [ ] PR obligatorio, aprobaciones ≥ 1, descarte ante commits nuevos, conversaciones resueltas.
- [ ] Checks requeridos por nombre estable; job resumen para matrix; nada flaky.
- [ ] Force-push y borrado bloqueados.
- [ ] CODEOWNERS en `.github/`, general→específico, con equipos con escritura explícita.
- [ ] `.github/workflows/` y el propio CODEOWNERS con dueño.
- [ ] Commits firmados / historial lineal ensayados antes de activar.
- [ ] `merge_group` en workflows si hay merge queue.
- [ ] Bypass mínimo, por App o rol, con registro de uso.
- [ ] Evidencia literal pegada.
