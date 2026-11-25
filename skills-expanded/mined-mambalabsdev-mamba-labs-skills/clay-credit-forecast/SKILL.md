---
name: clay-credit-forecast
description: |
  Forecast how far a Clay credit balance goes across a month of planned builds, and say which build to cut when it does not reach. Use when someone asks whether they have enough credits, how to plan a month of Clay work, or which campaign to drop on a fixed budget.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, clay_builds, clay_operator]
metadata:
  title: "Clay Credit Forecast"
  category: "clay-builds"
  tags: "agency_delivery, clay_builds, clay_operator"
  keywords: "clay, do i have enough clay credits, plan a month of clay work, which campaign should i drop, credit burn forecast, clay capacity planning"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Credit Forecast

## What this does

Credit balances are consumed by builds nobody priced. This skill takes the planned work for a period, prices each build at realistic pass rates, and produces a burn forecast with the date the balance runs out. When the plan exceeds the balance it names the build to cut and what that costs in pipeline, rather than trimming every build a little.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The balance and the planned builds | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- do I have enough Clay credits
- plan a month of Clay work
- which campaign should I drop
- credit burn forecast
- Clay capacity planning

## Inputs

- **balance**: current credit balance and renewal date
- **plan**: the builds planned for the period with row counts
- **history**: actual credits per row from past builds if available

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

1. Price each planned build per row using history where it exists and a stated assumption where it does not. Mark which is which.
2. Multiply by planned volume, apply gate pass rates, and sum.
3. Compare against the balance and produce the exhaustion date at the planned pace.
4. If the plan exceeds the balance, rank the builds by contacts per credit, not by credits. The cheapest build is not the most efficient one.
5. Recommend a whole build to cut or defer rather than shrinking every build, because a half sized campaign has the same fixed setup cost and less output.
6. State what the cut costs in expected contacts so the decision is priced.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A build by build forecast table, the exhaustion date, and a ranked cut list with the pipeline cost of each cut.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every per row cost is labeled as measured or assumed
- The exhaustion date is derived, not estimated in words
- Cut recommendations are whole builds
- The cost of each cut is expressed in expected contacts

## Optional: run it on live data

This skill works with no tool. To add live data, run People Finder and Email Verifier (https://apify.com/mambalabs/people-finder?fpr=mamba) on your own Apify
account to price a people search outside Clay credits as a comparison line.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-cost-audit`
- `clay-conditional-gates`
- `clay-people-search-workbook`

Ships in the **clay-operator**, **agency-delivery** packs.
