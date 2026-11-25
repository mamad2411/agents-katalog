---
name: public-award-prospecting
description: |
  Find companies that just won a government contract or public grant and reach them while the money is new. Use when someone wants to target contract winners, grant recipients, or public sector suppliers.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_based_selling, signal_research]
metadata:
  title: "Public Award Prospecting"
  category: "signal-research"
  tags: "signal_based_selling, signal_research"
  keywords: "signals, who won government contracts, grant recipients, public sector suppliers, contract award prospecting, federal award list"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Public Award Prospecting

## What this does

A public award is a funding event with a public record, a date, and an amount, and it is far less contested than a venture round. This skill reads the award registers, filters to awards large enough to change behavior, resolves the recipient to a domain, and builds outreach timed to the award date.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: public-award-monitor 0.005 USD per award winner returned. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- who won government contracts
- grant recipients
- public sector suppliers
- contract award prospecting
- federal award list

## Inputs

- **register**: which award register to read
- **window**: how far back to look
- **floor**: the minimum award value worth acting on

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Awards are read from the public register and the recipient is resolved to a company domain, which is the step that usually blocks this list from being usable.

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
| Government Contract Award Monitor | `monitor_public_awards` | public contract and grant awards with recipient domain resolution | https://apify.com/mambalabs/public-award-monitor?fpr=mamba |

Runnable example input, matched to the live tool schema:

`monitor_public_awards`:

```json
{
  "register": "us_federal_contracts",
  "window_days": "30",
  "min_award_value": "250000",
  "exclude_government_recipients": true,
  "resolve_domains": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Set the award floor from what the money would actually fund. An award below the cost of your offer is not a trigger.
2. Exclude government recipients. A public body receiving an award is not the same as a supplier winning one, and the two are mixed in most registers.
3. Resolve recipients to domains and report the resolution rate. An unresolved recipient is not a lead, and the rate tells you whether the register is usable for your market.
4. Read the award description for what is being delivered. That is where the angle is.
5. Time the outreach to the award date plus the ramp. Money awarded is not money spent, and spending starts weeks after the announcement.
6. Check for repeat winners. A company that wins the same award annually is running a program, not a project, and the message is different.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The filtered award list with recipient, domain, amount, date and description; the domain resolution rate; the timing plan; and the angle per award type.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Government recipients are excluded and the count is reported
- The domain resolution rate is stated
- The award floor is justified against the offer price
- Repeat winners are identified separately

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `funding-event-trigger`
- `event-presence-prospecting`
- `gtm-signal-aggregator`

Ships in the **signal-based-selling** pack.
