---
name: dissertation-agent-architecture-audit
description: Audit the dissertation agent's rule stack, memory layers, skill routing, tool discipline, window separation, persistence, and output gates for conflicts, stale context, hidden assumptions, or maintenance risk.
---

# Dissertation Agent Architecture Audit

Use this skill for deeper maintenance audits of the dissertation agent system, especially when rules conflict, behavior degrades, the user reports unreliable outputs, or new skills/workflows are added.

## Purpose

Adapt ECC agent-architecture audit to a local dissertation workflow. This is not a software production audit. It checks whether the current rules, skills, memory files, and window roles are coherent and source-grounded.

## Architecture Layers To Audit

| Layer | Dissertation Version | Common Failure |
|---|---|---|
| 1 | System/developer instructions | conflicts with project rules or window role |
| 2 | Current chat history | old task dominates current request |
| 3 | `AGENTS.md` | skill list or workflow outdated |
| 4 | `PROJECT_AGENT_PREFERENCES.md` | preferences duplicate or conflict with skills |
| 5 | `.agents/skills/` | overlapping triggers, missing frontmatter, stale rules |
| 6 | `research-wiki/TASK_STATE.md` | stale next action or missing handoff |
| 7 | knowledge-base / Obsidian | duplicate facts, broken links, unclear source of record |
| 8 | tool surface | browser, Word renderer, LMS, Obsidian, connectors assumed but not verified |
| 9 | output style rules | final answer shape conflicts with task need |
| 10 | persistence | local files, memory notes, and generated documents disagree |

## Audit Workflow

1. Define the symptom or audit scope.
2. Read only relevant files first:
   - `AGENTS.md`
   - `PROJECT_AGENT_PREFERENCES.md`
   - `research-wiki/TASK_STATE.md`
   - `research-wiki/WINDOW_WORKFLOW_PROMPTS.md`
   - relevant `SKILL.md` files
3. Map findings to the layer above.
4. Rank findings by severity:
   - `critical`: can produce wrong formal or ethical output
   - `high`: likely to cause repeated workflow failure
   - `medium`: creates confusion or duplicated effort
   - `low`: minor maintainability issue
5. Recommend minimal fixes.
6. Update `TASK_STATE.md` after confirmed rule changes.

## Findings Format

```text
Finding:
- Severity:
- Layer:
- Evidence:
- Risk:
- Fix:
- Affects Production Window: yes/no
```

## Default Fix Order

1. Remove or clarify conflicting rules.
2. Restore source-first and document-quality gates.
3. Clarify window role separation.
4. Update skill routing in `agent-orchestration`.
5. Update shared memory and task-state handoff.
6. Record residual risk.

## Guardrails

- Do not blame the model before checking wrapper/rule/memory layers.
- Do not rewrite many skills at once unless the defect is systemic.
- Do not edit dissertation content files unless the audit specifically concerns them and the user authorizes it.
- Do not treat a clean current state as proof that an earlier failure never happened.
