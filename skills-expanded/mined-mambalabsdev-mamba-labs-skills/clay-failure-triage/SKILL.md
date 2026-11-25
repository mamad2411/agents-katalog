---
name: clay-failure-triage
description: |
  Diagnose a Clay column that returns null, zero rows, or the wrong shape, by symptom rather than by guesswork. Use when a Clay enrichment stopped working, a column is empty for rows that clearly have data, a pipeline that worked last week is now blank, or someone asks why their Clay table is broken.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_builds, clay_operator]
metadata:
  title: "Clay Failure Triage"
  category: "clay-builds"
  tags: "clay_builds, clay_operator"
  keywords: "clay, my clay column is empty, clay enrichment returns null, find people returned zero rows, why is my clay table broken"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Failure Triage

## What this does

Clay failures cluster into a small number of recurring shapes, and almost all of them present as the same symptom: a column that is empty when the data is obviously there. This skill walks the symptom to the root cause in the order that resolves fastest, cheapest checks first, and never suggests re running the column until the cause is named.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The failing column | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- my Clay column is empty
- Clay enrichment returns null
- Find People returned zero rows
- this worked last week and now it does not
- why is my Clay table broken

## Inputs

- **column**: which column is failing and what action or provider backs it
- **symptom**: empty, wrong shape, zero rows, or intermittent
- **sample**: one row that should have worked, with its input values

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

1. Classify the symptom first: null on a row with good inputs, zero rows returned, an object where a scalar was expected, or a pipeline that degraded over time. The four take different paths.
2. Null with good inputs: check field name casing against the column output preview. This is the single most common cause and costs nothing to rule out.
3. Null with good inputs, casing correct: check whether the response is wrapped. A path of `results.0.field` and a path of `field` both look plausible and only one is real.
4. Zero rows: check the action name. Find People, Find People at Company and Enrich People are distinct actions. Enrich People needs a person identifier and returns nothing from a company filter.
5. Zero rows on a company lookup: check whether a company name was passed where a domain is required.
6. Object where a scalar was expected: read the provider schema in the response preview. Location is a string for some providers and a nested object for others.
7. Worked last week, blank now: the provider changed its response envelope. Re inspect raw JSON and update the extraction path. Log the date so the next degradation is measurable.
8. Intermittent: check the run condition, not the column. A conditional gate reading a column that is itself still running produces a race, not a failure.
9. Only after the cause is named, re run, and re run on 10 rows, not the table.
10. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A short triage report: symptom class, cause, the exact fix, and the check that proves the fix worked. If the cause cannot be isolated from the sample given, say which single piece of evidence would settle it.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The report names one root cause, not a list of possibilities
- The fix references a value the user can see in their own column preview
- No advice to re run the full table appears anywhere
- The proof step is a check, not an assertion

## Optional: run it on live data

This skill works with no tool. To add live data, run Company Identity Resolver (https://apify.com/mambalabs/company-identity-resolver?fpr=mamba) on your own Apify
account to resolve the company first when a domain input fails in a Clay column.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-build-gate`
- `clay-cost-audit`
- `clay-actor-column-wiring`

Ships in the **clay-operator** pack.
