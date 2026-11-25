---
name: cold-email-structure-checker
description: |
  Audit a cold email draft against a seven point outbound framework and return a pass or fail scorecard with a rewritten version. Use whenever someone pastes a cold email and asks whether it is good, whether it will get replies, or asks for a review of outreach copy.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, outbound_email]
metadata:
  title: "Cold Email Structure Checker"
  category: "outbound-email"
  tags: "cold_email_system, outbound_email"
  keywords: "outbound, review this cold email, is this email good, will this get replies, audit my outreach copy, fix this cold email"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Cold Email Structure Checker

## What this does

Most cold emails fail on structure before they fail on wording. This skill scores a draft on seven checks that are each objectively decidable, returns the scorecard, then rewrites the draft so every failed check passes without inventing facts the sender did not supply.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- review this cold email
- is this email good
- will this get replies
- audit my outreach copy
- fix this cold email

## Inputs

- **draft**: the email body, subject line included if there is one
- **context**: who it is going to and what the sender actually knows about them

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

1. Score the signal anchor: does the first line reference something specific and verifiable about the recipient, or is it a compliment. A compliment scores zero.
2. Score the relevance hook: does the email connect that signal to a problem the recipient plausibly has.
3. Score the value statement: is there one concrete claim, ideally with a number, rather than a list of capabilities.
4. Score social proof: is there one relevant reference, named or described, and is it the same size and shape as the recipient.
5. Score the call to action: exactly one, low commitment, and answerable in a sentence. Two calls to action score zero.
6. Score length: under 100 words in the body. Count them and print the count.
7. Score the spam scan: flag the words and formatting that trigger filters, and flag link and image counts.
8. Rewrite the draft so every failed check passes. Where a check fails because the sender lacks information, say what to go and find rather than inventing it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A seven row scorecard with pass or fail and the reason, the word count, the flagged terms, then the rewrite, then a one line note on what the sender still needs to find out.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The word count is printed as a number
- Any invented fact about the recipient is refused and named as a gap instead
- Exactly one call to action survives in the rewrite
- Each of the seven checks gets an explicit pass or fail, never a maybe

## Optional: run it on live data

This skill works with no tool. To add live data, run GTM Hiring Signal Scraper (https://apify.com/mambalabs/gtm-hiring-signal-scraper?fpr=mamba) on your own Apify
account to find a real signal for the first line the checker asks for.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `subject-line-lab`
- `outbound-copy-humanizer`
- `cold-email-sequence-system`

Ships in the **cold-email-system** pack.
