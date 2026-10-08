---
name: wf-upgrade
description: Operator checklist for intentionally editing the Wave Framework or repo-local wave surfaces (Upgrade Wavefoundry). Framework maintenance only, never product code changes.
---

# Upgrade Wavefoundry

**Backwards-compatible operator phrases:** *Upgrade wave framework*, *Upgrade wave context* — same checklist.

Use this checklist when intentionally editing the wave framework or repo-local wave surfaces.

## Gate sequence

1. Read `AGENTS.md` and `docs/prompts/upgrade-wavefoundry.prompt.md`.
2. Produce a file-level patch plan and wait for operator approval before broad framework-maintenance edits.
3. Create or update `.wavefoundry/guard-overrides.json` before editing:
   - `.wavefoundry/framework/`
   - `docs/prompts/`
   - `AGENTS.md`
   - tracked hook config files
4. Set `framework_edit_allowed.enabled: true` after the operator approves the file-level plan.
5. Set `seed_edit_allowed.enabled: true` before editing any `.wavefoundry/framework/seeds/*.prompt.md` file.
6. Delete the override file or set both flags back to `false` when the maintenance pass is complete.

## Verification sequence

1. Run framework tests when the test suite is present (development installs only — not included in distribution packs): `python3 -B .wavefoundry/framework/scripts/run_tests.py` (skip if `run_tests.py` does not exist)
2. `wf render-surfaces` (hooks, MCP, bin launchers, and `render_agent_surfaces.py` when `docs/agents/guru.md` exists)
3. Backfill `AGENTS.md` auto-Guru tier-1 sections per `seed-050` when missing; ensure `docs/agents/guru.md` exists; re-run step 2 if tier-1 was just added
4. `./.wavefoundry/bin/wf docs-gardener` — native Windows: `.\.wavefoundry\bin\wf.cmd docs-gardener` (or MCP `wf_garden_docs`)
5. `./.wavefoundry/bin/wf docs-lint` — native Windows: `.\.wavefoundry\bin\wf.cmd docs-lint` (or MCP `wf_validate_docs`)

## Guardrails

- Keep inventory and drift-detection lanes read-only unless explicit write ownership was granted.
- Update existing canonical docs in place instead of creating parallel files when a topical home already exists.
- Preserve journals, personas, wave archives, and historical records unless the upgrade explicitly retires a live replacement surface.
