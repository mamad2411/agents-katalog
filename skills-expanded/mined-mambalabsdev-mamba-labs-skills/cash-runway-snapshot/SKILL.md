---
name: cash-runway-snapshot
description: |
  Work out how many months of cash are left and what actually changes it. Use when someone asks about runway, cash position, whether they can afford a hire, or what happens if a payment is late.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [small_business_operations, small_business_ops]
metadata:
  title: "Cash Runway Snapshot"
  category: "small-business-ops"
  tags: "small_business_operations, small_business_ops"
  keywords: "small business, how much runway do we have, cash position, can we afford a hire, what if a client pays late, runway calculation"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Cash Runway Snapshot

## What this does

Runway calculated as cash divided by average burn is wrong in the one direction that matters, because it treats expected income as certain. This skill separates committed inflows from expected ones, models the late payment case, and gives a range with the assumption behind each end of it.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- how much runway do we have
- cash position
- can we afford a hire
- what if a client pays late
- runway calculation

## Inputs

- **cash**: current balance across accounts
- **outflows**: recurring costs and any known one offs
- **inflows**: invoices raised, contracts committed, and pipeline

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:


If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Split inflows into three: received, invoiced and unpaid, and expected but not invoiced. Only the first is cash and the third is not runway.
2. Model outflows from the actual recurring commitments, including the annual ones that fall due inside the window and are the usual surprise.
3. Compute the conservative case from received plus invoiced, with a realistic collection delay applied to invoiced.
4. Compute the expected case with the pipeline included at a stated conversion rate.
5. Report the range with the assumption at each end, never a single number, because a single runway number invites a decision the data does not support.
6. Run the late payment case: the largest single receivable arriving thirty days late, which is the failure mode that actually happens.
7. Say what the earliest action date is, meaning the date by which a decision must be made rather than the date cash runs out.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The inflow split, the outflow schedule including annual items, the conservative and expected runway with assumptions, the late payment case, and the earliest action date.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Expected but uninvoiced income is excluded from the conservative case
- Annual costs falling inside the window are included
- Runway is reported as a range with the assumption at each end
- The late payment case is modeled on the largest single receivable
- An action date is given, distinct from the date cash runs out

## Optional: run it on live data

This skill works with no tool. To add live data, run Google Sheets Import and Export (https://apify.com/mambalabs/google-sheets-import-export?fpr=mamba) on your own Apify
account to pull the cash and spend lines from the sheet they live in.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `month-end-narrative`
- `invoice-chaser`
- `monday-morning-brief`

Ships in the **small-business-operations** pack.
