---
description: "Scan for stale docs, count drift, quality issues, and tech debt across the ALZ accelerator."
agent: orchestrator
---

# Doc Gardening

Scan the repository for documentation entropy and report findings.
All entity counts must come from filesystem globs via the `count-registry` skill — never hard-code numbers.

## Tasks

1. **Stale documentation** — Check modification dates on key docs. Flag files not
   updated in >60 days:
   - `README.md`, `AGENTS.md`, `docs/*.md`, `docs/accelerator/*.md`
   - `site/src/content/docs/**/*.mdx`
   - `.github/copilot-instructions.md`

2. **Count drift** — Read `.github/skills/count-registry/SKILL.md` for the canonical
   counting methodology. Verify these counts match what's stated in docs:
   - Agent count (`.github/agents/*.md` excluding `_subagents/`)
   - Subagent count (`.github/agents/_subagents/*.md`)
   - Skill count (`.github/skills/*/SKILL.md`)
   - Tool count (`src/tools/*.py` excluding `__init__.py`)
   - Test count (`python -m pytest tests/ --collect-only -q | tail -1`)
   - Workflow count (`pipelines/github-actions/*.yml`)
   - WARA check count (sum of `grep -c "  - id:" src/config/wara_checks/*.yaml`)

   Scan these files for hardcoded numbers that may have drifted:
   - `README.md`, `AGENTS.md`, `.github/copilot-instructions.md`
   - `docs/guide.html`, `docs/workflow.md`, `docs/accelerator/architecture.md`
   - `site/src/content/docs/index.mdx`, `site/src/content/docs/reference/agents.mdx`
   - `site/src/content/docs/reference/tools.mdx`, `site/src/content/docs/reference/pipelines.mdx`

3. **Skill variant coverage** — Verify every skill directory has all 3 files:
   - `SKILL.md` (full)
   - `SKILL.digest.md` (compressed)
   - `SKILL.minimal.md` (minimal)
   Report any skills missing digest or minimal variants.

4. **Agent registry alignment** — Compare `tools/registry/agent-registry.json` entries
   against actual `.github/agents/*.md` files. Flag mismatches (missing entries,
   extra entries, wrong skill references).

5. **Cross-reference integrity** — Check that:
   - All agents referenced in `AGENTS.md` have corresponding `.github/agents/*.md` files
   - All skills listed in `.github/copilot-instructions.md` have corresponding skill directories
   - All workflows referenced in docs exist in `pipelines/github-actions/`

6. **Design doc status markers** — Scan `docs/*.md` for status headers containing
   "Planned", "Proposed", "Draft", or "In Progress" that should now say "Implemented"
   or "Completed".

## Output

Report findings to the user as a prioritized table:

| Priority | Category | File | Issue | Fix |
|----------|----------|------|-------|-----|
| P0 | Count drift | ... | Says X, actual Y | Update to Y |
| P1 | Stale doc | ... | Last modified N days ago | Review and refresh |
| P2 | Missing variant | ... | No SKILL.digest.md | Generate variant |

Do NOT auto-fix anything — present findings for user approval first.
