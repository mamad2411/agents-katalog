---
name: script-template-extraction
description: Extract embedded template content from Python/PowerShell scripts into separated .template files for syntax highlighting, SSOT, and runtime reading — companion automation for skill-factory §2.2.1.1 mandate #6.
category: General-Development
---

# Script Template Extraction (v1)

> **Skill ID:** `script-template-extraction`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This skill is a **base skill** — it owns the mechanical primitive of extracting
string-literal template content from scripts into standalone `.template` files.
It does NOT define which skills should have templates (that's the
[`skill-factory`](../skill-factory/SKILL.md) §2.2.1.1.6 mandate's job). It
provides a deterministic, reusable automation that any skill author or
library maintainer can invoke.

**Consumers:** All skills whose Python/PowerShell scripts write file content
(YAML, markdown, .gitignore, config) should run this extraction during the
authoring workflow. The [`skill-factory`](../skill-factory/SKILL.md) delegates
to this skill in its Post-Drafting Checklist (§3).

## Environment & Dependencies

| Requirement | Minimum | Notes |
|---|---|---|
| Python 3 | 3.10+ | `python3` on PATH (resolve via `mise` if workspace-configured) |
| `ast` module | stdlib | Parsing script structure |
| `argparse` module | stdlib | CLI flag processing |
| Write permission | — | To create `.template` files and modify `.py` files |

Verification:
```bash
python3 -c "import ast, argparse, json, re, shutil, sys, pathlib; print('OK')"
```

## When to Use

- A script contains multi-line string constants that represent file content
  (e.g. `YAML_TEMPLATE = """..."""`, `GITIGNORE = "...\n..."`, etc.).
- You are authoring a new skill and want to follow the Template-as-SSOT pattern
  from the start.
- You are cleaning up an existing skill repository and want to migrate its scripts
  to external templates.
- You are running the [`skill-factory`](../skill-factory/SKILL.md) Post-Drafting
  Checklist and the Composition Audit step flags an embedded template.

## Operational Logic

### Step 1 — Scan target script

Run a dry-run scan to preview what will be extracted without modifying files:

```bash
python3 scripts/extract-template.py --dry-run path/to/script.py
```

Review the JSON output. Each entry shows the template variable name, the
proposed `.template` filename, and the action (`"action": "would_extract"`).
Variables skipped because the `.template` file already exist show
`"action": "skipped"` with a reason.

### Step 2 — Extract templates

Run without `--dry-run` to perform the extraction:

```bash
python3 scripts/extract-template.py path/to/script.py
```

For each template variable found, the script:
1. Writes the string content to `<script-dir>/<name>.template` (with the
   leading newline stripped so the file starts at column 1).
2. Creates a backup of the original script at `<script>.py.bak`.
3. Rewrites the script: removes the string assignment, adds
   `from pathlib import Path`, adds a `<VAR>_PATH = Path(__file__).parent / "<name>.template"`
   constant, and replaces references to `<VAR>` with `<VAR>_PATH.read_text()`.

### Step 3 — Force re-extract existing templates

If a `.template` file already exists and you want to overwrite it:

```bash
python3 scripts/extract-template.py --force path/to/script.py
```

### Step 4 — Batch process a skill directory

To process all scripts in a skill at once:

```bash
python3 scripts/extract-template.py --recursive .agents/skills/my-skill/
```

### Step 5 — Verify

1. Run the original script to confirm it still works (the `.read_text()` call
   should produce identical output to the original embedded string).
2. Open the `.template` file and confirm syntax highlighting works for the
   template format (YAML, markdown, etc.).
3. Delete the `.bak` file once satisfied:
   ```bash
   rm path/to/script.py.bak
   ```

### Ad-hoc flags

| Flag | Purpose |
|---|---|
| `--dry-run` | Preview changes without writing |
| `--force` | Overwrite existing `.template` files |
| `--recursive` | Search directories recursively for `.py` files |

## Output format

The script emits a JSON array to stdout:

```json
[
  {
    "template": "content.template",
    "var": "TEMPLATE",
    "action": "extracted",
    "size": 1234
  }
]
```

Exit code `0` if all extractions succeeded; `1` if any file had errors.

## Template File Conventions

| Variable Naming Pattern | Template File Name | Notes |
|---|---|---|
| `TEMPLATE = """..."""` | `content.template` | Generic default |
| `MARKDOWN_TEMPLATE` | `markdown.template` | Markdown content |
| `YAML_TEMPLATE` | `yaml.template` | YAML content |
| `GITIGNORE_CONTENT` | `gitignore-content.template` | `.gitignore` content |
| Any other `UPPER_CASE` | `<kebab-name>.template` | Variable name lowercased, underscores → hyphens |

Template files are plain text, placed alongside the script in `scripts/`.
They retain their original content without the leading newline.

## Related Skills

- [`skill-factory`](../skill-factory/SKILL.md) — defines the Template Extraction
  Mandate (§2.2.1.1.6) that this skill enforces.
- [`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md) —
  the decomposition pattern (scripts vs. prose) that this skill complements
  (templates vs. script logic).
- [`script-language-tier-port`](../script-language-tier-port/SKILL.md) — porting
  scripts between language tiers, a related script-craftsmanship skill.
- [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md) —
  automated audit for skill graph issues (duplicates, empty sections, missing
  bridges); run after template extraction to verify skill health.
- [`python-script-generation`](../python-script-generation/SKILL.md) — standards
  for the Python scripts that this skill modifies.

## SSOT Compliance

- The **Template Extraction Mandate** is defined in
  [`skill-factory` §2.2.1.1.6](../skill-factory/SKILL.md#2211-universal-script-mandates)
  — this skill does NOT redefine the mandate, it automates remediation.
- The **No-Embedded-Script Mandate** (prohibition on inline scripts in markdown)
  is defined in [`ai-rule-standardization-rules.md` §4](../../../ai-agent-rules/ai-rule-standardization-rules.md).
  This skill is its companion — templates must not be embedded in scripts either.
- The **Universal Script Mandates** are owned by
  [`skill-factory` §2.2.1.1](../skill-factory/SKILL.md#2211-universal-script-mandates).

## Related Conversations

- Template extraction workflow design and implementation — `docs/conversations/template-extraction-workflow.md`
  (pending redaction pass before commit).
