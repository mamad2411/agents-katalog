# CLAUDE.md — engram-spira

All engineering rules for this repo live in **[AGENTS.md](AGENTS.md)**, which is imported below. Do not duplicate rules here — edit `AGENTS.md` so every agent gets the change.

@AGENTS.md

---

## Claude Code specifics

### Use CodeGraph before grep

This repo has a `.codegraph/` index. Reach for it **before** grep/find or reading files when locating or understanding code:

- `codegraph_explore` (MCP tool) — one call returns the relevant symbols' verbatim line-numbered source plus the call paths between them, including dynamic-dispatch hops grep cannot follow. Name a file or symbol to read its current source.
- `codegraph explore "<question or symbols>"` (shell) — same output, always available.

A direct CodeGraph answer is typically 1–3 calls; the equivalent grep/read loop is dozens. Do not delegate a lookup to a file-reading subagent that CodeGraph already answers.

`.codegraph/` is gitignored — it is a local index, never commit it.

### Verification is not optional

`AGENTS.md` §4 lists the three commands. Run them and quote real output before saying anything passes. **The baseline is currently green; always re-measure with the three commands in `AGENTS.md` §4** — capture it *before* your change so you can prove you did not add to it. Never report success from reasoning alone.

### Reading the docs

`AGENTS.md` §6 maps task → file under [docs/agents/](docs/agents/). Load only the file your task touches; each is self-contained and exhaustive. When a `docs/agents/` file disagrees with the code, the code wins — fix the doc in the same change.

### Docs that will mislead you

`README.md`, `docs/srs/`, `docs/project_report.md`, `docs/dev_prompt/*`, `docs/ui/design.md`, `docs/c4/`, `docs/erd/` are stale (see `AGENTS.md` §1). They are kept for history and because the in-app `/docs` page serves some of them. Treat them as archaeology, never as specification, and never copy a count, model name, or paste-ready snippet out of `docs/dev_prompt/`.

### Writing new docs

`.gitignore` ignores `/skills` (root-only — the vendored `ui-ux-pro-max` clone). `docs/superpowers/` is tracked: specs in `docs/superpowers/specs/`, plans in `docs/superpowers/plans/`. `.agents/skills/` is trackable and holds real skill packs (`elysiajs`, `solid-js-best-practices`) — do not confuse it with the ignored root folder. Write agent docs to `docs/agents/`, `docs/<topic>/`, `.agents/workflows/`, or the root `CLAUDE.md`/`AGENTS.md` — and confirm any new path with `git check-ignore -v <path>` first.

### Scope discipline

The repo has pre-existing defects and dead code catalogued in [docs/agents/known-issues.md](docs/agents/known-issues.md). Do not fix them as drive-by work — each entry is tagged with whether it is safe to touch. Fixing the Eden type collapse or deleting the dead `components/layout/` tree are real, worthwhile changes, but they are their own task and need their own decision.
