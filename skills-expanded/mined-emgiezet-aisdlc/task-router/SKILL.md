---
name: task-router
description: >
  Maintain a project's instruction hierarchy — a small CLAUDE.md routing table plus
  task-scoped playbooks and path-scoped rules — so agents load only what the task needs.
  Use when a CLAUDE.md has grown too large, agents ignore or contradict instructions, token
  cost per task is rising, or when adding a playbook, rule file, or router row to a project.
---

# Task Router

The failure mode this prevents: one large `CLAUDE.md` holding every convention for every
stack. Past a few hundred lines the model reads all of it for every task, spends context on
rules that do not apply, and follows the ones it does apply less reliably. Adding an
instruction makes every other instruction weaker.

The fix is a hierarchy with three tiers and a table as the only entry point. This is a skill
for whoever maintains the harness, not for whoever is executing a task.

## The three tiers

| Tier | Location | Loaded | Holds |
|------|----------|--------|-------|
| Root | `CLAUDE.md` | always | Identity, repo layout, invariants, the router table |
| Playbook | `.claude/playbooks/<task>.md` | on demand, via the router row | Order of operations for one task type |
| Rule | `.claude/rules/<stack>.md` | automatically, by `paths:` frontmatter | Conventions and verify commands for one stack |

Playbooks are **task-scoped**: they answer "in what order, and what must not be skipped".
Rules are **path-scoped**: they answer "how is code written here". A playbook never restates
a rule — it names the rule file and moves on. Duplicated content is worse than absent
content, because the two copies drift and the agent believes the wrong one.

## Budgets

- Root `CLAUDE.md`: ≤ 90 lines. It is paid for on every single task, including trivial ones.
- Playbook: ≤ 70 lines. One task type. If it needs two, it is two playbooks.
- Rule file: ≤ 70 lines, one stack, ending in a copy-pasteable verification block.
- Router table: ≤ 12 rows. More than that and rows stop being distinguishable — the agent
  picks the wrong one, which is worse than picking none.

Over budget means split, never shrink by deleting the specifics. Vague instructions cost
almost as many tokens as precise ones and buy nothing.

## Writing a router row

Each row is `| what the developer is trying to do | exactly what to read |`. Phrase the
left column as the task in the developer's words ("Change database schema or write a
migration"), not as a category name ("Database"). The agent matches its task against that
string, so it must read like a task.

Every row names **one** destination — a playbook file or a command. A row pointing at three
files is a row that will be half-read.

State the closed-world rule in the root file explicitly: *read only the files this row
names*. Without it, models helpfully open the neighbouring playbooks.

## When to add what

| Situation | Action |
|-----------|--------|
| A task type keeps getting done in the wrong order | New playbook + router row |
| A stack convention gets violated in one directory | New or extended `paths:`-scoped rule |
| An instruction applies to every task without exception | Root invariant (be strict — the list is short by design) |
| One playbook covers two genuinely different tasks | Split it; keep both under budget |
| A rule file is only read for one task type | It is a playbook, not a rule — move it |

## Diagnosing a router that is not working

1. **Run the task on the cheapest model.** A router only works if a weak model can follow
   it. If Haiku loads the wrong playbook, the row's wording is the defect. See `harness-eval`.
2. **Check what got loaded.** If the transcript shows three playbooks read for one task, the
   closed-world rule is missing or the rows overlap.
3. **Check for contradictions.** The same instruction in a rule and a playbook with different
   wording is the most common cause of an agent doing neither.
4. **Fix the instruction, not the model.** Raising the model to paper over a routing defect
   makes every future task more expensive and hides the defect from evals.

## Review checklist

- [ ] Root file under 90 lines and holds no stack-specific conventions
- [ ] Router rows read as tasks, ≤ 12 of them, one destination each
- [ ] Closed-world rule stated in the root file
- [ ] Every playbook under 70 lines, names its rule files instead of restating them
- [ ] No instruction appears in two tiers
- [ ] `make project-init` copies every new playbook and rule into bootstrapped projects
