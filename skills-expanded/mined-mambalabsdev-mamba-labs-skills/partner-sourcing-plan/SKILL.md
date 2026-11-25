---
name: partner-sourcing-plan
description: |
  Find the partners whose customers are your buyers, and structure the first conversation so it produces something. Use when someone wants referral partners, co marketing, channel relationships, or a warmer route into a market.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, agency_operations]
metadata:
  title: "Partner Sourcing Plan"
  category: "agency-operations"
  tags: "agency_delivery, agency_operations"
  keywords: "agency, find referral partners, co marketing, channel partnerships, who should we partner with, warm route into a market"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Partner Sourcing Plan

## What this does

Partner brainstorms produce a list of well known companies who will not reply. The partners worth approaching are the ones already serving your buyers with something adjacent, and that overlap is detectable rather than guessable. This skill finds them by overlap and structures the first exchange around a small reciprocal test rather than a partnership agreement.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: gtm-tech-stack-signal-scraper 0.015 USD per company; company-social-presence-mapper 0.015 USD per company. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- find referral partners
- co marketing
- channel partnerships
- who should we partner with
- warm route into a market

## Inputs

- **customers**: your customers and what else they buy
- **offer**: what you would give a partner
- **capacity**: how many partner relationships you can actually service

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Overlap is detected from the tools your customers already run and the vendors present on their sites, so the partner list comes from evidence rather than from a brainstorm.

This skill calls live data through the Mamba Labs MCP server, which runs the
actors on Apify with your own Apify token. No account yet: create one free at
https://console.apify.com/sign-up?fpr=mamba, then copy the token from https://console.apify.com/settings/integrations.

- Installed as a plugin: the server is already wired, and the plugin asks for the token once.
- Installed by hand: copy `.mcp.json` from this folder into your project root and set
  `APIFY_TOKEN` in your environment, or run:

```
claude mcp add mamba-gtm-suite -e APIFY_TOKEN=<your token> -- npx -y @mambalabsdev/mcp-gtm-suite@1.14.9
```

| Actor | MCP tool | Used for | Store page |
| --- | --- | --- | --- |
| GTM Tech Stack Signal Enrichment | `detect_gtm_tech_stack` | the adjacent tools your customers already run | https://apify.com/mambalabs/gtm-tech-stack-signal-scraper?fpr=mamba |
| Company Social Presence Mapper | `map_company_social_presence` | the partner's reach and audience | https://apify.com/mambalabs/company-social-presence-mapper?fpr=mamba |

Runnable example input, matched to the live tool schema:

`detect_gtm_tech_stack`:

```json
{
  "domain": "customer.example",
  "crawl_additional_pages": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Detect the overlap. Look at what your existing customers already use and who already serves them adjacent to your offer. That set is the partner list and it is evidence rather than a guess.
2. Rank by overlap size and by whether the partner has an incentive. A partner with a large overlap and no reason to care will not act.
3. Decide what you give before what you ask. A first approach that leads with an ask is a cold email with extra steps.
4. Structure the first exchange as a small reciprocal test: one introduction each way, or one piece of content each, with a date. Partnership agreements before a test are how these die.
5. Set the measurement: what a successful test looks like in referrals or meetings, and by when.
6. Cap the number of relationships at what can be serviced. An unserviced partner relationship is worse than none because it consumed the introduction.
7. Write down what happens if the test produces nothing, so the relationship ends cleanly rather than lingering.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The detected partner list ranked by overlap and incentive, what you give per partner, the reciprocal test with a date, the measurement, the capacity cap, and the clean ending condition.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Partners are found by detected overlap, not by brainstorm
- Partner incentive is assessed, not assumed
- The first exchange is a small reciprocal test with a date
- The relationship count is capped at serviceable capacity
- An ending condition is written

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `tech-stack-signal-reader`
- `client-onboarding-brief`
- `positioning-statement`

Ships in the **agency-delivery** pack.
