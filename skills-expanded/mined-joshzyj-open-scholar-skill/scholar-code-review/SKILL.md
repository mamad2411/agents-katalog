---
name: scholar-code-review
description: >
  Systematic multi-agent code review of all analysis scripts produced in a project.
  6 specialized agents review for: (1) correctness & logic errors, (2) robustness & defensive coding,
  (3) statistical implementation fidelity, (4) reproducibility & replication readiness,
  (5) code style & AI-generated anti-patterns, (6) data handling & variable construction
  (miscoded categories, wrong recodes, mishandled missing values, sample restrictions).
  Produces a consolidated review report with severity-ranked issues, fix checklist, and a per-script scorecard.
  Run after /scholar-analyze, /scholar-compute, or /scholar-eda to catch coding errors before manuscript drafting.
tools: Read, Bash, Write, Glob, Grep, Agent
argument-hint: "[full|correctness|robustness|statistics|reproducibility|style|data-handling] [optional: script-dir-or-file] [optional: design-doc-path], e.g., 'full output/scripts/' or 'data-handling output/scripts/01-clean.R'"
user-invocable: true
---

# Scholar Code Review: Multi-Agent Analysis Script Auditor

You are a systematic code review engine that examines **all analysis scripts produced by AI in a research project**. You deploy 6 specialized review agents in parallel, each examining every script from a different angle. Your goal is to catch errors, fragile patterns, statistical misimplementations, data handling mistakes, reproducibility gaps, and AI-generated anti-patterns **before they propagate into published results**.

## ABSOLUTE RULES

1. **Never modify scripts** — this skill is read-only. It diagnoses but does not fix.
2. **Every issue must cite exact file, line number, and code snippet** — vague complaints are worthless.
3. **Severity levels are binding** — CRITICAL issues must be fixed before trusting results; WARNINGS are advisory.
4. **Zero tolerance for false positives** — if you cannot confirm an issue by reading the code, do not flag it. Better to miss a minor issue than cry wolf.
5. **All 6 agents run in parallel** — they receive the same script package and run simultaneously.
6. **Design documents are the ground truth** — if a methods section or design doc exists, the statistics and data-handling agents check code against it.
7. **Codebooks matter** — the data-handling agent checks variable recoding against any available codebook, data dictionary, or survey documentation.
8. **Objectivity Mandate (anti-sycophancy)** — every review-code-* agent dispatched by this skill inlines `_shared/objectivity-mandate.md`. Code review reports MUST NOT open with praise of the script's structure, soften logic bugs into "stylistic suggestions," or grade a script PASS when CRITICAL bugs exist. The consolidated scorecard MUST report the actual count of CRITICAL/WARNING/INFO findings — not a politeness-weighted summary. Default to skepticism: require evidence (the code itself) to clear an item, not to flag one. Disagreement with the script author or with a prior review round is required when the evidence demands it.
9. **Code-only review — agents never open data files.** Every verification runs against the codebook, data dictionary, or design document — never against the dataset itself. No review-code-* agent may Read, Grep, or Glob a data file (`.csv`, `.dta`, `.sav`, `.rds`, `.parquet`, `.xlsx`, etc.), including files marked `CLEARED` in the safety sidecar, and including data files referenced by name inside a reviewed script. When a recode, sample restriction, or missing-value scheme cannot be verified without seeing actual data values, the verdict is **UNVERIFIABLE** (flag for manual check) — not a data read. The codebook, data dictionary, design document, and the analysis scripts themselves are the only ground-truth inputs.

---

## Arguments

The user has provided: `$ARGUMENTS`

Parse:
- **Mode**: `full` (default) | `correctness` | `robustness` | `statistics` | `reproducibility` | `style` | `data-handling`
- **Script path**: directory or specific file(s) to review — auto-detect if not specified
- **Design doc path**: methods section or design document for statistics agent to compare against (optional)

---

## Dispatch Table

| Keywords in `$ARGUMENTS`               | Route to                                        |
|----------------------------------------|-------------------------------------------------|
| `full`, `all`, `review`               | → All 6 agents                                   |
| `correctness`, `logic`, `bugs`        | → Agent 1 only (correctness)                     |
| `robustness`, `defensive`, `fragile`  | → Agent 2 only (robustness)                      |
| `statistics`, `stats`, `methods`      | → Agent 3 only (statistical implementation)      |
| `reproducibility`, `replication`      | → Agent 4 only (reproducibility)                 |
| `style`, `quality`, `ai-patterns`     | → Agent 5 only (style & AI anti-patterns)        |
| `data-handling`, `variables`, `recode` | → Agent 6 only (data handling & variable construction) |
| `pre-execution`, `pre_execution_planned`, `planned` | → Planned-script mode (see below): agent set per caller (default all 6; pre-exec protocol callers name their subset) |
| (no mode keyword)                      | → All 6 agents                                   |

### Planned-Script (Pre-Execution) Mode

Reviews scripts that have **not yet executed** — dispatched by `scholar-auto-research` Phase 6 (`review_engine.mode: pre_execution_planned`, all 6 roles), orchestrated fast-3 callers, and the standalone pre-execution protocol (`_shared/pre-execution-review.md` §3, per-skill subsets + phase tags). Semantics on top of the normal workflow:

- **Never execute anything.** No output-existence cross-referencing (Step 0a items 4–5 read manuscripts/results only if they already exist; planned scripts have produced nothing yet — their absence is not a finding).
- **Bugs found here are cheap** — the whole point is catching missing clustering / wrong SE / NA-as-0 / tautological outcomes BEFORE execution at scale.
- **Role-name crosswalk** (scholar-auto-research's contract uses its own labels): `statistical` → `review-code-statistics`, `style_ai_patterns` → `review-code-style`, `data_handling` → `review-code-data-handling`; `correctness`/`robustness`/`reproducibility` map 1:1.
- The reviewed-script manifest (Step 0c) and dispatch recording (Step 1) are REQUIRED in this mode — `pre-exec-review-check.sh` hash-binds execution to them.


---

## ABSOLUTE RULE — NEVER Fabricate Citations

> **ZERO TOLERANCE FOR CITATION FABRICATION.** Any reference cited in review reports, remediation recommendations, or code comments produced by this skill MUST be verified against Tier 0 (knowledge graph), Tier 1 (local library: Zotero/Mendeley/BibTeX/EndNote), or Tier 2 (CrossRef / Semantic Scholar / OpenAlex). Unverified references MUST be flagged `[CITATION NEEDED: describe required evidence]`. NEVER invent author names, titles, years, volumes, pages, or DOIs; NEVER cite packages or methods papers from Claude's training data without verifying they exist in the declared form.

Load the full verification protocol on first use:

```bash
cat "${SCHOLAR_SKILL_DIR:-.}/.claude/skills/_shared/citation-verification-protocol.md"
```

---

## Step 0: Setup & Script Discovery

### 0a. Locate Scripts

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
mkdir -p "${OUTPUT_ROOT}/code-review" "${OUTPUT_ROOT}/logs"
```

1. **User-specified path**: If user provided a script directory or file, use that.
2. **Auto-detect**: If not specified, search for all analysis scripts in the project:

```
Glob: output/scripts/*.R
Glob: output/scripts/*.py
Glob: output/scripts/*.do
Glob: output/scripts/*.jl
Glob: output/eda/*.R
Glob: output/eda/*.py
Glob: *.R (project root — but exclude renv/, packrat/, .Rproj.user/)
Glob: *.py (project root — but exclude venv/, .venv/, __pycache__/)
```

If no scripts found, halt with error: "No analysis scripts found. Specify a path or run /scholar-analyze first."

3. **Locate codebooks and data dictionaries** (for data-handling agent):
```
Glob: output/data/*.md
Glob: output/data/*codebook*
Glob: output/data/*dictionary*
Glob: *codebook* (project root)
Glob: *data-dictionary* (project root)
```

4. **Locate design documents** (for statistics and data-handling agents):
```
Glob: output/drafts/draft-methods-*.md → most recent
Glob: output/drafts/draft-design-*.md → most recent
Glob: output/design/*.md
```

4. **Locate manuscript** (for cross-referencing):
```
Glob: output/manuscript/full-paper-*.md → most recent
Glob: output/drafts/draft-results-*.md → most recent
```

### 0a-safety. Restricted-Data Advisory Scan (Tier B+)

This is a **code-only** review (ABSOLUTE RULE 9): the agents read scripts, codebooks, data dictionaries, and design docs — never the dataset itself. After 0a has located the scripts, this scan reads **only those scripts** (code is always safe) to surface any data files they reference that are marked restricted in the safety sidecar, so the orchestrator can list them as DO-NOT-OPEN in the review package (0d).

It never reads a data file, never uses `grep -r` (so it cannot recurse into `data/` or `materials/`), and never halts the review — a project under `LOCAL_MODE`/`HALTED`/`NEEDS_REVIEW` is still reviewable at the code level, which is the whole point. The PreToolUse hook (`scripts/gates/pretooluse-data-guard.sh`) remains the mechanical backstop if any agent attempts a data Read anyway.

```bash
# ── Step 0a-safety: restricted-data advisory (code-only; never reads data) ──
# Re-derive SCRIPT_PATHS IN THIS BLOCK — shell state does not persist across
# Bash calls. Scan ONLY those script files (explicit list, never `grep -r`).
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
SCRIPT_PATHS="${SCRIPT_DIR:-}"   # orchestrator may export SCRIPT_DIR for a custom path
if [ -z "$SCRIPT_PATHS" ]; then
  SCRIPT_PATHS="$(find "${OUTPUT_ROOT}/scripts" "${OUTPUT_ROOT}/eda" . -maxdepth 1 -type f \
        \( -name '*.R' -o -name '*.py' -o -name '*.do' -o -name '*.jl' \) 2>/dev/null \
        | grep -vE '/(renv|packrat|\.Rproj\.user|venv|\.venv|__pycache__)/' | sort -u)"
fi
if [ -z "$SCRIPT_PATHS" ]; then
  echo "0a-safety: no analysis scripts located yet (advisory only) — proceeding." >&2
else
  SIDECAR=".claude/safety-status.json"
  if [ -f "$SIDECAR" ] && command -v jq >/dev/null 2>&1; then
    # Extract data-file path literals from the SCRIPTS only — both quote styles.
    REFS=$( { grep -hoE '"[^"]*\.(csv|tsv|dta|sav|rds|rdata|parquet|feather|xlsx|xls|h5|hdf5|arrow|orc|pkl|pickle)"' $SCRIPT_PATHS 2>/dev/null | tr -d '"';
              grep -hoE "'[^']*\.(csv|tsv|dta|sav|rds|rdata|parquet|feather|xlsx|xls|h5|hdf5|arrow|orc|pkl|pickle)'" $SCRIPT_PATHS 2>/dev/null | tr -d "'"; } | sort -u )
    RESTRICTED=""
    for F in $REFS; do
      [ -e "$F" ] || continue
      ABS=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$F" 2>/dev/null || echo "$F")
      STATUS=$(jq -r --arg k "$ABS" '(.[$k] // empty)|tostring' "$SIDECAR")
      [ -z "$STATUS" ] && STATUS=$(jq -r --arg k "$F" '(.[$k] // empty)|tostring' "$SIDECAR")
      case "$STATUS" in
        NEEDS_REVIEW*|HALTED|LOCAL_MODE) RESTRICTED="${RESTRICTED}
  - $F → $STATUS" ;;
      esac
    done
    if [ -n "$RESTRICTED" ]; then
      cat >&2 <<ADVISORY
ℹ️  0a-safety advisory — reviewed scripts reference restricted data file(s):
$RESTRICTED
These are CODE-REVIEWED ONLY. Per ABSOLUTE RULE 9, no agent opens them.
List them under "RESTRICTED DATA FILES — DO NOT OPEN" in the review package (0d).
ADVISORY
    else
      echo "✓ 0a-safety: no restricted data files referenced by scripts."
    fi
  fi
fi
```

Limitation: the literal scan catches quoted single-file paths (`read_csv("data/x.csv")`); multi-arg path builders (`here::here("data","x.dta")`) and variable-built paths will not appear. That is acceptable — this scan is an advisory courtesy; ABSOLUTE RULE 9 plus the PreToolUse hook are the actual enforcement.

### 0b. Read All Scripts

Read every discovered script in full. For each script, record:
- File path
- Language (R / Python / Stata / Julia)
- Line count
- What it produces (tables, figures, data files — infer from write/save/ggsave calls)
- Packages/libraries loaded

### 0c. Build Script Inventory

```
SCRIPT INVENTORY
=================
| # | Script | Language | Lines | Packages | Produces |
|---|--------|----------|-------|----------|----------|
| 1 | output/scripts/01-clean.R | R | 142 | tidyverse, haven | clean_data.csv |
| 2 | output/scripts/02-models.R | R | 230 | fixest, modelsummary | table2.html, table3.html |
| 3 | output/scripts/03-figures.R | R | 185 | ggplot2, patchwork | figure1.pdf, figure2.pdf |
...
```

### 0c.5. Compute the Reviewed-Script Manifest (hash binding)

Generate a `review_id` (`cr-$(date +%Y%m%d)-<short-slug>`) and compute a SHA-256 per discovered script (`shasum -a 256` / `sha256sum`). These become the **reviewed-scripts manifest** — the machine-readable record of exactly which bytes this review adjudicated:

```json
{"schema": "code-review-manifest/v1",
 "review_id": "cr-YYYYMMDD-<slug>",
 "report": "code-review/code-review-report-YYYY-MM-DD.md",
 "mode": "<dispatch mode>", "phase_tag": "<caller's phase tag or 'standalone'>", "ts": "ISO-8601",
 "scripts": [{"path": "scripts/04-main-models.R", "sha256": "<hex64>"}],
 "out_of_scope": [{"path": "...", "reason": "..."}],
 "supersedes_review_id": null, "fixed_finding_ids": [], "remaining_blocking_count": 0}
```

Saved in Step 5 as `${PROJ}/code-review/reviewed-scripts-<review_id>.json`; the same `review_id` appears verbatim in the consolidated report header (`Review ID: <id>`). `scripts/gates/pre-exec-review-check.sh` recomputes these hashes before any reviewed script executes — a script edited after review fails the gate until re-reviewed (Step 6). Scripts deliberately excluded from adjudication (e.g., already-executed EDA context) go in `out_of_scope[]` with a reason.

### 0d. Build Review Package

Assemble the **CODE REVIEW PACKAGE** that all agents receive:

```
CODE REVIEW PACKAGE
====================

SCRIPT INVENTORY:
[the inventory table from 0c]

SCRIPT CONTENTS:
[For each script: file path + full source code with line numbers]

DESIGN DOCUMENT (if found):
[Full text of methods/design section — ground truth for statistics and data-handling agents]

CODEBOOK / DATA DICTIONARY (if found):
[Variable definitions, coding schemes, missing value codes — ground truth for data-handling agent]

MANUSCRIPT EXCERPT (if found):
[Results section — for cross-referencing what the code claims to produce]

RESTRICTED DATA FILES — DO NOT OPEN:
[Every data file the scripts reference (from 0a-safety), regardless of sidecar
 status. This review is CODE-ONLY (ABSOLUTE RULE 9): agents verify recodes and
 sample restrictions against the codebook/dictionary/design doc, never by Reading,
 Grep-ing, or Glob-ing these files. If a check requires the data values, the
 verdict is UNVERIFIABLE (flag for manual review) — not a data read.]

PROJECT CONTEXT:
- Target journal: [if known from manuscript or user context]
- Identification strategy: [if known from design doc]
- Key variables: [outcome, predictors, controls — if known]
```

### 0e. Process Logging (REQUIRED) — Reasoning · Action · Observation trace

This skill emits an append-only RAO trace at `${OUTPUT_ROOT}/logs/trace-scholar-code-review-<date>.ndjson` — the source of truth. The human-readable `process-log-scholar-code-review-<date>.md` is *rendered* from it. Full protocol + privacy rule: `_shared/process-logger.md`.

At each meaningful step (a decision, a script/tool run, a gate call, a subagent dispatch), append one record. `emit-trace.sh` derives `seq` from the file, so no state is tracked across the stateless Bash blocks:

```bash
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/emit-trace.sh" --skill scholar-code-review --step "<label>" \
  --reasoning "<the WHY — stated rationale, 1–2 lines>" \
  --action "<the WHAT — tool/script/gate call + key args>" \
  --observation "<the RESULT — verdict/metric/count/error/file ref>" --status ok    # ok|fail|skipped
```

At the end (Save Output), render the human-readable log and self-check:

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/render-trace.sh" "${OUTPUT_ROOT}/logs/trace-scholar-code-review-$(date +%Y-%m-%d).ndjson"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/trace-coverage-check.sh" "${OUTPUT_ROOT}" --skill scholar-code-review
```

Privacy (C-01 / LOCAL_MODE): the trace carries aggregate metrics, verdicts, counts, and file refs ONLY — never raw data rows, verbatim quotes, or PII.

---

## Step 1: Launch Review Agents

Based on the dispatch mode, launch the appropriate agents **in parallel** using the Agent tool. Each agent receives the full CODE REVIEW PACKAGE.

Read each agent profile before spawning:

```bash
cat .claude/agents/review-code-correctness.md
cat .claude/agents/review-code-robustness.md
cat .claude/agents/review-code-statistics.md
cat .claude/agents/review-code-reproducibility.md
cat .claude/agents/review-code-style.md
cat .claude/agents/review-code-data-handling.md
```

### Agent 1 — Correctness & Logic (`review-code-correctness`)
- Role: Catch errors that silently produce wrong results
- Focus: Data manipulation bugs, wrong function usage, variable reference errors, missing data handling, non-finite value (NaN/Inf) propagation, logical flow errors
- Spawn with: CODE REVIEW PACKAGE

### Agent 2 — Robustness & Defensive Coding (`review-code-robustness`)
- Role: Find fragile patterns that may break under different conditions
- Focus: Hardcoded assumptions, silent failure patterns, data boundary issues, reproducibility fragility, output integrity
- Spawn with: CODE REVIEW PACKAGE

### Agent 3 — Statistical Implementation (`review-code-statistics`)
- Role: Verify code implements the intended statistical design
- Focus: Model specification vs. design, SE specification, causal inference implementation, hypothesis testing, effect sizes, reporting standards
- Spawn with: CODE REVIEW PACKAGE (design document is critical input for this agent)

### Agent 4 — Reproducibility & Replication (`review-code-reproducibility`)
- Role: Evaluate whether scripts form a complete, portable, reproducible pipeline
- Focus: Pipeline completeness, dependency management, path portability, environment specification, documentation
- Spawn with: CODE REVIEW PACKAGE

### Agent 5 — Style & AI Anti-Patterns (`review-code-style`)
- Role: Catch AI-generated code smells and quality issues
- Focus: Hallucinated arguments/functions, deprecated APIs, DRY violations, dead code, naming, readability
- Spawn with: CODE REVIEW PACKAGE

### Agent 6 — Data Handling & Variable Construction (`review-code-data-handling`)
- Role: Verify variable recoding, categorization, missing value handling, and sample construction against codebooks and design documents
- Focus: Miscoded categories, wrong value mappings, reversed scales, unhandled missing value codes (GSS/PSID/NHANES sentinel values), non-finite values (Inf/NaN) surviving NA handling, incomplete case_when, sample restriction mismatches, factor level ordering, derived variable errors (age, income, indices)
- Spawn with: CODE REVIEW PACKAGE (codebook/data dictionary is critical input for this agent)
- **Variable Construction Completeness Check**: For every variable referenced in analysis scripts (used in subsetting, grouping, decomposition, or modeling), verify it was actually created in a data preparation script. Cross-reference against the data blueprint's variable dictionary. Flag any variable that is referenced but never constructed (e.g., `cohort_gen` used in decomposition but never defined).
- **Directional Coding Audit**: For every survey item that is recoded or reversed, verify: (1) the code comment correctly describes the original variable's coding, (2) the transformation produces the intended direction (higher = conservative or liberal as specified), (3) the comment does not confuse the variable's meaning with a related concept (e.g., "approve of the ruling banning X" vs. "approve of X"). Flag any item where the comment contradicts the codebook or where the recode direction appears wrong.

**All selected agents MUST be launched simultaneously** (parallel Agent tool calls in a single message) — and **separately**: one Agent tool-use block per reviewer, each returning its own `task_invocation_id`. One combined "review everything" dispatch violates the independent-reviewers contract and is RED-failed by `code-review-coverage-check.sh` (shared-agentId detection).

**Record each dispatch (REQUIRED):** after the Agent calls return, append one row per reviewer to the dispatch manifest so coverage is mechanically verifiable (standalone runs included):

```bash
_b="$HOME/.claude/scholar-skill-bootstrap.sh"; [ -f "$_b" ] || _b="${SCHOLAR_SKILL_DIR:-.}/scripts/scholar-skill-bootstrap.sh"; [ -f "$_b" ] && . "$_b"; unset _b
. "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/derive-proj.sh" 2>/dev/null || PROJ="${OUTPUT_ROOT:-output}"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/emit-task-dispatch.sh" --proj "$PROJ" \
  --subagent review-code-<dimension> --purpose "code review (<mode>)" \
  --phase "<caller's phase tag; standalone default: standalone-code-review>" \
  --agentId <id-from-the-Agent-tool-result>
# rc=2 (no manuscript found → null SHA) is acceptable for pre-manuscript projects; the row is still appended.
```

---

## Step 2: Collect Agent Reports

Collect the complete report from each agent. Each report follows the agent's specified output format with its own severity classifications and issue IDs.

Store all individual reports for inclusion in the final output.

---

## Step 3: Synthesize Consolidated Report

Combine all agent findings into a single **CONSOLIDATED CODE REVIEW REPORT**.

### 3a. Triage and Deduplicate

1. **Merge all issues** from all agents into a single list
2. **Deduplicate**: If multiple agents flag the same issue (e.g., Agent 1 flags wrong merge AND Agent 2 flags same merge as fragile), merge into one entry citing both agents
3. **Mark cross-agent agreement**: Issues flagged by 2+ agents get a **★★** marker (highest confidence)
4. **Organize by script**: Group issues by script file, then by severity within each script

### 3b. Severity Classification

| Severity | Definition | Action |
|----------|-----------|--------|
| **CRITICAL** | Produces or may produce wrong results; blocks reproduction; statistical misimplementation | MUST fix before trusting any results |
| **WARNING** | Fragile pattern, missing diagnostic, suboptimal practice | SHOULD fix before submission |
| **INFO** | Style improvement, minor readability issue | MAY fix |

### 3c. Build Fix Checklist

Generate actionable fix instructions for every CRITICAL and WARNING issue:

```
FIX CHECKLIST
=============

CRITICAL FIXES (must resolve before trusting results):

□ [CRIT-001] output/scripts/02-models.R, line 45
  - Agent(s): correctness ★★ statistics
  - Problem: Left join silently drops 234 observations; model N doesn't match design
  - Fix: Change to inner_join() and add N assertion, OR document exclusion in methods
  - Affects: Table 2, Table 3

□ [CRIT-002] output/scripts/02-models.R, line 78
  - Agent(s): statistics
  - Problem: Standard errors clustered at individual level but design specifies state-level clustering
  - Fix: Change vcov = ~state_fips in feols() call
  - Affects: All p-values in Table 2

WARNINGS (should resolve before submission):

□ [WARN-001] output/scripts/03-figures.R, line 12
  - Agent(s): robustness
  - Problem: No set.seed() before bootstrap CI computation
  - Fix: Add set.seed(12345) before bootstrap block

□ [WARN-002] output/scripts/01-clean.R, line 30
  - Agent(s): style
  - Problem: Hallucinated argument: haven::read_dta(encoding = "UTF-8") — no such argument
  - Fix: Remove encoding argument (haven auto-detects)
```

### 3d. Per-Script Scorecard

```
PER-SCRIPT SCORECARD
=====================

| Script | Lines | Critical | Warning | Info | Agents Flagging | Grade |
|--------|-------|----------|---------|------|-----------------|-------|
| 01-clean.R | 142 | 0 | 2 | 1 | style, robustness | B |
| 02-models.R | 230 | 3 | 1 | 0 | correctness, statistics, robustness | D |
| 03-figures.R | 185 | 0 | 1 | 3 | robustness, style | A |
| 04-robustness.R | 95 | 1 | 0 | 0 | statistics | C |
```

Grade rules:
- **A**: 0 CRITICAL, ≤1 WARNING
- **B**: 0 CRITICAL, 2-3 WARNINGS
- **C**: 1 CRITICAL or >3 WARNINGS
- **D**: 2-3 CRITICAL
- **F**: >3 CRITICAL

### 3e. Overall Review Scorecard

```
OVERALL CODE REVIEW SCORECARD
═══════════════════════════════

| Dimension               | Agent                     | Issues | Critical | Warnings | Score      |
|-------------------------|---------------------------|--------|----------|----------|-----------|
| Correctness & Logic     | review-code-correctness   | [N]    | [N]      | [N]      | [PASS/FAIL] |
| Robustness              | review-code-robustness    | [N]    | [N]      | [N]      | [PASS/FAIL] |
| Statistical Fidelity    | review-code-statistics    | [N]    | [N]      | [N]      | [PASS/FAIL] |
| Reproducibility         | review-code-reproducibility| [N]   | [N]      | [N]      | [PASS/FAIL] |
| Style & AI Patterns     | review-code-style         | [N]    | [N]      | [N]      | [PASS/FAIL] |
| Data Handling           | review-code-data-handling | [N]    | [N]      | [N]      | [PASS/FAIL] |

OVERALL
| Total Issues | Critical | Warnings | ★★ Cross-Agent | Overall Grade |
|-------------|----------|----------|----------------|---------------|
| [N]         | [N]      | [N]      | [N]            | [A-F]         |

VERDICT: [CLEAN — READY TO USE / FIXES NEEDED / MAJOR ISSUES — DO NOT TRUST RESULTS]
```

Verdict rules:
- **CLEAN — READY TO USE**: 0 CRITICAL issues, ≤5 WARNINGS total
- **FIXES NEEDED**: 1-5 CRITICAL issues OR >5 WARNINGS
- **MAJOR ISSUES — DO NOT TRUST RESULTS**: >5 CRITICAL issues OR any ★★ CRITICAL issue

---

## Step 4: Present Results to User

Display to the user:

1. **Script Inventory** (what was reviewed)
2. **Overall Review Scorecard** (headline result)
3. **Fix Checklist** (actionable items, CRITICAL first)
4. **★★ Cross-Agent Agreement items** (highest-confidence findings)
5. **Per-Script Scorecard** (which scripts need the most work)
6. **Top 3 most impactful issues** with full context

Then: **save the report + manifest unconditionally (Step 5 — mandatory, not an option)**, and ask:

> "CRITICAL findings need fixing before these results can be trusted. Default path: I apply the fixes, then **re-review is required** (Step 6 — the affected reviewer agents re-adjudicate the fixed scripts; fixes are never self-certified). Proceed with fix-then-re-review, or do you want to handle the fixes yourself first?"

Never present "fix the issues" without the re-review half — an unreviewed fix is the author-validates-own-fix pattern this skill exists to prevent.

---

## Step 5: Save Output

### Version Collision Avoidance (MANDATORY)

Follow the protocol defined in `.claude/skills/_shared/version-check.md`. Shell variables do NOT persist between Bash tool calls — re-derive `$BASE` in every new Bash call.

**Before EVERY Write tool call below**, run this Bash block to determine the correct save path. Do NOT hardcode paths from the filename templates — they show naming patterns only.

```bash
# MANDATORY: Run before every Write tool call
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
# BASE pattern: ${OUTPUT_ROOT}/code-review/code-review-report-$(date +%Y-%m-%d)
OUTDIR="$(dirname "${OUTPUT_ROOT}/code-review/code-review-report-$(date +%Y-%m-%d)")"
STEM="$(basename "${OUTPUT_ROOT}/code-review/code-review-report-$(date +%Y-%m-%d)")"
mkdir -p "$OUTDIR"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/version-check.sh" "$OUTDIR" "$STEM"


```

**Use the printed `SAVE_PATH` as `file_path` in the Write tool call.** Re-run this block (with the appropriate BASE) for each additional file. The same version suffix must be used for all related output files.

### 5a. Save Consolidated Report

Write the consolidated report containing:
1. Script Inventory
2. Overall Review Scorecard
3. Fix Checklist (CRITICAL + WARNING)
4. ★★ Cross-Agent Agreement section
5. Per-Script Scorecard
6. Agent 1 Detail: Correctness full report
7. Agent 2 Detail: Robustness full report
8. Agent 3 Detail: Statistical Implementation full report
9. Agent 4 Detail: Reproducibility full report (including pipeline map and dependency audit)
10. Agent 5 Detail: Style & AI Anti-Patterns full report
11. Agent 6 Detail: Data Handling & Variable Construction full report (including variable lineage map and missing value audit)

### 5a.5. Save the Reviewed-Script Manifest (REQUIRED)

Write the Step 0c.5 manifest to `${PROJ}/code-review/reviewed-scripts-<review_id>.json`, and confirm the consolidated report header carries the matching `Review ID: <review_id>` line. Without this pair, `pre-exec-review-check.sh` (and any orchestrator consumer) treats the scripts as unreviewed.

### 5b. Save Fix Checklist Separately

Save just the fix checklist to `${OUTPUT_ROOT}/code-review/fix-checklist-$(date +%Y-%m-%d).md`.

### 5c. Close Process Log

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
SKILL_NAME="scholar-code-review"
LOG_DATE=$(date +%Y-%m-%d)
LOG_FILE="${OUTPUT_ROOT}/logs/process-log-${SKILL_NAME}-${LOG_DATE}.md"
if [ ! -f "$LOG_FILE" ]; then
  LOG_FILE=$(ls -t "${OUTPUT_ROOT}"/logs/process-log-${SKILL_NAME}-${LOG_DATE}*.md 2>/dev/null | head -1)
fi
cat >> "$LOG_FILE" << LOGFOOTER

## Output Files
- Consolidated report: ${OUTPUT_ROOT}/code-review/code-review-report-${LOG_DATE}.md
- Fix checklist: ${OUTPUT_ROOT}/code-review/fix-checklist-${LOG_DATE}.md

## Summary
- **Steps completed**: 5/5
- **Scripts reviewed**: [N]
- **Total issues**: [N]
- **Critical issues**: [N]
- **Warnings**: [N]
- **★★ cross-agent issues**: [N]
- **Overall grade**: [A-F]
- **Verdict**: [CLEAN/FIXES NEEDED/MAJOR ISSUES]
- **Time finished**: $(date +%H:%M:%S)
LOGFOOTER
```

---

## Step 6: Post-Fix Re-Review (MANDATORY whenever findings are fixed)

Fixes to reviewed scripts — applied by the user, the main context, or the fix loop (`_shared/code-review-fix-loop.md`) — are **never self-certified**. Before the fixed scripts' results are trusted (and before they execute, under the pre-execution protocol):

1. **Re-dispatch the affected reviewers**: every agent whose findings were fixed re-reviews the UPDATED scripts (scoped to the fixed findings + any code the fix touched). Same dispatch rules as Step 1 (separate parallel Agent calls, recorded via `emit-task-dispatch.sh`).
2. **Log every fix** to `${PROJ}/logs/code-review-fixes-[date].md` (fix-loop row format). Report + fix log are MANDATORY artifacts once any fix is applied — not optional saves.
3. **Emit a superseding report + manifest**: new `review_id`; manifest sets `supersedes_review_id` (the prior review's id), `fixed_finding_ids`, `remaining_blocking_count`, and hashes the **fixed bytes**. The report header notes `Supersedes: <prior report filename>`.
4. **Iterate at most twice**: if blocking findings survive 2 fix→re-review cycles, escalate to the user (`${PROJ}/logs/code-review-escalation-[date].md`) — the classification was wrong (should have been ESCALATE) or the fix introduced a new defect.

Enforcement: wherever a gate consumer runs — `pre-exec-review-check.sh` before execution, the scholar-auto-research Phase 6 verifier under orchestration — the supersedes chain, hashes, and verdict are verified mechanically; a stale clean report over edited scripts fails. In a bare advisory session with no subsequent execution, this step is binding on the model like every other step in this file.

---

## Quality Checklist (Self-Audit Before Completion)

Before presenting results, verify:

- [ ] Every CRITICAL issue has exact file path, line number, and code snippet
- [ ] No false positives: each issue confirmed by reading the actual code
- [ ] Deduplication complete: no issue appears twice in the consolidated report
- [ ] ★★ markers applied to all issues flagged by 2+ agents
- [ ] Fix checklist entries are actionable (what to change, where, exact fix)
- [ ] Per-script grades follow the grading rules
- [ ] Verdict follows the rules in Step 3e
- [ ] If a design document was found, the statistics agent compared code against it
- [ ] Code-only discipline held: no agent Read/Grep/Glob'd a data file; unverifiable recodes flagged UNVERIFIABLE, not resolved by reading data
- [ ] Reviewed-scripts manifest saved (`code-review/reviewed-scripts-<review_id>.json`) and `Review ID:` present in the report header
- [ ] Every reviewer dispatch recorded in `logs/dispatch-manifest.jsonl` (one row per agent, distinct agentIds)
- [ ] If any finding was fixed: Step 6 re-review ran, superseding report+manifest emitted, fixes logged
- [ ] Process log is complete with all steps recorded

---

## Integration with Other Skills

| Skill | Integration Point | Mode | Gate? |
|-------|-------------------|------|-------|
| **scholar-analyze** | Sub-stage A2.5 pre-execution review (model-ladder scripts drafted, reviewed, THEN executed); remaining 3 agents post-save recommendation | `pre-execution` fast 3 | Yes — `pre-exec-review-check.sh` blocks execution |
| **scholar-eda** | Phase 11 handoff review (E-scripts before the pre-analysis memo hands off) | `pre-execution` correctness + data-handling | Yes — `pre-exec-review-check.sh` |
| **scholar-compute** | MODULE 0.7 pre-scale review (pipeline consolidated to scripts before at-scale run) | `pre-execution` fast 3 | Yes — `pre-exec-review-check.sh` blocks scale execution |
| **scholar-data** | W4/W6/W7 authored transformation/collection code (cleaning, scrapers, linkage) | `pre-execution` correctness + data-handling | Yes — `pre-exec-review-check.sh` |
| **scholar-simulate** | Generated downstream analysis scripts (aggregation, AME, ABM, sensitivity) | `pre-execution` statistics + correctness | Yes — `pre-exec-review-check.sh` |
| **scholar-ling** | Model-fitting L-scripts drafted, reviewed, then executed | `pre-execution` fast 3 | Yes — `pre-exec-review-check.sh` |
| **scholar-brainstorm** | DATA mode Step 4b.ii.5 (own equivalent gate + artifact schema; documented divergence) | 3 role reviews | Yes — its own severity gate |
| **scholar-respond** | R&R new-analysis path (`rr-NN-*.R` drafted, reviewed via this skill, then executed) | fast 3 | Yes — CRITICAL halts |
| **scholar-auto-research** | Phase 6 pre-execution review contract (`review_engine.mode: pre_execution_planned`, all 6 roles — see Planned-Script Mode crosswalk) | `pre_execution_planned` | Yes — vendored verifier |
| **scholar-replication** | Verification checklist (consumes existing report; recommends running if none exists) | reads report | Checklist item |
| **scholar-verify** | Complementary: scholar-verify checks output consistency; scholar-code-review checks code correctness | — | Independent |

Standalone protocol reference for the six pre-execution rows: `_shared/pre-execution-review.md` (state sequence, pilot definition, phase tags, receipt row).

---

## References

See `references/code-review-standards.md` for common error catalogs, AI code anti-pattern taxonomy, and journal-specific computational reproducibility requirements.
