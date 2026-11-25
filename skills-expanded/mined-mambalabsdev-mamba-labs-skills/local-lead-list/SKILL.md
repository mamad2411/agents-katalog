---
name: local-lead-list
description: |
  Build a clean list of local businesses for a category and area, with the fields a caller or emailer needs, duplicates removed and closed businesses dropped. Use when someone sells to local businesses, needs a list of plumbers, dentists or restaurants in a city, or wants a map based prospect list.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_research]
metadata:
  title: "Local Lead List"
  category: "signal-research"
  tags: "signal_research"
  keywords: "signals, list of local businesses, find plumbers in denver, local leads from google maps, map based prospect list, small business list for my city"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Local Lead List

## What this does

Local lists go wrong in the same ways: chains mixed with independents, the same business listed twice, closed places, and no way to reach the owner. This skill sets the category and the area, removes chains if you do not sell to them, deduplicates by phone and website, drops closed places, and ranks the rest by a simple signal you choose, such as a low review count or no website.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- list of local businesses
- find plumbers in Denver
- local leads from Google Maps
- map based prospect list
- small business list for my city

## Inputs

- **category**: the business type, in the words people search
- **area**: the city, zip codes, or radius
- **signal**: what makes a business a good prospect for you
- **rows**: an export you already have, if not running it live

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

1. Search the category in more than one wording. A single term misses businesses that describe themselves differently.
2. Remove chains and franchises unless you sell to them, and say how many were removed.
3. Deduplicate by phone number and website domain, not by name.
4. Drop places marked permanently closed.
5. Rank by the signal the user chose, and keep the field that shows it.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The list with name, category, address, phone, website, email where found, rating, review count and the ranking signal; plus counts of chains removed, duplicates merged and closed places dropped.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The category was searched in more than one wording
- Duplicates are merged by phone and website
- Closed places are dropped and counted
- Rows are ranked by the stated signal

## Optional: run it on live data

This skill works with no tool. To add live data, run Local Business Lead Builder (https://apify.com/mambalabs/local-business-lead-builder?fpr=mamba) on your own Apify
account to pull local businesses with phone, website and email for a category and city, and add Google Maps Places Scraper for ratings and review counts.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `icp-definition-builder`
- `cold-email-structure-checker`
- `sending-capacity-planner`
