# mykaia-web — Cursor instructions

## Three-role workflow

1. **Plan** — Agree scope and steps before large changes when Jeremy asks for a plan.
2. **Implement** — Execute one step at a time per the standing rules in `AGENTS.md`.
3. **Verify** — Run checks, confirm git/filesystem state, then commit and push.

## Branch policy

Work on `main` only. Do not create feature branches unless Jeremy explicitly asks.

## Commit and push per step

Every completed step: relevant checks pass, then commit, then push to `origin/main` of mykaia-web. Append a `docs/devlog.md` entry for that step before moving on.

## CDP

Live deployment to mykaia.app always requires Jeremy's separate explicit approval. Routine commit/push is not deployment.

## agents.mdc

`.cursor/agents.mdc` is read-only after Phase 0 creation. Do not edit it.
