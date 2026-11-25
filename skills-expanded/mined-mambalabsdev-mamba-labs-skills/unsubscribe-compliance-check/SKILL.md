---
name: unsubscribe-compliance-check
description: |
  Check that outbound campaigns carry a working unsubscribe path and that opt outs land somewhere that actually stops the next send. Use before launching, during a compliance review, or when someone asks what an outbound email legally needs.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, deliverability]
metadata:
  title: "Unsubscribe Compliance Check"
  category: "deliverability"
  tags: "cold_email_system, deliverability"
  keywords: "deliverability, do my emails need an unsubscribe, compliance review of outbound, test my opt out, unsubscribe handling, what does an outbound email legally need"
  version: "2.1.0"
  requirements: "Needs access to your sending platform (Instantly, Smartlead or similar); seed inboxes at Gmail, Microsoft and Yahoo that you control, or an inbox placement test service."
---

# Unsubscribe Compliance Check

## What this does

An unsubscribe link that renders is not an unsubscribe path. The path has three parts, and the one that breaks is always the third: the link, the confirmation, and the write that reaches the suppression layer before the next scheduled send. This skill tests all three end to end rather than checking that the footer exists.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Access to your sending platform (Instantly, Smartlead or similar) | Required | The campaign and its unsubscribe path | None beyond your existing sending plan. |
| Seed inboxes at Gmail, Microsoft and Yahoo that you control, or an inbox placement test service | Required | The end to end opt out test | Free with your own seed inboxes; a placement test service bills you directly. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- do my emails need an unsubscribe
- compliance review of outbound
- test my opt out
- unsubscribe handling
- what does an outbound email legally need

## Inputs

- **campaign**: the sequence and its footer
- **path**: where an unsubscribe click goes and what it writes
- **suppression**: the suppression layer it should reach

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Check the footer: a physical postal address, a clear identification of the sender, and an opt out that does not require a reply.
2. Check that the opt out works without a login and without a reply, because a link that asks for either is not an opt out.
3. Click it end to end on a seed address and confirm the write reaches the suppression layer, not just a confirmation page.
4. Check timing: the write must take effect before the next scheduled step for that contact, which for a fast sequence can be under a day.
5. Check every channel. An email opt out that does not stop a social touch is not honored, whatever the letter of the rule says.
6. Check the reply path: somebody who replies asking to stop must be treated as an opt out even though no link was clicked, so a human or a classifier has to be catching that.
7. Report each of the six as pass or fail with the evidence.
8. Approval stop. Before sending a test email to any address you do not own, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before sending a test email to any address you do not own. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

A six row check table with evidence per row, then a single compliant or not compliant verdict, then the fixes.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The opt out is tested end to end on a seed, not inspected in the template
- The write is confirmed at the suppression layer
- Timing against the next scheduled step is checked
- The reply based opt out path is checked, not only the link

## Optional: run it on live data

This skill works with no tool. To add live data, run Domain Deliverability Checker (https://apify.com/mambalabs/domain-deliverability-checker?fpr=mamba) on your own Apify
account to confirm the sending domains authenticate before you test the unsubscribe path.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `suppression-architect`
- `reply-classifier-router`
- `wave-launch-precheck`

Ships in the **deliverability**, **cold-email-system** packs.
