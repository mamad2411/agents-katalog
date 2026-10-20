---
name: validate-tehik-it-profile
description: "Validate a software project against the TEHIK IT Profile (the Ministry of Social Affairs technology compatibility matrix). Use this skill whenever the user asks to audit, check, verify or validate a project against the TEHIK IT Profile, IT-profiil, infotehnoloogiline profiil, IT standards stack, or the TEHIK technology selection matrix — even when phrased casually like 'is our stack TEHIK-approved?', 'are we using the right tech per the IT profile?', 'check our stack against TEHIK preferred technologies', 'find any forbidden frameworks', 'IT profile audit', or 'how badly do we deviate from the IT profile?'. Also trigger when the user references the TEHIK-EE/infotehnoloogiline-profiil GitHub repository, asks whether a specific tech (Spring, Drupal, PostgreSQL, Kubernetes, Liquibase, etc.) is preferred / acceptable / forbidden in a TEHIK context, asks about the Preferred / Acceptable / Do-not-select columns, or wants a Markdown report describing per-component verdicts. The skill fans out across parallel subagents (one per technology layer) so context stays manageable, and writes a per-component Markdown report at the project root."
---

# Validate TEHIK IT Profile

Audit a software project against the TEHIK IT Profile and produce a Markdown
report with per-component verdicts.

The upstream document lives at:
**https://raw.githubusercontent.com/TEHIK-EE/infotehnoloogiline-profiil/refs/heads/main/IT-profiil.en.md**

It is one large 5-column compatibility matrix (Component | Preferred |
Acceptable | Do not select | Comments) grouped into six technology layers
plus a hardware-standard appendix. Trying to evaluate the whole matrix in
one context window is a context-rot disaster, so this skill fans the work
out: one subagent per layer, run in parallel, each handed only its own
slice of the document plus a pre-flight fact sheet about the project.

## When this applies

- The user wants an end-to-end IT Profile audit of the current project (or
  a specific path they pass in).
- The user asks for a partial audit of one or more layers (e.g. "just check
  the application layer", "audit the database choices only").
- The user has produced earlier audits and wants a re-run after fixes.

## When NOT to use

- The user is asking *what* the IT Profile says, not whether their project
  complies with it — answer from the document directly without invoking
  this skill's full pipeline.
- The user wants to enforce these rules at commit/CI time. That is a
  different problem (a linter / CI step), not an LLM audit. Tell them so.
- The project is empty or nearly empty (no source files). Say so and refuse
  to produce a report; the report would be all `INSUFFICIENT_INFO` and
  `NOT_USED` rows and would mislead.
- The user wants to validate functional or non-functional requirements
  (logging shape, monitoring SLAs, source-code organisation). That is the
  job of `validate-tehik-nfr`, the sibling skill. The IT Profile is purely
  a tech-stack matrix.

## Sections that are intentionally out of scope

Three parts of the upstream document **must not** be audited — they cannot
be verified from source code:

1. **Servers — Hardware standard.** Physical-hardware requirements
   (X86-64, redundancy, hot-swap disks, remote management, NBD support
   contracts). Hardware/contract concerns, not source.
2. **Technical-requirement selection principles.** Five high-level
   principles ("prefer open standards", "minimise component diversity",
   etc.) that apply to the project as a whole, not to any individual
   component.
3. **General governance.** Three top-level points about how the IT Profile
   itself is updated and approved by the TEHIK architectural council.

The skill **must** surface these in the final report under explicit
"out of scope — verify out-of-band" blocks rather than silently dropping
them. Silent omission would mislead the reader into thinking those areas
were checked.

## Verdict taxonomy

The IT Profile is a compatibility matrix, not a list of pass/fail
requirements. Every component category gets exactly one of:

- **PREFERRED** — project uses a Preferred-column technology.
- **ACCEPTABLE** — project uses an Acceptable-column technology with no
  footnote attached.
- **NEEDS_COORDINATION** — project uses an Acceptable choice flagged with
  `[N]`, where the footnote says it must be coordinated (typically `Must
  be coordinated with TEHIK architect`). Compliance is conditional on that
  coordination existing.
- **FORBIDDEN** — project uses a Do-not-select technology. Direct violation.
- **UNAPPROVED** — project uses a technology not listed anywhere in the
  matrix. Per the IT Profile selection principles: "All components and
  products not mentioned require prior agreement with the TEHIK
  architectural council."
- **NOT_USED** — the project does not use any technology in this category
  (e.g. backend-only services have no Mobile client OS).
- **INSUFFICIENT_INFO** — cannot be verified from source alone (deployment
  choices, infrastructure-level concerns, contractual matters).

This taxonomy is wider than the NFR skill's PASS/FAIL/PARTIAL because the
matrix preserves a real distinction between "preferred", "acceptable", and
"acceptable with coordination". Do not collapse them in the report.

## Pipeline overview

```
[1] Pre-flight project intel  →  short fact sheet
[2] Fetch IT Profile document →  cached file + provenance JSON
[3] Split into 6 layers       →  per-layer .md + .json + manifest.json
[4] Dispatch subagents        →  one per layer, in parallel, each gets only
                                  its slice + project intel
[5] Aggregate findings        →  read each layer's findings file
[6] Write final Markdown report →  tehik-it-profile-audit-YYYY-MM-DD.md in
                                    project root
```

Each step is detailed below.

## Step 1: Pre-flight project intel

Before fetching anything, do a short read-only scan of the project root and
produce a fact sheet. The goal is to give every subagent a shared baseline
so 6 of them don't independently rediscover the same things. Spend at most
a few tool calls — this is a fact sheet, not an audit.

Capture, where present:

- **Languages** detected (file extensions, primary one first).
- **Build tool / package manifest** (`pom.xml`, `build.gradle(.kts)`,
  `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json`,
  etc.).
- **Frameworks** evident from manifests (Spring Boot, NestJS, Django,
  Angular, React, Vue, Quarkus, etc.). The matrix is dominated by
  framework-level decisions — be generous here.
- **Database access** (driver, ORM, migration tool: JPA/Hibernate/jOOQ,
  Flyway/Liquibase, Prisma, Alembic, raw SQL). Names matter — the matrix
  distinguishes Liquibase (preferred) from Flyway (acceptable).
- **Frontend** (build tool, framework: webpack, Vite, Angular, React,
  Next.js — Next.js needs coordination per the matrix).
- **Logging library / observability stack** (logback, log4j, winston,
  structlog, OpenTelemetry, Elastic APM, Prometheus client).
- **CI / CD presence** (`.gitlab-ci.yml`, `.github/workflows/`,
  `Jenkinsfile`). The matrix prefers GitLab CI; GitHub Actions need
  coordination.
- **Container / deployment** (`Dockerfile`, `docker-compose.yml`, helm
  charts, k8s manifests, terraform, ansible). Helm is preferred for live;
  Argo CD needs coordination.
- **Test runners** (Selenium / Selenide preferred; Cypress / Playwright
  need coordination).
- **Server / image base** if visible (Dockerfile FROM clause, base image
  tag), to inform the Server OS verdict.
- **Repository hint about app type** (presence of UI source, public-facing
  web routes, API-only signals, mobile-app source).

Format the fact sheet as ~10-30 lines of bullet points. Save it to the
audit's working directory so each subagent prompt can embed it verbatim.

There is **no app-type confirmation step** in this skill. Unlike the NFR
skill, the IT Profile matrix has no Self-service / Websites / COTS
applicability columns — applicability is decided per-component by the
subagent based on what the project actually uses. Don't ask the user to
pick an app type; it would not change the audit.

## Step 2: Fetch the IT Profile document

Run the bundled fetch script. It tries live → cached → bundled snapshot in
that order, computes a sha256, and emits provenance metadata.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/validate-tehik-it-profile/scripts/fetch_it_profile.py"
```

Capture the JSON output — its `path`, `url`, `source`, `sha256`,
`fetched_at`, and `fallback_reason` fields all flow into the final report.

Pass `--refresh` if the user explicitly asks for a fresh download. Pass
`--offline` if they say they're disconnected.

## Step 3: Split the document

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/validate-tehik-it-profile/scripts/split_layers.py" \
  "<path-from-step-2>" \
  --out "<workdir>/layers" \
  --source-meta "<path-to-stored-step-2-json>"
```

This produces `layer-NN-<slug>.md` and `layer-NN-<slug>.json` for each of
the (typically 6) layers, plus `manifest.json`. Inspect `manifest.json` to
confirm 6 layers were parsed; if a different number comes back the
upstream document changed structure — surface a warning to the user and
proceed with whatever was parsed.

The manifest also carries an `out_of_scope` block extracted from the
document: the Servers hardware standard items, the selection principles,
and the General governance points. Pass them through to the final report
without trying to score them.

## Step 4: Dispatch subagents

For each parsed layer (typically layers 1 through 6):

1. Read `references/subagent-brief.md`.
2. Replace every `{{...}}` placeholder using the per-layer data from
   `manifest.json` and the project intel. Resolve `{{COMMON_RULES_PATH}}`
   to the absolute path of
   `${CLAUDE_PLUGIN_ROOT}/references/auditor-common.md` so the subagent
   receives a concrete path it can `Read`.
3. Spawn one Agent in the same message per layer, all in parallel.
   Use
   `subagent_type: tehik-standards-validation:it-profile-layer-auditor`
   — the agent is pinned to Sonnet and locked to read-only tools (Read,
   Grep, Glob, Bash), so do not override the subagent type unless the
   user explicitly asks for a different model or wider tool access.
   Each subagent must write its findings to
   `<workdir>/findings/layer-NN.md` so a partial run can be resumed
   later.
4. Wait for all subagents to return.

Why parallel: each subagent runs in its own context window, so the
orchestrator never sees more than one layer's worth of components at a
time plus short summaries. This is the entire reason for the fan-out — do
not fall back to sequential or single-shot execution unless the user
explicitly asks for it.

If a subagent fails (Agent tool returns an error or no findings file), do
NOT silently continue. Report which layer failed in the report under
"Layer findings" with the error and a verdict of `INSUFFICIENT_INFO` for
all of that layer's components, so the gap is visible.

## Step 5: Aggregate findings

1. Read every `findings/layer-NN.md` produced by the subagents.
2. Tally verdict counts (PREFERRED / ACCEPTABLE / NEEDS_COORDINATION /
   FORBIDDEN / UNAPPROVED / NOT_USED / INSUFFICIENT_INFO) across all
   audited layers.
3. Build the out-of-scope blocks from `manifest.json` → `out_of_scope`:
   - **Servers hardware standard** — list each item verbatim.
   - **Selection principles** — list each verbatim.
   - **General governance** — list each verbatim.
4. Roll up critical issues: every FORBIDDEN and UNAPPROVED verdict, in
   component-id order. These are the IT Profile violations.
5. Roll up coordination items: every NEEDS_COORDINATION verdict, with the
   footnote text from the matrix. Compliance here is conditional, not
   missing.
6. Roll up unknowns: every INSUFFICIENT_INFO verdict, in component-id
   order.
7. Build a recommendations list: pull recommendations from FORBIDDEN /
   UNAPPROVED / NEEDS_COORDINATION findings, deduplicate near-identical
   ones, group by layer.

## Step 6: Write the report — must be SELF-CONTAINED

This is the part that goes wrong if you take shortcuts. Read it carefully.

Use `references/report-template.md` as the skeleton. The template has two
zones, separated by `<!-- begin rendered report -->` and
`<!-- end rendered report -->` HTML comments:

- The **rendered zone** between those markers is the literal Markdown that
  becomes the audit report. Copy it verbatim, replacing every
  `{{PLACEHOLDER}}`. Strip the marker comments themselves before writing.
- The **orchestrator-instructions zone** after the closing marker tells
  you, placeholder by placeholder, where each value comes from. Read it.
  Especially watch for the placeholder-specific notes on
  `{{LAYER_FINDINGS_BLOCKS}}`, `{{SKILL_VERSION}}`, and
  `{{RECOMMENDATIONS_LIST}}` — the last one carries an explicit
  "do not assert specific verdict counts in narrative prose" rule that
  prevents the report from drifting between the verdict table and prose
  references to it.

Write the resulting Markdown to
`<project-root>/tehik-it-profile-audit-YYYY-MM-DD.md`.

If a report file with that exact name already exists, append a `-N` suffix
rather than overwriting (the user may want to compare runs).

### The report MUST inline every audited component

The final report is the only artifact a reader will open. Treat it as the
single source of truth for the audit. That means:

- For every audited component (every component-id in every layer), the
  report must contain its full structured block — the H3 heading, the
  status line, the project-uses line, the matrix-says block, the
  confidence line, the evidence bullets with concrete `file:line`
  references, and the recommendation when not PREFERRED. Copy the block
  from the subagent's `findings/layer-NN.md` verbatim; do not paraphrase
  it into a one-paragraph layer summary.
- Layer-level narrative summaries (the "this layer had X PREFERREDs, the
  highlight is Y" paragraphs) are nice on top of the per-component list,
  not in place of it. If you only emit the narrative summary you have
  produced a half report.
- The report must NOT contain any reference like "Detailed evidence: see
  `.tehik-it-profile-audit/.../findings/layer-NN.md`" or "see fragment
  file X". The reader must be able to read the audit end-to-end without
  opening another file. If you find yourself wanting to write such a
  reference, inline the contents instead.

Concrete shape per audited component (matches what the subagent wrote):

```
### 4.2 — Relational DBMS
- **Status:** ACCEPTABLE
- **Project uses:** MariaDB (`docker-compose.yml:14`, `application.yml:7`)
- **Matrix says:**
  - Preferred: PostgreSQL
  - Acceptable: MariaDB (must be coordinated with TEHIK architect)
  - Do not select: MS SQL Server, Oracle DB, Sybase
- **Confidence:** HIGH
- **Evidence:**
  - `docker-compose.yml:14` — `image: mariadb:10.11`
  - `application.yml:7` — `driver-class-name: org.mariadb.jdbc.Driver`
- **Recommendation:** Document coordination with the TEHIK architectural
  council for the use of MariaDB, per footnote [1] in the Acceptable
  column. PostgreSQL is the Preferred alternative.
```

The Servers / selection-principles / general-governance out-of-scope
sections stay their own dedicated blocks with each item listed verbatim —
the same level of inlining (no fragment file references).

### Step 7: Verify the report is complete, then clean up

Before declaring success or deleting any working artifacts:

1. **Count component blocks in the report.** Count headings shaped like
   `### <N>.<n>` (or `#### <N>.<n>` — whichever you used consistently).
   The total must equal the count of components you set out to audit
   (sum of `component_count` across all layers in `manifest.json`). If
   the count is short, the report is incomplete.
2. **If the count matches** and the file size is reasonable (rule of
   thumb: ≥ 25 KB for a full audit), the run succeeded. Print the
   absolute path to the new report to the user, plus a one-line summary
   like "51 components total: PREFERRED=22 ACCEPTABLE=8
   NEEDS_COORDINATION=3 FORBIDDEN=4 UNAPPROVED=2 NOT_USED=8
   INSUFFICIENT_INFO=4".
3. **Then delete the working directory**
   (`<project-root>/.tehik-it-profile-audit/` in its entirety, not just
   the `<run-id>/` subdir if no other run-ids exist) so the project tree
   stays clean. The fingerprint and provenance are already preserved
   inside the final report, so nothing of value is lost.
4. **If the count is short, or the report looks truncated, do not delete
   the working directory.** Tell the user exactly which component blocks
   are missing and where the workdir is, so they can re-run or hand-patch.
   The workdir is also kept on any subagent failure or abort.

The default is "delete on success." Keeping the workdir is the explicit
exception, only when something went wrong.

## Working directory

Intermediate artifacts (layers, fact sheet, findings) live in a per-run
working directory at `<project-root>/.tehik-it-profile-audit/<run-id>/`
while the audit runs:

```
<project-root>/.tehik-it-profile-audit/<run-id>/
  intel.md
  source-meta.json
  layers/
    layer-01-...md
    layer-01-...json
    ...
    manifest.json
  findings/
    layer-01.md
    ...
```

`<run-id>` is the audit timestamp (`YYYYMMDDTHHMMSSZ`). The directory is
**deleted on successful completion** (see Step 7) so the project tree is
not polluted with intermediate fragment files. It is preserved only when
the run fails verification, when a subagent aborts, or when the user
explicitly passes `--keep-workdir` for debugging.

If the user runs the skill repeatedly and the workdir is around from a
prior failed run, ask before deleting it — they may want to inspect the
old findings before the new run overwrites them.

## Partial runs

If the user asks for "just the application layer" or "layers 3 and 4", do
steps 1-3 as normal but only dispatch the requested layers in step 4. The
aggregate report still acknowledges the unaudited layers — list each as
"skipped at user request" rather than dropping them silently.

## Re-runs and resumability

If the working directory for a run already contains some
`findings/layer-NN.md` files, treat those layers as done and skip
dispatching subagents for them. Tell the user which layers you're
skipping. Pass `--refresh` semantics through: if the user wants a clean
re-run, ask whether to delete the existing working directory first rather
than mixing old and new findings.

## Failure modes to watch for

- **Upstream document changed structure** — `split_layers.py` returns 0
  layers or `manifest.json` looks malformed (e.g. layers with 0
  components, missing out_of_scope block). Stop, tell the user, and ask
  whether to proceed with whatever was parsed.
- **Subagent timeout / error** — record the layer as `INSUFFICIENT_INFO`
  with the error reason, do not retry silently.
- **No matrix entries apply to the project** (e.g. a tiny CLI tool with
  almost no stack — no DB, no frontend, no auth) — the report will be
  mostly `NOT_USED`. That is a valid outcome; just make it obvious in the
  executive summary.
- **The user runs the skill in a non-project directory** — refuse and ask
  for a project root. Auditing a directory of unrelated files is noise.

## Bundled assets

- `scripts/fetch_it_profile.py` — fetch + cache + fingerprint the upstream
  doc.
- `scripts/split_layers.py` — split the matrix into per-layer chunks +
  parse the choice cells, footnote markers, and out-of-scope blocks.
- `references/it-profile-source.md` — bundled snapshot of the IT Profile
  used as offline fallback. Re-bundling on plugin updates is fine; the
  fingerprint in the report will reveal if a stale snapshot was used.
- `references/subagent-brief.md` — per-layer subagent prompt template.
- `references/report-template.md` — final report skeleton.

## Sibling skill

The plugin (`tehik-standards-validation`) also ships `validate-tehik-nfr`
for the non-functional-requirements document. The two skills share the
same fan-out pattern (fetch → split → dispatch → aggregate → report) but
target different upstream documents and verdict taxonomies. When users
say "audit our project against TEHIK", clarify whether they mean NFRs,
the IT Profile, or both — they are independent audits.
