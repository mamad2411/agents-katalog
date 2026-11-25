---
name: positioning-statement
description: |
  Write a positioning statement that names the real alternative and survives contact with a sales call. Use when messaging is vague, when a new product needs positioning, or when nobody can explain what the company does in one sentence.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, sales_enablement, seo_content_engine]
metadata:
  title: "Positioning Statement"
  category: "sales-enablement"
  tags: "agency_delivery, sales_enablement, seo_content_engine"
  keywords: "enablement, our messaging is vague, position this product, what do we actually do, write our positioning, one sentence pitch"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Positioning Statement

## What this does

Positioning fails when the alternative is unnamed, because a claim to be better is meaningless without a stated comparison, and the honest alternative is usually not a competitor but doing nothing or doing it manually. This skill forces the alternative into the statement and tests the result against the objection it invites.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- our messaging is vague
- position this product
- what do we actually do
- write our positioning
- one sentence pitch

## Inputs

- **product**: what it does mechanically
- **customer**: who it is for, narrowly
- **alternative**: what they do today instead, including nothing

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`
- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Name the alternative first, honestly. For most products it is a spreadsheet, a person doing it manually, or nothing at all, and positioning against a competitor when the real alternative is nothing produces messaging that does not land.
2. Write the statement: for a specific customer, who has a specific problem, this does a specific thing, unlike the named alternative, which fails in a specific way.
3. Test the specificity by inversion. If no sensible company would claim the opposite, the statement is a platitude and needs to be narrower.
4. Write the objection the positioning invites. Strong positioning always invites one, and a positioning statement with no objection is too broad to be useful.
5. Check it against the customer language from research, if any exists. Positioning written in internal vocabulary does not survive the first sales call.
6. Test it as a first line in an email and as a headline. Positioning that cannot survive those two uses will not be used.
7. Write the result into `BRAND.md` with the disallowed claims that follow from it.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The named alternative, the statement, the inversion test result, the invited objection, the email and headline tests, and the BRAND.md block.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The alternative is named and may be doing nothing
- The inversion test is applied and reported
- The invited objection is written down
- The statement is tested as an email first line and as a headline
- The result is written back into BRAND.md

## Optional: run it on live data

This skill works with no tool. To add live data, run Lookalike Company Finder (https://apify.com/mambalabs/lookalike-company-finder?fpr=mamba) on your own Apify
account to list the real alternatives a buyer compares you with.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `brand-context-builder`
- `customer-research-interview`
- `comparison-page-builder`

Ships in the **agency-delivery**, **seo-content-engine** packs.
