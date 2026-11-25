---
name: mnemon-evolve
description: >-
  Improve the SKILL.md skills this workspace uses, based on what actually happened. Use when the user asks to
  turn a repeated correction or procedure into a skill, when the same mistake keeps recurring, or when the user
  wants to review how skills are performing.
---

# Skills that improve with use

A skill is a `SKILL.md` file the agent loads on demand. Mnemon keeps the evidence that says whether it works: corrections, "from now on" instructions and repeated procedures, stored as memories and candidates.

## 1. Gather the evidence

1. `memory_manage` (`action: "candidates"`, `candidateAction: "list"`) and `memory_recall` (`action: "search"`) for corrections and standing instructions.
2. `memory_recall` (`action: "receipts"`) to see which skills and memories recent turns actually used.
3. Name the skill under review, and read it: `skills/<name>/SKILL.md` in this workspace or in the home folder.

## 2. Decide whether a skill is the right answer

Write a skill only when the same procedure recurs and has a stable shape. A one-off preference belongs in `USER.md`; a fact belongs in a memory space; a workflow belongs in a skill.

## 3. Draft the change

Produce a diff, not a rewrite:

- what the current `SKILL.md` says that is wrong, missing or ambiguous;
- the exact new wording, keeping the frontmatter `name` matching the folder and the `description` explaining both what the skill does and when to trigger it;
- which piece of evidence supports each change — cite the memory id or the turn it came from.

Never invent a rule the user did not state, and never widen a skill's scope beyond the evidence.

## 4. Backtest before adopting

Build a short case list from the evidence: the real situations where the old wording failed. For each case, state what the old skill would do and what the draft would do. Show the tally — for example `current 2/6 → draft 6/6` — and keep the cases with the draft so the next revision can be measured against them.

## 5. Apply only on Adopt

Show the diff and the backtest. Change nothing until the user adopts it. On adoption:

1. Write the new `SKILL.md`.
2. Keep the previous wording as a revision, or in a memory tagged `skill-history`, so the change can be reverted.
3. Record what changed with `memory_save` (`action: "remember"`), so the reason survives the next session.
