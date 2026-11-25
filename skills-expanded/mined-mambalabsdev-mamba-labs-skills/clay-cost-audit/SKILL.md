---
name: clay-cost-audit
description: |
  Price a Clay table before it runs and find the columns that are burning credits for no return. Use when someone asks what a Clay build will cost, why their credits are gone, how to cut Clay spend, or wants a run before a full table ramp priced out.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_builds, clay_operator]
metadata:
  title: "Clay Cost Audit"
  category: "clay-builds"
  tags: "clay_builds, clay_operator"
  keywords: "clay, what will this clay table cost, my clay credits are gone, how do i cut clay spend, price this clay build, credit optimization in clay"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Cost Audit

## What this does

Most Clay overspend comes from one pattern: an expensive column running on every row when it only needed to run on the rows that passed a cheap filter. This skill prices the table column by column, finds the columns with no run condition, and rewrites the run order so the expensive work sits behind the cheap work.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The table being priced | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- what will this Clay table cost
- my Clay credits are gone
- how do I cut Clay spend
- price this Clay build
- credit optimization in Clay

## Inputs

- **columns**: the column list with the provider or action behind each
- **rows**: current row count and the expected full volume
- **prices**: credit cost per column run, from the Clay column preview

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. List every column with a per run cost. Columns with zero cost are still listed because they are the candidates for run conditions.
2. Compute cost per row as the sum of every column that runs unconditionally.
3. Flag every paid column with no run condition. That is the finding, and it is usually most of the spend.
4. For each flagged column, name the cheap column that should gate it and the condition to write.
5. Re price the table with the gates applied, using a realistic pass rate for each gate rather than an optimistic one.
6. Present both numbers side by side, at the 10 row ramp, the 100 row ramp, and full volume.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A two column table, before and after, priced at three volumes, plus the list of run conditions to add in the order that saves the most first.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every paid column appears in the table with a unit cost
- The pass rate used for each gate is stated, not implied
- Savings are given in credits and in the currency the user asked about
- The recommendation orders fixes by money saved, not by column order

## Optional: run it on live data

This skill works with no tool. To add live data, run Email Waterfall Orchestrator (https://apify.com/mambalabs/email-waterfall-orchestrator?fpr=mamba) on your own Apify
account to run the email waterfall on your own provider keys instead of credit heavy columns.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-build-gate`
- `clay-conditional-gates`
- `clay-waterfall-designer`

Ships in the **clay-operator** pack.
