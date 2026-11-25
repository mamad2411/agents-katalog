---
name: deploy-safety-scan
description: "Deploys that race, half-apply or drop work: migration topology, deploy locks, gates, shutdown, env drift."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: deploy-safety-scan

## Premise

A deploy is safe when the events every release causes cost nothing: N replicas booting at once, a second push while the first deploy runs, a dispatch from a feature branch, a crash-looping image, a SIGTERM to every old pod, the prod environment reading its config. None of that is visible in one file. It is a join:
- the migration runner × where it runs (boot, entrypoint, initContainer, Job, hook, CI step) × the rendered replica floor × the runner's lock;
- the deploy unit × its concurrency group × its environment × the wait after the verb;
- the app's signal handler × the image's PID 1 × the drain number × the grace period;
- the config the code reads × the config each environment declares.

No tool in the ledger joins these. actionlint and zizmor see no deploy semantics; hadolint flags a shell-form CMD and nothing about the handler behind it. The runner fact decides the most: on 2026-10-10, three replicas booting MikroORM 6.6.16's `getMigrator().up()` against one Postgres applied a data migration **three times**, and on a DDL migration crashed two of the three (§ Migration runners).

This skill owns `ownership.json` rows `deploy-safety` (§1–§5) and `env-parity` (§6). `@deployment-engineer` (this pack) judges its rows.

**Every finding cites the line `<file:line>` + the deploy unit or service root it belongs to + the environment it reaches (from the render or the unit) + the platform or runner fact it rests on (with its date) + the oracle and its tier + the fix in the project's own syntax.** A grep hit or a `UNIT` row is a candidate, and a `ci-graph.py` row is a structural fact; neither is a finding. "Deploys look safe" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (deploy § 22–28). Platform facts come from [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) (C1–C3); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V227–V231 and V234.

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them to deploys):

1. **The unit ships somewhere real** (gates 1, 7). A CI job, script or platform release that deploys an environment that is not a per-PR preview (precedents § 24), or a service root a rendered workload runs. A dev overlay, a local stack or a test database migration (a CI e2e job) is Hardening or Refuted.
2. **The event happens** (gate 2). The replica floor read from the **render** is ≥ 2, or an HPA/KEDA floor is; two triggers can start the unit (two pushes, a push and a dispatch, two operators); the orchestrator sends SIGTERM to a served or consuming process.
3. **No control already handles it** (gate 4). A runner lock (the lock column below), a leader gate, a platform release phase, an environment-keyed group elsewhere, a `resource_group`, a `flock`, an Argo health gate, a manual handler that awaits the framework close, `tini` with a handler behind it.
4. **The oracle fired, or both ends are cited** (gate 6). The tier and V are in § Proof. Without a run, cite both ends — the migrate call and the replica floor; the verb and the missing wait; the hook and the missing handler — and the row is `[report-flagged]`.

## Boundaries

- **Migration statement safety** (a contract migration, a lock-taking DDL, an irreversible drop) → database `migration-safety` §4 (N-1) and §8, rehearsal → `migration-rehearsal`, when the database pack is installed. §1 here owns who runs the migration, how many times, under which lock and in which order; it reads the database verdict for DP-1d. Without the pack, the row prints `contract? (owner pack database not installed)`.
- **Probe handler semantics** (liveness that checks a shared dependency) → performance `request-path-scan` §15; **readiness that always answers 200** → observability `metric-hygiene-scan` §7 (HC-01); probe presence and timings → infrastructure `k8s-availability-scan` §2. Each when its pack is installed; without it, `N/A (owner pack <x> not installed)`. No devops detector re-derives DP-5.
- **Shutdown timing** (`preStop`, `terminationGracePeriodSeconds`, sidecar order and the `preStop + drain + 5 ≤ grace` arithmetic, `THR-SHUTDOWN-GRACE`) → infrastructure `k8s-availability-scan` §7. §5 here supplies the **drain number and the handler**; **PID 1** (shell-form CMD, npm as PID 1, an entrypoint with no `exec`) → `container-build-scan` §2 (this pack). Without the infrastructure pack, §5 applies `THR-SHUTDOWN-GRACE` itself and tags the row `arithmetic (owner pack infrastructure not installed)`. Telemetry flush on shutdown → observability.
- **Canary analysis** (DP-7: an AnalysisTemplate that cannot fail, selectors grounded with observability `rule-inventory.py --check=selectors`) and **flag safety** (DP-8, flag drift across environments) → `progressive-delivery` (this pack). **Rollback target retention** (DP-9) → `release-integrity-scan`; `revisionHistoryLimit` → infrastructure; deploy by a mutable tag → security `iac-scan` §3 (4j).
- **A deploy not gated on tests** (`DEPLOY-UNGATED`, `DEPLOY-ALWAYS`, `WORKFLOW_RUN-NO-CONCLUSION`), **an unvalidated ref**, **an unbounded wait** → `pipeline-integrity-scan` §4, §5, §6. They print in pre-flight 0c as context, routed, never posted here.
- **A GitOps controller's own gate** (Argo/Flux health, sync waves, self-heal) → `gitops-audit` and infrastructure. `replicas` beside an autoscaler → infrastructure `k8s-render-scan`.

## Adapt to the codebase — the lanes

Discover every deploy unit (pre-flight 0a–0d); never assume `.github/`, `k8s/` or `./Dockerfile`. A **deploy unit** is a GitHub job, a GitLab job or `extends:` base, a Jenkins stage, a CircleCI/Bitbucket/Azure file (read as one unit), or a deploy script, Makefile or Justfile. Print the lanes you ran in the header.

| Lane | Deploy unit | Mutex (§2) | Protection (§3) | Rollout wait (§4) |
|---|---|---|---|---|
| **GitHub Actions** | job (`ci-graph.py`: `deploys=yes`) | `concurrency:` keyed on the environment, `cancel-in-progress: false` (C1) | `environment:` + reviewers + branch policy (C3, settings read) | `rollout status --timeout`, `helm --wait`, `services-stable`, `argocd app wait` |
| **GitLab CI** | job, `extends:` base | `resource_group:` (C2); `interruptible: true` on a deploy is a defect | protected environment + `deployment_tier` (`glab api …/protected_environments` [K]) | same verbs in `script:` |
| **Jenkins** | `stage('…')` | `options { disableConcurrentBuilds() }`, `lock(resource:)` [K] | `input` with `submitter` [K] | same verbs in `sh` |
| **CircleCI · Bitbucket · Azure** | the file (read) | CircleCI: no native mutex [K?]; Azure: environment "Exclusive lock" check [K] | Bitbucket `deployment:`; Azure environment approvals [K] | same verbs |
| **Scripts, Makefiles** | the file | `flock`, a lease, a lock object — or one operator only (rule 2) | n/a: who can run it is the control | same verbs |
| **Platform release phase** | Heroku `release:`, Fly `release_command`, Render `preDeployCommand` | runs once before the swap [K] | the platform's | the platform's |
| **GitOps** | a CI job that only commits manifests | the controller | the controller | Argo/Flux health → `gitops-audit` (precedents § 23) |

### Migration runners (§1) — the lock column decides gate 4

Read the runner's version from the lockfile; a lock fact is valid only for the version it names.

| Runner | Boot or CLI signal | Cross-process lock (versions, dates and sources: `broker-semantics.md` MG1–MG14 and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 77) |
|---|---|---|
| **MikroORM** | `getMigrator().up(`, `mikro-orm migration:up` | **none** — [V] 6.6.16 (umzug 3.8.2), source read and measured 2026-10-10; still none in migrations 7.2.5 (MG9, source 2026-10-14). No advisory lock, no lock table; umzug's opt-in `FileLocker` is not attached (and is per-filesystem anyway); `mikro_orm_migrations` has no unique key on `name`. Three concurrent `up()` on postgres:16 with the defaults (`transactional`, `allOrNothing`): **DML-only migration → applied 3 times, 3 rows**; DDL migration → 1 applied, 2 boots exit 1 (`relation … already exists`, or a duplicate key on the catalog), the restart is a no-op; first-ever run → 2 of 3 fail creating the table itself. Re-read on another major |
| Prisma | `prisma migrate deploy` | **waits 10 s** [V] (MG1): `pg_advisory_lock`; after the timeout the loser fails (P1002) and crash-loops on a long migration; `PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK` removes it |
| TypeORM · Drizzle · Sequelize/umzug | `migrationsRun: true`, `.runMigrations()` · `migrate(db, …)`, `drizzle-kit migrate` · `db:migrate` | **none** [V] (MG10–MG12): TypeORM runs in a transaction with no lock; Drizzle reads the last applied row outside the transaction (a migration merged with an older timestamp is silently skipped); umzug's `FileLocker` is per host |
| Django · Alembic · Doctrine | `manage.py migrate` · `alembic upgrade` · `doctrine:migrations:migrate` | **none** [V] (MG13, MG14; Django #30490 wontfix; Doctrine: `precedents/performance.md` § 77). Alembic is cleared only by a `pg_advisory_lock` the project added in `env.py` (read it) |
| Knex · golang-migrate · EF Core ≥ 9 | `migrate:latest` · `migrate up` · `Database.Migrate()`, `dotnet ef database update`, a bundle | **waits** [V] (MG5–MG7): `knex_migrations_lock` row · `pg_advisory_lock` + dirty flag · the EF Core 9 lock. An EF Core SQL script takes no lock, its SQLite lock table can be abandoned, and EF Core < 9 has none |
| Flyway · Liquibase (Spring auto-run) | `spring.flyway/liquibase` on the classpath | **waits** [V] (MG3, MG4): PG advisory lock · `DATABASECHANGELOGLOCK` row, up to 5 min (a killed pod leaves it locked) |
| Rails | `db:migrate` / `db:prepare` | **fails fast** [V] (MG2): advisory lock; the others raise `ConcurrentMigrationError` and crash-loop instead of waiting; breaks under a transaction-mode pooler |
| Laravel | `artisan migrate --force` | **skips** with `--isolated` (cache mutex, `precedents/performance.md` § 77): a held or stale mutex (1 h default expiry) skips the migrations **and exits 0**, so the replica serves on an unmigrated schema; `--isolated=1` makes the skip exit non-zero. Without `--isolated`: none |
| goose | `goose up`, `goose.NewProvider` | **opt-in** [V] (MG8): `NewPostgresSessionLocker` passed to the Provider; default none |
| Ecto | `mix ecto.migrate`, a release `migrate/0` | `migration_lock` [K] |

Only a **waits** row clears gate 4, and only behind a session-mode pooler or none (`precedents/performance.md` § 77 *Flips back*). **Fails fast** turns the race into a crash-loop and **skips** into a silently unmigrated replica: both stay findings at floor ≥ 2. **None**, and **opt-in** without the locker passed, stay candidates unless the run is a Job, an init container or a release step.

A `[K]` / `[K?]` lock (Ecto; EF Core's Npgsql and Pomelo specifics) is settled by V227 on the fixture before a finding relies on it; until then the row is `[report-flagged]`.

### Shutdown (§5) — the handler per stack

| Stack | The app has a handler when | Drain primitive |
|---|---|---|
| NestJS | `app.enableShutdownHooks()`, **or** a `process.on(<signal>, …)` that awaits `app.close()` (the hooks run either way; a loop over `['SIGTERM','SIGINT']` is the usual form). Neither → `onModuleDestroy` / `beforeApplicationShutdown` / `onApplicationShutdown` never run on SIGTERM | Fastify `app.close()`, `forceCloseConnections` [K?] |
| Node (Express, Fastify, Koa) | `process.on('SIGTERM', …)`, terminus / lightship / http-terminator / close-with-grace. With none, Node's default SIGTERM action exits at once [K] | `server.close()`, `closeIdleConnections()` |
| Python | gunicorn / uvicorn / hypercorn own SIGTERM (server-managed) | `graceful_timeout` / `--graceful-timeout`, `--timeout-graceful-shutdown` |
| Go | `signal.NotifyContext` / `signal.Notify(…, SIGTERM)` | `srv.Shutdown(ctx)` with a bounded ctx |
| JVM · .NET | Spring `server.shutdown=graceful` [K?] · `IHostApplicationLifetime` | `timeout-per-shutdown-phase` · `HostOptions.ShutdownTimeout` [K?] |
| Workers (BullMQ, Celery, Sidekiq) | a SIGTERM path to `worker.close()`; Celery warm shutdown; Sidekiq `-t` | in-flight job finishes or returns to the queue (precedents § 25) |

## Tool lane and ledger

| Lane | Command | Trap that makes a clean result false |
|---|---|---|
| Graph | `python3 "$G" . --check=deploy-gate,deploy-concurrency --deploy-ancestors` (`ci-graph.py`, repo baseline; fallback `$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py`) | Exit 2 = NOT-RUN (no YAML loader, a parse error), never clean (precedents § 41); GitHub only; `deploys=` counts `environment:` or a deploy verb (`kubectl` with its global flags before the verb included; a job whose only verbs publish is `publishes=yes`, and gets no `DEPLOY-NOGROUP`) — a deploy through a third-party action with neither is read by hand |
| Render | `render.sh` from infrastructure `k8s-render-scan` when installed; else `kubectl --kubeconfig=<scratch> kustomize <dir>` and `helm template --kubeconfig <scratch>` into `$SCAN` | A failed render makes its replica rows `blocked (render failed: <dir>)`; a remote base is not fetched. The scratch kubeconfig never names a real cluster |
| Settings | `gh api repos/{o}/{r}/environments --jq '.environments[]\|{name,rules:[.protection_rules[]?.type],policy:.deployment_branch_policy,can_admins_bypass}'`; GitLab `glab api projects/:id/protected_environments` [K]. Offline: the same response saved as `environments.json` in a snapshot dir → `ci-graph.py --settings-dir=<dir>` prints one `ENVIRONMENT env= branch-policy= reviewers= admin-bypass=` row per environment (0c passes `$SETTINGS_DIR`) | 403/404 = `UNREADABLE(gh api …: 403)`, never "absent" (precedents § 6) |
| Helm | `helm version --short` and the CI's Helm pin | Helm 4 renamed `--atomic` to `--rollback-on-failure` (precedents § 42): read the major before a flag is a finding |
| Runtime | `docker` for V227 / V231 / V234 | No daemon → `blocked (no docker)` with the command written out |

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2, bash 5 and zsh give the same rows). Grep **N** feeds **§N**; 0 is the inventory, the render, the graph and the deploy-unit table. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits; in every rg call the include globs come first and the exclusion array last, because ripgrep lets the later `-g` win; `--hidden` is required for `.github`, `.gitlab-ci.yml` and `.env.example`. Nothing is written inside the repo: renders, sets and the graph go to `$SCAN`.

```bash
X=(--hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/{dist,build,out,target,vendor,.venv,venv,__pycache__,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test,e2e-spec}.*'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock,svg,map}' -g '!**/migrations/**' -g '!**/{locales,i18n}/**')
CI=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '.circleci/*.{yml,yaml}' -g '**/bitbucket-pipelines.yml'
    -g '**/azure-pipelines*.yml' -g '**/Jenkinsfile*' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**')
SH=(-g '*.{sh,bash}' -g '**/Makefile' -g '**/Justfile' -g '!**/{node_modules,vendor,test,tests,fixtures,__fixtures__,testdata,docs,.claude,.git}/**')   # an include glob overrides hidden: exclude agent tooling
CODE=(-g '*.{ts,js,mjs,cjs,py,go,rb,java,kt,cs,php,ex,exs,rs}' -g '!*.d.ts')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(#|//|\*|/\*)')   # drops comment-only hit lines
MIG='\bgetMigrator\(\)\s*\.\s*up\(|\bmikro-orm(-esm)?\s+migration:up\b|\bprisma\s+migrate\s+deploy\b|migrationsRun\s*:\s*true|\.runMigrations\(|\bmanage\.py\s+migrate\b|\brails\s+db:(migrate|prepare)\b|\balembic\s+upgrade\b|\bknex\s+migrate:latest\b|\bsequelize(-cli)?\s+db:migrate\b|\bdrizzle-kit\s+migrate\b|\bDatabase\.Migrate\(\)|\bphp\s+artisan\s+migrate\b|\bgoose\s+(-\S+\s+)*up\b|\bflyway\s+(-\S+\s+)*migrate\b|\bliquibase\s+(--\S+\s+)*update\b|\bspring\.(flyway|liquibase)\.enabled\s*[=:]\s*true'
SIG="process\.(on|once)\(\s*(['\"](SIGTERM|SIGINT)['\"]|[A-Za-z_\$][\w\$]*\s*,)|\benableShutdownHooks\s*\(|signal\.Notify(Context)?\(|\.Shutdown\(\s*\w*[cC]tx|server\.shutdown\s*[=:]\s*graceful|IHostApplicationLifetime|ApplicationStopping|\bSignal\.trap\(|@godaddy/terminus|\bcreateTerminus\(|\blightship\b|http-terminator|close-with-grace|\bcloseWithGrace\("
G=.claude/scripts/ci-graph.py; [ -f "$G" ] || G="$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py"
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/deploy-safety.XXXXXX")}"; echo "SCAN=$SCAN"
RENDERS() { find "$SCAN" -maxdepth 1 -name 'render-*.yaml' | sort; }   # no bare glob: zsh aborts on a glob with no match
echo '# 0a inventory: CI files, deploy scripts, platform release files; service roots (a server or worker dependency)'
rg --files "${CI[@]}" . | sort; rg --files "${SH[@]}" . | sort; rg --files . -g '{Procfile,fly.toml,render.yaml,app.json,railway.*,app.yaml}' -g '!**/node_modules/**'
{ rg -l --pcre2 -g '**/package.json' "${X[@]}" '"(express|fastify|@nestjs/core|koa|@hapi/hapi|hono|bullmq|bull|bee-queue|@nestjs/microservices)"\s*:' .
  rg -l --pcre2 -g '**/{requirements*.txt,pyproject.toml,Pipfile}' "${X[@]}" '(?i)^\s*["\x27]?(gunicorn|uvicorn|hypercorn|django|flask|fastapi|celery)\b' .
  rg -l -g '**/*.go' "${X[@]}" -e '^package main$' . | while IFS= read -r f; do d=${f%/*}; while [ "$d" != "." ] && [ ! -f "$d/go.mod" ]; do d=${d%/*}; done; echo "$d/go.mod"; done
  rg -l -g '**/Gemfile' "${X[@]}" -e '\b(rails|puma|sidekiq)\b' .
  rg -l -g '**/{pom.xml,build.gradle,build.gradle.kts}' "${X[@]}" -e 'spring-boot' .; rg -l -g '**/*.csproj' "${X[@]}" -e 'Microsoft\.NET\.Sdk\.Web' .
} | sed 's|/[^/]*$||' | sort -u > "$SCAN/roots.txt"
[ "$(wc -l < "$SCAN/roots.txt")" -gt 1 ] && sed -i.bak '/^\.$/d' "$SCAN/roots.txt"; ROOTS=(); while IFS= read -r r; do ROOTS+=("$r"); done < "$SCAN/roots.txt"; echo "roots: ${ROOTS[*]:-none}"
echo '# 0b render (offline, isolated kubeconfig); reuse the infrastructure render when it is there'
if [ -z "$(RENDERS)" ]; then RS=.claude/skills/k8s-render-scan/scripts/render.sh
  if [ -f "$RS" ]; then bash "$RS" . --out="$SCAN" --quiet; echo "render.sh exit=$?"; else
    rg --files . -g '**/kustomization.{yml,yaml}' "${X[@]}" | sed 's|/[^/]*$||' | while IFS= read -r d; do
      kubectl --kubeconfig="$SCAN/none.kubeconfig" kustomize "$d" > "$SCAN/render-$(echo "$d" | tr '/.' '__').yaml" 2>>"$SCAN/render.err" || echo "render FAILED: $d"; done
    rg --files . -g '**/Chart.yaml' "${X[@]}" | sed 's|/[^/]*$||' | while IFS= read -r d; do
      helm template x "$d" --kubeconfig "$SCAN/none.kubeconfig" > "$SCAN/render-$(echo "$d" | tr '/.' '__').yaml" 2>>"$SCAN/render.err" || echo "render FAILED: $d"; done; fi; fi
ls "$SCAN" | rg '^render-.*\.yaml$'
echo '# 0c graph (GitHub): deploy jobs, concurrency, gating; exit 2 = NOT-RUN, never clean'
if [ -n "$(rg --files --hidden -g '.github/workflows/*.{yml,yaml}' .)" ]; then python3 "$G" . --check=deploy-gate,deploy-concurrency --deploy-ancestors ${SETTINGS_DIR:+--settings-dir="$SETTINGS_DIR"} > "$SCAN/graph.txt"; echo "ci-graph exit=$?"
  rg 'deploys=yes|publishes=yes|DEPLOY-|GROUP-NOT-ENV|ENV-SPLIT|WORKFLOW_RUN|ENVIRONMENT|NOT-RUN|UNREADABLE' "$SCAN/graph.txt"; else echo 'ci-graph: N/A (no GitHub workflow)'; fi
echo '# 0d deploy units on every platform and in scripts: verbs, environment, mutex, unwaited verbs, smoke, version check, migrate order'
rg --files "${CI[@]}" "${SH[@]}" . | sort | while IFS= read -r f; do awk -f - "$f" <<'AWK'
function flush() { if (u != "" && (nv || env == "yes")) printf "%s:%d: UNIT %s unit=%s verbs=%d unwaited=%d env=%s mutex=%s interruptible=%s smoke=%s version=%s migrate=%s first=%s\n", FILENAME, (ml ? ml : ul), p, u, nv, pend, (p == "script" ? "n/a" : env), mtx, intr, smk, ver, mig, mut
  u=""; mut="-"; ml=0; nv=0; pend=0; env="no"; mtx=wmx; intr="no"; smk="no"; ver="no"; mig="no" }
function start(n) { flush(); u=n; ul=FNR }
BEGIN { V = "kubectl([ \t]+[^ \t|;&]+)*[ \t]+(apply|set[ \t]+image|replace|rollout[ \t]+(restart|undo)|create)([^A-Za-z0-9_-]|$)|kustomize[ \t]+edit[ \t]+set[ \t]+image|helm[ \t]+(upgrade|install|rollback)|terraform[ \t]+apply|tofu[ \t]+apply|pulumi[ \t]+up|fly(ctl)?[ \t]+deploy|railway[ \t]+up|vercel.*--prod|netlify[ \t]+deploy.*--prod|aws[ \t]+(ecs[ \t]+update-service|lambda[ \t]+update-function-code)|gcloud[ \t]+run[ \t]+deploy|az[ \t]+webapp[ \t]+deploy|serverless[ \t]+deploy|cdk[ \t]+deploy|argocd[ \t]+app[ \t]+sync" }
FNR==1 { p = (FILENAME ~ /\.github\/workflows/) ? "gh" : (FILENAME ~ /gitlab/) ? "gl" : (FILENAME ~ /Jenkinsfile/) ? "jenkins" : (FILENAME ~ /\.(sh|bash)$|Makefile|Justfile/) ? "script" : "ci"
  wmx="no"; injobs=0; if (p != "gh" && p != "gl" && p != "jenkins") start("(file)") }
/^[ \t]*(#|\/\/)/ || /^[ \t]*(\|\|[ \t]*)?(die|echo|say|warn|printf|log|info|fail)[ \t(]/ { next }
p=="gh" && /^jobs:/ { injobs=1; next }
p=="gh" && /^concurrency:/ { wmx="workflow-group" }
p=="gh" && injobs && /^  [A-Za-z0-9_-]+:[ \t]*$/ { n=$1; sub(/:$/, "", n); start(n); next }
p=="gl" && /^[A-Za-z0-9_.-]+:[ \t]*$/ { n=$1; sub(/:$/, "", n); if (n !~ /^(stages|variables|default|workflow|include|image|services|cache|before_script|after_script)$/) start(n); next }
p=="jenkins" && /disableConcurrentBuilds|lock[ \t]*\(/ { wmx="jenkins-lock"; mtx=wmx }
p=="jenkins" && /stage[ \t]*\([ \t]*['"]/ { n=$0; sub(/.*stage[ \t]*\([ \t]*['"]/, "", n); sub(/['"].*/, "", n); start(n) }
u=="" { next }
/^[ \t]+(environment|deployment_tier|deployment)[ \t]*:/ || (p=="jenkins" && /input[ \t]*\(/) { env="yes" }
/^[ \t]+(concurrency|resource_group)[ \t]*:/ { mtx = ($1 ~ /resource_group/) ? "resource_group" : "job-group" }
p=="script" && /flock|mkdir[^#]*\.lock|--lock|(^|[^a-z])lease([^a-z]|$)/ { mtx="script-lock" }
/interruptible[ \t]*:[ \t]*true/ { intr="yes" }
{ w = match($0, /rollout[ \t]+status|--wait|--rollback-on-failure|--atomic|services-stable|argocd[ \t]+app[ \t]+wait|rollouts[ \t]+status|kubectl([ \t]+[^ \t|;&]+)*[ \t]+wait([^A-Za-z0-9_-]|$)/); wp = RSTART }
$0 ~ V {
  nv++; vp = match($0, V); if (!w) { if ($0 !~ /kustomize[ \t]+edit/) pend++ } else if (wp < vp && pend > 0) pend--; if (mut == "-") { mut=$0; sub(/^[ \t-]*(run:|sh)?[ \t'"]*/, "", mut); mut=substr(mut, 1, 40); gsub(/[ \t]/, "_", mut); ml=FNR }; next }
w && pend > 0 { pend-- }
/curl|wget|smoke|k6[ \t]+run|hey[ \t]/ { smk="yes"; if ($0 ~ /version|[Ss][Hh][Aa]|COMMIT/) ver="yes" }
/jsonpath=[^ ]*image/ && ver == "no" { ver="spec" }
/getMigrator|migration:up|migrate[ \t]+deploy|manage\.py[ \t]+migrate|db:migrate|db:prepare|alembic[ \t]+upgrade|migrate:latest|drizzle-kit[ \t]+migrate|artisan[ \t]+migrate|goose[ \t].*up|flyway.*migrate|liquibase.*update/ { mig = (nv == 0) ? "before" : "AFTER-DEPLOY" }
END { flush() }
AWK
done
echo '# 1a migrate signals x where they run'
rg -n --pcre2 "${X[@]}" "$MIG" . | "${NC[@]}" | sort | awk -F: '{w="boot-code"; f=$1
  if (f ~ /(Dockerfile|Containerfile|entrypoint)/) w="image/entrypoint"; else if (f ~ /\.(sh|bash)$|Makefile|Justfile/) w="script"; else if (f ~ /(\.github\/|gitlab-ci|\.gitlab\/|\.circleci|Jenkinsfile|azure-pipelines|bitbucket-pipelines)/) w="ci-step"
  else if (f ~ /\.(ya?ml|tpl)$/) w="manifest"; else if (f ~ /(Procfile|fly\.toml|render\.yaml|app\.json|railway)/) w="platform-release"; else if (f ~ /package\.json$/) w="npm-script"; print w "\t" $0 }'
echo '# 1b placement: initContainers, hooks, Jobs; hooks with no delete policy'
rg -n --pcre2 -g '*.{yml,yaml,tpl}' "${X[@]}" '^\s*initContainers\s*:|helm\.sh/hook["\x27]?\s*:|argocd\.argoproj\.io/hook["\x27]?\s*:|^\s*kind\s*:\s*Job\b' . | "${NC[@]}"
rg -l --pcre2 -g '*.{yml,yaml,tpl}' "${X[@]}" 'helm\.sh/hook["\x27]?\s*:' . | while IFS= read -r f; do rg -q --pcre2 'helm\.sh/hook-delete-policy["\x27]?\s*:' "$f" || echo "$f: HOOK-NO-DELETE-POLICY"; done
echo '# 1c replica floor per rendered workload (replicas, HPA minReplicas, KEDA minReplicaCount) and on platform files'
FLOOR='/^---/ { k=""; n="" } /^kind:/ { k=$2 } /^  name:/ && n == "" { n=$2 } /^metadata:.*name:/ && n == "" { n=$0; sub(/.*name:[ \t]*/, "", n); sub(/[ ,}].*/, "", n) } /^  (replicas|minReplicas|minReplicaCount):/ { print F ": " k "/" n " " $1 " " $2 }'
if [ -n "$(RENDERS)" ]; then RENDERS | while IFS= read -r f; do awk -v F="${f##*/}" "$FLOOR" "$f"; done
else rg -l --pcre2 -g '*.{yml,yaml}' "${X[@]}" '^kind:\s*(Deployment|StatefulSet|HorizontalPodAutoscaler|ScaledObject)\b' . | while IFS= read -r f; do awk -v F="raw:$f" "$FLOOR" "$f"; done; fi
rg -n --pcre2 "${X[@]}" '\b(min_machines_running|desired_count|min_instances|instance_count|numInstances|minScale)\b\s*[=:]\s*["\x27]?\d+' . | "${NC[@]}"
echo '# 1d controls: release phases (Heroku, Fly, Render), leader gates, lock switches (Prisma, Rails advisory_locks, Laravel --isolated)'
rg -n --pcre2 -g 'Procfile*' -g 'fly.toml' -g 'render.yaml' -g 'app.json' -g 'railway.*' "${X[@]}" '^\s*release\s*:|\brelease_command\b|\bpreDeployCommand\b|\bpredeploy\b' .
rg -n --pcre2 "${X[@]}" '\b(RUN_MIGRATIONS|MIGRATE_ON_BOOT|PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK)\b|advisory_locks\s*:\s*false|\bmigrate\b[^\n]*--isolated\b|\bpg_(try_)?advisory_(xact_)?lock\b' . | "${NC[@]}"
echo '# 1e auto-rollback in a deploy unit; contract statements in migration dirs (database migration-safety decides)'
rg -n --pcre2 "${CI[@]}" "${SH[@]}" '(?:--atomic|--rollback-on-failure)\b|\brollout\s+undo\b|\bautoRollback\b|deployment_circuit_breaker' . | "${NC[@]}" | tee "$SCAN/autorollback.txt"
[ -s "$SCAN/autorollback.txt" ] && rg -l -i --pcre2 -g '**/migrations/**' -g '!**/node_modules/**' '\bdrop\s+(column|table)\b|\brename\s+(column|to)\b|\balter\s+column\b[^\n]*\b(type|set\s+not\s+null)\b' . | sort
echo '# 2 non-GitHub mutex lines (the UNIT rows carry mutex= per unit)'
rg -n --pcre2 "${CI[@]}" '^\s*interruptible\s*:\s*true\b|^\s*resource_group\s*:|\bdisableConcurrentBuilds\s*\(|\block\s*\(' . | "${NC[@]}"
echo '# 5a per service root: a shutdown signal in code, or a server that owns it (python/ruby/jvm: read the timeout)'
while IFS= read -r r; do [ -z "$r" ] && continue
  if [ -n "$(rg -n --pcre2 "${CODE[@]}" "${X[@]}" "$SIG" "$r" | "${NC[@]}" | head -1)" ]; then echo "$r: handler present"
  elif [ -n "$(rg -l --pcre2 -g '**/{requirements*.txt,pyproject.toml,Pipfile,Gemfile,pom.xml,build.gradle*}' '(?i)\b(gunicorn|uvicorn|hypercorn|celery|puma|sidekiq|spring-boot)\b' "$r")" ]; then echo "$r: server-managed (read the graceful timeout, 5c)"
  else echo "$r: NO-SHUTDOWN-HANDLER"; fi; done < "$SCAN/roots.txt"
echo '# 5b NestJS: lifecycle hooks vs enableShutdownHooks / a manual SIGTERM handler (comment lines dropped)'
while IFS= read -r r; do rg -q '"@nestjs/core"' "$r/package.json" 2>/dev/null || continue
  H=$(rg -n --pcre2 "${CODE[@]}" "${X[@]}" '\b(onModuleDestroy|beforeApplicationShutdown|onApplicationShutdown)\s*\(' "$r" | "${NC[@]}" | wc -l | tr -d ' ')
  E=$(rg -n --pcre2 "${CODE[@]}" "${X[@]}" '\benableShutdownHooks\s*\(' "$r" | "${NC[@]}" | head -1)
  M=$(rg -n --pcre2 "${CODE[@]}" "${X[@]}" "process\.(on|once)\(\s*(['\"](SIGTERM|SIGINT)['\"]|[A-Za-z_\$][\w\$]*\s*,)" "$r" | "${NC[@]}" | head -1)
  if [ -n "$E" ]; then echo "$r: hooks=$H enableShutdownHooks: $E"; elif [ -n "$M" ]; then echo "$r: hooks=$H manual handler (read: awaits app.close()?): $M"
  else echo "$r: NEST-HOOKS-INERT hooks=$H"; fi; done < "$SCAN/roots.txt"
echo '# 5c drain numbers the app sets (infrastructure k8s-availability-scan §7 does the THR-SHUTDOWN-GRACE arithmetic)'
rg -n --pcre2 -g '*.{conf,toml,ini,yml,yaml,properties}' "${CODE[@]}" "${X[@]}" '(?i)\b(shutdown|drain|grace(ful)?)[_-]?(drain[_-]?)?(timeout|delay|period|seconds|ms)\w*\s*[:=]\s*[\d_.]+|--graceful-timeout[ =]\d+|--timeout-graceful-shutdown[ =]\d+|timeout-per-shutdown-phase|\bforceCloseConnections\b|ShutdownTimeout' . | "${NC[@]}"
echo '# 6a read set (code) vs declared set (.env.example, compose, rendered env); envFrom refs make the declared set partial'
: > "$SCAN/env-read.txt"; [ ${#ROOTS[@]} -gt 0 ] && rg -o --no-filename --pcre2 "${CODE[@]}" "${X[@]}" -r '$1$2$3$4$5$6$7$8' -e 'process\.env\.([A-Z][A-Z0-9_]+)' -e "process\.env\[['\"]([A-Z][A-Z0-9_]+)" -e 'import\.meta\.env\.([A-Z][A-Z0-9_]+)' -e "os\.(?:environ\[|environ\.get\(|getenv\()['\"]([A-Z][A-Z0-9_]+)" -e 'os\.Getenv\("([A-Z][A-Z0-9_]+)' -e "ENV(?:\.fetch\(|\[)['\"]([A-Z][A-Z0-9_]+)" -e 'System\.getenv\("([A-Z][A-Z0-9_]+)' -e 'env::var\("([A-Z][A-Z0-9_]+)' "${ROOTS[@]}" | sort -u > "$SCAN/env-read.txt"
{ rg -o --no-filename --hidden --pcre2 -r '$1' -g '**/.env.{example,sample,template,dist}' -g '!**/node_modules/**' '^\s*(?:export\s+)?([A-Z][A-Z0-9_]+)=' .
  rg -o --no-filename --pcre2 -r '$1$2' -g '*compose*.{yml,yaml}' -g '!**/node_modules/**' '^\s+([A-Z][A-Z0-9_]+)\s*:|^\s+-\s*([A-Z][A-Z0-9_]+)=' .
  RENDERS | while IFS= read -r f; do rg -o --no-filename --pcre2 -r '$1$2' '^\s*-\s*name\s*:\s*["\x27]?([A-Z][A-Z0-9_]+)|^\s*-\s*([A-Z][A-Z0-9_]+)=' "$f"; done; } | sort -u > "$SCAN/env-declared.txt"
echo "read=$(wc -l < "$SCAN/env-read.txt" | tr -d ' ') declared=$(wc -l < "$SCAN/env-declared.txt" | tr -d ' ')"
echo "read, not declared: $(comm -23 "$SCAN/env-read.txt" "$SCAN/env-declared.txt" | tr '\n' ' ')"; echo "declared, never read: $(comm -13 "$SCAN/env-read.txt" "$SCAN/env-declared.txt" | tr '\n' ' ')"
rg -n --pcre2 -g '*.{yml,yaml}' "${X[@]}" '\b(secretRef|configMapRef)\s*:|\benv_file\s*:' . | "${NC[@]}"
echo '# 6b runtime versions per environment: version files, engines, FROM per Dockerfile, CI setup-*'
rg -n --pcre2 --hidden -g '.nvmrc' -g '.node-version' -g '.python-version' -g '.tool-versions' -g '!**/node_modules/**' '\S' .
rg -n --pcre2 -g '**/package.json' "${X[@]}" '"node"\s*:\s*"[^"]+"' .
rg -n --pcre2 -g '**/Dockerfile*' -g '**/*.dockerfile' -g '**/Containerfile*' "${X[@]}" '^\s*FROM\s+(\S+/)?(node|python|golang|ruby|eclipse-temurin|openjdk|php|dotnet/aspnet):\S+' .
rg -n --pcre2 "${CI[@]}" '\b(node-version|python-version|go-version|ruby-version|java-version)\s*:\s*\S+' . | "${NC[@]}"
```

How to read it:
- **0d `UNIT` rows** are the §2–§4 candidate table, one per deploy unit on every platform: `verbs` (deploy verbs, `kubectl --kubeconfig … -n ns apply` included; `npm publish`/`docker push` are `release-integrity-scan`'s), `unwaited` (verbs with no wait after them in the unit — a wait earlier on the same line, `rollout status … || rollout undo`, covers the verb before it, `kubectl -n ns wait` is a wait, and a local `kustomize edit set image` is never pending), `env`, `mutex`, `interruptible`, `smoke`, `version` (`yes` = the smoke compares a SHA or version; `spec` = the script reads the Deployment's image back, which with a completed `rollout status` equals what serves), `migrate` (`before` / `AFTER-DEPLOY`). Lines that only print a message (`die`, `echo`, `printf`) are skipped. For GitHub, `ci-graph.py` (0c) decides concurrency; the `UNIT` mutex column is context.
- **1a** labels each migrate call by where it runs: `boot-code`, `image/entrypoint`, `manifest` (read: initContainer, Job or hook), `ci-step` (counts only inside a deploy `UNIT`), `script`, `npm-script` (follow who calls it), `platform-release` (a control, precedents § 22).
- **5a** is a repo-level negative per service root, so its rows are candidates for the whole root: read the root's entry point before posting. **5b** reports NestJS separately because hooks exist and silently never run.
- **6a** is partial when a `secretRef`/`configMapRef`/`env_file` brings keys the repo cannot see: every "read, not declared" key is then Unconfirmed until the secret's key list is read (`kubectl get secret -o jsonpath='{.data}' --kubeconfig=<scratch>` on a sandbox, or the platform's secret list). A typed schema validated at boot is the declaration (precedents § 26).

Blind spots, worked around rather than trusted:
- **A migrate call behind a wrapper** (`node -e` in a Job, a `start` script, `npm run db:migrate` in an entrypoint): 1a shows the leaf; follow `npm-script` rows to their callers.
- **A deploy through an action** (`azure/k8s-deploy`, `aws-actions/amazon-ecs-deploy-task-definition`) has no verb: `ci-graph.py` counts it only when the job has `environment:`. Read every job whose name says deploy.
- **The fixed-name migration Job.** Applied by plain `kubectl apply` with a new image, the next release fails on the immutable Job template unless the unit deletes it first (or `ttlSecondsAfterFinished` / a hook delete policy removes it). Applied in the same `apply -k` as the Deployments, it races the rollout it should precede.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample (6 GitHub workflows, GitLab, Jenkinsfile, 2 deploy scripts, 6 service roots, kustomize base + 2 overlays, a Helm chart; 23 positives, 18 decoys, 1 routed) | 1.2 s, 0 rg errors; bash 3.2, bash 5 and zsh print the same rows. **23/23 positives surface** in their §: boot migrate × rendered `replicas: 3` + HPA 3, entrypoint migrate, alembic initContainer × 2, hook with no delete policy, GitLab migrate `AFTER-DEPLOY`, `--atomic` beside a `DROP COLUMN`; `DEPLOY-CANCEL`, `DEPLOY-NOGROUP`, `GROUP-NOT-ENV`, `ENV-SPLIT-GROUPS`, GitLab `interruptible` with no `resource_group`, Jenkins with no lock; a deploy job with no `environment:`; 3 unwaited units and a smoke with no version; `NEST-HOOKS-INERT`, 2 `NO-SHUTDOWN-HANDLER` (Express, BullMQ), gunicorn `graceful_timeout = 90`; a request-time key in no declared set; `.nvmrc` 22 vs `FROM node:20-alpine`. 3 decoys never appear (a runbook in `docs/`, a test fixture, PR CI's cancel); the rest surface and clear on read, each by one row or precedent (release phase ×2 § 22, migrate `before`, delete-policy hook, manual `rollout undo`, preview cancel § 15/§ 24, `resource_group`, waited and version-checked units ×2, GitOps bump § 23, manual NestJS handler, Go `NotifyContext`, `PORT` § 26, a defaulted key, a declared-unused key) |
| `benchmarks/fixtures/*` (15) | 9 fixtures print rows; 0 rg errors. Unseeded but real: 6 service roots with no shutdown handler (node-api, quality-mix ×2, review-decoys, brittle-suite, vuln-fullstack) and 2 `NEST-HOOKS-INERT` (quality-mix with 0 hooks, vuln-fullstack with 1). One FP class fixed before shipping: a Go library module (no `package main`) counted as a service root; roots are now modules holding a main package. slow-marketplace: an npm `migration:up` script, a SQL migration Job, raw `replicas: 3/4` (no kustomization, so the raw fallback ran), a `pg_try_advisory_lock` poller (a leader gate, not a migration lock), gunicorn `graceful_timeout = 30`. vuln-fullstack: its PR preview (precedents § 24). Declared sets are empty in 6 fixtures (no `.env.example`), so §6 stays Unconfirmed there |
| Real NestJS + Fastify monorepo (read-only, `git status` clean before and after) | 2.0 s. Migrations run as a Job applied **alone** before the rollout (delete → apply by label → `wait --for=condition=complete` → `apply -k`): 1a's `manifest` rows are the correct topology, and the `ci-step` row is the e2e database (Refuted). The deploy script waits on all three rollouts and reads the image back (`version=spec`); its one finding candidate is `mutex=no` (§2, Hardening while one operator deploys). A second script's unwaited `kubectl apply -f` applies a NetworkPolicy and a datasource ConfigMap (Refuted on read: no rollout to wait on). A dev-database rebuild script's boot-code `up()` is Refuted (local only). §5: the first run printed `NO-SHUTDOWN-HANDLER` + `NEST-HOOKS-INERT` — **a false positive**: `main.ts` registers `process.on(signal, …)` in a loop over `['SIGTERM','SIGINT']` and awaits `app.close()`; the literal-only regex missed it. Fixed (the variable-signal form), now `manual handler` with 7 hooks; drain `SHUTDOWN_DRAIN_TIMEOUT_MS = 30_000` handed to infrastructure §7 (10 + 30 + 5 ≤ 45). A workspace-root manifest whose `pnpm.overrides` names `fastify` was a phantom root; dropped when sub-roots exist. §6: 6 keys read and not declared, all Unconfirmed (`envFrom: secretRef`) |

## The 3,000-hit path

1. **Intersect** with the deploy units: keep hits inside a `UNIT` row, a `--deploy-ancestors` job, a service root a rendered workload runs, or a prod render. Dismiss the rest with one read each (a test database, a local stack, a dev overlay) and name them in the coverage block.
2. **Group** by unit (precedents § 5): a reusable workflow, a GitLab `extends:` base, a Helm chart's hook, a kustomize base, one service root, one migration runner.
3. **Rank:** prod deploy units first; then §1 rows on a lockless runner with a floor ≥ 2; then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** `ci-graph.py --check=deploy-concurrency` settles every GitHub §2 row; one V227 cold start per runner and version settles every §1 row on it; one V231 stop per base image and stack settles §5 for the roots that share them.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity follows the environment the unit reaches: prod first, never the job's name.

| § | Classes | Default severity |
|---|---|---|
| 1 | DP-1 migration topology: (a) migrate-on-boot × floor ≥ 2 × lockless runner; (b) placement (initContainer, hook with no delete policy, fixed-name Job); (c) order vs the deploy verb; (d) auto-rollback over a contract migration | H (C when the engine's DDL is not transactional: MySQL, Oracle) |
| 2 | DP-2 deploy concurrency | H |
| 3 | DP-3 environment unprotected | H (C on prod) |
| 4 | DP-4 rollout not gated; smoke with no version assertion | H |
| 5 | DP-6 shutdown chain, code side: no handler, inert hooks, the drain number | H |
| 6 | EP-1 config read but not declared; EP-2 runtime drift across environments; EP-4 schema drift | M (H when read at request time with no default) |

### 1. Migration topology (DP-1)

```
BAD:   main.ts  await app.get(MikroORM).getMigrator().up()   × render replicas: 3 / HPA minReplicas: 3   (lockless runner: a backfill runs 3×)
       initContainers: [{ command: [alembic, upgrade, head] }]       (once per pod, per restart, per scale-up)
       "helm.sh/hook": pre-upgrade  with no hook-delete-policy        (the next upgrade fails: the Job already exists)
       deploy_prod: kubectl apply …  then  pnpm exec mikro-orm migration:up  (new pods meet the old schema)
       helm upgrade --atomic  in the release that ships a DROP COLUMN   (auto-rollback lands old code on the new schema)
GOOD:  one migration Job applied alone, waited on, then the rollout · a platform release phase · a runner lock + one leader
```
**Read the code:**
- Where does each 1a row run (boot, entrypoint, initContainer, Job, hook, CI step)? Who calls an `npm-script` row?
- What is the floor on the **render** for the workload that runs it (1c): `replicas`, HPA `minReplicas`, KEDA `minReplicaCount`, `min_machines_running`, `desired_count`? A dev overlay's 1 is not prod's 3.
- Which runner and version (lockfile), and what does the lock column say? A leader gate (`RUN_MIGRATIONS=1` set on one instance only)? A release phase (1d)?
- Is the DDL transactional on this engine (Postgres yes; MySQL and Oracle no: a concurrent or killed run half-applies)?
- For an `AFTER-DEPLOY` row, or an auto-rollback (1e) beside a migration in the same release: is that migration a contract (database `migration-safety` §4 / §8)?
- A migration Job: is it applied alone and waited on before the Deployments, and deleted (or TTL'd) before the next release re-applies it?

**Finding when** N processes can apply the same migration (floor ≥ 2 with a **none**, **fails fast**, **skips**, locker-less **opt-in** or `[K?]` runner, an initContainer on a multi-replica workload, a CI matrix that migrates), the old pods meet a contract schema (`AFTER-DEPLOY` with an expand step missing, an auto-rollback over a contract), or a hook or Job blocks the next release. Precedents § 22 clears one replica plus a lock, a leader gate, or a release phase. **Proof (V227):** `docker compose up --scale app=3` (or three concurrent boots) from an empty database: exactly one row per migration, 0 crash-loops; a kill mid-run is recovered by the next start. The 2026-10-10 MikroORM run above is this oracle.

### 2. Deploy concurrency (DP-2)

```
BAD:   concurrency: { group: deploy-${{ github.ref }}, cancel-in-progress: true }   at workflow scope over a deploy job
       deploy-prod  concurrency: { group: deploy-${{ github.sha }} }               (keyed on the SHA: every push runs at once)
       production deployed under "deploy-<sha>" in one workflow and "production" in another   (ENV-SPLIT-GROUPS)
       GitLab deploy_prod: interruptible: true, no resource_group · Jenkins deploy with no disableConcurrentBuilds()/lock()
GOOD:  concurrency: { group: deploy-production, cancel-in-progress: false } in every workflow that deploys prod · resource_group: production
```
**Read the code:** Which rows does 0c print (`DEPLOY-CANCEL`, `DEPLOY-NOGROUP`, `GROUP-NOT-ENV`, `ENV-SPLIT-GROUPS`) and which `UNIT` rows say `mutex=no` or `interruptible=yes`? Is it PR CI or a per-PR preview (precedents § 15, § 24)? Does an expression turn cancel off for deploys (`cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}` keeps `main` deploys running)? For a script: can two triggers run it (CI and an operator, two operators)? One operator on one machine is Hardening.

**Finding when** a newer push can cancel a running apply, migration or `helm upgrade` (a half-applied release, a Terraform lock, Helm `pending-upgrade`), or two deploys of one environment can run at once and the older SHA can finish last (C1, C2). **Proof (V228):** the graph rows are gone after the fix (T); two pushes 10 s apart in a sandbox repo — the first deploy completes, the final SHA is the latest, no lock is left (L); the PR workflow still cancels superseded runs (the control).

### 3. Environment unprotected (DP-3)

```
BAD:   ship:  runs `helm upgrade --install api … --namespace prod` with no environment:      (no reviewer, no branch policy, no env secrets)
       environment: production  with  protection_rules: []  or  deployment_branch_policy: null  or  can_admins_bypass: true
GOOD:  environment: production + required reviewers + a branch policy (main or release tags); OIDC sub pinned to environment:production
```
**Read the code:** Which `UNIT` rows deploy prod with `env=no`? Then the settings read (§ Tool lane) for every environment the units name. Is it a preview or an ephemeral environment (precedents § 24)? Does the cloud trust pin the OIDC `sub` to `environment:production` (security or infrastructure corroborates; it is a control here)?

**Finding when** prod is reachable with no reviewer or no branch policy. A settings read that returns 403/404 leaves the row `UNREADABLE` → Unconfirmed, never cleared (precedents § 6). **Proof (V229):** the settings read shows reviewers and a branch policy on prod (A), and a dispatch from a feature branch is refused (R, sandbox).

### 4. Rollout not gated (DP-4)

```
BAD:   kubectl set image deploy/api api=…:${{ github.sha }}   (no rollout status: a crash-looping image leaves the job green)
       helm upgrade --install api charts/api                  (no --wait)
       curl -fsS https://app.example/healthz                  (the old pods answer 200: no version assertion)
GOOD:  kubectl rollout status deploy/api --timeout=5m · helm upgrade --wait --timeout 10m · curl -fsS …/version | grep -q "$GITHUB_SHA"
```
**Read the code:** Which `UNIT` rows say `unwaited ≥ 1`, or `smoke=yes version=no`? Is the unwaited object a workload (a ConfigMap, NetworkPolicy or ServiceMonitor has no rollout to wait on)? Is it a GitOps repo where CI only commits manifests (precedents § 23 → `gitops-audit`)? Which Helm major runs (precedents § 42: `--atomic` vs `--rollback-on-failure`, the `--wait` change)?

**Finding when** a deploy verb on a workload has no wait in its unit, or the post-deploy check cannot tell the new version from the old. An unbounded wait is `pipeline-integrity-scan` §6. **Proof (V230):** deploy a crash-looping image to a throwaway kind cluster through an isolated `--kubeconfig=<scratch>`: the pipeline turns red inside the timeout. Never the default context.

### 5. Shutdown chain, code side (DP-6)

```
BAD:   NestJS: onModuleDestroy() { await this.queue.close() }  and main.ts has no enableShutdownHooks() and no SIGTERM handler
       Express: app.listen(port) and nothing else                   (Node exits at once on SIGTERM: in-flight requests die)
       new Worker('emails', …) with no SIGTERM path to worker.close()   (the active job is lost or redelivered)
GOOD:  app.enableShutdownHooks() — or process.on(sig, () => app.close()) — + a bounded drain + PID 1 that receives the signal
```
**Read the code:**
- Per 5a/5b root: which entry point starts it, and does the handler run before exit (awaited `app.close()`, `srv.Shutdown(ctx)`, `server.close()`)? A variable signal (`process.on(signal, …)`) is the same handler as a literal one.
- Does the image deliver SIGTERM to that process (`container-build-scan` §2: exec-form CMD, `tini`/`--init`, an entrypoint that `exec`s)? A handler behind `sh -c` never runs.
- What is the drain (5c), and what are `preStop` and the grace on the render? Infrastructure §7 does the arithmetic; hand it the number.
- A worker with no inbound traffic (precedents § 25): does the in-flight job finish or return to the queue? Serverless and a one-shot Job are N/A.

**Finding when** a served or consuming process has no handler, its framework hooks are inert, or its drain cannot fit the grace (the arithmetic row from infrastructure, or `THR-SHUTDOWN-GRACE` here when that pack is absent). **Proof (V231):** `time docker stop -t 10 <container>` on the real image exits in under 10 s with a code other than 137, and a request in flight during the stop completes (B); without docker, `blocked (no docker)` and the command written out.

### 6. Config and runtime parity (EP-1, EP-2, EP-4)

```
BAD:   const key = process.env.STRIPE_KEY   (per request, no default; absent from .env.example and the prod render)
       .nvmrc 22 · engines >=22 · FROM node:20-alpine        (the image runs a runtime CI never tested)
GOOD:  a typed config schema validated at boot (fail fast, the key named) · one runtime version across .nvmrc, engines, CI and every FROM
```
**Read the code:** Is the key platform-set (`PORT`, `HOSTNAME`, `KUBERNETES_*`, `NODE_ENV`; precedents § 26)? Optional with a safe default? Read at boot (a crash at start is loud) or per request (silent until the path runs)? Is the declared set partial (a `secretRef`, `env_file`, a platform secret store)? Flags and flag drift are `progressive-delivery`'s; schema drift between environments (EP-4) needs a read of each environment's applied migrations (`SELECT name FROM <migrations table>`), so it is Unconfirmed offline.

**Finding when** a key read at request time with no default is absent from prod's declared set (H), any other read key is undeclared everywhere (M), or the runtime differs between what CI tests and what an environment runs (M). Declared-but-never-read keys are info. **Proof (V234):** boot the artifact with only the declared prod keys (`env -i <keys> node dist/main.js`, or the container with `--env-file`): readiness passes, or the validator names the missing key; `docker run --rm <img> node -v` equals `.nvmrc` across environments.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: a sandbox repository the user names, scratch builds, `${TMPDIR}` and throwaway kind clusters through an isolated `--kubeconfig=<scratch>` only — never the user's branches, environments, default kube context or cloud profile.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1 | Scale cold start: N concurrent boots on an empty database; one row per migration; a kill mid-run recovers | R | V227 |
| 2 | Graph assertion (`--check=deploy-concurrency` exits 0 after the fix) + a two-push race in a sandbox | T + L | V228 |
| 3 | Settings read + a dispatch from a feature branch refused | A + R | V229 |
| 4 | A crash-looping image turns the pipeline red inside the timeout (kind, isolated kubeconfig) | R | V230 |
| 5 | Stop timing on the real image: under the stop timeout, exit ≠ 137, the in-flight request completes | B | V231 |
| 6 | Declared-keys boot; runtime version equal across environments | B | V234 |

A fix is checked with `ci-graph.py --diff-guard="$FIX_BASE" --allow-job=<file>:<job>` (the `=` forms: with a space, `--diff-guard` expects two files and exits 2): a fix that changes `concurrency:`, `environment:`, `needs:` or `if:` outside the finding's job is rejected.

## Output

```
deploy-safety-scan — lanes: github-actions (6 workflows; ci-graph.py ruby-psych), gitlab, jenkins, scripts (2); render: kustomize ×3, helm ×1
Runners: MikroORM 6.6.16 (lockless [V 2026-10-10]), Prisma, Alembic · infrastructure: not installed (§5 arithmetic here) · database: installed

Findings: 3 · Unconfirmed: 3

1. apps/api/src/main.ts:8                                                  [report-with-fix]   high
   §1 DP-1a — `getMigrator().up()` at boot × prod render `Deployment/api replicas: 3` + `HPA minReplicas: 3`;
   MikroORM 6.6.16 takes no lock. Proof: 3 concurrent boots (V227) → a DML migration applied 3×. Fix: drop
   the boot call; run one migration Job applied alone and waited on before `kubectl apply -k` (the GOOD shape).

2. .github/workflows/cd.yml:8                                              [report-with-fix]   high
   §2 DP-2 — DEPLOY-CANCEL scope=workflow covers deploy-staging (env staging): a newer push cancels a running
   apply (C1). Proof: graph row (T, V228). Fix: move concurrency to the job, `group: deploy-staging`,
   `cancel-in-progress: false`; keep the PR workflow's cancel (precedents § 15).

3. .github/workflows/emergency.yml:22                                        [report-flagged]    critical
   §3 DP-3 — `helm upgrade --install api … --namespace prod` in job ship with no `environment:` (UNIT env=no).
   Unproven link: environments UNREADABLE(gh api …: no token). Settling test: V229 settings read + a feature-branch dispatch.

Verification: 64 candidates → 3 findings · 3 unconfirmed · 2 hardening · 0 pre-existing · 41 refuted (self-verified) · 15 routed

Class coverage:
  §1  migration topology        checked (6 migrate sites · 4 placements · floor from 3 renders → 1 finding, 3 unconfirmed; 2 release phases refuted § 22)
  §2  deploy concurrency        checked (graph: 5 rows; 4 non-GitHub units → 1 finding; preview refuted § 15/§ 24)
  §3  environment protection    Unconfirmed (8 deploy units, 1 without environment:; settings UNREADABLE)
  §4  rollout gate              checked (11 units → 4 unwaited; GitOps bump refuted § 23)
  §5  shutdown, code side       checked (6 roots → 3 no handler, 1 inert hooks; 1 manual handler refuted; drain 90 s → arithmetic)
  §6  config / runtime parity   checked (5 read · 3 declared → 1 finding; PORT refuted § 26; runtime 22 vs 20 → 1 finding)
  routed                        DEPLOY-UNGATED ×1 → pipeline-integrity-scan §4 · contract statement → database migration-safety §4
```

`[report-with-fix]`: the unit, its environment, the runner or platform fact and the oracle are in hand, and the fix is local to the unit. `[report-flagged]`: one link is unproven — a settings read, a `[K?]` lock, a render that failed, a partial declared set, no docker. The row names the link and the settling test.

The coverage block lists **all six** §s on every run: `checked (k hits → m findings)` only when the grep or graph ran on a lane that is present; `N/A (no deploy unit)` / `N/A (no service root)` / `N/A (no migration runner)`; `blocked (<reason>)` when a grep, the graph or a render failed (a `ci-graph.py` exit 2 makes every GitHub §2 row `blocked (ci-graph NOT-RUN: <reason>)`); `Unconfirmed (… UNREADABLE …)`; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 22** Migrate-on-boot with one replica (read from the render) plus a lock, a leader gate or a release phase. **§ 23** A GitOps CI that only commits manifests. **§ 24** Preview environments. **§ 25** Workers need checkpointing, not `preStop`. **§ 26** Platform-set variables; a typed schema is the declaration.
- **§ 15** `cancel-in-progress` on PR CI. **§ 3** Probe and manifest-timing rows are routed. **§ 5** One finding per unit. **§ 6** A 403 is `UNREADABLE`. **§ 41** A tool that errored is NOT-RUN. **§ 42** The Helm 4 flag rename.

Read-step rules measured on the real repo (2026-10-10), applied with a `file:line`: a `process.on(<variable>, …)` over a signal list that awaits the framework close **is** the handler; a migration Job applied alone and waited on before the rollout **is** the correct topology; a `kubectl apply` of a non-workload object has no rollout to wait on; a migrate call in a CI test job is not a deploy.

Rationalizations to reject:
- "Migrations are transactional, so concurrency is fine": a data migration applies N times, and the losers crash-loop.
- "We have `needs: test`": that is §4 of `pipeline-integrity-scan`, not a rollout gate.
- "The image uses exec form, so shutdown works": no handler as PID 1 is 10 s, then 137.
- "The deploy has a concurrency group": keyed on the SHA, it serialises nothing.

## When to run

- On any diff touching a deploy unit (CI deploy job, deploy script, Makefile target), a manifest, overlay or chart, a migration runner config, a service bootstrap (`main.ts`, `server.go`, `gunicorn.conf.py`), `.env.example` or a runtime version file.
- After `/deploy-stage` changes its path, and after a `/devops-fix` on a deploy row.
- On every whole-repo `/devops-audit`, reporting all six §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the unit or root, the environment, the runner or platform fact with its date, and the fix.
- **No replica count from source alone** when a kustomization or chart exists: the render decides. No lock fact without the runner's version.
- **No `checked` on a lane whose tool failed:** `ci-graph.py` exit 2, a failed render, an rg exit 2 are `blocked`.
- **Never run V227–V231 against the user's database, cluster, registry or branches.** Every `kubectl`/`helm` takes an isolated `--kubeconfig=<scratch>`; no default context, no cloud profile. Otherwise the row is Unconfirmed with the command written out.
- **No proposed fix may weaken a control to clear a row:** no `cancel-in-progress: true` on a deploy, no removed `environment:`, no deleted wait, no `PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK`.
- **Do not print "deploys look safe" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill and folds its coverage block into the deploy rows; `/devops-fix` closes them with V227–V231 and `--diff-guard`. `/deploy-stage`'s Safe-Delivery S2–S5 cite these rows instead of their own greps; `/rollback-deploy` asks whether N-1 code runs on today's schema (§1d).
- `@deployment-engineer` judges these rows; `@devops-architect` designs deploy paths this skill then judges.
- `pipeline-integrity-scan`, `container-build-scan`, `progressive-delivery`, `release-integrity-scan` and `gitops-audit` (this pack) own the neighbouring classes (§ Boundaries).
- `k8s-availability-scan` §7 and `k8s-render-scan` (infrastructure), `migration-safety` and `migration-rehearsal` (database), `request-path-scan` §15 (performance) and `metric-hygiene-scan` §7 (observability), each when its pack is installed.
- `ai/patterns/deployment.md` is the deploy shape the fixes follow.

## Sources

Platform rows from [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) (C1–C3, verified 2026-10-10). Classes, lock facts tagged `[R]`/`[K]` and the stack lanes from the devops research catalog (release and deploy reliability notes, DP-1–DP-6, EP-1–EP-4, 2026-10-10) and the batch-4 devops eval (DV-4). The MikroORM row is this skill's own reading of `@mikro-orm/migrations`, `@mikro-orm/knex` and `@mikro-orm/core` 6.6.16 and `umzug` 3.8.2 from the npm registry, plus three-replica runs on `postgres:16-alpine` (2026-10-10). Paraphrased; no text reproduced beyond identifiers.
