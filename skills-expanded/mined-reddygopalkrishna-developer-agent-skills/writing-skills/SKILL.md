---
name: writing-skills
description: Writes and improves Agent Skills (SKILL.md folders) that agents reliably load and follow. Use when the user asks to create, edit, review, or debug a skill, says a skill is not triggering or is ignored, or wants to turn a team workflow, checklist or runbook into a reusable skill. Not for writing general documentation.
license: MIT
---

# Writing Skills

A skill is instructions an agent loads only when its `description` matches the task. Most broken skills fail in one of two places: the description never triggers, or the body is too vague to change what the agent does. Fix those two first.

## When to use

- Creating a new skill from a workflow, checklist, runbook or style guide.
- A skill exists but the agent does not load it, or loads it for the wrong tasks.
- A skill loads but the agent's output does not change.
- Reviewing someone else's skill before adding it to a project.

Not for: project docs meant for humans (READMEs, wikis), or always-on rules that belong in a project instructions file such as `AGENTS.md`.

## Skill or something else?

| Need | Use |
| --- | --- |
| Rules that apply to every task in a repo | Project instructions file (`AGENTS.md` or the agent's equivalent) |
| A procedure needed only for some tasks | **A skill** |
| A deterministic, repeatable operation | A script or CLI (a skill may tell the agent to run it) |
| Live data from an external system | A tool / MCP server |

## Workflow

1. **Collect real examples first.** Get 3-5 concrete tasks the skill should handle and 2-3 nearby tasks it should not. Ask the user if you don't have them. Never write a skill from the topic name alone.
2. **Find what the agent gets wrong without the skill.** Run or reason through one example with no skill. The skill should contain only what closes that gap. Leave out what any competent agent already does.
3. **Write the description** (rules below). Check it against every example from step 1: it should clearly match the "should" tasks and clearly not match the "should not" tasks.
4. **Write the body** (structure below). Keep `SKILL.md` under about 300 lines. Move long tables, per-stack details and templates into `references/`.
5. **Test it.** Run each example task with the skill installed. Check that the agent loads it, follows the workflow, and meets the "Done when" criteria. Run one "should not" task and check it does not load.
6. **Fix what you saw**, not what you guess. If the agent skipped a step, make the step more concrete or move it earlier. If it loaded on the wrong task, tighten the description.

## Folder layout

```
skill-name/
├── SKILL.md          # required
└── references/       # optional: loaded only when SKILL.md says to
    └── topic.md
```

Optional `scripts/` or `assets/` folders are allowed by the format, but plain Markdown is the easiest for users to audit and trust. Add code only when a task must be exact and repeatable.

## Frontmatter

```yaml
---
name: skill-name
description: Does X. Use when ...
license: MIT
---
```

- `name`: lowercase letters, digits and hyphens; at most 64 characters; no leading, trailing or double hyphens; must match the folder name.
- `description`: required, at most 1024 characters. This is the only part the agent sees before deciding to load the skill.
- `name`, `description` and `license` work everywhere. Other fields (for example tool allowlists) are not supported by every agent, so leave them out of skills meant to be shared.

## Writing the description

- Start with what the skill does, in third person: "Plans zero-downtime schema migrations ...".
- Then `Use when ...` listing triggers: the task types, the words users actually type, file types, error messages, framework names.
- Add `Not for ...` when a nearby skill or task could be confused with it.
- Be specific. "Helps with databases" matches nothing reliably. "Use when adding, renaming or dropping columns, adding indexes, or backfilling data on a live database" matches the right tasks.

| Weak | Strong |
| --- | --- |
| Helps with testing. | Designs test suites and fixes flaky tests. Use when writing tests for new code, choosing unit vs integration vs e2e, or when a test fails intermittently in CI. |
| React best practices. | Applies modern React patterns ... Use when writing or reviewing React components, hooks, effects, or state management. |

## Writing the body

Structure (drop sections that add nothing):

1. `# Title` and 1-3 sentences with the core principle.
2. **When to use / when not to.**
3. **Workflow**: numbered, concrete, checkable steps.
4. **Decision tables and checklists** for the topic.
5. **Anti-patterns**: the mistakes that actually happen.
6. **Done when**: objective exit criteria.
7. **References**: each link with when to read it.

Rules:

- **Imperative and direct.** "Run X. If Y, do Z." Not "You might consider ...".
- **Concrete beats general.** Give the exact command, flag, threshold or code shape. A skill that says "write good tests" changes nothing.
- **Explain the why in one clause** for rules that look arbitrary, so the agent can handle cases you didn't list.
- **Decide for the agent.** Pick a default and say when to deviate. A list of five equal options leaves the agent where it started.
- **Safety gates.** Any destructive or outward-facing action (deleting data, force-pushing, deploying, sending messages) gets an explicit "stop and ask the user first".
- **Portable wording.** Say "run", "search the codebase", "read the file". Don't name tools that exist in only one agent.
- **No stale facts.** Avoid prices, model names and version numbers unless the skill is about that version. When a fact changes often, tell the agent where to check it.

## Progressive disclosure

- `SKILL.md` is loaded in full when the skill triggers, so every line costs context on every use.
- Put material needed only in some cases in `references/<topic>.md` and link it from `SKILL.md` with the condition, for example: `Read [references/mysql.md](references/mysql.md) when the database is MySQL.`
- Keep references one level deep. Don't chain reference files to each other.

## Review checklist

- [ ] Folder name equals `name`; name follows the format rules.
- [ ] Description says what it does and `Use when ...`, with real trigger words.
- [ ] Description was checked against "should" and "should not" examples.
- [ ] Body has a workflow of concrete steps and objective "Done when" criteria.
- [ ] Every command, flag and threshold is real; nothing invented.
- [ ] Destructive or outward actions have a confirmation gate.
- [ ] `SKILL.md` is under about 300 lines; details are in linked `references/`.
- [ ] No agent-specific tool names; no secrets, internal URLs or personal data.
- [ ] Tested on real tasks in at least one agent.

## Anti-patterns

- **Encyclopedia skill**: a long essay on the topic. The agent already knows the theory; give it the procedure and the decisions.
- **Vague description**: the skill never loads. Fix the description before touching the body.
- **Kitchen-sink skill**: one skill covering five unrelated tasks. Split it so each description can be precise.
- **Options without a default**: listing every approach with no recommendation.
- **Hidden side effects**: scripts that install, download or call the network without the skill saying so. Users stop trusting the whole pack.
- **Untested skill**: written and published without running a single real task.

## Done when

- The skill loads for every "should" example and not for the "should not" ones.
- On the test tasks, the agent's output is measurably better than without the skill (fewer mistakes, steps followed, criteria met).
- The review checklist above passes.
