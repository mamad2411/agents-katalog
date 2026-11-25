---
name: mvp-workflow
description: Orchestrate a Codex-first Web MVP planning workflow from rough idea to build-ready artifacts. Use when the user wants to turn an app idea into a structured MVP plan, PRD, technical blueprint, AGENTS.md context, and implementation tickets.
---

# MVP Workflow

Guide the user through the full Web MVP Blueprint workflow.

## Workflow

1. **Idea Brief** - clarify the first user, problem, smallest useful outcome, and MVP boundary.
2. **Evidence Research** - collect competitor, user, pricing, and feasibility evidence.
3. **Buildable PRD** - define pages, features, data objects, acceptance criteria, and success metrics.
4. **Technical Blueprint** - choose a practical stack and implementation route.
5. **Agent Context** - generate `AGENTS.md` and `agent_docs/`.
6. **Build Tickets** - generate task files that Codex can execute one at a time.

## State Check

Inspect the current project before choosing the next step:

| Artifact | Meaning |
|---|---|
| `docs/IdeaBrief-*.md` | Step 0 complete |
| `docs/EvidencePack-*.md` | Step 1 complete |
| `docs/BuildablePRD-*.md` | Step 2 complete |
| `docs/TechBlueprint-*.md` | Step 3 complete |
| `AGENTS.md` and `agent_docs/` | Step 4 complete |
| `tasks/*.md` | Step 5 complete |

## Routing

- If no idea brief exists, use `$mvp-idea-brief`.
- If idea brief exists but no evidence pack exists, use `$mvp-research`.
- If evidence exists but no buildable PRD exists, use `$mvp-prd`.
- If PRD exists but no technical blueprint exists, use `$mvp-tech-design`.
- If technical blueprint exists but no agent context exists, use `$mvp-agent-context`.
- If agent context exists but no task tickets exist, use `$mvp-build-tickets`.

## Rules

- Keep the user oriented with the current step and next artifact.
- Ask one question at a time when inputs are missing.
- Favor small Web MVP scope over broad product ambition.
- Preserve explicit "Not in MVP" decisions.
- Do not start implementation until agent context and tickets exist, unless the user explicitly skips planning.
