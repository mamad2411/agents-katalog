---
name: creator-shortlist
description: |
  Build a shortlist of creators for a brand partnership or sponsorship, judged on audience fit, recent activity and a way to reach them, not follower count alone. Use when a brand wants creators to work with, an agency needs a creator list, or someone asks for influencers in a niche.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [sales_enablement]
metadata:
  title: "Creator Shortlist"
  category: "sales-enablement"
  tags: "sales_enablement"
  keywords: "enablement, find creators for our brand, influencer shortlist, creators in this niche, who should we sponsor, creator outreach list"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Creator Shortlist

## What this does

Follower count is the field everyone sorts by and the one that predicts the least. This skill judges creators on whether their audience matches the buyer, whether they posted in the last 30 days, whether they already do sponsorships, and whether there is a business contact route, then returns a shortlist small enough to contact this week.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- find creators for our brand
- influencer shortlist
- creators in this niche
- who should we sponsor
- creator outreach list

## Inputs

- **niche**: the topic and the audience the brand sells to
- **platforms**: the platforms that matter
- **creators**: a list you already have, if not running it live

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Define audience fit in one sentence before looking at any creator.
2. Drop creators with no post in the last 30 days.
3. Mark creators who already run sponsorships. They know the process and have a rate.
4. Keep only creators with a business contact route: an email, a booking link, or a management contact.
5. Rank by audience fit first and audience size second, and cut the list to the number you can contact this week.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A shortlist with creator, platform, audience size, last post date, fit reason, sponsorship history and contact route; plus counts of creators dropped as inactive or unreachable.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Audience fit is defined before creators are judged
- Creators with no post in 30 days are dropped
- Every kept creator has a business contact route
- Ranking puts fit before size

## Optional: run it on live data

This skill works with no tool. To add live data, run Creator Finder (https://apify.com/mambalabs/creator-finder?fpr=mamba) on your own Apify
account to find creators in a niche with audience size and contact routes, and add Link in Bio Newsletter Checker to see which ones run a newsletter.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `newsletter-sponsor-prospecting`
- `linkedin-post-writer`
- `partner-sourcing-plan`
