---
name: subject-line-lab
description: |
  Generate and screen cold email subject lines against truncation, spam triggers and the preview text they create. Use when someone needs subject lines, has low open rates, or wants to test subject variants.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, outbound_email]
metadata:
  title: "Subject Line Lab"
  category: "outbound-email"
  tags: "cold_email_system, outbound_email"
  keywords: "outbound, write subject lines, my open rates are low, test subject variants, improve this subject line, subject line ideas"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Subject Line Lab

## What this does

Subject lines are judged on a phone, truncated, next to preview text pulled from the first line of the body. Most subject line advice ignores all three. This skill generates variants, then screens each against character truncation on the common clients, against filter triggers, and against the preview text it will actually appear beside.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- write subject lines
- my open rates are low
- test subject variants
- improve this subject line
- subject line ideas

## Inputs

- **email**: the body the subject sits on
- **audience**: who receives it
- **history**: past subject lines with their open rates, if any

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Generate variants across four distinct shapes: the specific observation, the direct question, the two word fragment, and the plain statement of the thing. Not four wordings of one shape.
2. Screen for truncation. Show each variant cut at 30 characters and at 45, which is roughly where mobile and desktop clients stop, and reject any variant whose meaning dies at 30.
3. Screen for filter triggers: currency symbols, exclamation marks, all caps words, and the specific phrases that read as promotional.
4. Render the preview text each variant will produce, which is the first line of the body. If the subject and the preview say the same thing, one of them is wasted.
5. Reject anything that promises what the body does not deliver. An open earned by a mismatch costs a reply.
6. Rank by expected performance and say what each variant is testing, so a test result means something.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A variant table with the 30 and 45 character truncations, the filter flags, the preview text pairing, and what each variant tests.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Variants span four distinct shapes, not four wordings
- Every variant is shown truncated at 30 and 45 characters
- Preview text is rendered beside each subject
- Each variant states what it is testing

## Optional: run it on live data

This skill works with no tool. To add live data, run News Media Mention Monitor (https://apify.com/mambalabs/news-media-mention-monitor?fpr=mamba) on your own Apify
account to find a recent mention that makes a subject line specific.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `cold-email-structure-checker`
- `outbound-copy-humanizer`
- `cold-email-sequence-system`

Ships in the **cold-email-system** pack.
