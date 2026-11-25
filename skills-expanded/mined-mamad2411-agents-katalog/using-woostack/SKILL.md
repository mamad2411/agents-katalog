---
name: using-woostack
description: Use when starting work in a project that references woostack from its root AGENTS.md, or when deciding whether a woostack skill or command applies before answering, editing, scaffolding, reviewing, or addressing PR feedback.
---

# using-woostack

<SUBAGENT-STOP>
If you were dispatched as a subagent for a narrow task, follow the dispatch prompt first.
Use this skill only when the prompt asks you to apply project-level woostack rules.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
When a project root `AGENTS.md` references woostack, treat that file as the project
authority. Load and follow its woostack rules before taking action.

This skill teaches rule loading and command routing only. It does not initialize,
scaffold, edit, review, or push anything by itself.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Follow instructions in this order:

1. The user's explicit request and the project's root `AGENTS.md`.
2. The specific woostack skill that applies to the task.
3. Other installed process or implementation skills.
4. Default agent behavior.

If `AGENTS.md` and a woostack skill disagree, prefer `AGENTS.md` and state the conflict
briefly when it matters to the work.

## The Rule

Before answering or acting in a woostack project, check whether a woostack rule or command
applies. If it does, load the specific woostack skill before proceeding.

Do not summarize the intended workflow from memory when the skill is available. The current
`SKILL.md` is the source of truth.

## Project Entry Check

At the start of work in a repository:

1. Read the root `AGENTS.md` if it exists.
2. If it references woostack, follow its woostack section as binding project policy.
3. Check whether the user's request maps to one of the woostack skills below.
4. Load the mapped skill before asking clarifying questions, making edits, opening PRs, or
   posting review feedback.

Do not run `/woostack-init`, create `.woostack/`, scaffold code, or add config unless the
user explicitly asks for that behavior or the loaded task-specific skill requires it as part
of an approved workflow.

**Feature-state invariant:** in a woostack project, every spec has exactly one plan
(`spec : plan : PRs = 1 : 1 : N`), and the spec's `status:`/`branch:` frontmatter is
load-bearing for the `/woostack-status` board. The phase enum and the join contracts are
defined once in
[`../woostack-status/references/conventions.md`](../woostack-status/references/conventions.md);
link it, never restate it.

## Command Routing

| Request | Load |
|---|---|
| `/woostack-init [path]`, initialize or repair the `.woostack/` workspace | `woostack-init` |
| `/woostack-bootstrap <goal>`, scaffold a new web/mobile/API project | `woostack-bootstrap` |
| `/woostack-build <goal>`, build a feature through the woostack loop | `woostack-build` |
| `/woostack-plan <spec-path>`, write the implementation plan for an approved spec as PR-sized increments | `woostack-plan` |
| `/woostack-execute <plan-path> [--inline\|--subagent]`, execute an approved plan as PR-sized stacked increments (inline or subagent-driven) | `woostack-execute` |
| `/woostack-commit`, commit session-relevant changes and update PR fields | `woostack-commit` |
| `/woostack-review [PR#]`, review a PR or local diff | `woostack-review` |
| `/woostack-address-comments [PR#]`, address unresolved review threads | `woostack-address-comments` |
| `/woostack-status [--all] [--fetch]`, show the derived feature board (what's in flight, what to do next) | `woostack-status` |
| `/woostack-visualize <source> [for <audience>]`, render a source as audience-tailored HTML | `woostack-visualize` |
| `/woostack-debug <target> [--auto]`, find a bug's root cause before fixing (gated; `--auto` for autonomous) | `woostack-debug` |

If the user asks for the behavior without using the exact command name, route by intent.
For example, "use woostack to review this PR" means load `woostack-review`.

## Red Flags

These thoughts mean stop and load the relevant rules:

| Thought | Reality |
|---|---|
| "I can just make the edit." | In a woostack project, the root `AGENTS.md` may define the required loop. |
| "The command name is just shorthand." | Woostack commands are skills with gates and constraints. |
| "I remember the workflow." | The installed skill may have changed. Load it. |
| "I'll initialize `.woostack/` to be helpful." | This skill is adoption-only; mutate project state only when requested or required by the task skill. |
| "This is only a review comment." | Review and address flows have posting, validation, and memory rules. |
| "I'll write another plan for this spec." | Specs and plans are 1:1. A second plan breaks the board's join — amend the one existing plan instead. See [`conventions.md`](../woostack-status/references/conventions.md). |
| "I'll just set `status:`/`branch:` by hand." | The build loop authors those fields and the `/woostack-status` board reads them; hand-editing or blanking them causes drift flags. |
| "I'll rename or move this spec or plan." | Renames break the spec↔plan↔PR joins (the `**Source:**` line, `branch:`, the `Spec:` PR trailer). Avoid it, or update every join at once. |

## AGENTS.md Usage

When a project wants woostack behavior, its root `AGENTS.md` should reference this skill and
state the local rules the agent must obey. Keep project-specific policy in `AGENTS.md`; keep
the reusable workflow in the woostack skills.

Minimal pattern:

```markdown
# AGENTS.md

This project follows woostack. At the start of work, use `using-woostack` to load the
project rules and route `/woostack-*` requests to the matching woostack skill.

Follow this file first when it conflicts with generic agent defaults.
```

## Missing Skills

If a mapped woostack skill is not installed, say exactly which skill is missing and ask the
user whether to install the woostack collection. Do not silently approximate a gated
workflow unless the user asks you to proceed without the skill.
