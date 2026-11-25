---
name: bounce-and-catchall-policy
description: |
  Decide what to do with catch all domains, role addresses and soft bounces before they cost you a domain. Use when verification returns unknown, when someone asks whether to send to catch all addresses, or when bounce rate is creeping up.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, deliverability]
metadata:
  title: "Bounce And Catch All Policy"
  category: "deliverability"
  tags: "cold_email_system, deliverability"
  keywords: "deliverability, should i send to catch all addresses, verification returned unknown, my bounce rate is creeping up, role addresses, what do i do with unknown emails"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Bounce And Catch All Policy

## What this does

Verification returns three answers and most teams only plan for two. Valid sends, invalid drops, and unknown, which is mostly catch all domains, is where the decision actually lives. Sending to all of them raises bounce rate; dropping all of them can remove a large share of an enterprise list. This skill sets a policy per class with the arithmetic that justifies it.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- should I send to catch all addresses
- verification returned unknown
- my bounce rate is creeping up
- role addresses
- what do I do with unknown emails

## Inputs

- **results**: verification results with counts per class
- **tolerance**: the bounce rate ceiling you will accept
- **value**: roughly what a reply is worth

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

1. Split the list into valid, invalid, catch all, role address, and disposable. Report the share of the list each class holds, because the decision changes entirely at 5 percent versus 40 percent.
2. Drop invalid and disposable without further thought.
3. For catch all, compute the bounce rate the whole send would carry if a stated share of them bounce, and compare against the tolerance. That arithmetic, not a rule of thumb, decides whether they are included.
4. If catch all is a large share and the tolerance is tight, send them on a separate domain rather than dropping them, so a bounce spike is contained.
5. For role addresses, decide by target. A role address is worthless for a founder persona and often correct for a support or procurement persona.
6. Set the soft bounce rule: how many soft bounces before the address is treated as hard, and where that is recorded.
7. Write the policy down as a rule other people can apply without asking.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The class split with shares, the bounce arithmetic against the tolerance, the decision per class, the separate domain recommendation if it applies, and the written policy.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Each class is reported as a share of the list
- The catch all decision shows the bounce arithmetic
- Role addresses are decided by persona, not by a blanket rule
- The soft bounce threshold is a number and its record location is named

## Optional: run it on live data

This skill works with no tool. To add live data, run Email Verifier (https://apify.com/mambalabs/email-verifier?fpr=mamba) on your own Apify
account to classify each address as valid, catch all, role or invalid before the policy applies.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-waterfall-designer`
- `email-deliverability-audit`
- `suppression-architect`

Ships in the **deliverability**, **cold-email-system** packs.
