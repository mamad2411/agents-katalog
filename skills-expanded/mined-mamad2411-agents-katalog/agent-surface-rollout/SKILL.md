---
name: agent-surface-rollout
description: Roll out a repository change consistently across cross-agent instruction surfaces. Use this whenever a change in this repository should be reflected across `.agents/skills`, `AGENTS.md`, `GEMINI.md`, `.github/`, `.windsurf/`, and README so that Codex, Copilot, Windsurf, Gemini CLI, and other agents stay aligned.
---

# Agent Surface Rollout

Use this skill when the task is not just "edit one file" but "make the repo's agent-facing surfaces line up."

## When to use

Use this when:

- a new skill should appear in examples
- repo-wide guidance changed
- Copilot and Windsurf examples drifted from the source skill
- `.agents/skills` needs to mirror a useful repository workflow

## Workflow

1. Find the source-of-truth change under `skills/` or root instruction files
2. Decide which agent surfaces are affected
3. Apply only the necessary updates to:
   - `.agents/skills/`
   - `AGENTS.md`
   - `GEMINI.md`
   - `.github/`
   - `.windsurf/`
   - `README.md`
4. Keep each surface scoped to its job

## Read These Files As Needed

- `references/surface-selection.md`
- `references/rollout-checklist.md`

## Rules

- Do not duplicate long workflow text everywhere
- Keep native surfaces idiomatic for their tool
- Mention any verification limits clearly
