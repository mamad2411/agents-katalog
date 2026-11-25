---
name: critique
description: Formalist Devil's Advocate — find logical flaws, data leakage, circular reasoning, and fallacies in ideas, hypotheses, code, or papers
disable-model-invocation: false
argument-hint: "[input] [--profile=scan|review|audit|code] [--checks=group1,group2,...] [--output=path]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
model: sonnet
---

# Formalist Devil's Advocate — Orchestrator

A systematic critic that finds logical flaws, data leakage, circular reasoning, and other fallacies in ideas, hypotheses, code, or papers. Dispatches specialized subagents for each analysis group and merges results into a unified critique report.

## Parameters

- **$0** (required): Input to critique — file path (PDF/MD/py/ipynb), directory, `[[wikilink]]`, or inline quoted text
- **Options** (optional):
  - `--profile=scan|review|audit|code`: Analysis profile (default: auto-detect from input type)
  - `--checks=group1,group2,...`: Override which check groups to run (can use `+group` to add to profile)
  - `--output=path`: Custom output path for the report

## Profiles

Profiles are pre-bundled combinations of check groups:

| Profile | Groups Included | Use Case | Time |
|---------|----------------|----------|------|
| `scan` | deterministic | Fast sweep for code bugs, patterns, Benford, claims | 1-2 min |
| `review` | deterministic, logic, methodology, rhetoric, formal | Paper/proposal review (no code) | 7-10 min |
| `audit` | deterministic, logic, methodology, code-review, novelty, rhetoric, formal | Pre-submission deep dive | 18-25 min |
| `code` | deterministic, code-review, methodology | Code-focused review (no rhetoric/logic) | 5-8 min |

## Check Groups

| Group | What It Checks | Method | Subagent |
|-------|---------------|--------|----------|
| `deterministic` | AST checks, rhetoric patterns, Benford/roundness, claim extraction, lineage, split strategy, effect size formulas | Python scripts via Bash | None (orchestrator runs directly) |
| `logic` | Circular reasoning, unfalsifiable claims, hidden assumptions, confirmation bias, base-rate neglect | mcp__pal__thinkdeep (3-stage) | critique-logic (Opus) |
| `methodology` | Data leakage, ablation validity, statistical smell, cross-model validity, reference validity, effect size audit | mcp__pal__consensus (2-model) | critique-science (Sonnet) |
| `code-review` | Full codebase read, AI code review, cross-experiment lineage analysis | mcp__pal__codereview + manual | critique-code (Sonnet) |
| `novelty` | arXiv prior art search, Zotero citation verification | mcp__arxiv + mcp__zotero | critique-science (Sonnet, extended) |
| `rhetoric` | Hollow claims, claim escalation, number provenance, framing analysis | mcp__pal__chat | critique-rhetoric (Sonnet) |
| `formal` | Proof correctness, notation/symbol consistency, algorithm pseudocode, figure–text agreement, bibliography hygiene, checklist consistency | mcp__pal__thinkdeep (3-stage) | critique-formal (Opus) |

## Usage Examples

```bash
# Auto-detect profile from input type
/critique playground/1_critic/

# Fast deterministic-only scan
/critique paper.md --profile=scan

# Paper review (logic + methodology + rhetoric)
/critique 1-Project/2026-ScaleAwareHypoFinder/AIR-1-scale-detection-paper.md --profile=review

# Add novelty check to a review
/critique paper.md --profile=review --checks=+novelty

# Use specific groups only (no profile)
/critique paper.md --checks=deterministic,logic

# Full audit (everything)
/critique playground/1_critic/ --profile=audit

# Code-focused review with custom output
/critique playground/SLoD-SH2/ --profile=code --output=temp/code-critique.md
```

## Workflow

### Step 1: Parse & Validate Input

1. **Extract arguments:**
   - Parse `$0` as the input (everything before first `--` flag)
   - Parse `--profile=`, `--checks=`, `--output=` flags
   - Default profile: auto-detect (Step 2)
   - Legacy support: `--depth=quick` → `--profile=scan`, `--depth=standard` → auto-detect, `--depth=thorough` → `--profile=audit`
   - Legacy support: `--tier=all` → `--profile=audit`, `--tier=X,Y` → map to groups

2. **Resolve input:**
   - If starts with `[[` and ends with `]]`: strip brackets, use Glob `**/{name}.md` to find file
   - If a file path: verify it exists with Read
   - If a directory path: verify it exists with `ls`
   - If quoted text (no file found): treat as inline text, write to temp file
   - Error if nothing provided:
     ```
     Error: No input provided.
     Usage: /critique [input] [--profile=scan|review|audit|code] [--checks=group1,...] [--output=path]
     ```

3. **Read input content:**
   - For files: Read full content (for PDFs, the Read tool extracts text)
   - For directories: list all `.py`, `.ipynb` files recursively
   - For inline text: use as-is
   - Store: `input_content`, `input_path`, `input_title` (filename stem or first 60 chars)

### Step 2: Detect Input Type & Select Profile

If `--profile=` was specified, use that. If `--checks=` was specified without a profile, use exactly those groups. Otherwise, auto-detect:

**Smart auto-detection (apply in order):**

1. **Directory with Python files** → `code` profile
2. **`.py`, `.ipynb`, `.R`, `.jl` file** → `code` profile
3. **`.pdf` file** → `review` profile
4. **Markdown/text with `## Abstract`, `\section{`, `\begin{document}`** → `review` profile
5. **Short text (<500 words, no code)** → `scan` profile + `logic` group
6. **Markdown ≥500 words** → `review` profile
7. **Fallback** → `scan` profile

**Expand profile to groups:**

- `scan` → `[deterministic]`
- `review` → `[deterministic, logic, methodology, rhetoric, formal]`
- `audit` → `[deterministic, logic, methodology, code-review, novelty, rhetoric, formal]`
- `code` → `[deterministic, code-review, methodology]`

**Apply `--checks=` overrides:**

- If `--checks=+novelty,+code-review`: *add* those groups to the profile's groups
- If `--checks=no-formal,no-novelty`: *remove* those groups from the profile's groups
- If `--checks=+novelty,no-rhetoric`: combine — add `novelty`, remove `rhetoric`
- If `--checks=deterministic,logic` (no `+`/`no-` prefix on any token): use *exactly* those groups, ignoring the profile

**Validation:** A single `--checks=` argument must use either prefixed (`+group` / `no-group`) tokens for profile-relative overrides, or unprefixed tokens for an exact set — not both. If mixed, error with: "Use either `groupA,groupB` for an exact set, or `+groupA,no-groupB` for profile-relative overrides — not both."

No group name may begin with `+` or `no-` (none currently do).

**Display to user:**
```
Detected input type: directory with Python files
Profile: code
Groups enabled: deterministic, code-review, methodology
```

### Step 3: Prepare Staging Directory & Run Deterministic Checks

1. Create staging directory:
   ```bash
   mkdir -p temp/critique-{YYYYMMDD-HHMMSS}
   ```

2. **Run deterministic group** (always runs first, in the orchestrator — no subagent needed):

   For text/paper inputs:
   ```bash
   python3 tasks/bin/critic-checks/statistical_checks.py all "{input_path}"
   python3 tasks/bin/critic-checks/claim_extractor.py "{input_path}"
   python3 tasks/bin/critic-checks/rhetoric_patterns.py "{input_path}"
   ```

   For code/directory inputs:
   ```bash
   python3 tasks/bin/critic-checks/ast_checks.py {file1.py} {file2.py} ...
   python3 tasks/bin/critic-checks/lineage_checker.py {directory}
   ```

   Parse all JSON output and store results.

3. Write `context.md` to staging dir containing:
   ```markdown
   # Critique Context

   **Source:** {input_path or "inline text"}
   **Title:** {input_title}
   **Profile:** {profile}
   **Groups enabled:** {comma-separated list}

   ## Deterministic Results

   {inline JSON summaries from all scripts run in step 2}

   ## Code Files Found

   {For code-review group: list of .py files with priority labels}
   - P1 (core logic): src/*.py, *evaluate*.py, *split*.py, *train*.py, *feature*.py
   - P2 (pipeline): scripts/*.py, *.py in experiment root
   - P3 (utility): utils/*.py, helpers/*.py, config/*.py

   ## Input Content

   {input_content — truncated to 12000 chars if longer, with "[...truncated...]" marker}
   ```

4. For `scan` profile: **STOP HERE.** The deterministic results ARE the findings. Skip Step 4, go directly to Step 5 to write the report from deterministic output only.

### Step 4: Dispatch AI Subagents

Only spawn subagents for AI groups that are enabled. The `deterministic` group has already run in Step 3.

**Dispatch rules:**

| Enabled Group | Agent to Spawn | Notes |
|---------------|---------------|-------|
| `logic` | `critique-logic` (Opus) | Pass deterministic results via context.md |
| `methodology` | `critique-science` (Sonnet) | Pass deterministic results; set `novelty_enabled: false` |
| `methodology` + `novelty` | `critique-science` (Sonnet) | Pass deterministic results; set `novelty_enabled: true` |
| `novelty` alone | `critique-science` (Sonnet) | Skip methodology checks; set `novelty_only: true` |
| `code-review` | `critique-code` (Sonnet) | Pass code file list with priorities from context.md |
| `rhetoric` | `critique-rhetoric` (Sonnet) | Pass deterministic results via context.md |
| `formal` | `critique-formal` (Opus) | Pass deterministic results and prior findings via context.md |

**Spawn order:** logic → methodology/novelty → formal → code-review → rhetoric (skip groups not enabled). Formal runs after methodology so it can read `findings-methodology.md` for context (e.g., a flagged proof step) without re-flagging the same issue from a different angle.

**For each enabled AI group, spawn:**

```
Agent(critique-{agent}):
  "Analyze the input for {group description}.

   Staging directory: temp/critique-{timestamp}/
   Read context.md for the input text and deterministic results.
   {If prior findings exist: 'Also read findings-{prior-group}.md for context from previous analysis.'}
   {For methodology+novelty: 'Novelty checking is ENABLED — run arXiv search and Zotero cross-check.'}
   {For methodology only: 'Novelty checking is DISABLED — skip arXiv and Zotero steps.'}

   Write your findings to temp/critique-{timestamp}/findings-{group}.md
   using the standard finding format documented in your agent instructions.

   Input file path: {input_path}
   {For code-review: 'Analyze ALL code files listed in context.md, prioritizing P1 files.'}
  "
```

**After each agent completes:** Verify the findings file was written. If not, log a warning and continue.

### Step 5: Merge & Write Report

1. **Read all findings files:**
   ```
   Glob: temp/critique-{timestamp}/findings-*.md
   ```
   Read each file.

2. **For deterministic-only results (scan profile or deterministic group):**
   Convert the JSON output from scripts into finding format:
   - AST check findings → F-C{n} (code findings)
   - Statistical check warnings → F-S{n} (science findings)
   - Rhetoric pattern matches → F-R{n} (rhetoric findings)
   - Lineage overlaps → F-S{n} (science findings, severity from JSON)

3. **Parse AI findings:** Extract individual findings from each agent's output. Each finding has:
   - Type (from section header)
   - Severity (CRITICAL, MAJOR, MINOR, NOTE)
   - Location, Evidence, Explanation, Repair fields

4. **Assign finding IDs:**
   - Logic findings: F-L1, F-L2, ...
   - Science/methodology findings: F-S1, F-S2, ...
   - Code findings: F-C1, F-C2, ...
   - Rhetoric findings: F-R1, F-R2, ...
   - Formal findings: F-F1, F-F2, ...
   - Deterministic findings: F-D1, F-D2, ... (if no AI tier claimed them)

5. **Sort by severity:** CRITICAL → MAJOR → MINOR → NOTE

6. **Count findings** for frontmatter metadata.

7. **Generate executive summary:** Based on the findings:
   - If any CRITICAL: lead with the most important one
   - Assess overall quality: "The {type} has {N} critical issues that undermine {aspect}."
   - If no CRITICAL: "The {type} is generally sound, with {N} areas for improvement."

8. **Determine output path:**
   - If `--output=` was specified: use that path
   - If input is in `1-Project/X/`: write to `1-Project/X/Reviews/Critique-YYYY-MM-DD.md`
   - If input is in `3-Resource/Zotero/`: write alongside as `{stem}-critique.md`
   - If input is in `playground/`: write to `playground/Reviews/Critique-YYYY-MM-DD.md`
   - If input is in `2-Area/`: write to `2-Area/{subfolder}/Reviews/Critique-YYYY-MM-DD.md`
   - Fallback: `temp/Critique-YYYY-MM-DD-{input_title_slug}.md`
   - If file exists: append `-v2`, `-v3` etc.
   - Create parent directories if needed (`mkdir -p`)

9. **Write the report** using the format below.

### Step 6: Display Summary

Show a concise summary to the user:

```
Critique complete.

Source:   {input_title}
Report:   {output_path}
Profile:  {profile}
Groups:   {list}

Findings: {total} total
  {N} critical  {N} major  {N} minor  {N} note

Top concern: {one-sentence description of the most critical finding}

Open in Obsidian: [[{output_path_as_wikilink}]]
```

## Report Template

```markdown
---
type: critique
source: "[[{input_path}]]"
critique-date: {YYYY-MM-DD}
profile: {profile}
groups-run: [{group list}]
findings-total: {N}
findings-critical: {N}
findings-major: {N}
findings-minor: {N}
findings-note: {N}
tags: [critique, devils-advocate]
---

# Critique Report: {Input Title}

**Source:** [[{input_path}]]
**Date:** {YYYY-MM-DD} | **Profile:** {profile} | **Groups:** {group list}

## Executive Summary

{2-3 sentences: strongest concern, overall quality judgment, what should be addressed first}

## Critical Findings

{Findings with CRITICAL severity, each with:}
### F-{group}{N}: {Flaw Type}
**Location:** {section/line/quote reference}
**Evidence:** {specific evidence showing the flaw}
**Explanation:** {why this matters, 1-2 sentences}
**Repair:** {concrete, actionable fix}

## Major Findings

{Same format as above for MAJOR severity}

## Minor Findings

{Same format for MINOR severity}

## Notes

{Same format for NOTE severity — brief, one-paragraph each}

## Methodology

**Profile:** {profile}
**Groups executed:**
{For each group run:}
- **{Group name}** ({method}): {brief description of what was checked}

**Deterministic checks:**
{List all Python scripts run and key statistics from their output}

**Analysis time:** {approximate duration}
```

## Error Handling

| Error | Action |
|-------|--------|
| No input provided | Print usage and stop |
| File not found | "Error: File not found at '{path}'. Check path and try again." |
| Wikilink not resolved | "Error: Could not find note matching '[[{name}]]' in vault." |
| PDF unreadable | "Warning: Could not extract text from PDF. Trying with fewer pages..." Use Read with pages="1-10" |
| Subagent fails to write findings | "Warning: {group} analysis did not produce findings. Continuing with other groups." |
| No findings from any group | Write report with "No significant issues found" and NOTE-level observations |
| Output directory doesn't exist | Create with `mkdir -p` |
| Deterministic script fails | Log warning, continue with remaining scripts and AI groups |
