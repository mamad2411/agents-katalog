---
name: rh-corpus-search
description: >-
  Search the RH semantic catalog before proposing or starting any RH mechanism,
  when a user pastes an external RH proposal, or when an RH round finishes.
  Surfaces prior kills, open edges, and reusable assets via rhcat. Use when
  the task mentions RH, Weil, L*, Mellin–Pick, Hilbert–Pólya, or a new
  tfpt-discovery probe.
---

# RH corpus search

`rh/catalog/` is a **semantic** index of the RH corpus. It is research
documentation — **no RH claim** in either direction.

Generated (never hand-edit): `rh_semantic_catalog.json`, `INDEX.md`, `stats.json`.
Hand-edit only `taxonomy.json`, `schema.json`, and `fragments/`.

## When to use

1. Before proposing or starting any RH mechanism, probe, or round.
2. When a user pastes an external RH proposal.
3. When an RH round finishes (write a fragment, then continue `rh-sync`).

## Grep → select → read

Never read `rh/README.md` whole (hook-blocked, ~680 KB). Never dump `INVENTORY.json`.

1. `python3 rh/catalog/rhcat.py search '<regex>'` or `family` / `kills` / `open`.
2. Select ≤ 3 round ids or paths from the compact hits.
3. Read only those probes / result JSON / the README window in `readme_lines`.
4. Cite **round ids** and **failure_class**, not paraphrases of the README.

## rhcat

```bash
python3 rh/catalog/rhcat.py search <regex>
python3 rh/catalog/rhcat.py family <id>
python3 rh/catalog/rhcat.py kind <id>
python3 rh/catalog/rhcat.py kills [--class X]
python3 rh/catalog/rhcat.py open
python3 rh/catalog/rhcat.py reusable [--family X]
python3 rh/catalog/rhcat.py dossier <round|path>
python3 rh/catalog/rhcat.py stats
python3 rh/catalog/rhcat.py check-new "<mechanism description>"
python3 rh/catalog/rhcat.py semsearch "<query>" [--k 10]
python3 rh/catalog/rhcat.py todo
python3 rh/catalog/rhcat.py new <path>
```

`--json` for machine output. Default lines clip at 120 chars.
`kills` / `open` / `reusable` / `check-new` default to curated-only; pass `--include-drafts` to opt in.
Enums live in `rh/catalog/taxonomy.json`.
Drafts: `python3 rh/catalog/autodraft.py`. Rebuild: `python3 rh/catalog/build_catalog.py`.
Audit: `python3 rh/catalog/build_catalog.py --check`.

## LLM helpers (optional)

Key never enters the repo. Set `OPENAI_API_KEY` or `OPENAI_API_KEY=...` in
`~/.config/tfpt/openai.env` (chmod 600). Repo `.env` only if gitignored.
`semsearch` is cosine over `rh/catalog/embeddings/` (keyword fallback if absent).
`autodraft.py --llm --only-new` fills draft semantic fields; `needs_review` stays
true; curated `part_*.json` is never overwritten. `llm_consistency.py` classifies
all records (cached) and writes disagreements; default stops if the estimate is
≥ $5. `build.sh gen` runs `--llm` + embeddings only when `TFPT_LLM_CATALOG=1`
and the key resolves. Hard budget default $5; cached hits are free. Audit is offline.

## Cite rounds and kill classes

- Round: `r645`, never a prose alias.
- Kill: `failure_class` ∈ {CIRCULAR, WORLD_BLIND, LOSSY_CONSTANT, STRUCTURAL_MISMATCH, NUMERIC_ARTIFACT, ORACLE_LEAK, RESTATEMENT, NO_BRIDGE, UNCONVERGED}.
- Status level lives in `solved` (`[E]`/`[C]`); the ledger wins on disagreement.

## Workflow

Start of RH work:

1. `python3 rh/catalog/rhcat.py stats`
2. `python3 rh/catalog/rhcat.py check-new "<idea>"`
3. `python3 rh/catalog/rhcat.py kills --class …` for the matching failure class.

End of a round:

1. `python3 rh/catalog/rhcat.py new <probe>` (skeleton from auto-draft).
2. Complete the fragment (schema `rh/catalog/schema.json`); set `confidence` / drop `needs_review`.
3. `python3 rh/catalog/build_catalog.py` — report counts before any other edit.
4. Continue `rh-sync` (INVENTORY, `run_rh.py`, README).

Weekly: `python3 rh/catalog/rhcat.py todo` and curate leftover drafts.

`auto_drafts.json` is GENERATED. Curated `part_*.json` override it. Do not hand-edit generated catalog files.

## Viewer

Exploration UI (no RH claim). After catalog rebuild:
`cd rh/catalog/viewer && npm install && npm run build-data && npm run dev`
Preview: `npm start`. Headless export check: `npm run export`.

## Hard rule

No proposal may be launched if `rhcat check-new` surfaces a KILLED record of the same family with failure_class in {CIRCULAR, WORLD_BLIND, LOSSY_CONSTANT, RESTATEMENT} unless the proposal states explicitly how it differs.

## Concept map

Use the typed map before proposing a cross-family bridge or renaming a known
criterion:

```bash
python3 rh/catalog/map/rhmap.py equivalents
python3 rh/catalog/map/rhmap.py gaps
python3 rh/catalog/map/rhmap.py path <concept-a> <concept-b> --avoid-killed
python3 rh/catalog/map/rhmap.py show <concept-id> --json
```

Check `gaps` and a non-killed `path` after `rhcat check-new`; cite edge sources,
and never treat `HEURISTIC`/`STATISTICAL` links as mathematical implications.
