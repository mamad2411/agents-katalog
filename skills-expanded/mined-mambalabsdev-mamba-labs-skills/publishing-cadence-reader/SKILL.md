---
name: publishing-cadence-reader
description: |
  Measure how often a company actually publishes and read that as a content investment signal. Use when someone wants to know if a company invests in content, is benchmarking against competitors, or is qualifying a content marketing buyer.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content, seo_content_engine, signal_based_selling]
metadata:
  title: "Publishing Cadence Reader"
  category: "seo-content"
  tags: "seo_content, seo_content_engine, signal_based_selling"
  keywords: "seo and content, how often do they publish, content investment signal, benchmark competitor publishing, qualify a content buyer, did their blog stop"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Publishing Cadence Reader

## What this does

Publishing frequency is a public, dated, hard to fake statement about whether a company is investing in content, and it is one of the cleanest qualifiers for anyone selling content services or tooling. This skill measures the real cadence from the site, spots the gap where a program stopped, and reads acceleration and decline as separate signals.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: blog-publishing-frequency 0.004 USD per domain. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- how often do they publish
- content investment signal
- benchmark competitor publishing
- qualify a content buyer
- did their blog stop

## Inputs

- **domains**: the companies to measure
- **window**: the period to measure over

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Cadence is measured from the site's own dated pages rather than from a feed, which catches sites whose feed is truncated or stale.

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
| Publication Cadence Tracker | `track_publication_cadence` | publishing volume and cadence by domain over a window | https://apify.com/mambalabs/blog-publishing-frequency?fpr=mamba |

Runnable example input, matched to the live tool schema:

`track_publication_cadence`:

```json
{
  "domains": [
    "example.com"
  ],
  "max_pages_to_date": 400
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Measure over at least twelve months. A three month window cannot distinguish a seasonal gap from a program that stopped.
2. Report cadence as posts per month over time, not as a total. The shape is the signal and the total hides it.
3. Identify the inflection: the month the rate changed, up or down, and check it against public events such as a funding round or a leadership change.
4. Treat a stopped program and a never started program as different signals with different messages.
5. Check whether output is coming from one author or many, where the data allows, since a single author program is fragile and a multiple author program is a budget.
6. Do not read undated pages as absence. A site with no visible dates is unmeasured, not inactive.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The posts per month series, the inflection point with a date, the classification as accelerating, steady, declining or stopped, the author concentration where available, and the angle for that classification.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The window is at least twelve months
- Cadence is reported as a series, not a total
- Undated pages are reported as unmeasured, not as absence
- Stopped and never started are distinguished

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `first-party-data-post`
- `tech-stack-signal-reader`
- `gtm-signal-aggregator`

Ships in the **seo-content-engine**, **signal-based-selling** packs.
