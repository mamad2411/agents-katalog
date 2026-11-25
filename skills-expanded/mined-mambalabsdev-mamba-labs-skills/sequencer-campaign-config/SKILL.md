---
name: sequencer-campaign-config
description: |
  Configure a sending platform campaign correctly the first time: schedule, tracking, limits, timezone and the fields that silently reset. Use when creating a campaign in a sequencer, when settings appear not to save, or when a campaign is sending at the wrong time.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [cold_email_system, outbound_email]
metadata:
  title: "Sequencer Campaign Config"
  category: "outbound-email"
  tags: "cold_email_system, outbound_email"
  keywords: "outbound, set up a campaign in my sequencer, my campaign settings did not save, sending at the wrong time, configure tracking and limits, campaign schedule"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+; Instantly v2 or Smartlead API key."
---

# Sequencer Campaign Config

## What this does

Sequencer campaign settings have a specific failure shape: some fields are dropped silently at creation and must be set in a second update call, and some values that look valid are rejected or, worse, stored as a literal zero. This skill sets the configuration in the order that survives, then reads it back and diffs it against what was intended.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: clay-to-instantly-smartlead-push 0.01 USD per lead pushed. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |
| Instantly v2 or Smartlead API key | Required | Creating the campaign, pushing leads and reading the campaign back | Comes with your existing sending plan. An Instantly v1 key does not work. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- set up a campaign in my sequencer
- my campaign settings did not save
- sending at the wrong time
- configure tracking and limits
- campaign schedule

## Inputs

- **platform**: which sending platform
- **schedule**: sending days, hours and the recipient timezone
- **limits**: per account daily limit and campaign level caps
- **tracking**: open and click tracking preference

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Pushing a finished list into the sequencer can run through the Mamba Labs push actor rather than a manual CSV, which keeps the field names identical between the enrichment table and the campaign payload. The push needs your Instantly v2 or Smartlead API key as `api_key`: read it from the environment at call time and never write it into a file or the output. Run with `dry_run` first, which returns the exact payload and writes nothing.

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
| Sequencer Lead Push | `push_leads_to_sequencer` | push enriched rows into a sequencer campaign with the field names preserved | https://apify.com/mambalabs/clay-to-instantly-smartlead-push?fpr=mamba |

Runnable example input, matched to the live tool schema:

`push_leads_to_sequencer`:

```json
{
  "sequencer": "instantly",
  "api_key": "${INSTANTLY_API_KEY}",
  "campaign_id": "example-campaign",
  "dry_run": true,
  "leads": [
    {
      "email": "jordan@example.com",
      "first_name": "Jordan",
      "company": "Example Co"
    }
  ]
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Create the campaign with the minimum viable settings, then set the rest in a second update. Fields dropped at creation are the most common cause of a campaign that sends with tracking on when tracking was meant to be off.
2. Set the timezone with the exact identifier the platform accepts. Platform timezone enums are not the standard database list and a rejected value falls back to a default silently on some platforms.
3. Distinguish clearing a field from setting it to zero. On several platforms null removes the setting and zero stores a literal zero, which is a hard cap of nothing.
4. Turn open tracking off unless there is a specific reason for it. Tracking pixels cost deliverability and the metric they produce is unreliable.
5. Set the daily limit per account below the platform maximum, leaving headroom for follow up steps already in flight.
6. Read the campaign back through the API or the interface and diff every field against the intent. This step is the point of the skill.
7. Send one test to a seed address on a different provider and read the raw source, not the rendered preview.
8. Approval stop. Before creating, changing, or launching a sequencer campaign, or pushing leads, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before creating, changing, or launching a sequencer campaign, or pushing leads. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The configuration as set, the read back diff with any field that did not stick, and the seed test result.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Configuration is read back and diffed, not assumed
- The timezone identifier used is one the platform accepts
- Null and zero are treated as different values and this is stated
- A seed test is sent and its raw source is read

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `merge-variable-linter`
- `wave-launch-precheck`
- `sending-capacity-planner`

Ships in the **cold-email-system** pack.
