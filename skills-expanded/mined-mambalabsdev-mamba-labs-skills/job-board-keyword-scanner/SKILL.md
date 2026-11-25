---
name: job-board-keyword-scanner
description: |
  Scan a company's job postings for the specific words that indicate a problem your product solves. Use when someone wants to find companies mentioning a tool, a process, or a pain in their job ads, or wants keyword based intent rather than role based intent.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_based_selling, signal_research]
metadata:
  title: "Job Board Keyword Scanner"
  category: "signal-research"
  tags: "signal_based_selling, signal_research"
  keywords: "signals, keyword intent from job postings, find companies building this function, scan job descriptions for a phrase, job ad intent"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Job Board Keyword Scanner

## What this does

Role titles are a coarse signal. The precise one lives in the body of the posting, where a company names the tool it is migrating off, the process it is trying to build, or the metric it is being measured on. This skill scans postings for a keyword set you define and reports which company said what, with the sentence around it.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: job-board-keyword-signal-scanner 0.05 USD per company. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- which companies mention this tool in job ads
- keyword intent from job postings
- find companies building this function
- scan job descriptions for a phrase
- job ad intent

## Inputs

- **domain**: the company domain, or a list
- **keywords**: the phrases that matter, and what each one implies
- **categories**: which role categories to scan

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

The scan reads full posting bodies from the company job board rather than titles from an index.

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
| Job Board Keyword Signal Scanner | `scan_job_board_keywords` | keyword hits inside job posting bodies, by role category | https://apify.com/mambalabs/job-board-keyword-signal-scanner?fpr=mamba |

Runnable example input, matched to the live tool schema:

`scan_job_board_keywords`:

```json
{
  "company_domain": "example.com",
  "role_categories": [
    "GTM"
  ],
  "custom_keywords": [
    "migrating",
    "outbound",
    "attribution"
  ],
  "enable_fallback": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Define the keyword set with an implication per keyword. A keyword with no stated implication produces a hit nobody can act on.
2. Separate keywords that indicate a problem from keywords that indicate a competitor. They lead to different messages.
3. Scan and capture the sentence containing each hit, not just the count. The count is not the signal; the context is.
4. Discard hits inside boilerplate. Benefits sections and equal opportunity statements produce false positives on many common words.
5. Rank companies by the strength of the implication, not by hit count. One mention of the exact problem beats six mentions of a generic word.
6. Write the angle from the quoted sentence, so the outreach can reference something the company itself wrote.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A company by keyword table with the quoted sentence per hit, the implication, and a ranked shortlist with the angle per company.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every keyword carries a stated implication
- Hits are reported with the surrounding sentence
- Boilerplate sections are excluded and this is stated
- Ranking is by implication strength, not hit count

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `hiring-signal-spotter`
- `tech-stack-signal-reader`
- `gtm-signal-aggregator`

Ships in the **signal-based-selling** pack.
