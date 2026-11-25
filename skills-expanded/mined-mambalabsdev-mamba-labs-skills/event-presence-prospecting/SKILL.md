---
name: event-presence-prospecting
description: |
  Find which conferences a company sponsors, exhibits at, or speaks at, and use that as a budget and audience signal. Use when someone wants event based prospecting, wants to know if a prospect will be at a show, or is planning outreach around a conference.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_based_selling, signal_research]
metadata:
  title: "Event Presence Prospecting"
  category: "signal-research"
  tags: "signal_based_selling, signal_research"
  keywords: "signals, which conferences do they sponsor, event based prospecting, will this company be at the show, conference outreach, who exhibits at this event"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Event Presence Prospecting

## What this does

Event presence is an unusually honest signal because it costs money and it is public. A company that buys a booth has both budget and a stated audience. This skill finds the events, separates sponsorship from attendance from speaking, and builds outreach that is timed to the event rather than generic.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: event-presence-index 0.005 USD per company. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- which conferences do they sponsor
- event based prospecting
- will this company be at the show
- conference outreach
- who exhibits at this event

## Inputs

- **domain**: the company domain
- **years**: which years to look at
- **event**: a specific event, if the question is about one

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Event presence is read from public sponsor, exhibitor and speaker listings for the years requested.

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
| Event Presence Index | `map_company_event_presence` | conference sponsorship, booth and speaker presence for a company | https://apify.com/mambalabs/event-presence-index?fpr=mamba |

Runnable example input, matched to the live tool schema:

`map_company_event_presence`:

```json
{
  "domain": "example.com",
  "company_name": "Example Co",
  "years": "2026",
  "include_own_events": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Separate the three presence types. Sponsoring is a budget signal, exhibiting is a pipeline signal, and speaking is a positioning signal. They imply different things.
2. Check whether the company runs its own events. A company with its own conference has a different marketing posture than one that buys booths at other people's.
3. Read the audience of the events, not just the names. Which events a company buys is a statement about who it thinks its buyer is.
4. Time the outreach. Before the event is about planning, during is crowded, and two weeks after is when the follow up backlog is being worked and a relevant message lands.
5. Write the angle from the specific event and the specific presence type, never from the fact of attendance.
6. Note the events they stopped attending, where the data supports it. A dropped sponsorship is a signal too.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The event list by year with presence type, the audience read, the timing recommendation, and the angle.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Presence types are separated and each one is interpreted differently
- Own events are distinguished from third party events
- The timing recommendation is tied to a date relative to the event
- The angle names the specific event

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `gtm-signal-aggregator`
- `account-intelligence-brief`
- `public-award-prospecting`

Ships in the **signal-based-selling** pack.
