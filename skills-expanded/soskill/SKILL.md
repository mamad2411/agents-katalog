---
name: soskill
description: Aggregate and analyze Codex/OpenClaw skills across GitHub sources with deterministic scripts. Use when tasks involve fetching SKILL.md indexes from official or community repositories, generating skills snapshots (JSON/CSV/Markdown), printing source and repository statistics, bootstrapping local collection clones, organizing collection coverage reports, or running risk audits for suspicious skill content.
---

# Soskill

## Overview
Use this skill to build and maintain a structured skill index from multiple GitHub sources.

## Quick Start
Run from any directory and keep outputs outside the skill folder.

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/soskill"
OUT_DIR="${PWD}/soskill-output"
mkdir -p "$OUT_DIR"

# One command: fetch + stats + security audit
python3 "$SKILL_DIR/scripts/run_workflow.py" \
  --mode secure-refresh \
  --skill-dir "$SKILL_DIR" \
  --out-dir "$OUT_DIR"
```

Set `GITHUB_TOKEN` (or `GH_TOKEN`) when you need higher GitHub API limits.

## Workflow Selection
- One-command workflow (recommended): run `scripts/run_workflow.py`.
- Refresh aggregated skill index: run `scripts/fetch_skills.py`.
- Print quick totals and top repositories: run `scripts/print_stats.py`.
- Build collection readiness report from index data: run `scripts/organize_collections.py`.
- Clone/pull collection repos for offline scanning: run `scripts/bootstrap_collections.py`.
- Audit suspicious skill patterns (dangerous commands, prompt override, credential leakage): run `scripts/audit_skills.py`.

## Task Playbooks

### 1. One-command Workflow (Recommended)
```bash
python3 "$SKILL_DIR/scripts/run_workflow.py" \
  --mode secure-refresh \
  --skill-dir "$SKILL_DIR" \
  --out-dir "$OUT_DIR"
```

Modes:
- `refresh`: fetch + stats
- `secure-refresh`: fetch + stats + audit
- `full`: fetch + stats + audit + organize collections
- `offline`: bootstrap collections + local organize (requires existing skills snapshot)

Common flags:
- `--skills-input <path>`: use an existing `skills.json` for `offline`/organize stage.
- `--bootstrap-dry-run`: preview clone/pull actions in `offline`.
- `--top <N>`: control top repositories shown by stats output.

### 2. Fetch and Aggregate Skills
```bash
python3 "$SKILL_DIR/scripts/fetch_skills.py" \
  --config "$SKILL_DIR/references/sources.json" \
  --output "$OUT_DIR/skills.json" \
  --csv "$OUT_DIR/skills.csv" \
  --markdown "$OUT_DIR/latest.md"
```

Use `--max-skills <N>` to do a faster bounded run.

### 3. Print Summary Stats
```bash
python3 "$SKILL_DIR/scripts/print_stats.py" \
  --input "$OUT_DIR/skills.json" \
  --format markdown \
  --top 15
```

### 4. Organize Collection Coverage
```bash
python3 "$SKILL_DIR/scripts/organize_collections.py" \
  --seed "$SKILL_DIR/references/collections.seed.json" \
  --skills "$OUT_DIR/skills.json" \
  --output "$OUT_DIR/collections.json" \
  --markdown "$OUT_DIR/collections.md"
```

To include local clone scanning, add `--local-root <path>`.

### 5. Bootstrap Local Collections
```bash
python3 "$SKILL_DIR/scripts/bootstrap_collections.py" \
  --seed "$SKILL_DIR/references/collections.seed.json" \
  --local-root "$OUT_DIR/.cache/collections" \
  --manifest "$OUT_DIR/collections.bootstrap.json"
```

Use `--dry-run` to preview clone/pull actions without changing local repositories.

Offline orchestration example:

```bash
python3 "$SKILL_DIR/scripts/run_workflow.py" \
  --mode offline \
  --skill-dir "$SKILL_DIR" \
  --out-dir "$OUT_DIR" \
  --skills-input "$OUT_DIR/skills.json"
```

### 6. Audit Skill Safety Risks
```bash
python3 "$SKILL_DIR/scripts/audit_skills.py" \
  --input "$OUT_DIR/skills.json" \
  --output "$OUT_DIR/skills.audit.json" \
  --markdown "$OUT_DIR/skills-audit.md" \
  --min-risk-score 2
```

For deep scan, add `--fetch-content --max-skills 500`.

## References
- `references/sources.json`: source definitions for index fetching.
- `references/collections.seed.json`: tracked collection metadata and source mapping.
- `references/architecture.md`: pipeline structure and design intent.
- `references/collections.md`: collection status model and output semantics.
