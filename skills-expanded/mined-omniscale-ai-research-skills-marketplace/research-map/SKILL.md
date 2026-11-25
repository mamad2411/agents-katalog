---
name: research-map
description: Generate or update a structured research map for a project with experiment graphs, findings, and narrative arc
argument-hint: "<project-path> [--depth=quick|standard|deep] [--focus=area]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Research Map Skill

Generate a structured, navigable research map for any research project. Inspired by codemaps (Cognition.ai) and DeepWiki-style navigation. The output is a single `research-map.md` with a deep heading hierarchy designed for sidebar navigation when converted to HTML via `/md-to-html --style=report`.

**Design principle:** The heading structure (h2/h3) IS the navigation. Each h2 becomes a sidebar section, each h3 becomes a subsection. The `/md-to-html --style=report` template auto-generates a sticky sidebar TOC from these headings.

**Update model:** First run generates the full map. Subsequent runs detect what changed in the project and incrementally update affected sections while preserving manual edits.

## Input

- **$0** (required): Path to project root directory
- **--depth=quick|standard|deep** (optional, default: `standard`)
- **--focus=\<area\>** (optional): Filter to specific experiment group, layer, or topic keyword

Output is always `<project-root>/research-map.md`.

## Workflow

### Step 1: Parse & Validate Arguments

1. Extract `project_path` from `$0`. If missing, print usage and stop:
   ```
   Usage: /research-map <project-path> [--depth=quick|standard|deep] [--focus=area]
   Example: /research-map ~/projects/SemanticScale
   Example: /research-map ~/projects/SemanticScale --depth=deep
   Example: /research-map SemanticScale --focus=behavioral
   ```

2. Resolve path:
   - Starts with `/` → use as-is
   - Starts with `~` → expand home directory
   - Bare name (no `/`) → try `~/projects/<name>`, then current directory
   - Verify directory exists; if not, list `~/projects/` and suggest matches

3. Parse `--depth=` flag; default to `standard`. Valid: `quick`, `standard`, `deep`.

4. Parse `--focus=` flag if present; store as `focus_filter`.

5. Set `depth` variable for use in later steps.

### Step 2: Check for Existing Map

1. Check if `<project_path>/research-map.md` exists.

2. **If exists** (UPDATE mode):
   - Read the file
   - Parse YAML frontmatter: extract `last-updated`, `experiments-known` list, `depth`
   - Note the existing depth level; if user requests a different depth, regenerate fully at new depth
   - Store existing content for later diffing

3. **If not exists** (CREATE mode):
   - Will generate from scratch

### Step 3: Phase A — Project Identity Scan

Read these files if they exist (use Glob + Read):

1. `README.md` at project root → extract project name, overview, thesis/hypothesis
2. `CLAUDE.md` → extract structural conventions, important paths, developer notes
3. `pyproject.toml` or `Cargo.toml` or `package.json` → identify language, dependencies
4. Check for `.git`:
   ```bash
   cd <project_path> && git log --oneline -15 2>/dev/null
   cd <project_path> && git remote -v 2>/dev/null
   ```
   Extract: recent activity summary, repo URL

Store as `project_identity`: name, description, thesis, language, repo_url, recent_activity.

### Step 4: Phase B — Documentation Discovery

Use Glob to find documentation files within `<project_path>`:

1. `**/narrative.md` → research story/narrative
2. `**/roadmap.md` → research plan with hypotheses and phases
3. `**/*DESIGN*.md` → experiment design documents
4. `**/data_dictionary.md` or `**/data_dict*` → data documentation
5. `**/reproduction*.md` or `**/REPRODUCE*` → reproduction guides
6. `docs/**/*.md` → any docs folder markdown

Read each discovered file (first 200 lines if large). Store as `docs_found` with file path and extracted content summary.

### Step 5: Phase C — Experiment/Module Structure Discovery

Try these heuristics in order. Stop at the first pattern that finds results:

**Pattern 1 — Explicit experiments directory:**
```
Glob: experiments/*/README.md
Glob: experiments/*/config.yaml
```

**Pattern 2 — Numbered directories:**
```
Glob: [0-9]*/README.md
```

**Pattern 3 — Notebook-driven:**
```
Glob: **/*.ipynb (exclude .git, __pycache__, node_modules, .venv)
```

**Pattern 4 — Script-driven:**
```
Glob: scripts/*.py or scripts/*.R
```

**Pattern 5 — Module-driven:**
```
Glob: */__init__.py (top-level packages)
```

**Pattern 6 — Papers/reports-driven:**
```
Glob: papers/**/*.md or reports/**/*.md
```

For each discovered unit, extract by reading its README.md (or first file):

- **name**: Directory name or file heading
- **status**: Grep the unit's files for these patterns (case-insensitive):
  - `CONFIRMED` or `confirmed` → confirmed
  - `PARTIAL` or `partial` → partial
  - `NOT CONFIRMED` or `null` or `failed` → null
  - `WIP` or `TODO` or `in progress` → wip
  - No match → unknown
- **hypothesis**: First sentence after a "Hypothesis" or "Goal" heading, or the first paragraph of README
- **key_result**: Look for "Key Result", "Result", "Finding" headings; extract first metric or summary sentence
- **dependencies**: Parse from:
  - `config.yaml`: look for paths referencing other experiments (e.g., `../../data/sh0`, `sh0_data_dir`)
  - README: look for "requires", "depends on", "uses output from" patterns
  - Import statements referencing other experiment modules

Store as `experiments[]` list.

### Step 6: Phase D — Findings Extraction (standard + deep only)

Skip if `depth == quick`.

1. Glob for `**/reports/**/*.md` and `**/*REPORT*.md` and `**/*report*.md`
2. For each report, read and extract:
   - Key metrics (look for tables with numbers, lines containing `=`, `F1`, `AUROC`, `rho`, `accuracy`, `p-value`)
   - Verdict/conclusion (look for "Conclusion", "Summary", "Verdict" headings)
3. Grep across all project files for negative results:
   - Pattern: `NOT CONFIRMED|null result|failed|negative|did not|no significant|no correlation`
   - Record experiment + finding for the Negative Results section
4. Grep for open questions:
   - Pattern: `future work|next step|open question|TODO|proposed|priority`

Update `experiments[]` with enriched findings data.

### Step 7: Phase E — Code & Data Pointers (deep only)

Skip if `depth != deep`.

1. For each experiment, find entry point scripts:
   ```
   Glob: <experiment_dir>/scripts/*.py
   Glob: <experiment_dir>/*.py (top-level scripts)
   ```
   Record first script found as `entry_script`.

2. For each experiment, find key source modules:
   ```
   Glob: <experiment_dir>/src/*.py
   ```
   Record module names.

3. Parse config files (`config.yaml`, `config.yml`) for:
   - Data paths and sizes
   - Model names
   - Key hyperparameters

4. Build data lineage: from config cross-references, construct a graph of which experiment's data feeds into which.

Store as `code_map[]` and `data_lineage[]`.

### Step 8: Thematic Grouping

Group experiments into thematic layers for the document structure:

1. **If roadmap.md exists**: Use its structure for grouping (it likely already organizes experiments by theme/phase/layer).

2. **If no roadmap**: AI-infer groupings based on:
   - Experiment names and descriptions
   - Dependency structure (experiments that share inputs likely belong together)
   - Common patterns: "mechanism/foundation", "control/steering", "application/systems", "evaluation/behavioral"
   - Fall back to sequential ordering if no clear grouping emerges

3. Assign section numbers:
   - Section 1: Overview (always)
   - Section 2: Data Management (standard+deep)
   - Sections 3–N: One per thematic layer
   - Final sections: Negative Results, Open Questions, Reproduction (deep), Glossary (deep)

Store as `layers[]`, each with: layer_name, layer_description, experiment_ids[].

### Step 9: Incremental Update Diff (UPDATE mode only)

Skip if CREATE mode.

1. Compare `experiments[]` names against `experiments-known` from frontmatter:
   - New experiments → mark for addition
   - Missing experiments (removed from project) → mark for removal

2. For experiments present in both:
   - Check if report/README files have changed (compare file mtime vs `last-updated` in frontmatter)
   - If changed → mark for update
   - If unchanged → mark for preservation (keep existing section text)

3. Determine which sections need regeneration:
   - **Always regenerate**: Overview thesis (reflects current state), dependency graph (topology may change), open questions
   - **Regenerate if experiments changed**: Layer sections with new/updated experiments, negative results
   - **Preserve if no changes**: Experiment detail sections for unchanged experiments, data management (deep), glossary

### Step 10: AI Synthesis & Document Assembly

Generate the research map markdown. Use the scanned data and AI synthesis together.

**YAML Frontmatter:**
```yaml
---
type: research-map
project: {project_name}
project-path: {absolute_path}
created: {YYYY-MM-DD}  # only set on CREATE; preserve on UPDATE
last-updated: {YYYY-MM-DD}
depth: {depth}
experiments-known:
  - {experiment_id_1}
  - {experiment_id_2}
  ...
---
```

**Document body — assemble these sections in order:**

#### Section 1: Overview (all depths)

```markdown
## 1. Overview

### 1.1 Research Thesis

{AI-synthesized 2-3 sentence thesis from README + roadmap. Define key terms inline.
For SemanticScale: "Frozen LLM representations encode a continuous Semantic Level of Detail (SLoD) axis..."}

### 1.2 Repository Structure

{Directory tree output, truncated to 2 levels. Annotate key directories with one-line descriptions.}

```
project-root/
├── experiments/          # 10 self-contained experiments (SH0–SH5d)
│   ├── sh0_weak_labels/
│   ├── sh1_linear_probe/
│   └── ...
├── docs/                 # Narrative, roadmap, data dictionary
├── data/                 # Downloaded datasets (~3.4 GB)
└── README.md
```

**Key conventions:** {extracted from CLAUDE.md or README — e.g., "each experiment is self-contained with config.yaml, DESIGN.md, scripts/, src/, reports/"}

### 1.3 Experiment Dependency Graph

```mermaid
graph LR
    {For each experiment, generate a node:}
    SH0["SH0: Weak Labels<br/>✅ 83K spans labeled"]
    SH1["SH1: Linear Probe<br/>✅ F1=0.72"]
    ...

    {For each dependency edge:}
    SH0 --> SH1
    SH1 --> SH2
    SH1 --> SH3
    ...

    classDef confirmed fill:#2d5016,stroke:#4a8c1c,color:#fff
    classDef partial fill:#7a5900,stroke:#b8860b,color:#fff
    classDef null fill:#5c1a1a,stroke:#b22222,color:#fff
    classDef wip fill:#1a3a5c,stroke:#4682b4,color:#fff
    classDef unknown fill:#444,stroke:#888,color:#fff

    class {confirmed_ids} confirmed
    class {partial_ids} partial
    class {null_ids} null
    class {wip_ids} wip
```
```

**Experiment status key:** ✅ Confirmed | 🟡 Partial | ❌ Not confirmed | 🔵 In progress | ⬜ Unknown

| # | Experiment | Hypothesis | Verdict | Key Result |
|---|---|---|---|---|
{For each experiment: | ID | Name | One-line hypothesis | Status icon | Key metric |}

```

#### Section 2: Data Management (standard + deep)

```markdown
## 2. Data Management

### 2.1 Data Setup

{How to get data: download script, total size, prerequisites.
Extract from setup_data.py, README, or data docs.}

### 2.2 Data Dictionary

| Dataset | Size | Key Files | Format |
|---|---|---|---|
{For each experiment's data: | name | size | key files | format |}

{If data_dictionary.md exists, summarize its key contents here.}
```

#### Sections 3–N: Layer Sections

For each thematic layer, generate one h2 section:

```markdown
## {N}. {Layer Name}: {Grouped Experiment Names} ({IDs})

{1-2 sentence layer description: what question does this group of experiments address together?}

### {N}.1 {Experiment ID} — {Experiment Name}

**Hypothesis:** {One sentence}

**Method:** {2-3 sentences or bullet points describing the approach}

**Key Results:**
{Bullet points with metrics, tables if available}
- {metric_name} = {value}
- Verdict: {✅|🟡|❌} {CONFIRMED|PARTIAL|NOT CONFIRMED}

**What This Means:** {AI-generated annotation: why does this result matter for the overall project? How does it connect to other experiments? What did it enable or block? This is the "trace guide" — the codemaps equivalent of explaining WHY things are grouped together.}

{DEEP ONLY — Data Flow → Code table:}

| Concept | Source File | Output Artifact |
|---|---|---|
| {e.g., "SLoD labeling"} | `src/heuristic_labeler.py` | `data/sh0/qasper_slod_spans.jsonl` |

**Files:** `README` · `config.yaml` · `scripts/` · `reports/`
```

At **quick** depth: omit per-experiment subsections entirely. The experiment index table in Section 1 serves as the full experiment listing.

At **standard** depth: include all subsections except the Data Flow → Code table.

At **deep** depth: include everything including Data Flow → Code tables.

#### Negative Results & Lessons (standard + deep)

```markdown
## {N+1}. Negative Results & Lessons

| What Failed | Experiment | Why It Matters |
|---|---|---|
| {description} | {ID} | {lesson learned — why this failure is informative} |

{AI-synthesized paragraph: What do the failures collectively teach? Are there patterns (e.g., domain mismatch, measurement problems vs method problems)?}
```

#### Open Questions (standard + deep)

```markdown
## {N+2}. Open Questions & Next Directions

{For each open direction found in docs or inferred from incomplete experiments:}

- **{Proposed experiment or question}** — {1 sentence description}. Priority: {High|Medium|Low}

{AI-synthesized paragraph: What are the most promising next steps and why?}
```

#### Reproduction Guide (deep only)

```markdown
## {N+3}. Reproduction Guide

### Environment Setup

{Python version, key dependencies, GPU requirements — from requirements.txt / pyproject.toml}

```bash
{setup commands — from reproduction.md or README}
```

### Execution Order

{Ordered list of experiments with commands to run each. From reproduction.md or inferred from dependency graph.}

1. **SH0** (foundational, no dependencies): `cd experiments/sh0_weak_labels && python scripts/01_run.py`
2. **SH1** (requires SH0): `cd experiments/sh1_linear_probe && python scripts/01_embed.py`
...

### Expected Outputs

{What to check for after each experiment runs — key output files, expected metric ranges.}
```

#### Glossary (deep only)

```markdown
## {N+4}. Glossary

| Term | Definition |
|---|---|
| {term} | {definition — extracted from docs or AI-inferred from context} |
```

### Step 11: Write Output

1. Write the assembled markdown to `<project_path>/research-map.md`

2. If UPDATE mode: use Edit tool to update only changed sections where possible. If the changes are too extensive (>50% of sections changed, or depth level changed), do a full Write.

### Step 12: Report to User

Print summary:

```
✓ Research map {'created' | 'updated'} at: <project_path>/research-map.md

Depth: {depth}
Experiments mapped: {count} ({confirmed} confirmed, {partial} partial, {null} null, {unknown} unknown)
Sections: {section_count}
{If UPDATE: "Updated sections: {list of changed sections}"}
{If UPDATE: "Preserved sections: {count} (no upstream changes)"}

For navigable HTML with sidebar: /md-to-html <project_path>/research-map.md --style=report
```

## Error Handling

| Error | Response |
|---|---|
| Missing project path argument | Print usage with examples |
| Project directory not found | List `~/projects/` contents, suggest closest match |
| No README and no .md files | Create minimal map from directory listing with warning |
| No recognizable experiment structure | Create overview-only map, note "no experiments detected" |
| Existing map with different depth | Full regeneration at new depth (with notice) |
| Very large project (>50 experiment units) | If no `--focus`, warn and suggest using `--focus=<area>` or `--depth=quick` |

## Graceful Degradation

The skill never fails — it produces the best map possible from what's available:

| What's Missing | Fallback |
|---|---|
| No README.md | Use directory name as project title; scan any .md for description |
| No experiments/ directory | Try notebooks, scripts, packages; group by directory |
| No reports or results | Mark all experiments as "status unknown" |
| No docs/ directory | Skip narrative-dependent sections; AI synthesizes from READMEs |
| No .git | Skip git history and repo URL |
| No config files | Skip data lineage; use README-based dependency inference |
| Single-file project | Minimal map: overview + code structure only |
| No recognizable structure at all | Directory tree + any markdown content found |

## Examples

### First run on a well-structured project
```
/research-map ~/projects/SemanticScale
```
Generates `~/projects/SemanticScale/research-map.md` with full standard-depth map.

### Quick overview for re-orientation
```
/research-map ~/projects/SemanticScale --depth=quick
```
Generates concise map: overview, dependency graph, experiment table.

### Deep map for onboarding a collaborator
```
/research-map ~/projects/SemanticScale --depth=deep
```
Full map including data flow tables, reproduction guide, glossary.

### Update after new experiments completed
```
/research-map ~/projects/SemanticScale
```
Detects changes, updates affected sections, preserves manual edits.

### Focus on specific area
```
/research-map ~/projects/SemanticScale --focus=behavioral
```
Maps only experiments matching "behavioral" (SH5 family).
