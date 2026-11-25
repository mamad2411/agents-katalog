---
name: find-a-power
description: Search or browse Operator Powers when the user asks what the plugin can do, describes a job without naming a skill, or asks whether a power exists.
---

# Find a Power

## The Job

Match what the user is trying to do to the right power, or tell them honestly that none fits.

## How to Run It

1. Read the local catalogue at `${CLAUDE_PLUGIN_ROOT}/catalog/powers.json` (fall back to `catalog/powers.json` two directories above this skill file). The local catalogue is the source of truth for what is actually installed.
2. Match the user's request using the catalogue's weighted order: an explicit power name first, then an exact trigger or deliverable phrase, then title terms, trigger terms, `oneLineJob`, and finally description terms. Shared topic words alone are weak evidence.
3. Apply `negativeTriggers` as vetoes, then use `${CLAUDE_PLUGIN_ROOT}/docs/ROUTING-CONTRACTS.md` for adjacent jobs. The primary deliverable decides ownership.
4. Return at most three ranked recommendations. For each: the job it completes, the name, and one sentence on why it matches this request. Lead with the job, not the identifier.
5. If exactly one clearly fits, offer to start it now with the context the user already gave.
6. If nothing fits, say so plainly and mention `request-a-power`. Never stretch a skill to a job it does not do.

## Live Enrichment (Optional)

If the `operator_powers` MCP server is connected and the user wants current information (newest additions, current examples, release notes), you may call its read tools (`search_powers`, `get_power`). Rules:

- The local catalogue decides what is installed. Never claim a skill from the live catalogue is available locally unless the local catalogue contains it; if it is newer than the installed version, say it arrives with a plugin update.
- If the service is unreachable, continue with the local catalogue and say live information was unavailable. Never block on it.

## Boundaries

- Browsing sends nothing anywhere; the MCP read tools receive only the search query, and only when the user wants live information.
- Never list internal file paths or metadata at the user; jobs and names only, unless they ask for detail.
- Weighted search is not an opaque personal score. It is a deterministic routing rule that favours explicit job language and uses negative phrases to prevent known collisions.
