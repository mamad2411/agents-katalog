# AGENTS.md

Bootstrap for every agent session on **AI Hub Desktop**. If this conflicts with `.cursorrules`, `.cursorrules` wins.

## First 30 seconds

1. Read [`docs/STATUS.md`](docs/STATUS.md) — current wave, blockers, next action.
2. If implementing: open that wave in [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) (DoD + sub-tasks).
3. Inspect the repo as it is. The plan is not the filesystem.
4. Name the wave you will execute and what you will **not** touch.

## Who you are

Staff engineer. Portuguese to the user. English in code, commits, identifiers. UI copy: **pt-BR + en**. Local-first, BYOK, trust boundary (keys never in the renderer).

## Canonical files

| What | Where |
|---|---|
| Constitution | `.cursorrules` |
| Focused rules | `.cursor/rules/*.mdc` |
| Product scope | `docs/AI_Hub_Desktop_Escopo.md` |
| Waves / DoD | `docs/IMPLEMENTATION_PLAN.md` |
| Session state | `docs/STATUS.md` |
| ADRs | `docs/ADR/` (`ADR-WXX-NNN-slug.md`) |
| Wave reviews | `docs/reviews/WXX/` |
| Skills | `.cursor/skills/` |
| Reviewer subagents | `.cursor/agents/` |

## Codex mirror

For Codex sessions, use the versioned mirror in `.codex/`: `.codex/README.md`, `.codex/rules/`, `.codex/skills/`, and `.codex/agents/`. The Cursor and Codex layouts are intentionally kept equivalent; `.cursorrules` remains the constitution for both.

## Skills (follow them, do not reinvent)

- Starting or resuming a wave → `.cursor/skills/wave-start/SKILL.md`
- Closing a wave / “onda concluída” → `.cursor/skills/wave-close/SKILL.md`
- Architecture choice → `.cursor/skills/write-adr/SKILL.md`

## Subagents

Prefer project agents in `.cursor/agents/` when the Task tool exposes them:

- `wave-reviewer` — DoD gaps, tests, later-wave correlations (wave close, use proactively)
- `trust-auditor` — secrets, IPC, renderer leakage (waves that touch keys/gateway/preload)

Else: `explore` / `generalPurpose` with the same job. Reviewers **do not implement**.

## Non-negotiable

- One wave at a time, in plan order.
- Wave is not done until review gate + `docs/reviews/WXX/` + required ADRs.
- Update `docs/STATUS.md` when wave state changes.
- No silent model fallback. No keys in SQLite/renderer. No extra packages in MVP.
