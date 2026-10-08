---
name: fable-5-brain
description: >
  Scaffold and operate Fable 5 Brain, a source-cited Obsidian brain for Claude Fable 5 model and Claude Code harness ai operations and source-cited best practices.
  Use when the user says "fable-5-brain", "Fable 5 Brain", "create a Claude Fable 5 model and Claude Code harness ai operations and source-cited best practices brain",
  "import sources", "synthesize plan", "render report", or wants a persistent
  vault-backed operating system for Claude Fable 5 model and Claude Code harness ai operations and source-cited best practices.
argument-hint: "new | ingest | synthesize | report | visuals | lint | next"
license: Custom license
---

# Fable 5 Brain

Operate the vault first. Read `CODEX.md`, `wiki/hot.md`, and `wiki/index.md`
before changing notes.

## Commands

```bash
/fable-5-brain new <client-slug> --owner <name>
/fable-5-brain ingest --vault <path> --file <source>
/fable-5-brain synthesize --vault <path>
/fable-5-brain report --vault <path>
/fable-5-brain visuals --vault <path>
/fable-5-brain lint --vault <path>
/fable-5-brain next --vault <path>
```

Source checkout equivalent:

```bash
fable-5-brain new <client-slug> --owner <name>
fable-5-brain ingest --vault <path> --file <source>
fable-5-brain synthesize --vault <path>
fable-5-brain report --vault <path> --html-only
```

## Required Operating Rules

1. Read `<vault>/CODEX.md`.
2. Read `<vault>/wiki/hot.md`.
3. Read `<vault>/wiki/index.md`.
4. Preserve `.raw/` as immutable source material.
5. Never store credentials in the vault.
6. Never make domain-specific claims without dated trustworthy sources.
7. Keep `hot`, `index`, `overview`, and `log` current.
8. Record research evidence in `references/source-ledger.json`.
9. Record domain adapter completion in `references/adapter-manifest.json`.

## Script Mapping

- `new` -> `python scripts/scaffold_vault.py`
- `ingest` -> `python scripts/ingest_source.py`
- `synthesize` -> `python scripts/synthesize_brain.py`
- `report` -> `python scripts/render_brain_report.py`
- `visuals` -> `python scripts/generate_vault_visuals.py`
- `lint` -> `python scripts/lint_vault.py`
- `next` -> `python scripts/guide_next_action.py`

## Quality Gates

- No claim about Fable 5 behavior without a dated source or a verbatim quote from the export
- Never present folklore or contested guidance as evidence-based
- No irreversible recommendation without owner, confidence, source, and rollback note
- Do not call this brain market-ready unless the audit gate passes

Do not call this brain market-ready unless `scripts/audit_brain.py --require
market-ready` passes. A scaffold is not a finished brain.

## Research Refresh

14 days

## Community

Operator support and updates: https://www.skool.com/ai-marketing-hub-pro
