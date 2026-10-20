# AGENTS.md — p3if docs/

## Layout

Topic-organized tree: `concepts/`, `guides/`, `tutorials/`, `technical/`,
`examples/`, `api/`, `diagrams/`, `visualization/`, `website/`, plus top-level
`README.md`, `FAQ.md`, `LLM_DEVELOPMENT_GUIDE.md`. `docs/README.md` is the entry.

## Key modules (from repo root)

- `src/` — p3if library implementation (see `technical/architecture.md`, `technical/data_model.md`).
- `scripts/`, `examples/`, `data/`, `outputs/` — orchestration, samples, artifacts.

## Conventions observed

- Root `.cursorrules` and `CLAUDE.md`/`PAI.md` carry agent conventions; consult before code changes.
- Docs links are relative; keep them verified against actual filenames (several
  aspirational links previously pointed at nonexistent pages — they are now marked
  "needs owner input" rather than left broken).

## Maintenance

Hand-maintained. When adding a guide or tutorial, register it in `docs/README.md`
and the FAQ navigation. `docs/manuscript/MANUSCRIPT_STATUS.md` records the
manuscript posture for this repo.
