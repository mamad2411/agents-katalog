---
name: skill-factory
description: Create / build / scaffold / add a NEW component to this plugin (agentic-forge) — a new skill, subagent/agent, or Python script — contract-first and evals-first, standard-compliant (agentskills.io), gated by the eval pyramid. ANY request to create or add a new skill / agent / script / workflow routes here, whatever the component is FOR — e.g. "create a skill for release notes", "scaffold an agent that reviews diffs for security"; that domain is the new component's purpose, and building the component is this skill's job (not release / security-review / code-review / develop). This is the meta-skill that builds everything else.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Skill Factory

Build agentic-forge components so they pass the gate the first time. The order is
non-negotiable: **contract -> evals -> implementation -> gate**. Never write a
component body before its `evals/evals.json` exists. Tier 0 enforces this; do not
rely on it — lead with it.

This is a maintainer skill of the agentic-forge repository (`.claude/skills/`, ADR 0105):
it does not ship, and every path below is relative to the repository root. The components
it builds ship in `plugin/`.

## When to use

Use this when adding any new component to the plugin: a workflow/router skill, a
sub-skill, a subagent role, or a shared Python script. Do not use it to *run* a
domain workflow (that is the workflow skill's job) or to edit unrelated code.

## Pick the component type

| Build a... | When | Author guide |
| --- | --- | --- |
| Skill | A workflow, procedure, or reusable knowledge Claude should load by description | [references/skill.md](references/skill.md) |
| Subagent | An isolated execution role (own tools/model) that skills delegate to | [references/agent.md](references/agent.md) |
| Script | Deterministic logic a skill runs; testable with pytest | [references/script.md](references/script.md) |

Default to a skill. Reach for a subagent only when isolation, a different model, or a
restricted toolset is needed. Reach for a script only when the work is deterministic
and better verified by tests than by an LLM.

For each type: read the author guide in `references/` for the rules, then copy the matching
file in `assets/` as the starting scaffold to fill in. Guides explain; templates are filled.

## The build process (always)

**A. Contract.** State, in one place: purpose (why it exists), inputs/outputs,
dependencies, and for skills the `should_trigger` / `should_not_trigger` prompt sets.
If purpose or triggers are unclear, ask the user when interactive; headless (no user to
ask), state the purpose and triggers you assume in the contract, proceed, and flag them in
the report.

**B. Evals first.** Copy [assets/evals.template.json](assets/evals.template.json) to
`<component>/evals/evals.json` and fill it in (superset format — see
[references/eval-loop.md](references/eval-loop.md)): `skill_name`, 2-3 realistic
`evals` with `assertions`, `component`, `thresholds`, and `triggers`. Do not write the
body yet.

**C. Implement.** Read the matching author guide, copy the template, and write the
component to the standard **at its canonical location**:

| Component | Lives at |
| --- | --- |
| Skill | `plugin/skills/<name>/SKILL.md` (+ `references/`, `assets/`, `scripts/`, `evals/evals.json`) |
| Subagent | `plugin/agents/<name>.md` + its contract `plugin/agents/evals/<name>.evals.json` |
| Shared script | `plugin/lib/agentic_forge/<name>.py` + pytest under `tests/` (pytest is the script's contract; a `script`-type evals.json is reserved for future use) |
| Skill-specific script | `plugin/skills/<skill>/scripts/`, referenced via `${CLAUDE_SKILL_DIR}` |

Keep skill bodies under 500 lines and push detail into `references/`.

**D. Gate.** Run the eval pyramid (see [references/eval-loop.md](references/eval-loop.md)):
Tier 0 (`python dev/validate.py` + `pytest` + `ruff` + `mypy`), then for skills the
skill-creator loop -> `benchmark` -> `gate`. Iterate in a bounded review loop until
every applicable threshold passes. Record the final numbers.

**E. Finish.** Confirm the whole gate is green, summarize the metrics achieved versus
thresholds, and hand off for commit. Do not mark a component done while any tier fails.

## Definition of done

- Tier 0 green: `dev/validate.py`, `pytest`, `ruff`, `mypy` all pass.
- `evals/evals.json` present and valid against `plugin/schemas/evals.schema.json`.
- Tier 1 (skills): recall and specificity meet `thresholds.tier1_trigger`.
- Tier 2 (skills/agents): pass-rate lower bound meets `thresholds.tier2_quality`.
- All persisted content in English; relative runtime paths only.

## Conventions

Router discipline: keep the set of always-on, model-invocable skills small and their
descriptions sharp; depth lives in `references/`. One source of truth per component:
the readiness contract is `evals/evals.json`, the behavior is `SKILL.md`.
