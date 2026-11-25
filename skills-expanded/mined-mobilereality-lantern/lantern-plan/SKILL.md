---
name: lantern-plan
description: Plan a change in a project that has a settled `.lantern/` map. Writes a structured plan file under `.lantern/plans/` that the Lantern app can read - goal, scope, impact on areas, features and files computed from the map, ordered stages with items and acceptance checks, the open questions of each stage, risks - and has the user approve it section by section. Use whenever the user asks to "plan", "plan this feature", "lantern plan", "zaplanuj", "make a plan before we delegate", "break this into stages", "what would this touch" or "review the plan", in a project with a `.lantern/map`. Refuses to start while the map is not settled. This is the entry skill - the gate, the process, and which small `lantern-plan-*` skill to read at each step. Not for building the map (`lantern-setup`) and not for doing the work (`lantern-delegate`).
---

# Lantern plan

A plan here is a file, not a document: `.lantern/plans/<slug>.plan`, line-based, tied to the map, committed
next to it. Lantern reads it, the user approves it section by section, and `lantern-delegate` executes it
item by item. Item progress is never written in the plan; it comes from the pull request records that name
the item. Format: `../lantern-setup/references/format.md`, "Plans".

`$P` is this skill's folder, `$L` is `lantern-setup`'s. Run `node $P/scripts/plan.mjs <command>` from the project root. Every script
is here; the other `lantern-plan-*` skills point back at it.

## Read before each step

Read the skill named for the step, from disk, in full, before you do the step. `plan.mjs skills` lists
any that are missing.

| step | what | read first |
|---|---|---|
| 1 | gate and request | `lantern-plan` |
| 2 | impact from the map | `lantern-plan-impact` |
| 3 | stages, items and questions | `lantern-plan-stages` |
| 4 | write and check the plan file | `lantern-plan-stages` |
| 5 | review section by section | `lantern-plan-review` |
| 6 | approve the plan | `lantern-plan-review` |
| 7 | hand off to lantern-delegate | `lantern-plan-handoff` |

## Language

Write every plan text (goal, scope, impact reasons, stage and item titles, acceptance, questions, risks) in the
map's primary language: `node $L/scripts/lang.mjs .` prints its code (`pl`, `en`, ...), and it comes from the
map itself, so nothing needs configuring. Plan keywords, ids and file paths stay as they are.

## Process

1. **Gate and request.** Run `plan.mjs gate`. Closed means stop: say in one line what failed. A map that is
   not settled: tell the user to set it up or refresh it first (`lantern-setup`). A missing skill: install
   with `pnpm run install-skills -- <project>`. Never plan on a map you could not validate.
   Then read the request and the map (`.lantern/features`, `.lantern/areas`, the texts in `lang/`). List
   only what you cannot find out and cannot sensibly default: ask it in **one message**, numbered, at most
   five, each with the answer you would assume. Not a questionnaire. A question that only blocks one stage
   waits for that stage (step 3).
2. **Impact.** Compute it from the map, do not guess it. Write the `#impact` section.
3. **Stages.** Split the work into ordered stages of items, each with an acceptance check; put each open
   question in the stage it blocks.
4. **Write and check.** Pick the slug from the goal: a few lowercase words joined by hyphens, at most 40
   characters (`plan-on-the-map`). `plan.mjs new`, then `plan.mjs add`, or edit the file; `plan.mjs check <slug>`
   must print OK.
5. **Review.** Show one section, get the user's answer, record the approval, show the next.
6. **Approve.** When every section is approved, record the plan-level approval. Commit the file.
7. **Hand off.** An approved plan goes to `lantern-delegate` as `Plan: <slug>`.

## Commands

| command | does |
|---|---|
| `gate` | map settled (`validate.mjs --settled`) and planning skills installed; exit 1 closed |
| `skills` | which planning skills resolve, and what to read at each step |
| `new <slug> --title <t> --goal <g>` | starts the file |
| `impact --file/--feature/--area ...` | dependents, dependencies, counts, areas and features |
| `add <slug> <kind> ...` | adds a goal, scope, impact, stage, item, touch, question, answer, explain, flow or risk line (impact and touch take the kinds area, feature, file and new; a touch may belong to a question; flow takes `--flow-file`) |
| `check <slug>\|--all` | shape, names against the map, approvals; exit 1 on errors |
| `show <slug> [<section>]` | the review queue, or one section as written |
| `approve <slug> <section\|plan> --by <who>` | records an approval |
| `verified <slug> <item> --by <who>` | the one status the plan stores |
| `status <slug>` | item status from the PR records, and what comes next |
| `handoff <slug>` | the items to delegate now; exit 1 unless approved and clean |

Every command takes `--json` and `--root <dir>`.

## Rules

- **Short lines, no prose blocks.** A goal is at most three lines, a scope bullet one line; `check` rejects
  more. If a section wants a paragraph, it is two sections or a question.
- **Names come from the map.** Features, areas and files in the plan must exist in `.lantern/`; copy them
  from `plan.mjs impact`. `check` errors on an unknown one and warns on a file deleted since.
- **Questions belong to a stage.** Never one list at the end.
- **Answers arrive pasted from Lantern.** The user answers in the app, which writes nothing; you record the
  answers, any `explain` or `flow` it asks for, and any new question (`lantern-plan-stages`).
- **Approval is the user's.** Only `approve` after the user said yes to what you showed. You never approve
  for them, and an edit after approval makes that section stale: show it again.
- **The plan never records progress** except `#verified`. Do not tick items by hand.
- **Scratch to `.ai/tmp/`.** Write only `.lantern/plans/`.
