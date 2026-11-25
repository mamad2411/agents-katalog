---
name: brand-context-builder
description: |
  Interview once and write the shared context files that every other skill reads. Use at the start of any engagement, when skills keep asking the same questions, or when someone wants their AI tools to stop needing re explaining.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_operations, clay_operator, cold_email_system]
metadata:
  title: "Brand Context Builder"
  category: "agency-operations"
  tags: "agency_operations, clay_operator, cold_email_system"
  keywords: "agency, set up my context, start a new engagement, write my brand and icp files, bootstrap"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Brand Context Builder

## What this does

Every skill in this catalog reads three files at the project root before it does anything: BRAND.md, ICP.md and VOICE.md. This skill runs the interview that produces them. It is the highest leverage twenty minutes in the whole catalog, because after it every other skill starts from a warm start instead of a questionnaire.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- set up my context
- the skills keep asking me the same things
- start a new engagement
- write my brand and ICP files
- bootstrap

## Inputs

- **business**: what you sell, to whom, and what it replaces
- **customers**: your best customers and why they were good
- **writing**: two or three things you actually wrote

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:


If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Ask the smallest set of questions that produces all three files. Do not ask anything you can read from the website, the existing files, or the samples.
2. Write BRAND.md: what the business does in one sentence a customer would recognize, the proof points with numbers, the positioning against the two real alternatives, the words to use and the words never to use, and the claims that are not allowed because they cannot be supported.
3. Write ICP.md: the firmographic filters as ranges and lists, the signals, the pain indicators, the exclusions, and the tier rule. If the ICP definition skill has run, this is its output rather than a second attempt at it.
4. Write VOICE.md: sentence length, contraction use, how the person opens and closes, the three phrases they actually use, and the register, derived from the writing samples rather than described in the abstract.
5. Mark every unknown as unknown rather than filling it with something plausible. A confident wrong proof point propagates into every email the catalog writes.
6. Set a review date on each file and record the date it was written, because positioning drifts and a stale voice file is worse than none.
7. Tell the user which skills change behavior now that the files exist, so the value is visible immediately.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

Three files written at the project root, each with a written date and a review date, plus a short list of what is still unknown and which skills are now warmer.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- All three files are written, or the missing ones are explained
- Unknowns are marked as unknown rather than filled in
- Voice markers are derived from real samples, not described in the abstract
- Every file carries a written date and a review date
- Disallowed claims are recorded in BRAND.md

## Optional: run it on live data

This skill works with no tool. To add live data, run Company Firmographic Enricher (https://apify.com/mambalabs/company-firmographic-enricher?fpr=mamba) on your own Apify
account to pull your own company's headcount, industry and location to seed BRAND.md and ICP.md.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `icp-definition-builder`
- `mamba-gtm-router`
- `linkedin-profile-optimizer`

Ships in the **cold-email-system**, **clay-operator**, **signal-based-selling**, **linkedin-authority**, **seo-content-engine**, **agency-delivery**, **small-business-operations**, **deliverability**, **crm-operations-pack** packs.
