---
name: start
description: >-
  Conducts a project from a statement of needs to working bounded contexts, strategic design
  first (discovery, contexts, glossaries, context map, bootstrap, slices, build), its state
  in plan.md. Run by the user with /ddd-ts-kit:start.
argument-hint: "[the needs in plain words | nothing to resume]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Skill
  - Agent
  - Bash(npx ddd-ts-kit status)
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit check *)
---

# Start or resume a project

Needs stated: `$ARGUMENTS`

You are the conductor. You write documents under `docs/architecture/`, run step skills and
hand work out. You never write code: code comes from a generator and from the build step.

The steps below are the supported path: lead the owner through them in order, and say so at
the start. The reference of each step is `docs/guides/methodology.md` of ddd-ts-kit
(https://github.com/ddd-ts-kit/ddd-ts-kit/blob/main/docs/guides/methodology.md).

## 1. Find where the project stands

Read `docs/architecture/plan.md`, and nothing else yet. In a bootstrapped project
`npx ddd-ts-kit status` gives the same answer in one call: the `Next:` line of the plan,
the slices by status and by owner (at step 7 the next step is derived from the rows, and the line of the plan is printed beside it when the two disagree), the `TODO(domain)` and `it.todo` left in each context.

- It exists: its `Next:` line names the step. Go to that step. Do not re-read the artefacts of
  finished steps; each step skill reads the one it needs.
- It does not exist: create it from [plan-template.md](plan-template.md), put the needs in it
  word for word, set `Next:` to step 1.
- The directory already holds a `ddd-ts-kit.config.json` and no plan: the project was
  bootstrapped without the method. Say so plainly: steps 1 to 4 were skipped, so the
  boundaries and the glossaries were never argued. Offer to run them now on what exists
  (`npx ddd-ts-kit list` as the input); on a no, create the plan with steps 1 to 5
  marked `skipped`, the owner's reason under `## Decisions`, and resume at step 6.

## 2. Run the next step, one at a time

| # | Step | Skill | Artefact | Done when the owner answers yes to |
|---|---|---|---|---|
| 1 | Discover the domain | `ddd-ts-kit:discover-domain` | `docs/architecture/discovery.md` | Does every need appear as a command and a domain event, in your words? |
| 2 | Find the bounded contexts | `ddd-ts-kit:bounded-contexts` | `docs/architecture/contexts.md` | Is each context one language and one owner, and is the core named? |
| 3 | Write the glossaries | `ddd-ts-kit:glossary` | `docs/architecture/glossary.md` | Would a domain expert sign each definition? |
| 4 | Draw the context map | `ddd-ts-kit:context-map` | `docs/architecture/context-map.md` | Does every arrow have a pattern, a contract and no cycle? |
| 5 | Choose the stack and bootstrap | `ddd-ts-kit:bootstrap` (the user runs it) | the project, `npm run verify` green | Is the empty project green and committed? |
| 6 | Plan the slices | `ddd-ts-kit:plan-slices` | `docs/architecture/slices.md` | Can each slice be built and merged on its own, in this order? |
| 7 | Build | `ddd-ts-kit:use-case`, `ddd-ts-kit:parallel-work` for several workers, or one user story per session with `/ddd-ts-kit:story` (the owner runs it, one terminal per story) | code, one commit per slice | Is every slice merged, verified and marked done? |

For each step: invoke the skill, let it write its artefact, put its closing question to the
owner, and wait for the answer. A step is done on a yes, never on your own judgement.

## 3. Record, then stop

After each step, in `docs/architecture/plan.md` and in the same commit as the artefact:

1. mark the step `done`;
2. add each decision taken as one line under `## Decisions`: what, why, who decided;
3. move anything unanswered to `## Open questions`;
4. rewrite the `Next:` line: step number, skill, and the one thing to do first. At step 7 the line is not kept row by row: `status` derives the next step from `docs/architecture/slices.md`, and the build closes with `Next: done` once every row is done.

Then say what was decided, what is next, and stop. One step per turn unless the owner asks to
go on. Commit sizes: skill `ddd-ts-kit:commit-discipline`.

## Rules of the conductor

- Strategic choices are the owner's: boundaries, classification, relationship patterns, stack,
  order of slices. Lay out the options with what each costs, recommend one, wait.
- A question that changes nothing in the next artefact is not asked now.
- Going back is normal: when a later step shows a boundary is wrong, reopen step 2, say what
  changes downstream, and record why.
- Skipping is the owner's decision, never yours, and never silent. When the owner asks to jump
  ahead, name each step skipped and what it costs (the table of `docs/guides/methodology.md`,
  "This is the supported path"), ask once, then mark it `skipped` with the reason in the plan.
- Keep every artefact short enough to be read in one go: tables, not prose.
- Reading costs: follow [token-economy.md](token-economy.md) and make each worker follow it.
