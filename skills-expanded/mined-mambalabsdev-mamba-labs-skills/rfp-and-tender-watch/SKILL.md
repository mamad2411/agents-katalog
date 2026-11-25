---
name: rfp-and-tender-watch
description: |
  Watch public tender and RFP portals for open notices that match what you sell, and send a weekly shortlist with deadlines and a bid or no bid call. Use when someone sells to the public sector, wants to find RFPs, or needs a tender watch that does not flood them with noise.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_research]
metadata:
  title: "RFP and Tender Watch"
  category: "signal-research"
  tags: "signal_research"
  keywords: "signals, find rfps for us, tender watch, public sector bids, government contracts we could win, weekly rfp shortlist"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Python 3."
---

# RFP and Tender Watch

## What this does

Public tenders are buying intent with a deadline, but the portals return hundreds of loosely matched notices. This skill sets keywords and exclusions from what you actually sell, keeps only open notices, ranks them by deadline and fit, and makes a bid or no bid call per notice with the reason, so the weekly list is short enough to act on.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: open-tender-rfp-finder 0.003 USD per notice row. |
| Python 3 with root certificates | Required | The direct actor script `scripts/apify-run.py` | Free. On a python.org install on macOS, run `Install Certificates.command` once, or the script falls back to the system certificate file and says so if it cannot. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- find RFPs for us
- tender watch
- public sector bids
- government contracts we could win
- weekly RFP shortlist

## Inputs

- **offer**: what you sell, in the words a buyer would use
- **exclude**: words that mark a notice you would never bid on
- **countries**: the countries you can deliver in

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

| Actor | MCP tool | Used for | Store page |
| --- | --- | --- | --- |
| Open Tender and RFP Finder | none, use `scripts/apify-run.py` | open tender and RFP notices that match your keywords, with deadline and value | https://apify.com/mambalabs/open-tender-rfp-finder?fpr=mamba |

This actor has no MCP tool. Call it directly:

```
APIFY_TOKEN=<your token> python3 scripts/apify-run.py open-tender-rfp-finder [input.json]
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

1. Write keywords from the offer and exclusions from past bad matches before the first search.
2. Keep only notices that are open and whose deadline leaves time to respond, ten working days by default.
3. Rank by fit first and deadline second.
4. Make a bid or no bid call per notice, with the reason: fit, size, deadline, or a requirement you cannot meet.
5. Rerun weekly with the same keywords and report only notices that are new since the last run.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A shortlist with title, buyer, country, value, deadline, link, fit reason and bid or no bid call; the keywords and exclusions used; and the count of notices filtered out.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Only open notices with time to respond are kept
- Every notice has a bid or no bid call with a reason
- Keywords and exclusions are stated
- Repeat runs report only new notices

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `public-award-prospecting`
- `hiring-signal-spotter`
- `competitor-battlecard`
