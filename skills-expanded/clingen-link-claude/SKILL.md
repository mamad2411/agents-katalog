# CLAUDE.md

@AGENTS.md

Claude Code entrypoint:

- Use `AGENTS.md` for shared, repo-wide instructions (project areas, the
  snapshot/refresh workflow, coding standards, File Size Discipline).
- `make ci-local` is the gate — run it before final handoff.
- Use `uv` only; never `pip install`. Prefer `Makefile` targets.
- Do not hand-edit the snapshot bundle (`clingen_link/data/clingen.sqlite.zst`)
  or `tests/fixtures/`.
