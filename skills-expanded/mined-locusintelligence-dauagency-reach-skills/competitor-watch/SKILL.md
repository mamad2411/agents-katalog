---
name: competitor-watch
description: Read-only Google Business Profile (GMB, Google My Business) competitor watch with the Reach MCP server. Lists the nearby businesses that outrank you in local search and Google Maps for your tracked keywords, then reads a chosen rival's 12-month rating and photo history and summarises what changed. Never changes anything. Use when someone asks who their local competitors are, what a competitor on Google Maps is doing, or how their rivals' reviews and photos are trending.
license: MIT
---

# Competitor watch

A read-only look at who competes with a business in local search and how those rivals have changed. This skill never writes.

## Setup

This skill needs the Reach MCP server connected in your AI client:

- Server URL: `https://reach.locus-intelligence.com/api/mcp` (remote, Streamable HTTP, OAuth sign-in, no API key)
- Setup for Claude, ChatGPT, Claude Code, Codex, Cursor, VS Code and others: [README](https://github.com/LocusIntelligence-DauAgency/google-business-profile-mcp#install)

## Steps

1. **Pick the location.** Call `get_account`. If there is more than one location, ask which one. If its `connectionStatus` is not `active`, tell the owner to reconnect Google in Reach and stop.
2. **List competitors.** Call `get_visibility` with `sections: ["competitors"]`. To focus on one keyword, pass it as the first item of `keywords`. Competitors come from tracked keywords only; if none are tracked, say so and stop (tracking is a separate, confirmed step in the rank audit task).
3. **Show the field.** A short table: each competitor's name, rank or position, rating and review count as returned, and how the business compares.
4. **Pick rivals.** Ask which competitors to look at closely, or take the top 3 above the business if the owner says "you choose".
5. **Rival history.** For each chosen rival, call `get_visibility` with `sections: ["competitors"]` and `rivalCid` set to that competitor's `cid` from step 2. This adds its 12-month rating and photo history.
6. **Summarise changes** per rival:
   - Rating and review count now versus the start of the history, and when the biggest moves happened.
   - Photo count changes over the period.
   - How the business compares on the same measures (from `get_listing` with `sections: ["reviews", "media"]` if needed).
7. **Close** with observations, not orders: what the data suggests the business could match, each tied to a number above.

## Rules

- Read-only. Do not call any tool that changes Google or Reach.
- Use only facts the tools returned. Do not guess a rival's revenue, ads spend, strategy or private data, and do not look them up elsewhere unless the owner asks.
- Name a cause only when a result shows it; otherwise call it a possibility.
- Never promise the business will overtake anyone.

## Safety

- This skill never publishes, edits or tracks anything.
- Stop if the location's `connectionStatus` is not `active`.
- Read `limitations` before saying there is no data; relay each message and its link.
- On `limit_reached` or `monthly_quota_exhausted`, say what was blocked, give the `manageUrl`, and stop. On `listing_only`, relay the message and `connectUrl`, and stop.
