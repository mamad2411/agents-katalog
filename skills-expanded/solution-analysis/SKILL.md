---
name: solution-analysis
description: Analyze a FileMaker solution and produce a structured profile covering data model, business logic, UI layer, integrations, and health metrics. Uses on-disk pre-processing to handle solutions of any size without sending raw XML through the agent. Use when the developer says "analyze solution", "solution overview", "solution analysis", "solution profile", "solution spec", "what does this solution do", "solution summary", or wants a high-level understanding of an entire FileMaker solution.
compatibility: Requires Python 3. Optionally networkx, pandas, matplotlib, jinja2 (via venv) for extended analysis.
---

# Solution Analysis

This skill produces a comprehensive profile of a FileMaker solution by running `agent/scripts/analyze.py` — a Python script that reads pre-indexed data (index files, xref, layout summaries, sanitized scripts) and synthesizes a structured overview. The agent never touches raw XML; all heavy processing happens on disk.

**Purpose**: Give a developer (or someone new to a solution) a complete understanding of what the solution does — its data model, scripted business logic, UI coverage, integration points, and health.

**Output**: `agent/sandbox/{solution} - solution-profile.json` and optionally a markdown specification document.

## Architecture

### Layer 1: Deterministic engine (`analyze.py`)

Pure Python analysis that reads pre-indexed data and produces structured output:

```bash
python3 agent/scripts/analyze.py -s "SolutionApp"                          # JSON profile
python3 agent/scripts/analyze.py -s "SolutionApp" --format markdown        # Markdown spec
python3 agent/scripts/analyze.py -s "SolutionApp" --deep                   # Full script analysis
python3 agent/scripts/analyze.py -s "SolutionApp" --ensure-prerequisites   # Build xref + layout summaries first
python3 agent/scripts/analyze.py --list-extensions                           # Show optional deps
```

The script automatically builds missing prerequisites (`xref.index`, layout summaries) when `--ensure-prerequisites` is passed.

### Layer 2: Agentic interpretation (this skill)

Reads the compact JSON profile and produces narrative insight — what the solution appears to do, how its parts connect, what patterns it follows, and what health issues deserve attention.

## Workflow

### Step 1: Identify the solution

Determine which solution to analyze:

1. If the developer named a specific solution, use that name
2. If `agent/CONTEXT.json` exists, read the `solution` field
3. If only one solution exists in `agent/context/`, auto-detect it
4. Otherwise, list available solutions and ask

### Step 2: Run the analysis

```bash
python3 agent/scripts/analyze.py -s "{solution}" --ensure-prerequisites
```

This:

- Builds `xref.index` (via `trace.py build`) if missing
- Builds layout summaries (via `layout_to_summary.py`) if missing
- Analyzes all six index files, sanitized scripts, custom functions, and layout summaries
- Writes `agent/sandbox/{solution} - solution-profile.json`

For deep analysis (when the developer requests it or the solution is small enough):

```bash
python3 agent/scripts/analyze.py -s "{solution}" --ensure-prerequisites --deep
```

### Step 3: Read the profile

Read `agent/sandbox/{solution} - solution-profile.json`. The profile contains these sections:

| Section          | Key                  | What it contains                                                                 |
| ---------------- | -------------------- | -------------------------------------------------------------------------------- |
| Summary          | `summary`            | Top-level counts (tables, fields, scripts, layouts, etc.)                        |
| Data Model       | `data_model`         | Tables with field breakdowns, TO groups, relationship summary, topology analysis |
| Naming           | `naming_conventions` | Detected prefix patterns and case styles                                         |
| Business Logic   | `business_logic`     | Script folders, call graph, entry points, utility scripts, clusters, line counts |
| Custom Functions | `custom_functions`   | Function inventory, categories, dependency chains                                |
| UI Layer         | `ui_layer`           | Layout inventory, classifications, portal usage, orphaned layouts                |
| Integrations     | `integrations`       | External data sources, value lists, external script calls                        |
| Multi-file       | `multi_file`         | Cross-file references and correlated solutions                                   |
| Health           | `health`             | Dead objects, disconnected tables, empty scripts                                 |

### Step 4: Produce the narrative

Using the profile data, produce a narrative specification that covers:

1. **Executive Summary** — What this solution appears to be (CRM, ERP, inventory system, etc.) based on table names, script domains, and integration patterns. Mention the solution's scale (table count, script count, field count).

2. **Data Architecture** — Describe the topology pattern (anchor-buoy, spider-web, hybrid). Identify the core entity tables and how they relate. Note the naming convention and what it tells us about the development approach.

3. **Business Logic Domains** — Walk through the script folder hierarchy. For each major folder, describe what that functional area does based on script names and entry points. Highlight the largest scripts and utility scripts that serve as shared infrastructure.

4. **UI Coverage** — Which tables have layouts and which don't. Note the layout classification distribution. Call out orphaned layouts and any portals that reveal parent-child UI patterns.

5. **Integration Points** — External data sources, API calls (Insert from URL), email integration, import/export capabilities.

6. **Health Observations** — Dead object counts, disconnected tables, empty scripts. Frame these as observations, not criticisms — solutions grow organically and some "dead" objects may be intentional placeholders.

### Step 5: Optionally generate markdown

If the developer wants a shareable document:

```bash
python3 agent/scripts/analyze.py -s "{solution}" --format markdown --ensure-prerequisites
```

This produces `agent/sandbox/{solution} - solution-profile.md` — a structured markdown document with tables, the Mermaid ERD, and all metrics.

## Optional extensions

The analysis script supports optional Python libraries that enable deeper analysis. Check availability:

```bash
python3 agent/scripts/analyze.py --list-extensions
```

Extended features include:

- **networkx**: Anchor-buoy topology detection with confidence scores, script community detection, cycle detection, bridge relationship identification
- **pandas**: Statistical profiling, outlier detection, table health scorecards
- **matplotlib**: Embedded visualizations in the markdown report
- **jinja2**: Customizable report templates

If any are missing and the developer wants extended analysis, guide them through setup:

> **Extended analysis requires additional Python dependencies.**
>
> Core analysis works without them — install only if you want topology detection, statistical profiling, visualizations, or templated reports.
>
> **Option A: venv in the project folder (recommended)**
> ```bash
> python3 -m venv agent/.venv
> source agent/.venv/bin/activate
> pip install -r .cursor/skills/solution-analysis/assets/requirements-analyze.txt
> ```
>
> Once set up, run the analysis with the venv active, or prefix with `agent/.venv/bin/python3`:
> ```bash
> agent/.venv/bin/python3 agent/scripts/analyze.py -s "{solution}" --ensure-prerequisites
> ```

If the developer declines, proceed with the core analysis — all six profile sections are still generated, just without the extended metrics.

## Performance contract

- **Never read raw xml_parsed XML** — the analysis script reads only pre-indexed data
- **Run analyze.py once** — don't re-run unless the developer changes parameters
- **Read the JSON profile selectively** — for very large solutions, read specific sections rather than the entire file
- **Parallel tool calls** — when reading the profile and checking for prerequisites, batch independent reads

## Multi-file solutions

When a FileMaker solution uses a data separation model (UI file + data file) or references other FM files, the analysis automatically detects and incorporates cross-file relationships into a single unified profile.

### How it works

1. `detect_multi_file()` parses `external_data_sources/` XML to find referenced files
2. If correlated solutions exist in `agent/context/` (both files have been exploded and indexed via `fmcontext.sh`), the analysis loads both solutions' index data
3. Table occurrences are classified as Local or External using the enriched `table_occurrences.index` (columns: `TOName|TOID|BaseTableName|BaseTableID|Type|DataSource`)
4. External TOs are mapped to correlated solutions via base table overlap matching
5. The unified profile shows all tables with their `source_file` attribution

### Workflow

```bash
# Standard analysis — auto-detects correlated files
python3 agent/scripts/analyze.py -s "SolutionApp" --ensure-prerequisites

# Explicitly name correlated solutions
python3 agent/scripts/analyze.py -s "SolutionApp" --correlated SolutionData
```

### Profile enrichments for multi-file

The JSON profile includes these additional fields when multi-file is detected:

- `multi_file.file_architecture`: `"data_separation"`, `"multi_file"`, or `"single"`
- `multi_file.data_source_map`: Maps external data source names to correlated SolutionApps (e.g., `{"Data": "SolutionData"}`)
- `multi_file.files`: Array with per-file summary (name, role, local table count, TO counts)
- `data_model.tables[*].source_file`: Which FM file owns each base table
- `data_model.tables[*].is_external`: `true` for tables from correlated solutions
- `data_model.base_table_edges[*].cross_file`: Whether a relationship crosses file boundaries
- `data_model.local_tables` / `data_model.external_tables`: Tables grouped by ownership
- `data_model.to_classification`: Breakdown of Local vs External TOs by data source

### Output format differences

**HTML**: The relationship graph colors nodes by source file (blue = local, orange = data file). Cross-file edges use dashed orange lines. A legend shows the file-to-color mapping. The tables DataTable includes a "Source" column.

**Markdown**: The ERD uses a Mermaid `flowchart` with `subgraph` blocks per file (instead of `erDiagram`). Cross-file edges are dashed. A "Multi-File Architecture" section shows the pattern, per-file summary table, and table ownership.

**JSON**: All enrichments above are machine-readable for agent consumption.

### Narrative guidance

When describing a data separation model solution:

- Lead with the architecture pattern: "This is a data separation model with X as the UI file and Y as the data file"
- Note which tables are local UI/utility tables vs core domain tables stored in the data file
- Highlight that most table occurrences in the UI file are external references
- The true ERD (entity relationships between domain tables) lives in the data file
- The UI file's relationship graph primarily connects external TOs for layout/portal purposes
