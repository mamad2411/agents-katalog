---
name: weekly-pipeline-review
description: |
  Run a weekly pipeline review that finds the deals that are quietly dying rather than admiring the big ones. Use for a weekly sales review, forecasting, or when someone asks which deals to focus on this week.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [crm_operations_pack, small_business_operations, small_business_ops]
metadata:
  title: "Weekly Pipeline Review"
  category: "small-business-ops"
  tags: "crm_operations_pack, small_business_operations, small_business_ops"
  keywords: "small business, weekly pipeline review, which deals should i focus on, forecast this week, sales review agenda, what is stuck"
  version: "2.1.0"
  requirements: "Needs read access to your CRM, or an export of the records."
---

# Weekly Pipeline Review

## What this does

Pipeline reviews spend their time on the largest deals, which are usually the ones already getting attention. The deals that decide the quarter are the ones that stopped moving three weeks ago and nobody noticed. This skill sorts by movement and staleness first, and asks one specific question per deal instead of a general update.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Read access to your CRM, or an export of the records | Required | The open deals | None beyond your existing CRM. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- weekly pipeline review
- which deals should I focus on
- forecast this week
- sales review agenda
- what is stuck

## Inputs

- **deals**: open deals with stage, amount, close date and last activity
- **cycle**: the normal time in each stage
- **capacity**: how many deals can actually get attention this week

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

1. Sort by days since last activity, not by amount. The stale list is the agenda.
2. Flag every deal past the normal time in its stage, and treat that as the default state rather than an exception. Most pipelines have more of these than anyone expects.
3. Flag close dates that have moved more than once. A date that has slipped twice will slip again, and the forecast should reflect that rather than the latest date.
4. For each flagged deal, write the one question that would resolve it. Not an update request, a specific question whose answer changes what happens next.
5. Cut the list to capacity. A review that flags forty deals when five can be worked is a list, not a plan.
6. Separate the forecast from the review. The forecast is what will close; the review is what to do this week, and mixing them makes both worse.
7. Name the deals to close out. Ending a dead deal is a result, and pipelines that never shrink are not forecasts.
8. Approval stop. Before writing any stage or close date change to the CRM, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before writing any stage or close date change to the CRM. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The staleness sorted list, the stage overrun flags, the slipped date flags, one question per flagged deal, the capacity cut, and the close out list.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The list is sorted by staleness, not by amount
- Deals with twice slipped close dates are flagged and the forecast reflects the pattern
- Each flagged deal carries one specific question, not an update request
- The working list is cut to stated capacity
- A close out list is produced

## Optional: run it on live data

This skill works with no tool. To add live data, run Job Change Tracker (https://apify.com/mambalabs/job-change-tracker?fpr=mamba) on your own Apify
account to flag deals whose champion changed jobs.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `lead-lifecycle-designer`
- `deal-attribution-audit`
- `monday-morning-brief`

Ships in the **small-business-operations**, **crm-operations-pack** packs.
