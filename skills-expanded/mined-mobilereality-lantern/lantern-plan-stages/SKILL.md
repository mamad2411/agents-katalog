---
name: lantern-plan-stages
description: Split a planned change into ordered stages of items, give every item an acceptance check and the features and files it touches, put each open question in the stage it blocks, then write and check the `.plan` file with `plan.mjs add` and `plan.mjs check`. Use at steps 3 and 4 of `lantern-plan`, and whenever the user asks to "break this into stages", "split the work", "what order should we do this in", "list the open questions", "dopisz etap", or to edit a plan file. Not for the impact section (`lantern-plan-impact`) or approvals (`lantern-plan-review`).
---

# Lantern plan: stages, items, questions

A **stage** is what gets implemented before the next one can start. An **item** is one delegate's pull
request. A **question** is something the user must decide before a stage can be built.
`$P` is the `lantern-plan` folder; run from the project root.

## Stages and items

- **Order by dependency**: the contract or data first, then the logic that uses it, then wiring and UI,
  then tests and docs where they are their own work. A stage is done when all its items are merged.
- **One item, one goal.** A title of at most 100 characters that passes the delegate test: someone holding
  only the title and the diff can say yes or no. An "and" joining unrelated work is two items.
- **Every item names what it touches**: `--touch file:<path>` or `feature:<id>` from `plan.mjs impact`
  (at least one), and `--touch new:<path>` for each file the item will create. A new file needs its
  `#impact new <path> <purpose>` line first (`lantern-plan-impact`); `check` errors without it. Stage-level
  `touch` lines are for what the whole stage shares.
- **Every item has an acceptance check** (`--accept`, one line, at most 160 characters): a command or an
  observable result that would fail if the item were not done. "Tests pass" is not a check; "`vitest run
  test/x.test.ts` fails on main and passes here" is.
- Aim for two to five items a stage and a stage a day of work. Three delegates run at once, so items of
  one stage should not share files.

```
node $P/scripts/plan.mjs add <slug> stage "Read plans in the main process"
node $P/scripts/plan.mjs add <slug> item s1 "Load every plan with its PR states" --touch file:src/main/lantern-prs.ts --accept "A test loads one plan and two PRs and gets one open and one merged item."
node $P/scripts/plan.mjs add <slug> touch s1 feature pull-requests
```

Ids are assigned for you: stages `s1`, `s2`, items `s1.1`, `s1.2`, questions `s1.q1`.

## Questions, per stage

- Attach a question to the **stage it blocks**, not to the plan. `plan.mjs add <slug> question s2 "<text>"`.
- Ask only what the map and the request cannot answer. Make it closed, with the choices and your default:
  "Stage list in the review pane or beside the macro view? Default: beside."
- An unanswered question blocks the **delegation** of its stage; it does not block approving the plan.
  When the user answers: `plan.mjs add <slug> answer <question id> <who> <answer>` (an answer does not
  make the stage's approval stale).
- Help the user decide: name what the question concerns with `plan.mjs add <slug> touch <question id> file
  <path>` (or `feature`/`area`/`new`), so Lantern can mark it on the map. Add `explain` lines (at most four,
  200 characters each) when the choice needs more than the question says, and a `flow` when a picture of who
  does what would settle it. None of these makes the stage's approval stale.

```
node $P/scripts/plan.mjs add <slug> explain s2.q1 "The pane scrolls with the review; beside the map it stays in view."
node $P/scripts/plan.mjs add <slug> flow s2.q1 --flow-file .ai/tmp/flow.json
```

`flow.json` is the same array a pull request record takes for `sync.mjs pr --flow-file`: one to five
stories `{"title", "steps", "below"}`, texts of at most 80 characters, in plain words from the user's side.
Write stage and item titles, acceptance checks, questions, explanations, flow texts and risks in the map's primary language (`node $L/scripts/lang.mjs .`); keywords, ids and file paths stay as they are.
Give a step `"files": ["<path>"]` (up to six) for the files that carry it; `check` wants each in the map or
in an `#impact new` line. `--replace` swaps what is there instead of adding to it. In the file the lines
follow the `#question`: `#touch`, `#explain`, `#story` with `#step`, `#below` and `#file`, then `#answer`.

## Answers pasted from Lantern

The user answers in Lantern and pastes one text: the plan slug, then per question its id, `Answer:` and any
`Request:` ("explain s2.q1 more", "draw the flow for s2.q1"). Lantern writes nothing to the plan; you do.

1. For each `Answer:`, `plan.mjs add <slug> answer <id> <who> <text>`; `<who>` is the user's name.
2. If an answer changes the plan (a stage, an item, a touch), change it, then `check`; a changed section
   goes back to review (`lantern-plan-review`).
3. For each `Request:`, write the `explain` lines or the `flow` it names under that question.
4. If an answer raises a new question, add it to the stage it blocks (`add <slug> question <stage> "<text>"`
   with the choices and your default), and tell the user which questions are still open.
5. Run `plan.mjs check <slug>`; it must print OK.

## Also in the file

`goal` (up to three lines), `scope in` (at least one) and `scope out` lines, and `risk` lines
(at most ten, one line each, risk and mitigation together):

```
node $P/scripts/plan.mjs add <slug> scope out "Planning from the app; the skill plans."
node $P/scripts/plan.mjs add <slug> risk "Many branches multiply git scans; stay on the checked-out one."
```

## Check

`plan.mjs check <slug>` until it prints OK. It errors on: an unknown area, feature or file; a duplicate id;
stages out of order; a stage with no item; an item with no check or no touch; a new file touched with no
purpose in `#impact`; a question with no stage; an approval for a section that does not exist. Warnings (a
file deleted since, a `new` path that already exists, a touch the impact section does not cover, no scope out) need a decision, not silence. Edit by hand if you prefer; the file is one tagged
line each (`#stage`, `#item`, `#touch`, `#accept`, `#question`, `#explain`, `#story`, `#answer`); `check` tells you the line.
