---
name: tokextract
description: Extract a design system (DTCG tokens + DESIGN.md + audit) from any SwiftUI codebase
trigger_phrases:
  - "extract design tokens from this repo"
  - "run tokextract"
  - "audit my SwiftUI design system"
  - "what design tokens does this app use"
  - "recover the design system from this codebase"
---

# Tokextract

Reverse-engineers an implicit SwiftUI design system into three artifacts:
- `tokens.json` — W3C DTCG 2025.10 design tokens (all 9 categories)
- `DESIGN.md` — LLM-readable brand narrative companion (Google @google/design.md alpha format)
- `audit.md` — Drift report: magic numbers, near-duplicate colors, off-scale values, Liquid Glass violations, harmonization recommendations

Invoke as: `/tokextract --path <swift-repo> [--output <dir>] [--no-llm]`

---

## Pipeline

When invoked, run this pipeline. Each step is restartable; if any LLM task fails,
re-running picks up where it left off (`findings.raw.json` is durable).

`--no-llm` mode skips Steps 2, 3, 4, 6, 7 entirely. Steps 1, 5, 8 still run.

### Step 1 — Parse + analyze (deterministic)

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/extract.js parse \
  --path <path> \
  --output <out> \
  [--no-llm] \
  [--max-files 2000] \
  [--delta-e-threshold 2.5] \
  [--skip <categories>] \
  [--target-os <ver>] \
  [--vendor-namespace <s>] \
  [--force-color-space srgb|display-p3|oklch]
```

This emits:
- `<out>/.tokextract/findings.raw.json` — AST + regex extraction results for all 9 categories
- `<out>/.tokextract/clusters.json` — color cluster analysis
- `<out>/.tokextract/numericClusters.json` — numeric cluster analysis (spacing/radius/shadow)
- `<out>/.tokextract/drift.json` — off-scale numeric values
- `<out>/.tokextract/meta.json` — vendor namespace + target OS
- `<out>/.tokextract/llm-tasks.json` — manifest of pending LLM passes (unless `--no-llm`)
- `<out>/.tokextract/prompts/normalize-<category>-<n>.md` — per-category normalize prompts

### Step 2 — Run pending normalize tasks (skip if --no-llm)

Read `<out>/.tokextract/llm-tasks.json`. For each task with `status: "pending"` and `pass: "normalize"`:

Spawn an Agent subagent with:
- `subagent_type`: "general-purpose"
- `model`: `task.recommendedModel` (e.g. "claude-haiku-4-5-20251001")
- `description`: `task.id` (e.g. "normalize-color-1")
- `prompt`: contents of `task.promptPath`, prepended with:

```
Read the prompt below and write your structured JSON response to <task.responsePath>
using the Write tool. Validate that your output matches the Mapping[] schema before writing.
Reply with exactly the word "done" after writing.

---
[contents of task.promptPath]
```

Independent tasks (different categories or chunks) can run in parallel.
After all tasks complete, verify each `task.responsePath` exists.

### Step 3 — Plan harmonize (skip if --no-llm)

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/extract.js plan-harmonize \
  --output <out> \
  [--model-harmonize claude-sonnet-4-6]
```

This reads `clusters.json` + `numericClusters.json` and appends a `harmonize` task to `llm-tasks.json`.
If there are no clusters, this is a no-op.

### Step 4 — Run harmonize task (skip if --no-llm)

Read `<out>/.tokextract/llm-tasks.json`. For the task with `pass: "harmonize"` and `status: "pending"`:

Spawn one Agent subagent with `task.recommendedModel` against the harmonize prompt.
The subagent writes `<out>/.tokextract/llm-out/mapping.harmonize.json` directly via the Write tool.

### Step 5 — Emit final artifacts (deterministic)

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/extract.js emit \
  --output <out> \
  [--no-llm]
```

This:
- Reads LLM normalize outputs from `<out>/.tokextract/llm-out/`
- Merges normalize + harmonize mappings with findings (Node-side)
- Validates against DTCG 2025.10 schema (Ajv — hard error on failure)
- Writes `<out>/tokens.json`, `<out>/audit.md`, `<out>/DESIGN.md` (stub in --no-llm)
- Writes `<out>/preview.html` — self-contained visual review of the extracted system (open it directly in a browser; no server, no build step)
- Computes diff vs `<out>/.tokextract/previous/tokens.json` (if it exists) → appended to audit.md
- Snapshots `tokens.json` to `<out>/.tokextract/previous/tokens.json` for diff on next run

### Step 6 — Plan narrate (skip if --no-llm)

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/extract.js plan-narrate \
  --output <out> \
  [--model-narrate claude-sonnet-4-6]
```

This reads `tokens.json` + `audit.md` and appends a `narrate` task to `llm-tasks.json`.

### Step 7 — Run narrate task (skip if --no-llm)

Read `<out>/.tokextract/llm-tasks.json`. For the task with `pass: "narrate"` and `status: "pending"`:

Spawn one Agent subagent with `task.recommendedModel` against the narrate prompt.
The subagent reads `tokens.json` + `audit.md` and writes `<out>/DESIGN.md` directly via the Write tool.
This is the highest-leverage LLM step — the subagent generates the full brand narrative prose.

### Step 8 — Finalize

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/extract.js finalize \
  --output <out> \
  [--no-llm]
```

Runs the DESIGN.md lint pass (8 rules: broken-ref, missing-primary, contrast-ratio,
orphaned-tokens, token-summary, missing-sections, missing-typography, section-order).
Prints a summary of what was extracted.

---

## Flags (parse subcommand)

| Flag | Default | Description |
|---|---|---|
| `--path <dir>` | (required) | Swift repo root |
| `--output <dir>` | `<path>/.tokextract-out` | Output directory |
| `--no-llm` | false | Skip LLM passes (CI-safe, mechanical token names) |
| `--max-files <n>` | 2000 | Hard limit on .swift files |
| `--delta-e-threshold <n>` | 2.5 | CIEDE2000 distance for near-duplicate clustering |
| `--model-normalize <id>` | claude-haiku-4-5-20251001 | Model for normalize pass |
| `--model-harmonize <id>` | claude-sonnet-4-6 | Model for harmonize pass |
| `--model-narrate <id>` | claude-sonnet-4-6 | Model for narrate pass |
| `--skip <cats>` | (none) | Comma-separated categories to skip |
| `--force-color-space <s>` | (auto) | Override color space: srgb \| display-p3 \| oklch |
| `--target-os <ver>` | (auto-detect) | Target iOS version; gates Liquid Glass (26) and @Entry (18) |
| `--vendor-namespace <s>` | (from Info.plist) | Override $extensions vendor key |
| `--self-critique` | false | Enable self-critique pass after narrate |
| `--verbose` | false | Verbose output with per-category counts |

---

## Output structure

```
<output-dir>/
├── tokens.json              # W3C DTCG 2025.10 — canonical machine truth (all 9 categories)
├── DESIGN.md                # Brand narrative (stub until narrate pass runs)
├── audit.md                 # Drift report (7 sections: magic numbers, near-duplicates,
│                            #   orphaned tokens, off-scale values, glass violations,
│                            #   harmonization, changes since last extraction)
├── preview.html             # Self-contained visual review (swatches, ΔE clusters, type scale)
└── .tokextract/            # Internal state — delete to force clean re-run
    ├── findings.raw.json
    ├── clusters.json
    ├── numericClusters.json
    ├── drift.json
    ├── meta.json            # vendorNamespace + targetOs
    ├── llm-tasks.json
    ├── prompts/
    │   ├── normalize-color-1.md
    │   ├── normalize-typography-1.md
    │   ├── harmonize.md
    │   └── narrate.md
    ├── llm-out/
    │   ├── mapping.color.1.json
    │   ├── mapping.typography.1.json
    │   └── mapping.harmonize.json
    └── previous/
        └── tokens.json      # Snapshot for diff on next run
```

---

## Error handling

- `--max-files` exceeded → hard abort with clear error (don't silently degrade)
- Schema validation failure → hard abort with Ajv error details
- DESIGN.md lint failure → hard abort with lint rule details
- LLM task failure → mark task as `error` in manifest; re-run to retry
- Missing Asset Catalog file → finding emitted with `assetMissing: true`, `severity: error`
- No clusters → `plan-harmonize` no-ops cleanly

---

## Installation

This is a Claude Code plugin distributed through the `conorluddy` marketplace. To install:

```bash
# Add the marketplace (one-time):
/plugin marketplace add conorluddy/tokextract

# Install the plugin:
/plugin install tokextract@tokextract
```

The plugin is shipped pre-built — no `npm install` step required at install time.

For local development (modifying the plugin source), build from the source repo:

```bash
cd /Users/conor/Development/Extoken/plugins/tokextract
npm install
npm run build
```

After rebuilding, refresh the installed plugin: `/plugin marketplace update tokextract`.
