---
name: clay-actor-column-wiring
description: |
  Wire an external actor or API into a Clay column so the types survive the round trip. Use when someone wants to call an Apify actor from Clay, add an HTTP API column, pass Clay values into a scraper, or is getting type errors from an external enrichment.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_builds, clay_operator]
metadata:
  title: "Clay Actor Column Wiring"
  category: "clay-builds"
  tags: "clay_builds, clay_operator"
  keywords: "clay, call an apify actor from clay, add an http api column, pass clay values to a scraper, type error from external enrichment, wire an actor into clay"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Actor Column Wiring

## What this does

Clay sends every column value as a string. An external tool that declares a field as a number, a boolean or an array will reject or silently mishandle what Clay sends it. This skill covers the wiring: how to type the fields on the tool side, how to build the request body, and how to read the response back into extraction columns without guessing at the path.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The table being wired | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- call an Apify actor from Clay
- add an HTTP API column
- pass Clay values to a scraper
- type error from external enrichment
- wire an actor into Clay

## Inputs

- **tool**: the actor or endpoint being called and its input schema
- **fields**: which Clay columns feed the request
- **output**: which fields you need back

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

1. Read the tool's input schema. Every field the request will carry from Clay must be declared as a string on the tool side, with the tool coercing internally. A field declared as a number will fail validation on a value Clay sent as text.
2. Build the request body with the Clay column references, and send one row first. Not ten, one.
3. Open the column output preview on that one row and copy the actual response shape. Do not write extraction paths from documentation.
4. Decide whether the response is wrapped. Write the extraction path against what the preview shows.
5. Add extraction columns one field at a time, each verified on the same single row before adding the next.
6. Only then ramp to 10 rows, then 50 to 100, then the table.
7. Set a run condition on the actor column before the full ramp, because an external call is almost always the most expensive column in the table.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The request body, the verified extraction paths with the preview evidence they came from, the run condition, and the ramp plan.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every field crossing the boundary is typed as a string on the tool side
- Extraction paths are quoted from the column preview, not from documentation
- The first run is one row
- The actor column carries a run condition before the full ramp

## Optional: run it on live data

This skill works with no tool. To add live data, run Domain to LinkedIn URL Resolver (https://apify.com/mambalabs/domain-to-linkedin-url-resolver?fpr=mamba) on your own Apify
account to use it as the worked example column: domain in, company profile URL out.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-failure-triage`
- `clay-build-gate`
- `clay-cost-audit`

Ships in the **clay-operator** pack.
