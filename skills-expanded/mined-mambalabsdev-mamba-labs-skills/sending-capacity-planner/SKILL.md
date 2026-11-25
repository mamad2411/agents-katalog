---
name: sending-capacity-planner
description: |
  Work out how many contacts a set of sending accounts can actually reach per week, and how long a list will take to work through. Use when someone asks how many emails they can send, how many inboxes they need, how long a campaign will run, or whether to buy more domains.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, deliverability, outbound_email]
metadata:
  title: "Sending Capacity Planner"
  category: "outbound-email"
  tags: "cold_email_system, deliverability, outbound_email"
  keywords: "outbound, how many emails can i send, how many inboxes do i need, how long will this campaign take, should i buy more domains, sending capacity"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Sending Capacity Planner

## What this does

Sending capacity is usually estimated from the per inbox daily limit and then quietly broken by follow up steps, which multiply every new contact by the number of steps in the sequence. This skill computes capacity from the sequence shape rather than from the contact count, so the plan survives contact with the second week.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- how many emails can I send
- how many inboxes do I need
- how long will this campaign take
- should I buy more domains
- sending capacity

## Inputs

- **accounts**: number of sending accounts and the per account daily limit
- **sequence**: number of steps and the day offsets
- **list**: total contacts to work through
- **days**: sending days per week

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

1. Compute raw weekly capacity: accounts times daily limit times sending days.
2. Compute the steady state multiplier. Once the sequence is full, every new contact added consumes one slot per step, so effective new contacts per week is raw capacity divided by the number of steps.
3. Compute the ramp: in week one only step one fires, so week one absorbs more new contacts than week four. Show the first four weeks separately rather than averaging them.
4. Divide the list by steady state new contacts per week to get the calendar length, and give the finish date.
5. If the finish date is beyond the point where the list goes stale, say so and give the two options: more accounts, or fewer steps.
6. Price the extra accounts option, including domains and warmup time before they are usable.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

Weekly capacity, steady state new contacts per week, a four week ramp table, the calendar finish date, and the two options if the date is unacceptable.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Capacity accounts for follow up steps, not only first touches
- The first four weeks are shown separately from steady state
- Warmup time is included before a new account counts toward capacity
- The finish date is a date

## Optional: run it on live data

This skill works with no tool. To add live data, run Domain Deliverability Checker (https://apify.com/mambalabs/domain-deliverability-checker?fpr=mamba) on your own Apify
account to confirm each sending domain is healthy before it counts as capacity.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `domain-warmup-planner`
- `cold-email-sequence-system`
- `email-deliverability-audit`

Ships in the **cold-email-system**, **deliverability** packs.
