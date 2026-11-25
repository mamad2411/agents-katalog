---
name: merge-variable-linter
description: |
  Check that every merge variable in a sequence resolves against the fields actually present on the rows, before the campaign sends. Use when someone is about to launch, has seen blank gaps in a sent email, or wants their personalization tokens verified.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, outbound_email]
metadata:
  title: "Merge Variable Linter"
  category: "outbound-email"
  tags: "cold_email_system, outbound_email"
  keywords: "outbound, check my merge variables, blank gaps in my sent email, verify personalization tokens, about to launch check the copy, why is my email missing a word"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Merge Variable Linter

## What this does

An unresolved merge variable is the quietest failure in outbound. It does not raise an error and it does not stop the send. It renders as nothing, leaving a sentence that reads like a bug, and it is only visible after the email has gone. This skill compares the variables used in the copy against the fields present on the rows and reports the gaps before the send rather than after.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- check my merge variables
- blank gaps in my sent email
- verify personalization tokens
- about to launch, check the copy
- why is my email missing a word

## Inputs

- **copy**: the sequence steps as they will be uploaded
- **fields**: the field names present on the rows being uploaded
- **sample**: one real row with values

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

1. Extract every variable token from every step, including subject lines, and deduplicate.
2. Compare each against the field list by exact name. Case and separator differences are misses, not matches.
3. For each miss, say whether the fix is renaming the field on the rows or renaming the token in the copy, and pick one so both sides do not get changed at once.
4. Render every step against the sample row and read the result as a sentence. A variable that resolves to an empty string still leaves broken grammar.
5. Check fallbacks: every variable needs one, and the fallback must read naturally in the sentence rather than as a bracketed placeholder.
6. Report the count of variables used, matched, missing, and without a fallback.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A variable table with used, matched, fallback present, and the rendered sample. Plus a go or no go line.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Matching is by exact name, and near matches are reported as misses
- Every step is rendered against a real row, subject lines included
- The report gives a single go or no go verdict
- Fallbacks are checked for grammar, not just for presence

## Optional: run it on live data

This skill works with no tool. To add live data, run Lead File Import Checker (https://apify.com/mambalabs/lead-file-import-checker?fpr=mamba) on your own Apify
account to check the lead file itself before the merge variables are linted against it.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `cold-email-sequence-system`
- `sequencer-campaign-config`
- `cold-email-structure-checker`

Ships in the **cold-email-system** pack.
