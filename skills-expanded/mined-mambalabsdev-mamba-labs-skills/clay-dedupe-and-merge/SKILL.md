---
name: clay-dedupe-and-merge
description: |
  Deduplicate and merge people or company rows across Clay tables without losing enrichment or double counting a person. Use when merging lists, importing a second source into an existing table, deduping a people pool, or deciding which record wins on a conflict.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, clay_builds, clay_operator]
metadata:
  title: "Clay Dedupe And Merge"
  category: "clay-builds"
  tags: "agency_delivery, clay_builds, clay_operator"
  keywords: "clay, merge two clay lists, dedupe my people pool, import a second source into this table, which record wins, am i double counting people"
  version: "2.1.0"
  requirements: "Needs a Clay workspace."
---

# Clay Dedupe And Merge

## What this does

Merging two lists is easy. Merging them without losing the enrichment already paid for, and without counting the same person twice under two email addresses, is the part that goes wrong. This skill sets the match key, the precedence rule, and the audit that proves the merge did not silently drop rows.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| A Clay workspace | Required | The tables being merged | Billed by Clay in credits on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- merge two Clay lists
- dedupe my people pool
- import a second source into this table
- which record wins
- am I double counting people

## Inputs

- **tables**: the tables or lists being merged and their row counts
- **key**: candidate match keys available on both sides
- **precedence**: which source is more trusted, and on which fields

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

1. Pick the match key by uniqueness on your own data, not by intuition. Email is unique per address, not per person. LinkedIn URL is unique per person. Domain is unique per company only after normalization.
2. Normalize before matching: lowercase, strip protocol and trailing slash from URLs, strip the www prefix, strip plus addressing from emails.
3. Count rows before the merge on both sides, and count distinct keys. The gap between them is the internal duplication you are about to inherit.
4. Set field level precedence, not record level. The newer record usually wins on job title and the older one usually wins on verified email.
5. Preserve enrichment. A field that is populated on one side and blank on the other takes the populated value regardless of precedence.
6. After the merge, count again. Rows in, rows out, distinct keys, and rows where a populated field became blank. That last count must be zero.
7. Approval stop. Before merging or deleting any row in a live table, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before merging or deleting any row in a live table. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The match key with its uniqueness measured, the normalization steps, the precedence table by field, and the before and after audit counts.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Match key uniqueness is measured on real rows, not assumed
- Normalization is applied to both sides identically
- Precedence is set per field
- The post merge audit includes a count of fields that went from populated to blank, and that count is zero

## Optional: run it on live data

This skill works with no tool. To add live data, run Company Identity Resolver (https://apify.com/mambalabs/company-identity-resolver?fpr=mamba) on your own Apify
account to give every row a canonical domain before you merge, so near duplicates match.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `clay-build-gate`
- `crm-dedupe-plan`
- `people-pool-builder`

Ships in the **clay-operator**, **agency-delivery** packs.
