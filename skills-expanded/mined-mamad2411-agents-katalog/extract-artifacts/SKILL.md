---
name: extract-artifacts
version: 2.0.0
description: |
  Reads any Layer 1 source file (skill report, meeting note, news item, discussion, or
  document) and extracts structured Layer 2 cards into the artifact knowledge base.
  Deduplicates by canonical ID, merges additive fields, logs conflicts, and updates
  all Layer 3 indexes. Run after any skill that produces a source, or drop a raw input
  (meeting note, WhatsApp summary, news item) and run manually.

triggers:
  - extract artifacts
  - extract cards
  - process this source
  - ingest this meeting
  - ingest this paper review
  - update the knowledge base

input:
  - source_file_path: path to the Layer 1 source file (mutually exclusive with --dir)
  - --dir: path to a skill workspace directory; auto-discovers and processes all extractable files in dependency order
  - --dry-run: print what would be written without writing (optional)
  - --force: re-extract even if source is already marked extracted: true (optional)

output:
  - cards/paper-cards/ — new and updated paper cards (claims/evidence inline in card body)
  - cards/persons/ — new and updated person cards
  - cards/organizations/ — new and updated organization cards
  - cards/experiments/ — new and updated experiment cards (from experiment-report sources only)
  - indexes/ — paper-registry, person-index, organization-index, topic-map, experiment-registry updated
  - _conflicts.md — any conflicts appended for human review
  - source file — Extracted Cards section added, frontmatter marked extracted: true
  - extractions/{slug}_{date}/ — phase workspace with intermediate artifacts

note: claim-ledger.md is retired. Run /synthesize-hypotheses separately to update hypothesis-ledger.md after new paper cards are created.

allowed-tools:
  - Agent
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /extract-artifacts

Any Layer 1 source file → entity cards extracted → knowledge base updated → indexes current.

**Mode routing:** if `--dir` is provided, skip to [Directory Mode](#directory-mode---dir) and follow that section's loop — do not run the single-file Setup. Otherwise follow Setup → Phase 1–4 → Completion.

---

## Agent Spawn Convention

All agent definitions live in `agents/` alongside this SKILL.md.
Always `subagent_type="claude"`. Inject the agent definition and all required context into the prompt.

```
[Orchestrator]
Read: .claude/skills/extract-artifacts/agents/<agent-name>.md → AGENT_DEF

Agent(
  subagent_type="claude",
  description="<short description>",
  prompt="""
{AGENT_DEF}

---

## Context for this invocation

<task-specific variables and paths>
"""
)
```

---

## Setup

Read `config/workspace.json` → CONFIG.
```
OUTPUT_ROOT    = resolve(CONFIG.output_root)
ANALYTICS_PATH = CONFIG.analytics_folder + "/events.jsonl"
```

**Analytics — write start event** (append to ANALYTICS_PATH via `write_file` mode=append):
```
RUN_ID = "ea-{YYYYMMDD-HHMMSS}"
MODE   = "--dir" if dir mode else "single"
```
```json
{"ts":"{ISO_NOW}","run_id":"{RUN_ID}","event":"skill_start","skill":"extract-artifacts","version":"2.0.0","mode":"{MODE}","input_summary":"{source_path_or_dir}"}
```
If ANALYTICS_PATH does not exist yet, create it (empty file) before appending.

Resolve `source_path` to an absolute path. If the path does not exist, stop with:
```
Error: source file not found: {source_path}
```

Read `source_path` frontmatter only (first ~20 lines). Check:
- `source_type` present? If not → stop: "source_type missing from frontmatter. Add it and retry."
- `extracted: true` present? If yes and `--force` not set → stop: "Already extracted. Use --force to re-extract."

Set:
```
SOURCE_TYPE  = frontmatter.source_type
SOURCE_DATE  = frontmatter.source_date
CLAIM_CEILING = {
  skill-report      → observed,
  experiment-report → observed,
  document          → plausible,
  meeting-note      → speculative,
  discussion        → speculative,
  news-item         → speculative
}[SOURCE_TYPE]

SOURCE_SLUG = {first 4 significant words of filename, hyphens, lowercase}
WORKSPACE   = {OUTPUT_ROOT}/extractions/{SOURCE_SLUG}_{SOURCE_DATE}/
```

Create `WORKSPACE` directory. Write `state.json`:
```json
{
  "source_path": "...",
  "source_type": "...",
  "source_date": "...",
  "claim_ceiling": "...",
  "workspace": "...",
  "output_root": "...",
  "phase": "setup",
  "dry_run": false,
  "force": false
}
```

Print: `Source: {source_path} | Type: {SOURCE_TYPE} | Ceiling: {CLAIM_CEILING}`

---

## Directory Mode (`--dir`)

Use when pointing at a completed research or review workspace directory instead of a single source file. Processes all extractable files in the correct dependency order so that paper cards exist before claims reference them, and claim cards exist before evidence cards reference them.

### Step 1 — Detect workspace type

Read `config/workspace.json` → `OUTPUT_ROOT = resolve(config.output_root)`.

Resolve `{dir}` to an absolute path. Scan for marker files:

| Marker present | Detected type |
|----------------|---------------|
| `workspace_manifest.md` | `custom` — parse manifest's `processing_plan` |
| `01_claim_registry.md` | `paper-review` |
| `05_claim_evidence_ledger.md` or `05_evidence_ledger.md` | `deep-research` |

If no marker matches, stop:
```
Error: cannot detect workspace type in {dir}.
Add a workspace_manifest.md or point to a single file instead.
```

### Step 2 — Build processing plan

**paper-review** — process in this order:

| # | File | Role |
|---|------|------|
| 1 | `00_paper_content.md` | Paper metadata + cited papers |
| 2 | `01_claim_registry.md` | Structured claims |
| 3 | `04_final_review.md` | Synthesis + QML criteria verdicts |

**deep-research** — process in this order:

| # | File | Role |
|---|------|------|
| 1 | `01_literature_merged.md` | All surveyed papers |
| 2 | `05_claim_evidence_ledger.md` (fallback: `05_evidence_ledger.md`) | Claims + evidence items |
| 3 | `06_final_report.md` | Synthesis + conclusions |

**custom** — read the `processing_plan` list from `workspace_manifest.md` frontmatter (see format below).

Skip any file in the plan that does not exist on disk — print a warning and continue.

### Step 3 — Loop: run Phase 1–4 for each file

For each file in the plan:

1. Set:
   ```
   source_path    = {dir}/{file}
   SOURCE_TYPE    = skill-report          ← injected; do NOT read from file frontmatter
   SOURCE_DATE    = file frontmatter.source_date if present, else today's date
   CLAIM_CEILING  = observed
   SOURCE_SLUG    = {first 4 significant words of filename, hyphens, lowercase}
   WORKSPACE      = {OUTPUT_ROOT}/extractions/{SOURCE_SLUG}_{SOURCE_DATE}/
   ```
2. Skip the `source_type` and `extracted: true` frontmatter checks — workspace files are not expected to carry them.
3. Write `state.json` and print: `[{N}/{total}] {file} — Ceiling: observed`
4. Run Phase 1 → Phase 4 for this file, passing `SOURCE_TYPE = skill-report` as an explicit context variable to the source-classifier (not derived from file frontmatter).
5. After Phase 4 completes, record counts from `{WORKSPACE}/02_write_report.md` into a running total.
6. Print: `  → Created: {N}  Merged: {N}  Conflicts: {N}`

Carry `--dry-run` and `output_root` from the dir-mode invocation into every file's run. If `--dry-run`, skip Phase 4 for all files.

### Step 4 — Print combined summary

```
✓ /extract-artifacts --dir complete

Directory:  {dir}
Type:       {workspace_type}
Files:      {processed}/{total}  (skipped: {N})

Cards written (total):
  Created:   {N}
  Merged:    {N}
  Conflicts: {N}  →  {OUTPUT_ROOT}/_conflicts.md
  Skipped:   {N}

Indexes updated: paper-registry, person-index, organization-index, topic-map

Tip: run /synthesize-hypotheses to update hypothesis-ledger.md from the new paper cards.
```

If any conflicts: `⚠  {N} conflict(s) need human review → {OUTPUT_ROOT}/_conflicts.md`

---

### `workspace_manifest.md` format (custom workspaces)

```markdown
---
workspace_type: custom
source_date: {YYYY-MM-DD}
processing_plan:
  - file: 00_paper_content.md
    role: Paper metadata
  - file: 01_claim_registry.md
    role: Claims
  - file: 04_final_review.md
    role: Final synthesis
---
```

Place this file in the workspace directory. The `source_date` applies to all files unless a file's own frontmatter overrides it.

---

## Phase 1 — Source Classification

**Goal:** Parse the source file and extract all raw entities into a structured document.

**Agent:** `agents/source-classifier.md`

```
Read: .claude/skills/extract-artifacts/agents/source-classifier.md → AGENT_DEF

Agent(
  subagent_type="claude",
  description="Parse source file and extract all raw entities",
  prompt="""
{AGENT_DEF}

---

## Context for this invocation

source_path: {source_path}
source_type: {SOURCE_TYPE}
claim_status_ceiling: {CLAIM_CEILING}
workspace: {WORKSPACE}

Read the source file at source_path. Extract all entities per your protocol.
Write output to: {WORKSPACE}/00_source_parsed.md
"""
)
```

**Gate Phase 1 → Phase 2:**
- `{WORKSPACE}/00_source_parsed.md` exists and is non-empty ✓
- No validation errors reported in the parsed document ✓

Update `state.json`: `"phase": "phase-1-complete"`.

---

## Phase 2 — Entity Generation

**Goal:** Assign canonical IDs to all extracted entities and generate complete card bodies.

**Agent:** `agents/entity-extractor.md`

Read the card schemas to inject:
```
Read: artifacts/paper_card_schema.md        → PAPER_SCHEMA
Read: artifacts/person_card_schema.md       → PERSON_SCHEMA
Read: artifacts/organization_card_schema.md → ORG_SCHEMA
```

If `SOURCE_TYPE == experiment-report`, also read:
```
Read: artifacts/experiment_card_schema.md → EXPERIMENT_SCHEMA
```

Note: claim_card_schema and evidence_card_schema are retired. Claims and evidence are embedded inline in paper card bodies.

```
Read: .agents/skills/extract-artifacts/agents/entity-extractor.md → AGENT_DEF

Agent(
  subagent_type="claude",
  description="Generate canonical card content for all extracted entities",
  prompt="""
{AGENT_DEF}

---

## Context for this invocation

workspace: {WORKSPACE}
source_type: {SOURCE_TYPE}
claim_status_ceiling: {CLAIM_CEILING}
source_path: {source_path}
output_root: {OUTPUT_ROOT}

## Card Schemas (use these as the template for each card type)

### Paper Card Schema
{PAPER_SCHEMA}

### Person Card Schema
{PERSON_SCHEMA}

### Organization Card Schema
{ORG_SCHEMA}

### Experiment Card Schema (only if source_type is experiment-report)
{EXPERIMENT_SCHEMA}

Read: {WORKSPACE}/00_source_parsed.md
Generate canonical IDs and complete card bodies for paper, person, and organization entities (or,
if source_type is experiment-report, for the experiment entity) only.
Claims and evidence are embedded inline in the paper card body — do NOT create separate claim or evidence cards.
Write output to: {WORKSPACE}/01_entities.md
"""
)
```

**Gate Phase 2 → Phase 3:**
- `{WORKSPACE}/01_entities.md` exists ✓
- ID Assignment Log section present ✓

Update `state.json`: `"phase": "phase-2-complete"`.

---

## Phase 3 — Card Writing

**Goal:** Create new cards or merge into existing ones. Log conflicts.

**Agent:** `agents/card-writer.md`

```
Read: .claude/skills/extract-artifacts/agents/card-writer.md → AGENT_DEF

Agent(
  subagent_type="claude",
  description="Write or merge entity cards into the artifact repo",
  prompt="""
{AGENT_DEF}

---

## Context for this invocation

workspace: {WORKSPACE}
output_root: {OUTPUT_ROOT}
source_path: {source_path}
conflicts_path: {OUTPUT_ROOT}/_conflicts.md

Read: {WORKSPACE}/01_entities.md
For each entity: check {OUTPUT_ROOT}/cards/{type}/{id}.md, create or merge, log conflicts.
Write output to: {WORKSPACE}/02_write_report.md
"""
)
```

**Gate Phase 3 → Phase 4:**
- `{WORKSPACE}/02_write_report.md` exists ✓
- Summary counts present (created, merged, conflicts) ✓

If `--dry-run`: print the write report and stop. Do not proceed to Phase 4.

Update `state.json`: `"phase": "phase-3-complete"`.

---

## Phase 4 — Index Update

**Goal:** Update all four indexes to reflect new and updated cards. Mark source as extracted.

**Agent:** `agents/index-updater.md`

```
Read: .claude/skills/extract-artifacts/agents/index-updater.md → AGENT_DEF

Agent(
  subagent_type="claude",
  description="Update knowledge base indexes and mark source as extracted",
  prompt="""
{AGENT_DEF}

---

## Context for this invocation

workspace: {WORKSPACE}
output_root: {OUTPUT_ROOT}
source_path: {source_path}
source_date: {SOURCE_DATE}

Read: {WORKSPACE}/02_write_report.md
Update indexes in {OUTPUT_ROOT}/indexes/.
Append Extracted Cards section to {source_path}.
Mark {source_path} frontmatter: extracted: true, extracted_date: {today}.
"""
)
```

**Gate Phase 4 → Completion:**
- `paper-registry.md` updated (rows added/updated) ✓
- Source file has `## Extracted Cards` section ✓
- Source frontmatter has `extracted: true` ✓

Note: `claim-ledger.md` is retired — do not update it. Run `/synthesize-hypotheses` after extraction to update `hypothesis-ledger.md`.

---

## Completion

**Analytics — write end event** (append to ANALYTICS_PATH):
```json
{"ts":"{ISO_NOW}","run_id":"{RUN_ID}","event":"skill_end","skill":"extract-artifacts","version":"2.0.0","outcome":"success","duration_s":{elapsed},"output_path":"{WORKSPACE}"}
```

Read `{WORKSPACE}/02_write_report.md` for counts. Print:

```
✓ /extract-artifacts complete

Source:   {source_path}
Type:     {SOURCE_TYPE}
Ceiling:  {CLAIM_CEILING}

Cards written:
  Created:   {N}
  Merged:    {N}
  Conflicts: {N} — see {OUTPUT_ROOT}/_conflicts.md
  Skipped:   {N}

Indexes updated: paper-registry, person-index, organization-index, topic-map
Workspace: {WORKSPACE}

Tip: run /synthesize-hypotheses to update hypothesis-ledger.md from the new paper cards.
```

If any conflicts were logged, add:
```
⚠  {N} conflict(s) need human review → {OUTPUT_ROOT}/_conflicts.md
```

---

## Fast Mode (`--dry-run`)

Runs Phases 1–3 only. Prints the write report. Does not write any cards or update any indexes. Use to preview what would change before committing.

---

## Failure Modes to Avoid

```
❌ Reading source_type from frontmatter in --dir mode — SOURCE_TYPE is always injected as skill-report for workspace files
❌ Re-extracting an already-extracted source without --force — check extracted: true
❌ Skipping conflict logging — every disagreement must be recorded
❌ Letting index-updater run if card-writer reported zero cards — nothing to index
❌ Hardcoding output_root — always read from config/workspace.json
```
