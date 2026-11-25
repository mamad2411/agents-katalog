---
name: sales-one-pager
description: |
  Write the one page document a prospect forwards internally to the person who has to approve. Use when a deal needs an internal champion, when someone asks for a leave behind, or when a prospect says they need to check with someone.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, sales_enablement]
metadata:
  title: "Sales One Pager"
  category: "sales-enablement"
  tags: "agency_delivery, sales_enablement"
  keywords: "enablement, write a one pager, they need to check with someone, leave behind for the meeting, our champion needs something to forward, sales collateral"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Sales One Pager

## What this does

A leave behind is not read by the person you met. It is forwarded to somebody who was not in the meeting, has no context, and is deciding whether to spend money. This skill writes for that second reader, which changes what goes on the page: the problem in their language, the cost of not acting, and the shape of the commitment.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- write a one pager
- they need to check with someone
- leave behind for the meeting
- our champion needs something to forward
- sales collateral

## Inputs

- **prospect**: the company, the champion, and the approver if known
- **problem**: what the champion said was wrong, in their words
- **commitment**: what you are asking them to agree to

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`
- `ICP.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Write for the forward, not for the meeting. The reader has no context and did not agree to talk to you.
2. Open with the problem in the champion's own words, quoted where you have them. That sentence is what makes the approver believe the champion, which is the actual mechanism.
3. State the cost of not acting before the solution. An approver who does not feel the cost reads the rest as a purchase rather than a fix.
4. Give the commitment shape: what it costs in money, time and people, and what happens first. Vagueness here reads as risk.
5. Include one proof point that resembles them, and only one.
6. Answer the two questions the approver will ask that the champion cannot: why now, and what happens if it does not work.
7. One page. If it does not fit, the ask is not clear enough yet.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A one page document: the problem quoted, the cost of inaction, the commitment shape, one proof point, the two approver questions answered, and the next step.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The page is written for a reader who was not in the meeting
- The problem appears in the champion's own words where available
- The cost of inaction appears before the solution
- The commitment states money, time and people
- It fits one page

## Optional: run it on live data

This skill works with no tool. To add live data, run Company Firmographic Enricher (https://apify.com/mambalabs/company-firmographic-enricher?fpr=mamba) on your own Apify
account to pull the prospect facts the page cites.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `objection-handling-library`
- `positioning-statement`
- `account-intelligence-brief`

Ships in the **agency-delivery** pack.
