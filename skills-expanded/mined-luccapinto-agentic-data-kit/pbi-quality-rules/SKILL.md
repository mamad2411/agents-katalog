---
name: pbi-quality-rules
description: Validate a Power BI semantic model with the Best Practice Analyzer (BPA) — the real engine via the free Tabular Editor 2 CLI, or a Python fallback over TMDL when TE2 is not installed — using the shareable bpa-rules.json. Use when asked to lint, audit, check or validate a model, after significant model changes, and before publishing.
---

# Skill: pbi-quality-rules

Two scripts in this skill's `scripts/` folder (Python 3.9+, standard library only):

| Script | What it does |
|---|---|
| `run_bpa.py <model>` | Runs the real BPA through **Tabular Editor 2** (`TabularEditor.exe <definition-folder> -A bpa-rules.json -V`). If TE2 is not found, it runs the fallback and says so. |
| `bpa_fallback.py <model>` | The same rules re-implemented in Python over the TMDL files (or `model.bim`). Approximate; rules it cannot evaluate are listed as `SKIPPED`, never as passed. |

`<model>` = the `.pbip`, the project folder, `<Name>.SemanticModel/`, its `definition/` folder,
or a `model.bim`. Options: `--format json`, `--rules <file>`, and for `run_bpa.py` also
`--te <path>` and `--no-fallback`. TE2 is looked up via `--te`, `$TABULAR_EDITOR_PATH`, `PATH`,
then the default Windows install folders.

Exit codes: `0` no error-severity violations · `1` errors found · `2` bad path / TE2 failed.

## Run it
```bash
python3 <skill>/scripts/run_bpa.py path/to/Sales.pbip
```
1. **Disk is the input.** With Desktop open and MCP edits pending, ask the user to save (Ctrl+S)
   first — the BPA reads the TMDL Desktop wrote, not the live model.
2. Present **errors first**, then warnings, grouped by category; omit info unless asked. Say
   which engine ran; for the fallback, recommend installing Tabular Editor 2 for exact results.
3. For each `error`, offer a fix (through the Modeling MCP when Desktop is open — see
   `pbi-semantic-layer-tmdl`). Warnings: suggest, don't force.

## Rule set — `bpa-rules.json`
Tabular Editor's native format (`ID`, `Name`, `Category`, `Severity`, `Scope`, `Expression` in
Dynamic LINQ over the TOM). Severity `3` error · `2` warning · `1` info. It loads directly into
TE2's BPA window too.

Adding a rule: add it to `bpa-rules.json` (TE2 picks it up at once), then add a predicate with the
same `ID` to `CHECKS` in `scripts/bpa_fallback.py` so the fallback covers it; until then the
fallback reports it as `SKIPPED`.

## In CI
Run `run_bpa.py --no-fallback --format json` on a Windows runner with TE2 (fails on exit 1), or
`bpa_fallback.py --format json` anywhere for a lighter gate.
