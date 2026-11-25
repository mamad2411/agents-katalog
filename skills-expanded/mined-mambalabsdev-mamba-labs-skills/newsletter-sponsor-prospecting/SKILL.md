---
name: newsletter-sponsor-prospecting
description: |
  Find the brands that already pay to sponsor newsletters, podcasts and creators in a niche, and turn their sponsorship history into a prospect list. Use when selling sponsorships, an audience, or marketing services to brands that already spend on creator and newsletter ads.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_research]
metadata:
  title: "Newsletter Sponsor Prospecting"
  category: "signal-research"
  tags: "signal_research"
  keywords: "signals, who sponsors newsletters in my niche, find sponsors for my newsletter, brands that buy creator sponsorships, sponsor prospect list, podcast sponsor leads"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Python 3."
---

# Newsletter Sponsor Prospecting

## What this does

A brand that sponsored three newsletters in a niche last quarter has a budget line and a buyer for exactly what a sponsorship seller offers. This skill reads the sponsors of the newsletters in a niche and the brands seen sponsoring creators, groups the sightings by brand, and ranks brands by how recently and how often they bought, so the list starts with active buyers instead of guesses.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: newsletter-sponsor-tracker 0.004 USD per sponsor row and 0.065 USD per brand search; brand-sponsor-finder 0.02 USD per brand row and 0.005 USD per sighting row. |
| Python 3 with root certificates | Required | The direct actor script `scripts/apify-run.py` | Free. On a python.org install on macOS, run `Install Certificates.command` once, or the script falls back to the system certificate file and says so if it cannot. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- who sponsors newsletters in my niche
- find sponsors for my newsletter
- brands that buy creator sponsorships
- sponsor prospect list
- podcast sponsor leads

## Inputs

- **niche**: the topic and audience
- **newsletters**: newsletters in the niche you know of, as URLs
- **window**: how far back a sponsorship counts, 90 days by default

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

| Actor | MCP tool | Used for | Store page |
| --- | --- | --- | --- |
| Newsletter Sponsor Tracker | none, use `scripts/apify-run.py` | the sponsors in recent issues of each newsletter | https://apify.com/mambalabs/newsletter-sponsor-tracker?fpr=mamba |
| Brand Sponsor Finder | none, use `scripts/apify-run.py` | brands seen sponsoring creators, podcasts and newsletters in the niche | https://apify.com/mambalabs/brand-sponsor-finder?fpr=mamba |

These actors have no MCP tool. Call them directly:

```
APIFY_TOKEN=<your token> python3 scripts/apify-run.py newsletter-sponsor-tracker [input.json]
APIFY_TOKEN=<your token> python3 scripts/apify-run.py brand-sponsor-finder [input.json]
```

With no input file the script runs the example in `scripts/inputs/`. It exits non zero
on a failed or empty run, so an empty result is never read as an answer.

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Collect sponsorship sightings from both sources, each with the date, the placement and the publisher.
2. Group sightings by brand domain, not by brand name, so one brand under two spellings counts once.
3. Rank brands by recency first and frequency second. A brand that bought last month outranks one that bought five times last year.
4. Drop brands whose only sighting is older than the window.
5. For each brand, name the placements it already buys, which is the opening line of the pitch.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A ranked brand list with domain, sightings in the window, last sighting date, placements bought, and an opening line; plus the count of brands dropped as outside the window.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Sightings are grouped by brand domain
- Brands are ranked by recency, then frequency
- Brands with no sighting inside the window are dropped and counted
- Each brand names the placements it already buys

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `event-presence-prospecting`
- `competitor-battlecard`
- `partner-sourcing-plan`
