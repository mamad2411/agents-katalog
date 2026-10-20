---
name: github-cli-automation
description: Uso de la CLI `gh` para operar GitHub desde la terminal y desde scripts — PRs, issues, corridas de Actions, releases, settings de repo, secrets/variables y `gh api` con paginación y `--jq`; autenticación y scopes; diferencias entre Bash y PowerShell en Windows; y qué acciones puede ejecutar un agente solo y cuáles exigen confirmación humana. Usar al abrir o consultar un PR, diagnosticar una corrida fallida, automatizar una tarea repetida sobre varios repos, o antes de que un agente ejecute cualquier comando `gh` que escriba.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# `gh` — automatización de GitHub

Flags verificados contra cli.github.com/manual. Ante la duda: `gh <comando> --help` es la
fuente de verdad de la versión **instalada**; no escribas flags de memoria
(`anti-hallucination-guard`).

## 1. Autenticación y scopes

```bash
gh auth status                       # quién soy, en qué host, con qué scopes
gh auth login                        # interactivo (navegador)
gh auth refresh --scopes read:project   # agregar un scope sin re-loguear de cero
gh auth refresh --remove-scopes delete_repo
```

- Headless / CI: variable de entorno **`GH_TOKEN`**. En Actions:
  `env: { GH_TOKEN: ${{ github.token }} }` y el alcance lo da el bloque `permissions` del workflow.
- Para fine-grained PATs, la doc recomienda `GH_TOKEN` en vez de `gh auth login --with-token`.
- Scopes mínimos de `gh`: `repo`, `read:org`, `gist`. Todo lo demás se agrega a demanda y se
  **quita** al terminar. `delete_repo` no se deja puesto nunca.
- Qué tipo de token usar para cada caso: `github-security-features` §7.
- Otro repo sin hacer `cd`: `-R owner/repo` o `GH_REPO`.

## 2. Pull requests

```bash
gh pr create --draft --base develop --title "fix(agenda): …" --body-file pr.md
gh pr create --fill                 # título y cuerpo desde los commits
gh pr create --dry-run              # muestra qué haría (puede pushear igual)
gh pr ready                         # draft → listo para review
gh pr status                        # mis PRs y los que esperan mi review
gh pr view 42 --json title,state,mergeable,reviewDecision,statusCheckRollup
gh pr checks 42 --watch --fail-fast # esperar CI; --required para solo los obligatorios
gh pr diff 42
gh pr merge 42 --squash --delete-branch
gh pr merge 42 --auto --squash      # mergea solo cuando se cumplan los requisitos
```

- Otros flags de `create`: `--reviewer`, `--label`, `--assignee @me`, `--milestone`,
  `--project`, `--template`, `--head`.
- `--body-file` > `--body`: evita pelearte con comillas y saltos de línea en el shell.
- `gh pr merge` contra una rama con **merge queue** no necesita estrategia: encola, o activa
  auto-merge si faltan checks. `--match-head-commit <sha>` garantiza que mergeás lo que revisaste.
- `--admin` saltea requisitos: prohibido para agentes (§8).

## 3. Issues y labels

```bash
gh issue list --search "solapamiento agenda" --state all   # buscar duplicados ANTES de crear
gh issue create --title "…" --body-file bug.md --label "tipo:bug"
gh issue view 123 --comments
gh issue comment 123 --body-file hallazgo.md
gh label clone org/repo-plantilla            # copia labels al repo actual; los existentes se saltean
gh label clone org/repo-plantilla --force    # …o se sobrescriben
```

`gh label clone` no borra labels que sobran en el destino: la poda es aparte y manual.

## 4. Corridas de Actions

```bash
gh run list --branch mi-rama --status failure --limit 5
gh run view <id> --log-failed        # SOLO los pasos fallidos: empezá siempre por acá
gh run view <id> --job <job-id> --log
gh run watch <id> --exit-status      # bloquea hasta terminar; exit ≠ 0 si falló
gh run rerun <id> --failed           # re-ejecuta solo lo fallado (y sus dependencias)
gh run rerun <id> --debug            # con logging de depuración
gh run download <id>                 # artefactos (traces de Playwright)
gh workflow run deploy.yml --ref main -f entorno=staging
```

- `gh workflow run` exige que el workflow tenga `on.workflow_dispatch`. `-f` manda string crudo;
  `-F` respeta la sintaxis `@archivo`; `--json` lee los inputs por stdin.
- Un rerun verde no cierra un fallo: clasificá primero (`e2e-failure-triage`,
  `root-cause-debugging`).

## 5. `gh api`

```bash
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].title'
gh api --paginate --slurp repos/{owner}/{repo}/pulls --jq 'flatten | length'
gh api repos/{owner}/{repo}/issues/123/comments -f body='Texto'          # con campos → POST
gh api -X PATCH repos/{owner}/{repo} -F delete_branch_on_merge=true
gh api graphql -f query='query { viewer { login } }'
```

| Flag | Para qué |
|---|---|
| `--paginate` | Recorre **todas** las páginas. Sin esto ves solo la primera y sacás conclusiones falsas |
| `--slurp` | Junta las páginas en un único array JSON (con `--paginate`) |
| `-q, --jq` | Filtra con sintaxis jq; no hace falta tener `jq` instalado |
| `-f` / `-F` | Campo string crudo / campo tipado (número, booleano, `@archivo`, `@-` stdin) |
| `-X` | Método HTTP (default GET; con campos pasa a POST) |
| `-H` | Header |
| `--input` | Cuerpo del request desde archivo |
| `-i` / `--verbose` | Ver status, headers o el intercambio completo al depurar |
| `--cache 1h` | Cachear respuestas en scripts que consultan lo mismo |

- `{owner}`, `{repo}`, `{branch}` se sustituyen desde el repo actual o `GH_REPO`.
- **Contar sin `--paginate` es un bug.** `--jq 'length'` sobre una página devuelve el tamaño
  de la página, no el total.

## 6. Releases, repo, secrets y variables

```bash
gh release create v1.4.0 --verify-tag --generate-notes --notes-start-tag v1.3.0
gh release create v2.0.0-rc.1 --prerelease --draft --generate-notes
gh repo edit --delete-branch-on-merge --enable-squash-merge \
  --enable-merge-commit=false --enable-rebase-merge=false --enable-auto-merge
gh repo edit --squash-merge-commit-message pr-title-description
gh secret set API_KEY < clave.txt             # por stdin: no queda en el historial del shell
gh secret set API_KEY --env production
gh secret set -f .env.ci                      # varios desde un dotenv
gh variable set API_URL --body "https://…" --env staging
```

- Para apagar un setting: `--<flag>=false`.
- **Nunca** `gh secret set X --body "valor-literal"` en una terminal con historial ni en un
  script versionado. Los secrets no se pueden leer de vuelta: `gh secret list` solo da nombres.
- Cambiar visibilidad exige `--accept-visibility-change-consequences` a propósito: desprende
  forks, deshabilita push rulesets y puede exponer historial y logs de Actions.

## 7. Scripting: Bash vs PowerShell (Windows)

| Tema | Bash (Git Bash) | PowerShell 5.1 |
|---|---|---|
| Placeholders `{owner}` | Tal cual | **Entre comillas**: `gh api "repos/{owner}/{repo}"` |
| Expresión `--jq` | Comillas simples | Comillas simples; si hay comillas dobles internas, probá el resultado antes de confiar |
| Encadenar | `a && b` | `a; if ($?) { b }` — no existe `&&` |
| Texto multilínea | Heredoc o `--body-file` | Here-string `@'…'@` o `--body-file` (preferido) |
| Variable de entorno | `GH_TOKEN=… gh …` | `$env:GH_TOKEN = '…'; gh …` |
| JSON → objeto | `--jq` | `gh … --json a,b \| ConvertFrom-Json` |
| Stdin a secret | `gh secret set X < f` | `Get-Content f \| gh secret set X` |

Sobre los mismos cinco repos hermanos:

```bash
for r in api web mobile modelo landing; do
  gh label clone mi-org/plantilla -R "mi-org/$r"
done
```

```powershell
foreach ($r in 'api','web','mobile','modelo','landing') {
  gh label clone mi-org/plantilla -R "mi-org/$r"
}
```

Reglas de script:
1. Chequeá el exit code de cada `gh`. `gh run watch --exit-status` y `gh pr checks --watch`
   existen para eso.
2. Idempotente: correrlo dos veces no duplica issues, labels ni releases.
3. `--json` + `--jq` para parsear. Nunca el texto "lindo" de la salida humana.
4. Sin paginación, sin conclusión.
5. Ensayo en seco cuando exista (`--dry-run`) y, si no, un `echo` del comando antes del real.

## 8. Uso seguro por agentes

| Acción | Agente solo | Requiere confirmación humana explícita |
|---|---|---|
| Leer: `view`, `list`, `status`, `checks`, `diff`, `run view`, `api` GET | Sí | — |
| Crear rama, PR en **draft**, comentario, issue con plantilla | Sí | — |
| `gh pr ready`, pedir review, poner labels | Sí, si la tarea lo incluye | — |
| `gh run rerun` | Una vez, tras clasificar el fallo | Reintentos repetidos |
| `gh pr merge` (cualquier estrategia, incluido `--auto`) | **No** | Sí |
| `gh pr close`, `gh issue close/delete/transfer` ajenos | No | Sí |
| `gh release create/delete`, crear o mover tags | No | Sí |
| `gh workflow run` de deploy | No | Sí |
| `gh secret set/delete`, `gh variable set` | No | Sí |
| `gh repo edit`, rulesets, colaboradores, deploy keys, webhooks | No | Sí |
| `gh repo delete/archive/rename`, cambio de visibilidad | **Nunca** | Humano, a mano |
| `--admin`, force-push a rama protegida | **Nunca** | — |
| `gh auth refresh` para ampliar scopes | **Nunca** | Humano |

- La aprobación vale para **esa** acción en **ese** contexto; no se arrastra a la siguiente.
- Antes de escribir: mostrar el comando exacto y el repo destino (`-R`). Un `gh` en el
  directorio equivocado opera sobre el repo equivocado.
- Si `gh` responde 401/403, el agente reporta BLOCKED con el mensaje literal; no busca otro token.
- Nada de tokens, secretos ni datos personales en cuerpos de PR, issues o comentarios.

## Anti-patrones

- Flags inventados por analogía con otro subcomando.
- Parsear la salida de tabla con `grep`/`awk` en vez de `--json`.
- Conclusiones sobre la primera página de `gh api`.
- `gh pr merge --admin` para "destrabar".
- Secretos por `--body` en la línea de comandos.
- Scripts que asumen Bash corriendo en PowerShell (`&&`, heredocs, `$VAR`).

## Checklist

- [ ] `gh auth status` revisado: cuenta, host y scopes correctos y mínimos.
- [ ] Flags confirmados con `--help` de la versión instalada.
- [ ] `-R` o directorio verificado antes de cualquier escritura.
- [ ] `--paginate` en todo conteo o listado completo.
- [ ] `--json` + `--jq` para parsear; exit codes chequeados.
- [ ] Sintaxis correcta para el shell en uso (placeholders entre comillas en PowerShell).
- [ ] Secrets por stdin o archivo, nunca literales.
- [ ] Acciones de la columna derecha de §8: confirmación humana obtenida y citada.
