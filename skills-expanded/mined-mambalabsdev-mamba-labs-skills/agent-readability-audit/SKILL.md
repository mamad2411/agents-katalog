---
name: agent-readability-audit
description: |
  Check whether a website can be read and used by AI agents, and fix what blocks them. Use when someone asks about AI search visibility, agent accessibility, structured data, or whether their site works for AI crawlers.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content, seo_content_engine]
metadata:
  title: "Agent Readability Audit"
  category: "seo-content"
  tags: "seo_content, seo_content_engine"
  keywords: "seo and content, ai search visibility, can agents read my site, structured data audit, llms txt, ai crawler accessibility"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Node.js 18+."
---

# Agent Readability Audit

## What this does

A growing share of buying research happens through agents that never render a page. What they can read is a small, checkable set of things: the crawl directives, the structured data, the machine readable endpoints, and whether the important content survives without scripting. This skill audits those four and returns the fixes in the order that changes an agent's answer.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: agent-accessibility-auditor 0.005 USD per domain. |
| Node.js 18 or newer | Required | The MCP tool calls | Free. It starts the Mamba Labs MCP server with `npx`. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- AI search visibility
- can agents read my site
- structured data audit
- llms txt
- AI crawler accessibility

## Inputs

- **domain**: the site to audit
- **pages**: the pages that matter commercially

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

The audit reads the live site's crawl directives, structured data and endpoints.

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
| Agent Accessibility Auditor | `audit_agent_accessibility` | crawl directives, structured data, endpoints and agent readability checks | https://apify.com/mambalabs/agent-accessibility-auditor?fpr=mamba |

Runnable example input, matched to the live tool schema:

`audit_agent_accessibility`:

```json
{
  "domain": "example.com",
  "check_endpoints": true,
  "check_structured_data": true
}
```

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Check the crawl directives first. A site that blocks agent user agents has one fix that makes every other fix matter, and many sites block them without knowing.
2. Check structured data on the commercially important pages, not on the homepage. Product, pricing and documentation pages are where an agent answer is sourced.
3. Check whether the key content is present without scripting. Content that requires a rendered page is invisible to a large share of readers.
4. Check the machine readable surfaces: a documentation endpoint, a sitemap that is current, and any published index of what the site contains.
5. Rank the fixes by whether they change what an agent can answer. A missing schema type on a blog post does not; a blocked user agent does.
6. Re test after fixing rather than assuming, since crawl directives interact in ways that are easy to get wrong.
7. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A four section audit with pass or fail per check, the ranked fix list with the answer each fix unblocks, and the re test result.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Crawl directives are checked before anything else
- Structured data is checked on commercially important pages, not the homepage
- Content availability without scripting is tested
- Fixes are ranked by what they change in an agent answer
- A re test is run after the fixes

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `listing-page-optimizer`
- `programmatic-seo-planner`
- `comparison-page-builder`

Ships in the **seo-content-engine** pack.
