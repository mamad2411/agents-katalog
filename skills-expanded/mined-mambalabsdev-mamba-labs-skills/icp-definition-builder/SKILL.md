---
name: icp-definition-builder
description: |
  Turn a description of a business into a structured ideal customer profile with firmographic criteria, signals, pain indicators and exclusion rules. Use when someone asks who to sell to, wants to define their ICP, build targeting criteria, or segment a market.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_operator, identity_enrichment, signal_based_selling]
metadata:
  title: "ICP Definition Builder"
  category: "identity-enrichment"
  tags: "clay_operator, identity_enrichment, signal_based_selling"
  keywords: "identity, who is my ideal customer, define my icp, build targeting criteria, help me segment my market, set up account filters"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# ICP Definition Builder

## What this does

Most ICP documents are a list of adjectives that no filter can apply. This skill produces a profile whose every line is either a filter you can run or a signal you can detect, plus the exclusion rules that matter more than the inclusion rules, because exclusions are what keep a list clean.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- who is my ideal customer
- define my ICP
- build targeting criteria
- help me segment my market
- set up account filters

## Inputs

- **business**: what is sold, to whom, and what it replaces
- **wins**: the best customers you have, and why they were good
- **losses**: deals that closed and churned, or never closed

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

1. Start from the wins, not from the aspiration. The ICP is a description of who already buys well, and it is usually narrower and less flattering than the aspiration.
2. Derive firmographics as ranges and lists, never as adjectives. Mid market becomes a headcount band with a number on each end.
3. Derive the signals: what is observably true about a company at the moment it becomes a good time to reach them.
4. Derive the pain indicators, which are the things a company does when it has the problem you solve, and which are usually visible in hiring, stack or public statements.
5. Write the exclusions explicitly, including the ones that feel obvious. Competitors, existing customers, companies below a size floor, regulated segments you cannot serve, and geographies you cannot support.
6. Write the tier rule: what makes an account tier A rather than tier B, expressed so two people would sort the same list the same way.
7. Finish with the disqualifying question, the one thing a rep can ask on a first call that reliably ends a bad fit early.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The ICP as a structured block: firmographic filters, signals, pain indicators, exclusions, tier rule, and the disqualifying question. Written so it can be pasted into `ICP.md` at the project root.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every firmographic criterion is a range or a list, never an adjective
- Exclusions are present and include existing customers and competitors
- The tier rule is deterministic enough that two people sort the same list identically
- The profile is derived from stated wins rather than from ambition

## Optional: run it on live data

This skill works with no tool. To add live data, run ICP Fit Scorer (https://apify.com/mambalabs/icp-account-lead-scoring-fit-scorer-0-100-for-clay?fpr=mamba) on your own Apify
account to score a company list against the ICP this skill writes.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `icp-fit-scoring`
- `company-discovery-list-builder`
- `clay-people-search-workbook`

Ships in the **signal-based-selling**, **clay-operator** packs.
