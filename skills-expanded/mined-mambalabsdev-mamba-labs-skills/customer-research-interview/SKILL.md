---
name: customer-research-interview
description: |
  Run customer interviews that produce usable language instead of agreement, and turn the transcripts into a sharper ICP. Use when someone wants to talk to customers, needs messaging research, or does not know why their best customers bought.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, sales_enablement, signal_based_selling]
metadata:
  title: "Customer Research Interview"
  category: "sales-enablement"
  tags: "agency_delivery, sales_enablement, signal_based_selling"
  keywords: "enablement, talk to my customers, messaging research, why do people buy from us, customer interviews, voice of customer"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Customer Research Interview

## What this does

Customer interviews fail by producing agreement. Ask whether a problem is painful and everyone says yes. This skill asks about what happened instead of what people think, extracts the language customers actually use, and writes the result into the shared ICP file so every other skill in the catalog gets sharper from it.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- talk to my customers
- messaging research
- why do people buy from us
- customer interviews
- voice of customer

## Inputs

- **customers**: who to talk to, ideally recent buyers and recent losses
- **questions**: what you are trying to decide
- **transcripts**: the interviews, once they exist

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Decide what the research changes before writing a question. Research that would not change a decision produces a document nobody uses.
2. Interview recent buyers and recent losses. Losses tell you more and are the group nobody calls.
3. Ask about events, not opinions. What were you doing the week you started looking, rather than what matters to you in a vendor.
4. Trace the trigger. Almost every purchase has a specific event behind it, and that event is the signal you should be targeting.
5. Capture exact language. The words a customer uses for the problem are worth more than the summary of what they meant, and they belong in the copy verbatim.
6. Stop when the answers repeat. Five interviews that agree are more useful than fifteen that were run to feel thorough.
7. Write the findings into `ICP.md`: the trigger events, the language, and the exclusions the losses revealed.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The interview guide, the trigger events found, the verbatim language bank, the pattern across losses, and the updated ICP block ready to write to the file.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The decision the research informs is stated before the questions are written
- Losses are included, not only buyers
- Questions ask about events rather than opinions
- Language is captured verbatim
- The output is written back into ICP.md

## Optional: run it on live data

This skill works with no tool. To add live data, run Review Platform Reputation Enricher (https://apify.com/mambalabs/review-platform-reputation-enricher?fpr=mamba) on your own Apify
account to read public reviews before the interviews, so the questions start from real language.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `icp-definition-builder`
- `positioning-statement`
- `win-loss-analysis`

Ships in the **agency-delivery**, **signal-based-selling** packs.
