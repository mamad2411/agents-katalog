---
name: project-analyze
description: >
  Deep framework-agnostic codebase analysis. Observes and describes only — never scores, never produces FIX_MANIFEST entries.
  Produces analysis-report.md at project root and updates ai-context/ [auto-updated] sections.
  Trigger: /project-analyze, analyze project, project analysis, understand project codebase.
  Also invoked by: project-audit Phase A extension (internal).
format: procedural
---

# project-analyze

> Deep framework-agnostic codebase analysis. Observes and describes — never scores, never produces FIX_MANIFEST entries.

**Triggers**: `/project-analyze`, analyze project, project analysis, understand project codebase, codebase analysis

**Also invoked by**: `project-audit` Phase A extension (internal, reads `analysis-report.md` as output)

---

## Purpose

`project-analyze` is a pure observation skill. It reads the project structure, detects the technology stack, samples source conventions, and compares observed structure against any documented architecture. It writes its findings to `analysis-report.md` (consumed by `project-audit` D7) and updates `[auto-updated]` sections in `ai-context/` files.

It does NOT score. It does NOT produce FIX_MANIFEST entries. All findings are descriptions, not verdicts.

---

## Process

### Step 1 — Read config

Read `openspec/config.yaml` to extract analysis configuration. All keys in the `analysis` block are optional; if absent the skill proceeds with safe defaults.

**Keys to read:**

| Key | Default | Description |
|-----|---------|-------------|
| `analysis.max_sample_files` | `20` | Maximum number of source files to read during convention sampling |
| `analysis.analysis_targets` | (none) | Explicit list of file paths — when set, overrides auto-sampling entirely |
| `analysis.exclude_dirs` | (none) | List of directory names to skip during all analysis steps (e.g., `node_modules`, `.git`, `dist`) |

**Behavior when keys are absent:**

- If `analysis` key is missing entirely: use all defaults — `max_sample_files=20`, auto-detect source directories, no exclusions beyond `.git` and `node_modules`.
- If `analysis.max_sample_files` is absent: default to `20`.
- If `analysis.analysis_targets` is absent: auto-detect source directories using Step 3 results.
- If `analysis.exclude_dirs` is absent: apply standard exclusions (`.git`, `node_modules`, `dist`, `build`, `.next`, `__pycache__`, `target`, `vendor`).

This step shares its Bash call with Step 2 (manifest detection). Both happen within the same Bash invocation — maximum 1 Bash call for Steps 1+2 combined.

---

### Step 2 — Stack detection

Detect the project's technology stack using a manifest-first approach. If no manifest is found, fall back to file-extension sampling.

**Manifest-first detection order:**

Attempt to read manifests in this exact order (stop at the first group found; multiple manifests from the same ecosystem can coexist):

1. `package.json` — JavaScript / TypeScript / Node.js
2. `pyproject.toml` — Python (modern)
3. `requirements.txt` — Python (legacy)
4. `pom.xml` — Java (Maven)
5. `build.gradle` or `build.gradle.kts` — Java / Kotlin (Gradle)
6. `go.mod` — Go
7. `Cargo.toml` — Rust
8. `mix.exs` — Elixir
9. `composer.json` — PHP

From the found manifest(s), extract:
- Primary language and runtime version (if declared)
- Framework(s) and their versions
- Database or ORM dependencies (inferred from package names)
- Testing framework(s)
- Build tool(s)
- Top 10 dependencies by apparent importance (core runtime deps over dev tooling)

**File-extension-sampling fallback:**

When no recognized manifest is found:
- Run `find [project_root] -maxdepth 3 -type f` and count by extension
- Report the top 5 extensions with file counts
- Infer likely language from extension (`.md`/`.yaml`/`.sh` → documentation/config project; `.py` → Python; `.rb` → Ruby; etc.)
- Note: "No manifest found — stack inferred from file extension distribution"

**This step MUST NOT error or produce an empty section.** Even on a project with no recognizable stack (pure binary files, empty repo), the Stack section in `analysis-report.md` states what was observed, even if only "No manifest found and no recognizable source extensions detected."

This step shares its Bash call with Step 1. Maximum 1 Bash call total for Steps 1+2.

---

### Step 3 — Structure mapping

Map the project's folder organization using a 2-level folder tree, then classify the organizational pattern.

**Folder tree:**

Run:
```bash
find [project_root] -maxdepth 2 -type d
```

Apply `exclude_dirs` from Step 1 config to filter results. Always exclude `.git`, `node_modules`, `__pycache__`, `.next`, `dist`, `build`, `target`, `vendor` even if not in config.

Annotate each top-level directory with its inferred purpose based on name heuristics:
- `src/`, `lib/`, `app/` → source root
- `test/`, `tests/`, `spec/`, `__tests__/`, `e2e/` → test root
- `docs/`, `documentation/` → documentation
- `scripts/`, `bin/` → tooling / scripts
- `config/`, `.config/` → configuration
- `public/`, `static/`, `assets/` → static assets
- `dist/`, `build/`, `out/` → build output (excluded from analysis)
- `packages/`, `apps/`, `libs/` → monorepo workspaces

**Organization pattern classification (four rules, applied in order):**

1. **Monorepo**: Top-level contains a `packages/`, `apps/`, or `libs/` directory AND multiple sub-`package.json` or equivalent manifest files are found within those directories.

2. **Feature-based**: Top-level `src/` (or equivalent source root) contains subdirectories named after business domain concepts rather than technical layers. Signals: directories named after entities/features (e.g., `user/`, `auth/`, `billing/`, `dashboard/`, `product/`), or directories under `src/features/`, `src/modules/`, `src/domain/`.

3. **Layer-based**: Top-level `src/` (or equivalent source root) contains subdirectories named after technical layers. Signals: `api/`, `services/`, `components/`, `models/`, `repositories/`, `controllers/`, `handlers/`, `middleware/`, `utils/`, `helpers/`.

4. **Flat**: Source files are primarily at the root or a single `src/` level with few or no subdirectories. Fewer than 4 meaningful subdirectories under the source root.

If no single pattern dominates or multiple signals are mixed: classify as `mixed`.
If the folder structure is too shallow or ambiguous to classify: classify as `unknown`.

**Confidence levels:**

- `high`: Two or more strong signals align to the same pattern
- `medium`: One strong signal or two weak signals
- `low`: Pattern is inferred from one weak signal or is ambiguous

**Source root detection heuristics:**

Directories are considered source roots when they:
- Are named `src/`, `lib/`, `app/`, `source/`, or `core/`
- Contain files with the dominant extension detected in Step 2
- Are NOT build output, vendor, or tooling directories

**Test root detection heuristics:**

Directories are considered test roots when they:
- Are named `test/`, `tests/`, `spec/`, `__tests__/`, `e2e/`, `integration/`, `unit/`
- Contain files matching patterns like `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go`
- Are sibling to a source root, or nested within source directories

This step uses 1 Bash call.

---

### Step 4 — Convention sampling

Sample source files to observe naming and coding conventions in use. The sample is bounded by `max_sample_files` from Step 1 config (default: 20).

**File selection algorithm:**

1. If `analysis.analysis_targets` is set in config: use exactly those files. Do not auto-sample.
2. Otherwise, auto-sample from the detected source root(s):
   - Enumerate source files in each source directory (filtered by dominant extension from Step 2)
   - Apply `exclude_dirs` filter
   - Distribute files proportionally across directories: each directory gets `ceil(max_sample_files / num_source_dirs)` files
   - Within each directory, select the most recently modified files (recency-first ordering)
   - Hard ceiling: never exceed `max_sample_files` total, regardless of directory count

**Observations to extract from the sample:**

1. **File naming pattern**: Analyze basenames — detect `kebab-case`, `snake_case`, `PascalCase`, `camelCase`, or `mixed`. Include a concrete example from the sample.

2. **Function and class naming**: Use regex over file content to find function/method/class declarations — detect `camelCase`, `snake_case`, `PascalCase`, `mixed`. Include a concrete example.

3. **Import style**: Identify how modules are imported — `relative` (starts with `./` or `../`), `absolute` (starts with project root alias or bare name), `alias-based` (uses `@/`, `~/`, or configured path mappings), or `mixed`. Include a concrete example.

4. **Error handling patterns**: Detect dominant error handling style — `try/catch`, `Result type` (e.g., `Result<T, E>`, `Either`), `panic/recover` (Go), `exceptions` (Java/Python class-based), `callbacks` (Node.js `err` first), or `mixed`. If no clear pattern is visible in the sample: state `not detected`.

**The Conventions section in `analysis-report.md` MUST state:**
- The exact sample size used (number of files read)
- Which directories were sampled (list them)
- Whether `analysis_targets` was used (configured) or auto-detection was used

This step uses 1 Bash call (a single multi-file read batch).

---

### Step 5 — Architecture drift detection

Compare the observed project structure (from Steps 2–3) against the documented architecture in `ai-context/architecture.md`, if it exists.

**Reading the baseline:**

Read `ai-context/architecture.md` if it exists. Extract:
- Any fenced code block following a `## Folder Structure` heading (documented folder tree)
- All rows from the `## Architecture Decisions` table
- Any paths or directory names mentioned in `## Main Flow` or `## Entry Points`

This step performs no Bash call — it reads a single file using the Read tool.

**Comparison and classification:**

For each documented folder, path, or pattern in `architecture.md`, check whether the corresponding path was observed in Step 3. Classify each item as one of three states:

| Status | Meaning |
|--------|---------|
| `match` | Documented path/pattern is observed in the actual repo structure |
| `minor drift` | Small discrepancy — documented path exists but under a different name, or an expected sub-directory is missing |
| `significant drift` | Structural mismatch — an entire documented layer or module is absent, or the observed organization pattern differs fundamentally from what is documented |

**Drift summary classification:**

- `none`: All documented items match. Zero drift entries.
- `minor`: One or more `minor drift` entries; no `significant drift` entries.
- `significant`: One or more `significant drift` entries.

**When `ai-context/architecture.md` is absent:**

- The Architecture Drift section states: "No `ai-context/architecture.md` found — drift comparison not possible."
- No drift entries are produced.
- No error is emitted.
- The skill proceeds to Step 6 without interruption.
- The `Drift Summary` line reads: `N/A — no baseline found`.

**All drift entries are informational only.** No severity labels. No FIX_MANIFEST references. No score deductions. Language is neutral:
- "Documented: X — Observed: Y"
- "Path `X` documented but not found in observed structure"
- "Directory `Y` observed but not mentioned in architecture.md"

---

### Step 6 — Write outputs

Write the analysis results to `analysis-report.md` and update `ai-context/` files.

**`analysis-report.md`:**

Write to `[project_root]/analysis-report.md`. Overwrite if it already exists. The file structure is defined in the Output Format section below.

**`ai-context/` update — `[auto-updated]` marker strategy:**

`project-analyze` only writes to `ai-context/` files that already exist. It NEVER creates new `ai-context/` files or the `ai-context/` directory itself.

If `ai-context/` does not exist: write only `analysis-report.md`, and note in the `## ai-context/ Update Log` section: "ai-context/ not found — no update performed. Run `/memory-init` to create the memory layer."

For each file that exists, use the merge algorithm below to update auto-updated sections:

**Section IDs written per file:**

| File | section-id | Content written |
|------|-----------|-----------------|
| `ai-context/stack.md` | `stack-detection` | Auto-detected stack table from Step 2 |
| `ai-context/architecture.md` | `structure-mapping` | Observed folder tree and organization pattern from Step 3 |
| `ai-context/architecture.md` | `drift-summary` | Summary of drift detection from Step 5 |
| `ai-context/conventions.md` | `observed-conventions` | Naming, import style, error handling from Step 4 |

`known-issues.md` and `changelog-ai.md` are NEVER written by `project-analyze`.

**Marker syntax:**

```markdown
<!-- [auto-updated]: stack-detection — last run: YYYY-MM-DD -->
## Stack (auto-detected)

[content written by project-analyze]

<!-- [/auto-updated] -->
```

**Merge algorithm (per file):**

```
READ full file content
PARSE: split into blocks:
  - auto-updated block: starts at <!-- [auto-updated]: X --> and ends at <!-- [/auto-updated] -->
  - human block: everything else

FOR each auto-updated block project-analyze wants to write:
  IF matching <!-- [auto-updated]: section-id --> found in file:
    REPLACE content between markers (inclusive) with new content
    UPDATE the "last run: YYYY-MM-DD" date in the opening marker
  ELSE:
    APPEND new auto-updated block at end of file

WRITE updated file
```

Use the Read tool to load each target file, compute the merged content in-context, then use the Write tool to write the updated file. Do not use Bash or the Edit tool for this merge.

This algorithm is deterministic and idempotent: running `project-analyze` twice produces the same result.

**Print summary to user:**

After writing all outputs, print a concise summary:
```
Analysis complete.
  analysis-report.md — written to [project_root]
  ai-context/stack.md — [updated section: stack-detection | unchanged | not found]
  ai-context/architecture.md — [updated sections: structure-mapping, drift-summary | not found]
  ai-context/conventions.md — [updated section: observed-conventions | not found]

Stack: [detected stack summary]
Organization: [pattern]
Drift: [none|minor|significant|N/A]
```

---

## Rules

### Hard rules — never violated

1. **NEVER scores or assigns severity levels** to findings — all output is description only. No numeric scores, no CRITICAL/HIGH/MEDIUM/LOW labels used in a pass/fail context.

2. **NEVER produces FIX_MANIFEST entries** — `project-analyze` has no `required_actions`, no `violations[]` with severity, and no structured action lists directed at `project-fix`.

3. **NEVER modifies content outside `[auto-updated]` markers** — content before the opening marker and after the closing marker is preserved byte-for-byte.

4. **NEVER creates `ai-context/` if it does not exist** — if the directory is absent, write `analysis-report.md` only and instruct the user to run `/memory-init` first.

5. **Maximum 3 Bash calls per execution** — Steps 1+2 share 1 call (manifest detection + config read), Step 3 = 1 call (folder tree), Step 4 = 1 call (file batch read). Steps 5 and 6 use the Read and Write tools, not Bash.

### Always-on rules

- Always writes `Last analyzed:` date (YYYY-MM-DD format) to `analysis-report.md`.
- Always reports which `ai-context/` sections were updated vs preserved in the `## ai-context/ Update Log` section.
- Always states the sample size and which directories were sampled in the Conventions section.
- Proceeds through all steps even when earlier steps find nothing — every section in `analysis-report.md` is always written, with a "not detected" or "N/A" note when appropriate.

---

## Output Format

`analysis-report.md` is written to `[project_root]/analysis-report.md` with the following structure. D7 in `project-audit` reads this file; the section structure is stable and must not be reordered.

```markdown
# Analysis Report — [Project Name]

Last analyzed: [YYYY-MM-DD HH:MM]
Analyzer: project-analyze
Config: sample_size=[N], targets=[auto-detected|configured]

---

## Summary

[3-5 line human-readable summary of what the project is and how it is structured]

Stack detected: [language(s)] / [framework(s)] / [database if any]
Organization pattern: [feature-based|layer-based|monorepo|flat|mixed|unknown]
Architecture drift: [none|minor|significant|N/A]
Conventions documented: [yes|partial|no]

---

## Stack

Source: [manifest filename(s) | file-extension-sampling]

| Category | Detected | Source |
|----------|----------|--------|
| Language | [value] | [manifest key or extension count] |
| Framework | [value] | [manifest key] |
| Database | [value] | [manifest key or none] |
| Testing | [value] | [manifest key or test file pattern] |
| Build tool | [value] | [manifest key or config file] |

Key dependencies (top 10 by apparent importance):
| Package | Version | Inferred purpose |
|---------|---------|-----------------|
| [name] | [version] | [inferred] |

---

## Structure

Organization pattern: [feature-based|layer-based|monorepo|flat|mixed|unknown]
Confidence: [high|medium|low] — [reason]

Top-level layout:
```
[folder tree, 2 levels deep, annotated with detected purpose]
```

Source root(s): [list of detected source directories]
Test root(s): [list of detected test directories, or "none detected"]
Entry point(s): [list of detected entry points]

---

## Conventions Observed

Sample size: [N] files across [M] directories
Sampling method: [auto-detected | configured via analysis_targets]
Directories sampled: [list]

### Naming
- Files: [detected pattern: kebab-case|snake_case|PascalCase|mixed]
  Example: [concrete file name from sample]
- Functions/methods: [detected: camelCase|snake_case|PascalCase|mixed]
  Example: [concrete function name from sample]
- Classes/types: [detected pattern]
  Example: [concrete type name from sample]
- Constants: [detected pattern]
  Example: [concrete constant from sample]

### Import style
[Detected pattern: absolute|relative|alias-based|mixed]
Example: [concrete import from sample]

### Error handling
[Detected pattern: try/catch|Result type|exceptions|mixed|not detected]
Example: [concrete pattern from sample]

### Module/layer boundaries
[Detected: what calls what, based on import graph sampling]

---

## Architecture Drift

[This section is the primary input for project-audit D7]

Basis for comparison: [ai-context/architecture.md exists | ai-context/architecture.md not found — no drift comparison possible]

### Documented vs Observed

| Documented (architecture.md) | Observed in repo | Status |
|------------------------------|------------------|--------|
| [folder/pattern documented] | [what was found] | match / minor drift / significant drift |

### Drift Summary

[none|minor|significant|N/A — no baseline found]

Drift entries:
- [description of each discrepancy, if any]
  - Documented: [what architecture.md says]
  - Observed: [what was actually found]
  - Impact: [informational|architectural]

[If no drift: "No structural drift detected between architecture.md and observed folder structure."]
[If architecture.md not found: "No architecture.md found — drift comparison not possible. Run /memory-init to create architecture.md, then re-run /project-analyze for full D7 scoring."]

---

## ai-context/ Update Log

Files modified:
- [filename]: [which [auto-updated] sections were updated]
- [filename]: [unchanged — sections matched, no differences detected]

Human-edited sections preserved:
- [filename] → [section headings that were left untouched]

[If no ai-context/ exists: "ai-context/ not found — no update performed. Run /memory-init to create the memory layer."]
```

**D7 consumption contract (for `project-audit`):**

`project-audit` D7 reads `analysis-report.md` by locating:
1. `Last analyzed:` field (line 3) — for staleness check
2. `Architecture drift:` field in `## Summary` — for quick status
3. `### Drift Summary` line under `## Architecture Drift` — for scoring (`none` / `minor` / `significant` / `N/A`)
4. `Drift entries:` list under `## Architecture Drift` — for violations list

These four items are at fixed positions. D7 does not need to parse arbitrary markdown.
