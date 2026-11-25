---
name: architecture-visualizer
description: "Architecture visualizer: maps module dependencies, detects layer violations, circular dependencies, entry points, and computes structural health score. Generates Mermaid diagrams. Read-only. Audience: Both. Trigger: /arch-vis"
trigger: /arch-vis
---
# /arch-vis - Architecture Visualizer

## What this is for

As codebases grow, their architecture degrades: layer boundaries blur, circular
dependencies emerge, and no one has a current dependency map. This skill
reverse-engineers the module graph from source code imports, detects structural
issues, and generates Mermaid diagrams for visualization.

Maps the module dependency graph of a target directory. Produces a structured
report with Mermaid diagrams, layer violation analysis, circular dependency
detection, and structural health metrics.

## Usage

```
/arch-vis                  # interactive (prompts for directory)
/arch-vis <dir>            # scan directory directly
/arch-vis -help            # show usage
```


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. `-help` / `-h` -> print usage, exit 0.

### Step 2

2. Confirm target directory exists.

### Step 3

3. Run `scripts/arch-scan.ps1 -ProjectDir <dir>`.

### Step 4

4. LLM reads the JSON output and:

### Step 5

- Interprets the module dependency graph per layer

### Step 6

- Analyzes layer violations (read both files, determine legitimacy)

### Step 7

- Analyzes circular dependencies (read cycle files, suggest fix)

### Step 8

- Generates Mermaid diagrams (module graph + layer violation map)

### Step 9

5. Write `arch-vis-report.md` to the working directory.

## Analysis Dimensions

| Dimension | Description |
|-----------|-------------|
| Module graph | Import relationships between all project files |
| Layer boundaries | Configurable layer map; violations when lower layer imports higher |
| Circular deps | Cycles in module graph with full path and fix suggestion |
| Entry points | Files with no inbound imports |
| Health score | Weighted metric from cycles, violations, and coupling |

## Output

`arch-vis-report.md` with:
- Executive summary (modules, layers, cycles, violations, health score)
- Mermaid diagrams (module graph, layer violation map)
- Layer-by-layer analysis (modules per layer, dependency flow)
- Circular dependencies (paths and LLM remediation)
- Central modules (top 5 by fan-in/fan-out)
- Entry points and their dependency trees
- False positives (violations dismissed by LLM)
- Open questions
