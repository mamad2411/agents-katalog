---
name: validate-tehik-nfr
description: "Validate a software project against TEHIK's non-functional requirements (NFRs). Use this skill whenever the user asks to audit, check, verify or validate a project against TEHIK NFRs, TEHIK standards, mittefunktsionaalsed nõuded, or the TEHIK quality requirements document — even when phrased casually like 'are we TEHIK-compliant?', 'check if this passes TEHIK', 'NFR audit', 'run a TEHIK standards check', or 'how badly are we violating the TEHIK rules?'. Also trigger when the user references the TEHIK-EE/mitte-funktsionaalsed-nouded GitHub repository, asks about specific NFR section topics in a TEHIK context (logging, monitoring, source code, deployment package), or wants a Markdown report describing per-requirement compliance status. The skill fans out across parallel subagents (one per NFR section) so context stays manageable, and writes a per-requirement Markdown report at the project root."
---

# Validate TEHIK NFRs

Audit a software project against the TEHIK non-functional requirements
document and produce a Markdown report with per-requirement verdicts.

The upstream standards document lives at:
**https://raw.githubusercontent.com/TEHIK-EE/mitte-funktsionaalsed-nouded/refs/heads/main/mittefunktsionaalsed-nouded.en.md**

It is one large Markdown table of ~140 requirements grouped into 12 sections.
Trying to evaluate the whole thing in one context window is a context-rot
disaster, so this skill fans the work out: one subagent per section, run in
parallel, each handed only its own slice of the document plus a pre-flight
fact sheet about the project.

## When this applies

- The user wants an end-to-end NFR audit of the current project (or a
  specific path they pass in).
- The user asks for a partial audit of one or more sections (e.g. "just
  audit the logging NFRs", "section 7 only").
- The user has produced earlier audits and wants a re-run after fixes.

## When NOT to use

- The user is asking *what* the TEHIK NFRs are, not whether their project
  meets them — answer from the document directly without invoking this
  skill's full pipeline.
- The user wants to enforce these rules at commit/CI time. That is a
  different problem (a linter / CI step), not an LLM audit. Tell them so.
- The project is empty or nearly empty (no source files). Say so and refuse
  to produce a report; the report would be all `INSUFFICIENT_INFO` rows and
  would mislead.

## Section 1 is intentionally out of scope

Section 1 ("Compliance with general standards") references many external
documents — X-Road, OWASP ASVS, WCAG 2.2, IT Profile of the Ministry of
Social Affairs, e-Government CFR, RIA cryptographic guidance, EMTAK
classification, ADS address service, Veera design system, RFC 5322, etc.
Verifying those compliances requires dedicated tooling, third-party security
testing, manual review, or paid services that a static repository audit
cannot perform.

The skill therefore **must not** attempt to verify section 1. Instead:

- Skip section 1 in the dispatch step (no subagent is spawned for it).
- Surface every section 1 NFR in the final report under an explicit
  "out of scope — verify out-of-band" block, with the linked external
  standards listed.

This is non-negotiable — silently dropping section 1 would mislead the
reader into thinking those requirements were checked.

## Pipeline overview

```
[1] Pre-flight project intel  →  short fact sheet
[2] Fetch NFR document         →  cached file + provenance JSON
[3] Split into 12 sections     →  per-section .md + .json + manifest.json
[4] Determine application type →  self-service / websites / cots / unknown
[5] Dispatch subagents         →  one per audited section (sections 2-12),
                                  in parallel, each gets only its slice
[6] Aggregate findings         →  read each section's findings file
[7] Write final Markdown report→  tehik-nfr-audit-YYYY-MM-DD.md in project root
```

Each step is detailed below.

## Step 1: Pre-flight project intel

Before fetching anything, do a short read-only scan of the project root and
produce a fact sheet. The goal is to give every subagent a shared baseline
so 11 of them don't independently rediscover the same things. Spend at most
a few tool calls — this is a fact sheet, not an audit.

Capture, where present:

- **Languages** detected (file extensions, primary one first).
- **Build tool / package manifest** (`pom.xml`, `build.gradle(.kts)`,
  `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
- **Frameworks** evident from manifests (Spring Boot, NestJS, Django,
  Angular, React, Vue, etc.).
- **Database access** (JPA/Hibernate, Flyway/Liquibase migrations directory,
  Prisma schema, Alembic, raw SQL).
- **Logging library** if obvious (logback config, log4j, winston, structlog).
- **CI presence** (`.gitlab-ci.yml`, `.github/workflows/`, `Jenkinsfile`).
- **Container / deployment** (`Dockerfile`, `docker-compose.yml`, helm
  charts, k8s manifests).
- **Test directories** and the test runner used.
- **Repository hint about app type** (presence of UI source, public-facing
  web routes, API-only signals).

Format the fact sheet as ~10-30 lines of bullet points. Save it to the
audit's working directory so each subagent prompt can embed it verbatim.

## Step 2: Fetch the NFR document

Run the bundled fetch script. It tries live → cached → bundled snapshot in
that order, computes a sha256, and emits provenance metadata.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/validate-tehik-nfr/scripts/fetch_nfrs.py"
```

Capture the JSON output — its `path`, `url`, `source`, `sha256`,
`fetched_at`, and `fallback_reason` fields all flow into the final report.

Pass `--refresh` if the user explicitly asks for a fresh download. Pass
`--offline` if they say they're disconnected.

## Step 3: Split the document

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/validate-tehik-nfr/scripts/split_sections.py" \
  "<path-from-step-2>" \
  --out "<workdir>/sections" \
  --source-meta "<path-to-stored-step-2-json>"
```

This produces `section-NN-<slug>.md` and `section-NN-<slug>.json` for each
of the 12 sections, plus `manifest.json`. Inspect `manifest.json` to confirm
12 sections were parsed; if a different number comes back the upstream
document changed structure — surface a warning to the user and proceed with
whatever sections were found.

## Step 4: Determine application type

The NFR table tags each requirement with applicability across three
application types (`Self-service`, `Websites`, `COTS product`). Filtering by
the right type lets subagents skip obviously irrelevant rows.

1. Inspect the project intel from step 1 and propose one of:
   - `self_service` — backend service, business application, API serving
     authenticated users.
   - `websites` — public-facing web/marketing site, public portal.
   - `cots` — commercial off-the-shelf product being integrated.
   - `unknown` — cannot tell from source; audits *all* applicable rows.
2. Confirm with the user before dispatching subagents (use
   AskUserQuestion). Lead with your best guess as the recommended option;
   they can override or pick `unknown` to be exhaustive.

If the user starts with `--app-type=<value>` or pre-states their choice,
skip the confirmation prompt.

## Step 5: Dispatch subagents

For sections 2 through 12 (NOT section 1):

1. Read `references/subagent-brief.md`.
2. Replace every `{{...}}` placeholder using the per-section data from
   `manifest.json` and the project intel. Resolve `{{COMMON_RULES_PATH}}`
   to the absolute path of
   `${CLAUDE_PLUGIN_ROOT}/references/auditor-common.md` so the subagent
   receives a concrete path it can `Read`.
3. Spawn one Agent in the same message per section, all in parallel.
   Use `subagent_type: tehik-standards-validation:nfr-section-auditor` —
   the agent is pinned to Sonnet and locked to read-only tools (Read,
   Grep, Glob, Bash), so do not override the subagent type unless the
   user explicitly asks for a different model or wider tool access.
   Each subagent must write its findings to
   `<workdir>/findings/section-NN.md` so a partial run can be resumed
   later.
4. Wait for all subagents to return.

Why parallel: each subagent runs in its own context window, so the
orchestrator never sees more than one section's worth of NFRs at a time
plus short summaries. This is the entire reason for the fan-out — do not
fall back to sequential or single-shot execution unless the user explicitly
asks for it.

If a subagent fails (Agent tool returns an error or no findings file), do
NOT silently continue. Report which section failed in the report under
"Section findings" with the error and a verdict of `INSUFFICIENT_INFO` for
all of that section's NFRs, so the gap is visible.

## Step 6: Aggregate findings

1. Read every `findings/section-NN.md` produced by the subagents.
2. Tally verdict counts (PASS / FAIL / PARTIAL / NOT_APPLICABLE /
   INSUFFICIENT_INFO) across all audited sections.
3. Build the section-1-out-of-scope block from the section 1 JSON: list
   each section 1 NFR with its requirement text and the URL(s) extracted
   from its explanation column (so the user has a checklist).
4. Roll up critical issues: every FAIL verdict, in section order.
5. Roll up unknowns: every INSUFFICIENT_INFO verdict, in section order.
6. Build a recommendations list: pull recommendations from FAIL/PARTIAL
   findings, deduplicate near-identical ones, group by section.

## Step 7: Write the report — must be SELF-CONTAINED

This is the part that goes wrong if you take shortcuts. Read it carefully.

Use `references/report-template.md` as the skeleton. Fill placeholders;
write the resulting Markdown to `<project-root>/tehik-nfr-audit-YYYY-MM-DD.md`.

If a report file with that exact name already exists, append a `-N` suffix
rather than overwriting (the user may want to compare runs).

### The report MUST inline every audited NFR

The final report is the only artifact a reader will open. Treat it as the
single source of truth for the audit. That means:

- For every audited NFR (sections 2-12), the report must contain its full
  structured block — the H3/H4 heading, the requirement summary, the
  status line, the confidence line, the evidence bullets with concrete
  `file:line` references, and the recommendation when non-PASS. Copy the
  block from the subagent's `findings/section-NN.md` verbatim; do not
  paraphrase it into a one-paragraph section summary.
- Section-level narrative summaries (the "this section had X PASSes, the
  highlights are Y and Z" paragraphs) are nice on top of the per-NFR list,
  not in place of it. If you only emit the narrative summary you have
  produced a half report.
- The report must NOT contain any reference like "Detailed evidence:
  `.tehik-nfr-audit/.../findings/section-NN.md`" or "see fragment file X".
  The reader must be able to read the audit end-to-end without opening
  another file. If you find yourself wanting to write such a reference,
  inline the contents instead.

Concrete shape per audited NFR (matches what the subagent wrote):

```
### NFR 4.6 — Log entries must be in JSON format
- **Status:** PARTIAL
- **Confidence:** HIGH
- **Evidence:**
  - `src/main/resources/logback-spring.xml:14` configures plain pattern layout
  - `pom.xml:78` includes `logstash-logback-encoder` but it is not wired up
- **Recommendation:** Switch the appender to `LogstashEncoder` to emit JSON
```

Section 1 stays its own dedicated "out of scope" block with each
requirement's external URL(s) — the same level of inlining (no fragment
file references).

### Step 8: Verify the report is complete, then clean up

Before declaring success or deleting any working artifacts:

1. **Count NFR blocks in the report.** Count headings shaped like
   `### NFR <section>.<n>` (or `#### NFR <section>.<n>` — whichever you
   used consistently). The total must equal the count of NFRs you set out
   to audit (sections 2-12 plus the 19 in section 1 listed under
   out-of-scope). If the count is short, the report is incomplete.
2. **If the count matches** and the file size is reasonable (rule of
   thumb: ≥ 30 KB for a full audit; the SKAIS reference report is ~120
   KB), the run succeeded. Print the absolute path to the new report to
   the user, plus a one-line summary like "164 NFRs total, audited 145
   (skipped 19 in section 1): PASS=82 FAIL=12 PARTIAL=21 NOT_APPLICABLE=18
   INSUFFICIENT_INFO=12".
3. **Then delete the working directory** (`<project-root>/.tehik-nfr-audit/`
   in its entirety, not just the `<run-id>/` subdir if no other run-ids
   exist) so the project tree stays clean. The fingerprint and provenance
   are already preserved inside the final report, so nothing of value is
   lost.
4. **If the count is short, or the report looks truncated, do not delete
   the working directory.** Tell the user exactly which NFR blocks are
   missing and where the workdir is, so they can re-run or hand-patch.
   The workdir is also kept on any subagent failure or abort.

The default is "delete on success." Keeping the workdir is the explicit
exception, only when something went wrong.

## Working directory

Intermediate artifacts (sections, fact sheet, findings) live in a per-run
working directory at `<project-root>/.tehik-nfr-audit/<run-id>/` while the
audit runs:

```
<project-root>/.tehik-nfr-audit/<run-id>/
  intel.md
  source-meta.json
  sections/
    section-01-...md
    section-01-...json
    ...
    manifest.json
  findings/
    section-02.md
    ...
```

`<run-id>` is the audit timestamp (`YYYYMMDDTHHMMSSZ`). The directory is
**deleted on successful completion** (see Step 8) so the project tree is
not polluted with intermediate fragment files. It is preserved only when
the run fails verification, when a subagent aborts, or when the user
explicitly passes `--keep-workdir` for debugging.

If the user runs the skill repeatedly and the workdir is around from a
prior failed run, ask before deleting it — they may want to inspect the
old findings before the new run overwrites them.

## Partial runs

If the user asks for "just section 4" or "sections 4 and 7", do steps 1-4
as normal but only dispatch the requested sections in step 5. The aggregate
report still acknowledges the unaudited sections — list each as "skipped at
user request" rather than dropping them silently.

## Re-runs and resumability

If the working directory for a run already contains some `findings/section-NN.md`
files, treat those sections as done and skip dispatching subagents for them.
Tell the user which sections you're skipping. Pass `--refresh` semantics
through: if the user wants a clean re-run, ask whether to delete the existing
working directory first rather than mixing old and new findings.

## Failure modes to watch for

- **Upstream document changed structure** — `split_sections.py` returns
  fewer than 12 sections or `manifest.json` looks malformed. Stop, tell the
  user, and ask whether to proceed with whatever was parsed.
- **Subagent timeout / error** — record the section as
  `INSUFFICIENT_INFO` with the error reason, do not retry silently.
- **No NFRs apply to the project** (e.g. user picked `cots` and all section
  rows lack a `V` for that column) — the report will be mostly
  `NOT_APPLICABLE`. That's a valid outcome; just make it obvious in the
  executive summary.
- **The user runs the skill in a non-project directory** — refuse and ask
  for a project root. Auditing a directory of unrelated files is noise.

## Bundled assets

- `scripts/fetch_nfrs.py` — fetch + cache + fingerprint the upstream doc.
- `scripts/split_sections.py` — split the doc into per-section chunks +
  parse applicability metadata.
- `references/nfr-source.md` — bundled snapshot of the NFR document used
  as offline fallback. Re-bundling on plugin updates is fine; the
  fingerprint in the report will reveal if a stale snapshot was used.
- `references/subagent-brief.md` — per-section subagent prompt template.
- `references/report-template.md` — final report skeleton.

## Future skills in this plugin

The plugin (`tehik-standards-validation`) is intentionally named at a
broader level than this skill. Sibling skills validating other TEHIK
standards documents (e.g. development guidelines, security baselines) will
follow the same fan-out pattern — fetch, split, dispatch subagents,
aggregate, report. When adding a new sibling skill, mirror this directory
shape (`scripts/`, `references/`) and reuse the report-template structure.
