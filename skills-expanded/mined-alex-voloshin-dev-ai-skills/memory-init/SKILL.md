---
name: memory-init
description: Use this skill when bootstrapping memory in a freshly cloned repo or when upgrading from a pre-memory plugin version — to initialize the .ai-skills-memory/ skeleton in the current project (directory structure, .gitignore rules, learnings.md template, .committed/ allowlist). Idempotent — safe to re-run on a project that already has memory wired.
context: fork
argument-hint: ""
---

# /memory-init — Memory Skeleton Initializer

Create the `.ai-skills-memory/` directory tree from `plugin/memory/templates/`. Idempotent. Layer model and write rules: `plugin/docs/concepts/memory.md`.

## When to use

- After cloning a repo that uses ai-skills but has no `.ai-skills-memory/` (first run on a fresh checkout)
- After upgrading the plugin to a version that adds new memory paths
- When `/plugin-doctor` reports "no memory tree present"

Not needed when running `/ai-skills-init` — that workflow runs memory-init as one of its steps.

## Behavior

1. Detect current project root (`<repo>` = the cwd where the user runs the command).
2. Check for existing `.ai-skills-memory/`:
   - If missing → create
   - If present → no-op for existing files; create only what is missing (idempotent)
3. Create directory tree:
   ```
   <repo>/.ai-skills-memory/
   ├── .gitignore               (from plugin/memory/templates/ai-skills-memory.gitignore)
   ├── learnings.md             (empty header template)
   ├── runs.jsonl               (touch-create, append-only)
   ├── errors.log               (touch-create, append-only)
   ├── redactions.log           (touch-create, append-only)
   ├── sessions/                (per-session subdirs created by hooks)
   ├── ralph/                   (per-RALF-run subdirs)
   ├── pending-flush/           (PreCompact flush markers)
   ├── designs/                 (/feature-design output summaries)
   ├── env-reports/             (/env-analyze baselines)
   ├── refactor/                (/refactor logs)
   ├── migrate/                 (/migrate plans)
   ├── spikes/                  (/spike reports)
   ├── security-audits/         (/security-audit findings)
   ├── docs/                    (/docs-pack generation summaries)
   ├── knowledge-sync/          (/knowledge-sync per-run logs + run-lock)
   └── .committed/
       ├── README.md            (from plugin/memory/templates/committed-readme.md)
       ├── .allowlist-extensions.txt   (project-extension allowlist, empty by default)
       ├── conventions.md       (from plugin/memory/templates/conventions-schema.md, empty body)
       └── learnings.md         (committed-learnings template, empty body)
   ```
4. Append `.ai-skills-memory/` rule to `<repo>/.gitignore` if not already present.
5. Print summary: created vs skipped paths.

## Hard rules

- **Never overwrite** existing files. If a file exists, skip it and report "skipped: <path>".
- **Never write to `.committed/` paths outside the allowlist** — `pre-tool-use-committed-write.py` hook enforces this; the skill must not bypass.
- **PII filter applies** to any seeded content per `memory-discipline.md` rule 2.

## Failure modes

- **No write permission in cwd:** report error, suggest `cd` to a writable directory or run with elevated permissions.
- **Existing `.ai-skills-memory/` corrupted (bad JSON, bad allowlist):** flag corrupted files but do not delete or rewrite them. Suggest user inspect and back up before re-running.

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | On first init | `.ai-skills-memory/init-summary.md` — timestamp + version + paths created |

## Integration

- **Templates source**: `${CLAUDE_PLUGIN_ROOT}/memory/templates/` (7 files: ai-skills-memory.gitignore, committed-allowlist.txt, committed-readme.md, conventions-schema.md, eval-baseline.schema.json, learnings-schema.md, untrusted-content-wrapper.md). PII pattern file lives separately at `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/pii-patterns.txt` because the secret-scan + memory-curator hooks load it directly.
- **Called by**: `/ai-skills-init` (full bootstrap including memory), used standalone for upgrades
- **Rules**: `memory-discipline` (write rules per layer), `memory-validation` (entry validation)
- **Hooks**: `pre-tool-use-committed-write.py` validates `.committed/` writes against allowlist
- **Layer model**: `plugin/docs/concepts/memory.md` documents the L0–L5 layers. This skill creates L3 dirs (`sessions/`, `ralph/`) and L4 files (`learnings.md`, `runs.jsonl`, etc.) inside `.ai-skills-memory/`.
