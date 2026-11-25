---
name: doc-drift-scan
description: "Human docs vs code and config: dead paths, symbols, scripts, flags, env, endpoints, pins, breaking notes, runbooks."
kind: skill
pack: documentation
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: doc-drift-scan

## Premise

A doc drifts when it tells a reader something the code and config no longer back: a path that moved, a script that was renamed, a flag the parser dropped, an env var nothing reads, an endpoint the spec does not serve, a `Node 20+` the pins exclude, a breaking change the changelog never announced, a CronJob a runbook still restarts by its old name. In the top 1,000 GitHub projects, 28.9% carry at least one doc reference to a deleted code element and such a reference survives 4.7 years on average (Tan, Wagner & Treude, EMSE 2024). Nothing fails when a doc lies, so nothing catches it unless the claim is resolved against its oracle.

This skill owns the **docs-against-code-and-config** classes DR-1–DR-5, DS-2, DS-3, DE-1–DE-3, DA-1, DH-1, DK-1 and DK-2 (§1–§14). Docs against docs (links, anchors, ADR graph, changelog grammar, translations, nav, the docs gate) are `doc-structure-scan`; samples and spec examples are `doc-sample-scan`; executing the setup is `quickstart-verify`.

**Every finding cites the doc line and the oracle line (or the oracle's silence after the written search), the axis, the class, and the recheck that proves it.** The engine `scripts/doc-claims.py` extracts every claim once and resolves it; an engine row is a candidate, never a finding. "No drift" is never printed without the class-coverage block (§ Output).

**Three axes, three fixes.** Every finding names its axis first, because a reader must know whether to delete a line or rewrite it, and an absence has no line to cite:

| Axis | The doc says… | …and the truth is | Classes |
|---|---|---|---|
| **DEAD** | X exists | X was deleted or renamed | DR-1–DR-4, DE-1, DA-1 (MISS), DK-1, DK-2 |
| **WRONG** | X behaves like this | X exists and behaves otherwise | DR-5, DS-2, DS-3, DE-3, DA-1 (method), DR-3 (wrong package) |
| **UNDOCUMENTED** | nothing | X exists and readers need it | DE-2, DH-1 |

`BROKEN = DEAD + WRONG`. UNDOCUMENTED is counted apart: nothing lies, something is missing.

## The rule

A candidate becomes a finding only when all four hold:

1. **The claim is real and in scope.** The doc is a human doc (README, CONTRIBUTING, `docs/**`, a package README, a runbook), not a dated record, tool config, test data, versioned docs or agent-facing knowledge ([precedents § 1, § 2, § 12, § 27, § 28](../../../../snippets/precedents/documentation.md)); the token is a claim, not an illustration (§ 6) or vocabulary (§ 9).
2. **The oracle was read and named.** The tree under the resolution ladder, the manifest, the parser, the pins, the env schema, the spec or router, git history, the manifests: the row cites which.
3. **The resolution is negative or the values differ**, and the recheck (`doc-claims.py --recheck=<id>`) still prints the row.
4. **No record makes it intentional.** Not a versioned doc set, not a generated doc fixed at its source (§ 17), not a third-party or live-infra name (§ 19).

**Direction is not decided here.** About half of the outdated references real projects fixed were fixed by restoring the code (Tan et al.). The finding reports both ends; `/doc-refresh --from-audit` decides which end moves, and a doc that is the contract (spec-first OpenAPI, a published reference, a versioned public CLI, an ADR-backed promise) routes to `/fix-bug` or `/backend-fix` instead of being edited to bless the code (§ 16).

## Boundaries

- **Agent-facing knowledge** (`ai/**` except `ai/runbooks/**` and `ai/decisions/**`, `CLAUDE.md`, `AGENTS.md`, `.claude/`) → the learning pack's `knowledge-ref-scan`; the engine prints those docs as `-> learning` in its ledger and never grades them. Refract's own `ai/` setup artifacts → `/setup-project-health`.
- `.env.example` against the env schema and `.env` → backend `env-diff`, when the backend pack is installed; §8–§10 take **prose** docs against the same oracle and cite an `env-diff` row as corroboration. Without the backend pack, the example-file half is out of scope here and the coverage block says so.
- The committed spec against code or runtime → backend `http-contract-scan` §10 (when installed); §11 takes prose endpoints against the spec and the router. The changelog version against the release → devops `release-integrity-scan` RL-2 (when installed); §12 takes the breaking set against the notes.
- Accepted ADRs and convention docs against code → align `convention-oracle` AL-03/04 (when installed); this skill never reads an ADR body as a claim (§ 1, § 13).
- Links, anchors, ADR metadata, changelog grammar, translations, placeholders, nav and the docs gate → `doc-structure-scan`; fences that do not compile, doctests, embedded snippets and spec examples → `doc-sample-scan`; the setup run → `quickstart-verify`; docstrings → `docstring-coverage`; diagrams → `diagram-sync`.

## Lanes

The engine reads every renderer's source format and every stack's oracle below. Read each tool **and its version** from the lockfile before trusting a default.

| Surface | Read as | Notes |
|---|---|---|
| Markdown / MDX (GitHub, MkDocs, Docusaurus, VitePress, mdBook, Hugo) | fence-aware, front matter and HTML comments skipped; inline code spans and shell fences carry the claims | the renderer is detected from `mkdocs.yml`, `docusaurus.config.*`, `book.toml`, `.vitepress/config.*`, `hugo.*` |
| reStructuredText (Sphinx) | `code-block` and `::` blocks, ``literal`` spans, `` `t <target>`_ `` links | partial: anchors print CHECK |

| Stack | Scripts (§3) | Flags (§4) | Env (§8–§10) | Endpoints (§11) | Pins (§6–§7) |
|---|---|---|---|---|---|
| **Node / TS** | `package.json` scripts in every workspace, dependency bins, `turbo.json` tasks; pnpm / npm / yarn / bun forms, `--filter`, `-C`, `cd` | the script file a doc runs (`node`, `tsx`, `./x.sh`) and its one-hop imports; `bin` entries | `process.env`, `import.meta.env`, zod / envalid / t3-env / Joi schemas, `configService.get` | Nest `@Controller` + `@Get`, Express / Fastify `router.get`, `setGlobalPrefix` | `.nvmrc`, `engines`, `packageManager`, `volta`, Dockerfile, CI `node-version` |
| **Python** | `[tool.poe.tasks]`, `[project.scripts]`, tox envs | argparse / click / typer names in the script and imports | `os.getenv`, `os.environ`, pydantic-settings (`env_prefix`) | FastAPI `@router.get` + `APIRouter(prefix=)`, Flask `@app.route` | `.python-version`, `requires-python`, `.tool-versions` |
| **Go** | Makefile, Taskfile | `go run ./cmd/x` package sources (cobra, `flag`) | `os.Getenv`, `os.LookupEnv`, envconfig tags | `HandleFunc`, gin / chi / echo routes | `go.mod` `go` line |
| **Rust** | Makefile, justfile | `cargo run` package sources (clap) | `env::var` | — (partial) | `rust-toolchain(.toml)` |
| **JVM / .NET** | Gradle tasks [K?], Makefile | picocli / System.CommandLine sources | `System.getenv`, `@Value("${x:d}")`, `GetEnvironmentVariable` | Spring `@RequestMapping` + `@GetMapping` | `pom.xml`, `.java-version`, Dockerfile |
| **PHP / Ruby** | `composer.json` scripts, Rakefile [K?] | artisan sources [K?] | `env('X')`, `getenv`, `ENV.fetch` | `Route::get` | `composer.json` `php`, `.ruby-version` |
| **Deploy** | — | — | compose, k8s, Helm values, CI env | — | compose / k8s `image:` tags |

A stack the table marks [K?] or partial prints `checked · partial` in the coverage block, never plain `checked`.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe; shell state does not survive between tool calls). `DC` is the installed engine. `DOCS` narrows the claims to changed docs on a diff run (the oracles stay whole-repo). Every grep ends in `ck`: exit 2 is a blocked class, never zero hits. `doc-claims exit 1` is candidates, not a failure; exit 2 is BLOCKED, and the ledger's last line names the lane.

```bash
DC="${DC:-.claude/skills/doc-drift-scan/scripts/doc-claims.py}"; DOCS="${DOCS:-}"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/doc-drift.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0 CI=true DO_NOT_TRACK=1; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
python3 -I "$DC" . --lanes=paths,symbols,scripts,flags,versions,tools,env,endpoints,breaking,resources ${DOCS:+--docs="$DOCS"} --out="$OUT/run" > "$OUT/claims.tsv" 2> "$OUT/ledger.txt"
echo "doc-claims exit $? — 0 clean · 1 candidates (not a failure) · 2 BLOCKED: read the ledger's last line"; cat "$OUT/ledger.txt"
cut -f2,3 "$OUT/claims.tsv" | sort | uniq -c | sort -rn                          # status · class
cut -f3,7 "$OUT/claims.tsv" | sort | uniq -c | sort -rn | head -20                 # one root cause = one claim value
X=(-g '!**/node_modules/**' -g '!**/{dist,build,vendor,.venv,target,coverage}/**' -g '!ai/**' -g '!.claude/**' -g '!{CLAUDE,AGENTS}.md' -g '!**/{test,tests,fixtures,testdata}/**')
# D1. The env schema files §8–§10 read: files that read the environment AND build a schema (the refuter reads these).
rg -l0 --pcre2 'process\.env|import\.meta\.env|os\.environ|os\.getenv|BaseSettings' -g '*.{ts,js,mjs,py}' "${X[@]}" . | xargs -0 -r rg -l --pcre2 'z\.object\(|cleanEnv\(|createEnv\(|\(BaseSettings\)|Joi\.object\(|envalid|registerAs\('; ck D1 $?
# D1b. An env schema declared apart from its loader (`env.schema.ts` holds the zod object, `config.loader.ts` reads process.env): named for env, built as a schema.
rg -l --pcre2 '\b\w*[Ee]nv\w*\s*=\s*(?:z\.object|cleanEnv|createEnv|Joi\.object)\(|class\s+\w*(?:Settings|Env)\w*\((?:pydantic_settings\.)?BaseSettings\)' -g '*.{ts,js,mjs,py}' "${X[@]}" .; ck D1b $?
# D2. Docs that run the project's own CLIs: bin and console-script names §4 resolves against their parser.
rg -n --pcre2 '"bin"\s*:|^\[project\.scripts\]|^\[tool\.poetry\.scripts\]|^\[\[bin\]\]' -g 'package.json' -g 'pyproject.toml' -g 'Cargo.toml' "${X[@]}" .; ck D2 $?
# D3. STALE: `Updated:` / `last_reviewed:` stamps in human docs (informational; never counted in BROKEN).
rg -n --no-heading --pcre2 '^(?:Updated|Last updated|Last reviewed|last_reviewed|updated)\s*:\s*\d{4}-\d{2}-\d{2}' -g '*.{md,mdx}' "${X[@]}" . > "$OUT/stamps.txt"; ck D3 $?
python3 -I -c 'import re,sys,datetime as d;t=d.date.today();[print("STALE %s (%d days)"%(l.split(":")[0],(t-d.date.fromisoformat(m.group(1))).days)) for l in open(sys.argv[1]) for m in [re.search(r"(\d{4}-\d{2}-\d{2})",l)] if m and (t-d.date.fromisoformat(m.group(1))).days>30]' "$OUT/stamps.txt"
# Tool lane (§12): spec breaking changes between the last tag and HEAD. oasdiff exits 0 on a breaking diff without --fail-on.
TAG=$(git describe --tags --abbrev=0 2>/dev/null); SPEC=$(rg --files -g '{openapi,swagger}*.{json,yaml,yml}' "${X[@]}" . | head -1)
if [ -z "$TAG" ]; then echo "§12 oasdiff N/A (no release tag)"; elif [ -z "$SPEC" ]; then echo "§12 oasdiff N/A (no committed spec)"
elif ! command -v oasdiff >/dev/null; then echo "§12 oasdiff NOT-RUN (not installed; never npx -y)"
else oasdiff breaking --fail-on ERR "$TAG:${SPEC#./}" "HEAD:${SPEC#./}" > "$OUT/oasdiff.txt"; echo "§12 oasdiff exit $? — 0 none · 1 breaking (each must be in the notes) · other BLOCKED"; fi
find . -newer "$OUT/stamp" -type f -not -path './node_modules/*' -not -path './.git/*' | head -3; echo "write check done (empty = nothing written)"
```

The engine's ledger comes first: a `blocked` lane, a `-> learning` count that looks like most of the corpus, or a write-check hit is settled before any row is read. Its row format is `id · status · class · surface · doc · line · claim · detail`; `status` is MISS (DEAD), WRONG, or CHECK (ambiguous: read it). The `id` is stable for the recheck. `--all` adds the resolved and skipped rows, each skip with its precedent §.

## Measured

Measured 2026-10-19 with `doc-claims 1.0` (self-test 46/46: one seed and one decoy per lane).

- **A real NestJS + React monorepo** (read-only, write check empty, 15 s, 13,621 files). Scope: 107 human docs in scope (66 docs, 40 ADRs, 1 changelog; 47 runbooks), 329 agent-facing docs routed `-> learning`, 553 tool-config docs § 2, 3 test-data § 27, 2 templates § 6. Today's step 1, run verbatim, printed 3,446 MISS (3,250 in dated audits) and step 8 exited 2 on `src apps libs`. The engine's first run printed 309 candidates; after the scope, resolution and parsing fixes recorded below it prints **25**: DR-1 0 MISS (1,047 claims; 11 per-module layout names § 3, 18 build outputs § 4), DR-2 7 (592 claims; third-party vocabulary skipped § 9), DR-3 2 CHECK (package-local scripts run from the root, § 31), DR-4 0 (202 flags, 198 on third-party CLIs § 19), DS-2 0 (17 claims; `moduleResolution node10` was a false hit before the separator fix), DE-1 2 CHECK (in `.env.example`, read by no code), DA-1 0 (27 claims; 14 curls to Prometheus, Loki and Alertmanager ports § 19), DK-1 5 (a deleted health-controller path, a dated plan the runbook still links), DK-2 7 (from 43: `kubectl create secret generic` parsed `generic` as a name; third-party chart Services and out-of-band Secrets now § 19; a KEDA-derived HPA resolves through its ScaledObject; still open: an alert name no rule declares, and an HPA the runbook reads by the workload's name while KEDA names it `keda-hpa-<name>`). DH-1 N/A (0 tags). Greps: D1 2 (the env schema and the config loader; it printed 300+ zod contract files before it required an env read in the same file) · D2 0 · D3 0; no grep exited 2.
- **The 23 fixtures** carry no doc corpus beyond their own `DEFECTS.md` answer keys; every row there is a reference to the parent repo (`benchmarks/run.sh`, `templates/packs/…`) or framework vocabulary, so the seeded corpus is the engine's `--self-test` until a doc fixture lands (integrator request). Greps: D1 1 on `backend-defects`, `ds-defects` and `quality-mix`, 0 elsewhere; D2 and D3 0; no grep exited 2.
- **The `doc-drift` fixture** (`benchmarks/fixtures/doc-drift`, 2026-10-19; staged with `run.sh`, whose key line `Stage with: --git --history` runs the fixture's history-staging script: 14 commits, tags v1.4.0 and v1.5.0; write check empty): 42 docs in scope, renderer mkdocs (`docs/guide`), 3 package roots. The pre-flight printed **29 candidates, two per class for all fourteen §s** — the 28 doc-drift-scan seeds, every one, plus one same-cause twin (DR-3 on the Arabic setup page's `pnpm dev:all`, which is the DI-3 seed's root cause); 0 of the fixture's 22 decoys printed as a candidate (platform env § 8, third-party flags § 19 (11), gitignored paths § 4, a provenance banner § 20 and `/metrics` § 7 printed as skips). Without the history script DH-1 prints `N/A (no release tags)`. Greps: D1 0 (the schema file reads no `process.env`; its loader does), D1b 1 (`env.schema.ts`; added after this run: D1b is 1 on `backend-defects`, 0 on every other fixture), D2 1, D3 0; no grep exited 2; oasdiff NOT-RUN (not installed). Gaps the run found in the engine, fixed in the integration pass the same day with failing-first self-test cases (`--self-test` 53 checks; `tests/doc-claims/run.sh` pins the 61 fixture rows): DH-1 counted a note as announced on a section-wide word vote (now one line must carry half the subject's words as whole words plus a breaking or removal signal); DE-2 rows carried no `file:line` (now the schema line, surface primary).

Fixes the measurement forced: route matching is exact-first with a suffix match only on routes of two or more static segments (a `/rules` suffix matched a pricing route and printed a false method mismatch); curl claims to a port that is not the app's are third-party (§ 19); `kubectl` value flags (`--field-selector`, `-l`) no longer become resource names; YAML metadata is read line by line (a backtracking regex hung on the deploy manifests); env reads include test harnesses (load-test and e2e variables documented in runbooks).

## The 3,000-row path

1. **Check the scope first.** An area holding more than 30% of the rows is checked against precedents § 1, § 2, § 27, § 28 before a single row is read. A ledger with most of the corpus in scope and `ai/` missing from the skip list means the scope rules did not load.
2. **Group by claim value, not by line.** `cut -f3,7 claims.tsv | sort | uniq -c`: one renamed script, path, env var or Deployment is **one finding with N sites**; `--claim=<value>` lists them.
3. **Read in this order:** primary surface rows (README, quickstart, CONTRIBUTING, runbooks), then WRONG over DEAD over UNDOCUMENTED, then secondary docs.
4. **Close a group with one checked reason** (`14 DA-1 curls to :9090 and :3100: Prometheus and Loki APIs, § 19`).
5. **Ledger the rest** as `Live, unreviewed (k groups / n rows)` with the `--class` command that continues it; never `checked`.

## Scans for

Severity is set by who follows the doc and when ([precedents](../../../../snippets/precedents/documentation.md), the claim). **Primary surface**: README, quickstart and setup docs, CONTRIBUTING, runbooks, published API or SDK docs. **Secondary**: internal guides and how-tos (one step lower). **BLOCKER** is reserved for a runbook step that acts on the wrong resource (a renamed workload whose old name now belongs to something else) and a setup step that destroys data.

| § | Class | Engine lane | Finding when | Default (primary) | Oracle |
|---|---|---|---|---|---|
| 1 | DR-1 dead path | paths | MISS after the ladder, gitignore and rename lookup | MEDIUM | V433 |
| 2 | DR-2 dead symbol | symbols | a project-shaped name defined nowhere in source or config | MEDIUM | V433 |
| 3 | DR-3 dead script / target | scripts | no manifest or task file defines it where the doc runs it | HIGH | V434 |
| 4 | DR-4 dead flag | flags | the project CLI's parser does not declare it | MEDIUM | V434 |
| 5 | DR-5 deprecated as current | symbols, endpoints | a deprecation marker on a symbol the doc presents as current | MEDIUM | V435 |
| 6 | DS-2 version claim ≠ pins | versions | the claimed version is admitted by no pin | MEDIUM | V436 |
| 7 | DS-3 tool mismatch | tools | the command uses a package manager the lockfile does not | MEDIUM | V436 |
| 8 | DE-1 dead env | env | in an env context, read by nothing, in no example, deploy file or schema | MEDIUM | V438 |
| 9 | DE-2 required env undocumented | env | required with no default, named in no doc and no example | HIGH | V438 |
| 10 | DE-3 env default / values wrong | env | the doc's default or value set ≠ the schema's | MEDIUM; HIGH on a security- or money-relevant setting | V438 |
| 11 | DA-1 prose endpoint | endpoints | no spec path and no router declaration, or another method | MEDIUM; HIGH in public API docs | V439 |
| 12 | DH-1 breaking change unannounced | breaking + oasdiff lane | a `!:` / `BREAKING CHANGE:` commit or an oasdiff ERR missing from its section | HIGH for a published package or API, else MEDIUM | V445 |
| 13 | DK-1 runbook command | paths, scripts, flags in runbooks | §1, §3 or §4 inside a runbook | HIGH | V434 |
| 14 | DK-2 runbook resource | resources | a kind/name, namespace, compose service, alert or queue no manifest declares | HIGH; BLOCKER when the name now belongs to another resource | V446 |

### 1. Dead path (DR-1)

```
BAD:   README.md      "Config lives in `apps/api/src/config/settings.ts`."   (moved to apps/api/src/config/index.ts)
GOOD:  README.md      "Config lives in `apps/api/src/config/index.ts`."        · or the file restored when the doc is the contract
```
**Read the docs and the code:** Does the ladder miss it everywhere: root, the doc's directory, every package root, a unique suffix? Is it gitignored (`git check-ignore`, the directory form too) or a build output (§ 4)? Does the line say a command produces it (§ 5, CHECK)? What does the engine's detail say about history: `renamed -> <new> (<sha>)` gives the repoint; `deleted in <sha>` asks whether the deletion was intended. **Finding when** the path resolves nowhere and no precedent applies. **Proof:** V433, `--recheck=<id>` fails before and passes after; `--claim=<path>` prints no row in any doc.

### 2. Dead symbol (DR-2)

```
BAD:   docs/architecture.md   "`OrderReconciler` retries failed payouts."          (renamed PayoutReconciler)
GOOD:  "`PayoutReconciler` retries failed payouts."
```
**Read the docs and the code:** The engine reports only a project-shaped name (`…Service`, `…Processor`, `…Input`) or a member of a project receiver (`ordersService.cancelAll()`); framework vocabulary is § 9. Is the name a third-party API the project merely calls (search the lockfile's packages)? A rename in `git log -S<name>`? **Finding when** the project defines nothing by that name in source or config. **Proof:** V433.

### 3. Dead script or target (DR-3)

```
BAD:   README.md   ```bash  pnpm dev:all  ```          (root package.json: dev, dev:api, dev:web)
       runbook     make restore-db                      (Makefile: db-restore)
GOOD:  pnpm dev     ·   make db-restore
```
**Read the docs and the code:** Which package does the command run in: the root, a `--filter` / `-F` / `-C` target, a preceding `cd`? A script defined only in a sub-package and run from the root is CHECK (§ 31): does the doc `cd` first? Is the token a dependency bin (`pnpm vitest`)? A prose word ("npm package") is never a claim: the engine reads code spans and shell fences only. **Finding when** no manifest or task file defines it where the doc runs it. **Proof:** V434, the command's manifest lookup, plus every form of the same script across docs and CI.

### 4. Dead flag (DR-4)

```
BAD:   README.md   node tools/import.js --legacy-import     (tools/import.js declares --import, --format)
GOOD:  node tools/import.js --import
```
**Read the docs and the code:** Is the CLI the project's own: a script file the doc runs, a `bin` entry, a `[project.scripts]` name, `go run ./cmd/x`? A third-party CLI's flag is § 19 (the engine skips it and counts it). Is the flag built from a variable, a `--no-` negation, or declared in an imported module the one-hop read missed? **Finding when** the parser and its imports declare no such option. **Proof:** V434, the parser declaration (or a `--help` capture at the pinned version).

### 5. Deprecated API presented as current (DR-5)

```
BAD:   docs/sdk.md   "Call `getOrders()` to page through orders."     (orders.ts: /** @deprecated use listOrders */)
GOOD:  "Call `listOrders()` …"   ·   or "`getOrders()` is deprecated; use `listOrders()`."
```
**Read the docs and the code:** Which marker: JSDoc `@deprecated`, `#[deprecated]`, `// Deprecated:`, `@Deprecated`, `DeprecationWarning`, OpenAPI `deprecated: true`? Is the doc a migration guide naming the old API on purpose? **Finding when** the doc steers a reader to the marked API with no deprecation note. **Proof:** V435.

### 6. Version claim against the pins (DS-2)

```
BAD:   README.md   "Requires Node 20+."            (.nvmrc 22; engines.node >=22.12)
       CONTRIBUTING "Python 3.10"                   (requires-python >=3.12)
GOOD:  "Requires Node 22.12+."
```
**Read the docs and the code:** Which pins exist (the engine lists them): `.nvmrc`, `engines`, `.tool-versions`, `.python-version`, `requires-python`, `go.mod`, Dockerfile `FROM`, compose `image:`, the CI matrix? A documented support matrix wider than the dev pin is fine when CI tests it. A claim for a runtime with no pin prints `skip no-pin` in the ledger: UNVERIFIED, not a finding. **Finding when** no pin admits the claimed version. **Proof:** V436.

### 7. Package manager or tool mismatch (DS-3)

```
BAD:   README.md   npm install && npm run dev        (pnpm-lock.yaml; packageManager pnpm@10.29.2)
GOOD:  pnpm install && pnpm dev
```
**Read the docs and the code:** Is the doc for contributors or for consumers installing the published package (`npm install <name>` is fine)? Does corepack enforce `packageManager`? **Finding when** a contributor step uses a tool the lockfile does not. **Proof:** V436.

### 8. Dead env var (DE-1)

```
BAD:   docs/config.md   | `SEARCH_INDEX_URL` | search backend |       (no read, no schema key, no example, no manifest)
GOOD:  the row removed, or the variable wired again
```
**Read the docs and the code:** Is the line an env context (an env table, `.env`, `export`, `X=` in a fence)? Is it platform- or SDK-read (§ 8)? Is it a constant (§ 9)? Is it read under another name (a pydantic `env_prefix`, a `configService.get` key, a k6 `__ENV`)? A CHECK row "in `.env.example` but no code reads it" is `env-diff`'s to confirm. **Finding when** nothing reads it and nothing sets it. **Proof:** V438.

### 9. Required env var undocumented (DE-2)

```
BAD:   env.schema.ts   PAYMENTS_WEBHOOK_SECRET: z.string(),        (no default; in no doc and no .env example)
GOOD:  documented in the setup section and in .env.example with a comment
```
**Read the docs and the code:** Is it really required at boot (no `.optional()`, `.default()`, `devDefault`)? Is it mentioned anywhere: the manual, `.env` example comments, error messages, schema descriptions (§ 24)? **Finding when** no doc surface names it. The finding opens on the schema line that declares the key — no doc line is wrong when no doc names it — and says which docs lack it. **Proof:** V438. Corroborate with `env-diff` when the backend pack is installed.

### 10. Env default or values wrong (DE-3)

```
BAD:   docs/config.md   "`RETRY_LIMIT` (default `5`)"          env.ts: RETRY_LIMIT: z.coerce.number().default(3)
       docs/config.md   "`LOG_FORMAT`: `json` or `text`"       env.ts: z.enum(["json", "pretty"])
GOOD:  default `3` · `json` or `pretty`
```
**Read the docs and the code:** Is the doc describing another deploy profile (a Helm values default that overrides the schema)? Is the value security- or money-relevant (a token TTL, a rate limit, a currency): then HIGH. **Finding when** both values are in hand and differ. **Proof:** V438.

### 11. Prose endpoint not served (DA-1)

```
BAD:   docs/api.md   `POST /orders/{id}/void`             (spec and router: POST /orders/{id}/cancel)
GOOD:  `POST /orders/{id}/cancel`
```
**Read the docs and the code:** Did the engine resolve the global prefix and version (`setGlobalPrefix`, `servers[].url`)? For a Nest API, when the backend pack is installed, the router oracle is backend `validation-boundary-scan`'s `dto-types.py --routes <api src>` (run from that installed skill's folder): stdout is a header plus `HANDLER` rows only (verb in column 4, the mounted path with prefix, version and `exclude` applied in column 9; the statistics go to stderr), so it needs none of the backend audit's F-lines (measured on the `doc-drift` API: 12 handlers, 10 under the `v1` prefix, `metrics` and `health` excluded). Is the route excluded from the spec by design (§ 7)? Is the line a how-to or an illustration (§ 6, CHECK)? Is a curl aimed at a third-party port (§ 19)? A method mismatch on an exact path is WRONG; on a suffix match only it is CHECK. **Finding when** neither the spec nor the router serves it. **Proof:** V439; route to backend `http-contract-scan` §10 when the spec itself is stale.

### 12. Breaking change shipped with no release note (DH-1)

```
BAD:   git log v1.4.0..v1.5.0:  feat(api)!: drop the page param       CHANGELOG ## [1.5.0]: no mention
GOOD:  ## [1.5.0] ### Changed — **BREAKING** `page` removed; use `cursor`   (retro-adding is endorsed, § 25)
```
**Read the docs and the code:** Is the package published (an npm or PyPI name, a public API)? Is the changelog generated (§ 17: fix the commit footer or the generator config, then regenerate)? Per-package tags (§ 18) map to per-package changelogs. The oasdiff lane adds spec ERRs between the last tag and HEAD. No tags means N/A, never PASS. **Finding when** a breaking item is missing from the section that covers it. **Proof:** V445.

### 13. Runbook command (DK-1)

```
BAD:   docs/runbooks/restore.md   make restore-db · node tools/failover.js --region   (target renamed; flag removed)
GOOD:  make db-restore · node tools/failover.js --to <region>
```
**Read the docs and the code:** §1, §3 and §4 applied inside a runbook (by path, `type: runbook`, or Rollback / Mitigation headings). A runbook step fails when nobody can think; every row is HIGH. **Finding when** §1, §3 or §4 holds in a runbook. **Proof:** V434; the drill itself stays `/add-runbook`'s hygiene.

### 14. Runbook resource (DK-2)

```
BAD:   docs/runbooks/nightly-jobs.md   kubectl -n app get cronjob reports-nightly    (deploy/k8s/cron.yaml: reports-daily)
GOOD:  kubectl -n app get cronjob reports-daily
```
**Read the docs and the code:** Is the name in the repo's manifests, Helm values or compose file at all? A Service a third-party chart creates (a release or chart name in the resource name), a Secret created out of band, a KEDA-derived HPA, and a name created earlier in the same runbook are § 19 or resolved. Does the old name now belong to **another** resource (BLOCKER: the step acts on the wrong thing)? **Finding when** the repo declares the kind but not the name. **Proof:** V446.

Two claim types ride on this § (read lane; `doc-claims.py` does not extract them, so list each as `Live, unreviewed` until read): **a size or slug in a create command** (`--size`, `--node-size`, `--machine-type`, `--instance-type`) contradicted by the repo's own inventory table or IaC for the same resource — re-running the step builds a different, often costlier, resource (MEDIUM; finops `candidate-pricing` prices the difference when that pack is installed); and **a table named as absent** (`no longer exists`, `was dropped`) in a doc or comment while a migration or the schema still creates it (MEDIUM; the database owner confirms which side is current).

## Output

```
doc-drift-scan — doc-claims 1.0 · renderer github · 107 docs (329 -> learning) · pins: .nvmrc, engines, packageManager
Doc drift — DEAD=3  WRONG=2  UNDOCUMENTED=1  STALE=2   (BROKEN = DEAD + WRONG = 5)

Findings: 4 · Unconfirmed: 2

1. README.md:41                                              [report-with-fix]  HIGH · DEAD · §3
   `pnpm dev:all` — no script dev:all in 6 manifests (root: dev, dev:api, dev:web). Recheck 3fa91c02d1 fails.
   Fix: `pnpm dev` (2 more sites: CONTRIBUTING.md:18, docs/de/setup.md:12 → one finding, 3 sites).
2. docs/runbooks/nightly-jobs.md:22                          [report-with-fix]  HIGH · DEAD · §14
   CronJob/reports-nightly — deploy/k8s/cron.yaml:4 declares reports-daily (renamed in 9c1e2ab). Fix: the new name.
3. docs/configuration.md:12                                     [report-with-fix]  MEDIUM · WRONG · §10
   `RETRY_LIMIT` default 5 — apps/api/src/config/env.ts:9 `.default(3)`. Fix: 3.
4. CHANGELOG.md:7                                            [report-flagged]   HIGH · UNDOCUMENTED · §12
   6e0f1d2 feat(api)!: drop the page param — not in ## [1.5.0]. Unproven link: is @acme/api published? (package.json private: false)

Verification: 25 candidates → 4 findings · 2 unconfirmed · 6 hardening · 0 pre-existing · 13 refuted

Class coverage:
  §1  dead path              checked (1,047 claims → 0; 11 layout names § 3, 18 build outputs § 4)
  §2  dead symbol            checked (592 claims → 7 → 0; third-party vocabulary § 9)
  §3  dead script            checked (117 claims → 2 → 1)
  §4  dead flag              checked (202 claims → 0; 198 third-party § 19)
  §5  deprecated as current  checked (0 markers on documented symbols)
  §6  version vs pins        checked (17 claims → 0) · 3 UNVERIFIED (no pin for postgres: skip no-pin)
  §7  tool mismatch          checked (0 claims)
  §8  dead env               checked (72 claims → 2 CHECK → env-diff)
  §9  required undocumented  checked (14 schema keys → 0)
  §10 env default / values   checked (3 claims → 1)
  §11 prose endpoint         checked (27 claims → 0; 14 third-party ports § 19)
  §12 breaking unannounced   N/A (no release tags) · oasdiff N/A
  §13 runbook command        checked (448 claims → 5 → 1)
  §14 runbook resource       checked (265 claims → 7 → 1) · Live, unreviewed (2 groups / 4 rows — continue with --class=DK-2)
  routed                     agent-facing docs → learning knowledge-ref-scan (329) · .env.example → backend env-diff (2)
```

`[report-with-fix]`: both ends cited, the recheck fails, the fix is a local edit (or the code restored, § 16). `[report-flagged]`: one link unproven (publication, a contract question, a resource a chart might create); the row names it and the probe that settles it. The header line is a contract `/doc-refresh` reads: keep `Doc drift — DEAD=… WRONG=… UNDOCUMENTED=… STALE=…`. STALE counts docs whose `Updated:` stamp is older than 30 days (D3) and is never part of BROKEN. Every run prints **all fourteen** §s as `checked (k claims → m)`, `N/A (<reason>)`, `blocked (<lane>: <reason>)`, `→ <owner> (k)` or `Live, unreviewed`; a [K?] lane says `checked · partial`.

## Precedents

The verifier reads [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 1 dated records, § 3 package roots, § 4 gitignored outputs, § 5 produced paths, § 8 platform env, § 9 constants and vocabulary, § 16 the doc is the contract, § 17 generated docs, § 19 third-party and live infra, § 28 agent-facing knowledge, § 31 package-local scripts. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation, V433–V439, V445, V446.

## When to run

- On every whole-repo `/doc-refresh --audit`, printing all fourteen §s.
- On a diff that renames or deletes a file, script, flag, env key, route, export or k8s resource, or bumps a pin: run with `DOCS` unset (the oracle changed, every doc may now lie); on a diff that only edits docs, set `DOCS` to the changed docs.
- Before a release: §12 with the oasdiff lane.

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/doc-refresh --audit` that is `@verifier` in refute mode on every BLOCKER and HIGH; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any finding without its axis, the doc line, the oracle line (or the written search), the engine row id and the V-number.
- Do not decide the direction here, and never propose editing a contract doc to match the code (§ 16); never hand-edit a generated doc (§ 17).
- Do not read a row from a lane the ledger prints `blocked`; its §s print `blocked`, never `checked`. `doc-claims exit 2` with no ledger is a blocked run.
- Do not grade agent-facing knowledge, dated records or tool config; the ledger's skip counts are the record.
- Write nothing into the repo: no `--out` or `--fences` inside it (the engine refuses), no doc edits from this skill; the write check must print nothing.
- Do not print "no drift" without the class-coverage block.

## Related

- `scripts/doc-claims.py` (this skill) — the engine; `doc-structure-scan` and `doc-sample-scan` run its other lanes, and `/doc-refresh --from-audit` re-runs `--recheck` and `--claim` to close findings failing first.
- `quickstart-verify` executes the setup; `docstring-coverage` grades the API reference; `diagram-sync` checks diagrams; `changelog-generate` writes the notes §12 checks.
- Backend `env-diff`, `http-contract-scan` §10 and `dto-types.py --routes` (backend pack), devops `release-integrity-scan` RL-2, align `convention-oracle`, and the learning pack's `knowledge-ref-scan`, each when its pack is installed.
