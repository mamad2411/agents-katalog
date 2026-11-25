---
name: ai-adoption-signal-reader
description: |
  Detect whether a company has shipped AI features or adopted AI vendors, and read that as a budget and priority signal. Use when someone targets companies adopting AI, wants to know if a prospect is building AI features, or needs an AI readiness read on an account list.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [signal_based_selling, signal_research]
metadata:
  title: "AI Adoption Signal Reader"
  category: "signal-research"
  tags: "signal_based_selling, signal_research"
  keywords: "signals, are they using ai, find companies adopting ai, ai readiness of this account list, did they ship ai features, ai vendor detection"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# AI Adoption Signal Reader

## What this does

AI adoption splits companies into three groups that need different messages: shipped it, announced it, and neither. This skill detects vendor presence and product surface on the live site, places the company in one of the three, and reads the pricing page for whether the AI is a feature or a line item, which is the part that indicates real budget.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: ai-tooling-detector 0.003 USD per domain. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- are they using AI
- find companies adopting AI
- AI readiness of this account list
- did they ship AI features
- AI vendor detection

## Inputs

- **domain**: the company domain
- **vendors**: which AI vendors or surfaces to check for

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Vendor detection and the pricing page read run against the live site. Pass the vendors you named as `vendors` to report only those; detection is unchanged and costs the same either way.

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
| AI Tooling Detector | `detect_ai_tooling` | AI vendor presence, product surface and pricing signals from the live site | https://apify.com/mambalabs/ai-tooling-detector?fpr=mamba |

Runnable example input, matched to the live tool schema:

`detect_ai_tooling`:

```json
{
  "domain": "example.com",
  "check_pricing": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Detect vendor presence on the live site and in the product surface.
2. Read the pricing page. An AI capability that appears as a priced tier or an add on is a budget signal; one that appears only in marketing copy is an announcement.
3. Place the company: shipped, announced, or neither, and say which evidence put it there.
4. For shipped, the angle is operational, about what happens after launch. For announced, the angle is about the gap between announcement and delivery. For neither, do not invent an AI angle at all.
5. Cross check against hiring. A company with no AI on the site and three AI roles open is in the announced group, not the neither group.
6. State what would change the classification, so the read can be refreshed rather than repeated.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The classification with its evidence, the pricing read, the cross check against hiring, the angle for that group, and the refresh trigger.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The classification names the evidence that produced it
- No AI angle is written for the neither group
- Pricing evidence is distinguished from marketing copy
- The hiring cross check is run before the classification is final

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `tech-stack-signal-reader`
- `hiring-signal-spotter`
- `gtm-signal-aggregator`

Ships in the **signal-based-selling** pack.
