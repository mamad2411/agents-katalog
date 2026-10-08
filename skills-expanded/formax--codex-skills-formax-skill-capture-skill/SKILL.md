---
name: formax-skill-capture
description: Use when we want to turn a just-finished Formax workflow (e.g. commands, overlays, tools, hooks, permissions, UI parity) into a reusable Codex Skill under .codex/skills, including scaffolding, guardrails, and the minimum test checklist.
---

# Formax skill capture (create skills from our workflow)

## What this is

This skill is a **Formax-specific wrapper** around skill authoring: it helps us reliably convert “we just figured out how to do X” into a repo-local skill under `.codex/skills/<skill-name>/`.

It complements the built-in `skill-creator` (system skill) by adding Formax conventions:
- repo-local skills (checked into git)
- “where to change what” file map
- invariants (UI parity, model injection orthogonality, etc.)
- minimum regression tests to lock behavior

## When to use

Trigger this when the user says:
- “把这个流程沉淀成 skill”
- “以后别再忘了怎么改 /xxx”
- “给我一个复用的修改清单/固定套路”

## Minimal questions to ask (do not proceed until answered)

1) Skill name (kebab-case), e.g. `formax-slash-command-workflow`
2) 1–2 sentence description: **when** should Codex use it?
3) Scope: which subsystem? (pick one)
   - slash commands / overlays
   - tools (spec/handler/presenter)
   - hooks
   - permissions/policy
   - stability/input routing
4) Any explicit “don’t change” constraints? (UI copy/spacing/colors, contracts, etc.)

## Output requirements

The resulting skill must include:
- a short “Goal” section
- “Where to change what” (file list)
- “Patterns” (2–4 common patterns)
- “Tests to update” (minimum regression set)
- “Guardrails” (what must not regress)

Avoid long prose; prefer checklists.

## Create a new skill (scaffold)

Use the scaffold script:

```sh
bash .codex/skills/formax-skill-capture/scripts/new-skill.sh <skill-name> "<description>"
```

Then fill `SKILL.md` body with the content above.

## Refactor policy for skills

When a skill is created from a workflow we already shipped:
- **Do not broaden scope** (no extra features)
- **Do not rewrite UI** (unless explicitly requested)
- **Write/extend tests first** if behavior has regressed before

