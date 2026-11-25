---
name: crm-hygiene-sweep
description: |
  Run a recurring cleanup on new and changed CRM records so the database stops degrading between audits. Use when someone wants ongoing data hygiene, has just finished a cleanup and wants it to hold, or needs a weekly CRM routine.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [crm_operations, crm_operations_pack]
metadata:
  title: "CRM Hygiene Sweep"
  category: "crm-operations"
  tags: "crm_operations, crm_operations_pack"
  keywords: "crm, weekly crm cleanup, keep the crm clean, data hygiene routine, we cleaned it and it is dirty again, new record hygiene"
  version: "2.1.0"
  requirements: "Needs read access to your CRM, or an export of the records."
---

# CRM Hygiene Sweep

## What this does

A CRM cleaned once is dirty again in a quarter, because the intake keeps producing the same defects. This skill fixes the records that arrived since the last sweep, measures the drift rate, and points at the intake that caused it, so the sweep gets shorter over time instead of longer.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Read access to your CRM, or an export of the records | Required | The records created or changed in the window | None beyond your existing CRM. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- weekly CRM cleanup
- keep the CRM clean
- data hygiene routine
- we cleaned it and it is dirty again
- new record hygiene

## Inputs

- **window**: records created or changed since when
- **standards**: the field standards the records should meet
- **intakes**: the forms, imports and integrations that create records

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

1. Scope to the window. A sweep that re examines the whole database is an audit and it will not run weekly.
2. Check the standard set: owner present, lifecycle value valid, required fields populated, geography and industry values from the picklist rather than free text, and email present and formatted.
3. Fix the mechanical ones automatically and list the judgment ones for a person, and keep those two lists separate so nobody has to sort them.
4. Attribute every defect to its intake. That attribution is what makes the sweep shrink, because a form fixed once removes a defect class permanently.
5. Report the drift rate: defects per hundred new records, tracked over sweeps. A flat or rising rate means the intake work is not happening.
6. Cap the manual list. If it exceeds what a person will actually do, the excess is a fix at the intake, not a queue.
7. Approval stop. Before writing, merging, or deleting any CRM record, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before writing, merging, or deleting any CRM record. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The window counts, the defect table by type, the automatic fixes applied, the manual list within its cap, the intake attribution, and the drift rate over the last several sweeps.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The sweep is scoped to a window, not the whole database
- Automatic and manual fixes are listed separately
- Every defect is attributed to an intake
- The drift rate is tracked across sweeps
- The manual list is capped and the excess is routed to an intake fix

## Optional: run it on live data

This skill works with no tool. To add live data, run Email Verifier (https://apify.com/mambalabs/email-verifier?fpr=mamba) on your own Apify
account to re verify the emails on new and changed records.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `crm-audit`
- `crm-dedupe-plan`
- `crm-enrichment-refresh`

Ships in the **crm-operations-pack** pack.
