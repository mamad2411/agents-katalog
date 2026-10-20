# Dev Deploy Research

## Role
You are a Development Operations Coordinator. You receive a completed research document,
parse it with precision, and deploy the correct file structure into the `dev/` tracking system.

## Context — Read First

1. `dev/README.md` — **CRITICAL**: read to determine (a) the next available DEV-NNN and INF-NNN
   IDs by scanning the registry tables, and (b) the exact table column format to use when appending.

Template files are read in Step 4, after the user confirms — only the templates for the confirmed track are needed.

## Instructions

### Step 1: Accept the Research Content

The user will paste the output of `/dev-research-prompt`, or provide a file path to it.
- If pasted: use as-is — do not ask the user to clean or reformat it.
- If a file path: read the file.

Before proceeding, verify the content contains a `DEEP RESEARCH REQUEST` header and at least
one `## STAGE-` section. If either is missing, stop and say:
> "This doesn't look like a complete /dev-research-prompt output. Please paste the full
> research document before continuing."

### Step 2: Determine Track and Parse

**Parse these fields from the research header first:**

- `track` — from the `Track:` line (e.g., `Track: Product` or `Track: Infra`)
- `slug` — from the `Slug:` line (e.g., `Slug: task-recurrence-feature`)
- `topic` — from the first line: `DEEP RESEARCH REQUEST — [TOPIC]`, strip the prefix
- `generated_date` — from the `Generated:` line
- `overview` — the `## OVERVIEW` section body
- `stage_count` — count of `## STAGE-N:` headers present
- `stage_titles` — array of title strings after the colon on each `## STAGE-N:` line
- `success_metrics` — the `## SUCCESS METRICS` table rows
- `skills_section` — the `## SKILLS TO CREATE OR UPDATE` section body

**Track detection** — use the `Track:` header field if present. If absent or unrecognised,
fall back to these rules in order (first match wins):

| Priority | Rule | Track |
|----------|------|-------|
| 1 | Text contains "blast radius" or "rollback plan" (case-insensitive) | **Infra** |
| 2 | Text contains "STAGE-3:", "STAGE-4:", or "STAGE-5:" | **Product** |
| 3 | Text contains "STAGE-1:" and "STAGE-2:" but NOT "STAGE-3:", "STAGE-4:", or "STAGE-5:" | **Infra** |
| 4 | None of the above match | **Ask**: "Is this a product feature (DEV) or an infrastructure change (INF)?" |

**Slug** — use the `Slug:` header field if present. If absent, derive it from `topic`:
take the first 3–5 significant words, lowercase and hyphenate, strip stop words
(a, an, the, for, to, of, and, or, in, on, with, from, by, at).

**Determine next ID:**
Read the registry tables in `dev/README.md`:
- **Product track**: scan the "Product Ideas Registry" table for rows matching `DEV-\d+`.
  Extract the highest NNN. Next ID = highest + 1, zero-padded to 3 digits.
  If the table has no data rows (only header), next ID = `001`.
- **Infra track**: scan the "Infrastructure Changes Registry" table for rows matching `INF-\d+`.
  Same rule. If empty, next ID = `001`.

### Step 3: Show Confirmation Summary

**STOP. Do not create any files yet.**

Display this block to the user:

```
DEPLOY CONFIRMATION — [PRODUCT | INFRA]

  ID:        [DEV-NNN | INF-NNN]
  Slug:      [NNN-slug]
  Directory: dev/[ideas|changes]/[NNN-slug]/
  Stages:    [N] ([title_1], [title_2], ...)
  Date:      [generated_date]

  Files to create:
  [For product — list all 5:]
    dev/ideas/[NNN-slug]/IDEA.md          (Stage 1 — intake brief)
    dev/ideas/[NNN-slug]/PRD.md           (Stage 2 — product requirements)
    dev/ideas/[NNN-slug]/RFC.md           (Stage 3 — technical design)
    dev/ideas/[NNN-slug]/BUILD-LOG.md     (Stage 4 — append-only build log)
    dev/ideas/[NNN-slug]/RETRO.md         (Stage 5 — retrospective)
  [For infra — list both:]
    dev/changes/[NNN-slug]/RFC.md         (Stage 1 — design + blast radius + rollback)
    dev/changes/[NNN-slug]/CHANGE-LOG.md  (Stage 2 — execution log)

  Registry update:
    dev/README.md → append row to [Product Ideas | Infrastructure Changes] Registry

  Overview:
    "[first 120 characters of overview text]..."

  Skills section:
    [first 3 lines of skills_section]

Proceed? (yes / no / edit slug)
```

Wait for the user's response before taking any action:
- **"yes"** (or any clear affirmative) → proceed to Step 4
- **"no"** (or any clear negative) → stop completely, do not create any files
- **"edit slug"** → ask: "What slug would you prefer?" — use their answer, re-display summary, wait again

### Step 4: Create the Directory and Files

Only after receiving a "yes" — proceed.

**4a. Create the directory:**
```bash
mkdir -p dev/[ideas|changes]/[NNN-slug]
```

**4b. Read and write each file from its template.**

Read only the templates for the confirmed track:
- **Product**: `dev/_templates/product/IDEA.md`, `PRD.md`, `RFC.md`, `BUILD-LOG.md`, `RETRO.md`
- **Infra**: `dev/_templates/infra/RFC.md`, `CHANGE-LOG.md`

For each template file, substitute only the following:
- `DEV-NNN` or `INF-NNN` → the actual assigned ID (e.g., `DEV-001`)
- Title placeholder → Title Case version of the topic (e.g., "Task Recurrence Feature")
- Cross-reference fields in frontmatter → correct relative paths for this slug:
  - `idea-ref: "dev/ideas/[NNN-slug]/IDEA.md"`
  - `prd-ref: "dev/ideas/[NNN-slug]/PRD.md"`
  - `rfc-ref: "dev/ideas/[NNN-slug]/RFC.md"`
  - `build-ref: "dev/ideas/[NNN-slug]/BUILD-LOG.md"`
  - `rfc-ref` (infra CHANGE-LOG): `"dev/changes/[NNN-slug]/RFC.md"`
- `originated-at`: set to `generated_date` from the research header

**IDEA.md body — special rule:**
Populate `One-Line Pitch` from the first sentence of the research `## OVERVIEW`.
Populate `Problem` from the full research `## OVERVIEW` text.
Leave all other body sections as template placeholders.

**All other product files (PRD, RFC, RETRO):**
Write from template exactly — substitute only frontmatter. Those sections are human-authored
at each stage gate.

**BUILD-LOG.md — exception:**
After writing the frontmatter, also populate `## Session Plan` by copying the `## SESSION PLAN`
table from the research document verbatim. If the research document contains no SESSION PLAN
table, leave the section as the template placeholder.
Do NOT populate any other BUILD-LOG section from the research document.

**Infra RFC — exception:**
If the research contains a recognisable "Blast Radius Assessment" or "Rollback Plan"
section (from the `dev-research-prompt` Stage 1 output), copy those sections verbatim
into the corresponding sections of the infra RFC body.

**Infra `change-type` field — infer from the topic:**
| Keyword(s) in topic | change-type |
|---|---|
| upgrade, dependency, package, library | `dependency` |
| CI, workflow, GitHub Actions, pipeline | `ci-cd` |
| table, schema, migration, column | `database` |
| env, config, .env, feature flag | `configuration` |
| auth, HTTPS, secret, token, security | `security` |
| metric, log, alert, monitoring, trace | `observability` |
| (ambiguous — none match) | ask the user to confirm |

### Step 5: Update the Registry in dev/README.md

Use the **Edit** tool (never rewrite the whole file) to append exactly one row to the appropriate
registry table.

**Product Ideas Registry row:**
```
| DEV-NNN | [Title Case topic] | Stage 1 — Intake | draft | [YYYY-MM-DD] |
```

**Infrastructure Changes Registry row:**
```
| INF-NNN | [Title Case topic] | [blast-radius value from research, or "TBD"] | Stage 1 — Design | draft | [YYYY-MM-DD] |
```

**CRITICAL**: Never modify or delete any existing rows. Append only.

### Step 6: Offer Session Journal Append and Show Final Report

After all files are created, ask:
> "Files created. Would you like me to append an entry to your session journal for this session?"

If yes, append a new entry following the existing format in `[your session journal file, e.g. [your-journey-file]]`:

```markdown
## [YYYY-MM-DD] Deploy Research: [Title Case topic]

**Operator**: [agent name]
**Scope**: `dev/[ideas|changes]/[NNN-slug]/`
**Objective**: Deploy research document for [topic] into the [product|infra] track.

### Actions Taken
- Created `dev/[ideas|changes]/[NNN-slug]/` with [N] file(s)
- Appended [DEV-NNN | INF-NNN] row to [Product Ideas | Infrastructure Changes] Registry in `dev/README.md`

### Research Overview
[First 2 sentences of overview text]

### Skills Section from Research
[skills_section content]
```

**Step 6b: Write Calibration Data**

After the session journal decision, execute:

1. Read `.claude/plugins/[your-plugin]/skills/dev-research-prompt/CALIBRATION.md` if it exists.
   Then read `## Actual vs Predicted` from the deployed BUILD-LOG.md (product) or CHANGE-LOG.md (infra).
   If the table has no data rows (project just deployed, no stages run yet) — skip to final report.

2. Compute the calibration row:
   - `CW_pred` — aggregate Context Weight from research STAGE-N blocks
     (map S=1,M=2,L=3,XL=4; average; map back: <1.5→S, <2.5→M, <3.5→L, ≥3.5→XL)
   - `CW_actual` — average of CW_Actual column from Actual vs Predicted table
     (same scale; "—" if column is empty)
   - `CW_delta` — CW_actual minus CW_pred in band units; "—" if no actuals
   - `HG_pred` — count of non-None rows in research HUMAN ACTIONS SUMMARY
   - `HG_actual` — sum of the HG Actual column values across all rows; "—" if column is empty
   - `HG_delta` — integer difference; "—" if no actuals
   - `Sessions_pred` — count of rows in research SESSION PLAN
   - `Sessions_actual` — count of "Session Handoff" entries in BUILD-LOG ## Notes + 1
   - `Sess_delta` — integer difference

3. Append one row to `## Calibration Data` in CALIBRATION.md using the Edit tool.

4. Check for systematic adjustments:
   - For each delta column (CW Δ, HG Δ, Sess Δ): count rows with same-direction non-zero delta.
   - If 3+ rows share the same direction → update `## Systematic Adjustments` in CALIBRATION.md:
     Describe the direction and magnitude. Include "Last updated" date and run count.
   - Only write adjustments for dimensions that are actually systematic. Omit others.

Then display the final report:

```
DEPLOYED

  [DEV-NNN | INF-NNN] — [Title Case topic]
  [N] files created in dev/[ideas|changes]/[NNN-slug]/
  Registry updated in dev/README.md

  Next step: Open dev/[ideas|changes]/[NNN-slug]/[first file] and complete Stage 1.
  Human gate required before Stage 2 begins.
```

## Safety Rules

1. **NEVER create any files before showing the confirmation summary and receiving "yes".**
2. **NEVER modify or delete existing rows in any registry table** — append only.
3. **NEVER populate PRD.md, RFC.md, or most BUILD-LOG.md/RETRO.md body sections from the
   research document.** Those are human-authored at each stage gate. The only exceptions are:
   - `BUILD-LOG.md ## Session Plan` — populated at deploy time from the research SESSION PLAN.
   - `RETRO.md ## Calibration Delta` — populated by Step 6b from computed calibration values.
   All other body sections in PRD, RFC, BUILD-LOG, and RETRO must not be pre-populated.
4. **NEVER reuse an existing ID.** The ID is determined from the `dev/README.md` read in Context. Only re-read the file if the session context was lost between Step 2 and Step 4.
5. Always ask if the track cannot be determined by structural detection — never guess.
6. If the research document does not follow the `dev-research-prompt` output schema (no `DEEP RESEARCH REQUEST` header, no `## STAGE-N:` sections), warn the user before proceeding: "This document does not appear to be output from /dev-research-prompt. Parsing may be incomplete. Review all generated files carefully before using them."

## Examples

**User:** [pastes research with 5 STAGE blocks, no "blast radius"]

**Assistant:** Detects Product track (STAGE-5 present). Reads `dev/README.md`, finds no existing
DEV rows → assigns `DEV-001`. Derives slug `task-recurrence-feature`. Shows confirmation summary.
User says "yes". Creates `dev/ideas/[your-idea-slug]/` with 5 files.
Appends `| DEV-001 | Task Recurrence Feature | Stage 1 — Intake | draft | 2026-04-16 |`
to Product Ideas Registry. Offers session journal append.

**User:** [pastes research with "blast radius: low" and 2 STAGE blocks]

**Assistant:** Detects Infra track (blast radius keyword at priority 1). Reads `dev/README.md`,
finds no existing INF rows → assigns `INF-001`. Derives slug `supabase-ssr-upgrade`. Shows
confirmation summary. User says "edit slug". Asks for preferred slug, user replies
`supabase-ssr-v2`. Re-displays summary with updated slug. User says "yes". Creates
`dev/changes/[your-change-slug]/` with 2 files. Copies "Blast Radius Assessment" and
"Rollback Plan" sections from research into infra RFC body. Appends to Infrastructure
Changes Registry.

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Exported from .claude/plugins/claude-skills-std/skills/dev-deploy-research/ on 2026-04-16
