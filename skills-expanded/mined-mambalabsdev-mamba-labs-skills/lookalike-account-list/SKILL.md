---
name: lookalike-account-list
description: |
  Turn your best customers into a list of companies that look like them, scored on why they match, with firmographics filled and existing customers removed. Use when someone wants more accounts like their best ones, a seed based target list, or lookalike audiences for outbound.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_research]
metadata:
  title: "Lookalike Account List"
  category: "signal-research"
  tags: "signal_research"
  keywords: "signals, find companies like my best customers, lookalike accounts, more accounts like these, seed list to target list, similar companies"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+; Python 3."
---

# Lookalike Account List

## What this does

A list built from a few great customers beats a list built from filters, but only if the match is explained and checked. This skill starts from seed domains, finds companies that share their market and model, fills firmographics, removes customers and open deals, and keeps the reason each company matched, so a seller can see why it is on the list.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: lookalike-company-finder 0.005 USD per lookalike company; company-firmographic-enricher 0.0035 USD per company. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |
| Python 3 with root certificates | Required | The direct actor script `scripts/apify-run.py` | Free. On a python.org install on macOS, run `Install Certificates.command` once, or the script falls back to the system certificate file and says so if it cannot. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- find companies like my best customers
- lookalike accounts
- more accounts like these
- seed list to target list
- similar companies

## Inputs

- **seeds**: three to ten domains of your best customers
- **exclude**: current customers and open deals, as domains
- **icp**: the firmographic limits the list must meet

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

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
| Lookalike Company Finder | none, use `scripts/apify-run.py` | companies similar to the seed domains, with a match score and reason | https://apify.com/mambalabs/lookalike-company-finder?fpr=mamba |
| Company Firmographic Enricher | `enrich_company_firmographics` | headcount, industry and location for each match | https://apify.com/mambalabs/company-firmographic-enricher?fpr=mamba |

This actor has no MCP tool. Call it directly:

```
APIFY_TOKEN=<your token> python3 scripts/apify-run.py lookalike-company-finder [input.json]
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

1. Pick seeds that are good for the same reason. Seeds that are good for different reasons produce a list with no center.
2. Find lookalikes per seed and keep the match reason with each result.
3. Fill firmographics, then apply the ICP limits.
4. Remove current customers and open deals by domain before the list leaves this skill.
5. Report how many lookalikes each seed produced. A seed that produces nothing useful is a signal about the seed.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The account list with domain, the seed it matched, the match reason, score, and firmographics; the count removed by the ICP limits and by the exclusion list; and the yield per seed.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Each account keeps its match reason and seed
- Customers and open deals are removed by domain
- ICP limits are applied after firmographics are filled
- Yield per seed is reported

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `icp-fit-scoring`
- `company-discovery-list-builder`
- `firmographic-enrichment`
