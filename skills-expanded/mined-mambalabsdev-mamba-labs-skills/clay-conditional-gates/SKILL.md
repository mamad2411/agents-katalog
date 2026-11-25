---
name: clay-conditional-gates
description: |
  Write the run conditions that stop expensive Clay columns from firing on rows that will never qualify. Use when someone wants to skip enrichment for non ICP rows, gate a waterfall, add a run condition, or stop paying to enrich junk.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_builds, clay_operator]
metadata:
  title: "Clay Conditional Gates"
  category: "clay-builds"
  tags: "clay_builds, clay_operator"
  keywords: "clay, add a run condition, skip enrichment for non icp rows, gate this column, only enrich rows that, stop paying to enrich junk"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Conditional Gates

## What this does

A run condition is the cheapest performance work in Clay and the most commonly skipped. This skill turns a qualification rule stated in plain language into the exact condition expression, placed on the right column, in the right order, with the pass rate estimated so the saving is known before the run.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The table being gated | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- add a run condition
- skip enrichment for non ICP rows
- gate this column
- only enrich rows that
- stop paying to enrich junk

## Inputs

- **rule**: the qualification rule in plain language
- **available**: which columns already exist and are cheap enough to gate on
- **target**: the expensive column that should be gated

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

1. Restate the rule as a boolean over columns that already exist. If it needs a column that does not exist yet, say so and place that column first in the order.
2. Prefer a deterministic cheap column over a model judgment for the gate. A gate that costs as much as the column it guards saves nothing.
3. Write the condition expression, and write the negative case explicitly so blank values do not silently pass.
4. Estimate the pass rate from the user's own data if they have any rows, from a stated assumption if they do not.
5. Order multiple gates so the highest rejection rate runs first.
6. State what happens to rejected rows: left blank, tagged, or moved. Blank is a choice, not a default.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The condition expression per column, the placement in the run order, the estimated pass rate, and the resulting cost change.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Blank and null inputs are handled explicitly in every condition
- No gate costs more per row than the column it guards
- Gates are ordered by rejection rate
- The fate of rejected rows is stated

## Optional: run it on live data

This skill works with no tool. To add live data, run ICP Fit Scorer (https://apify.com/mambalabs/icp-account-lead-scoring-fit-scorer-0-100-for-clay?fpr=mamba) on your own Apify
account to score rows first, so expensive columns fire only on rows that qualify.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-cost-audit`
- `clay-build-gate`
- `clay-waterfall-designer`

Ships in the **clay-operator** pack.
