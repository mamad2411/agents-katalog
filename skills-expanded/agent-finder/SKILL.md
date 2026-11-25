---
name: agent-finder
description: >-
  Use when the user wants to find or evaluate real estate agents in an area or for a
  property — search agents, pull their profile, recent listings/sales, and reviews,
  then return a vetted shortlist. Triggers on "find a realtor in …", "who are the top
  agents for …", "who listed this house", "best selling agents near …", "agent
  reviews for …".
allowed-tools: Bash, Read, Write, WebFetch
version: 1.0.0
homepage: https://www.realtyapi.io
repository: https://github.com/realtyapi/realtyapi-skills
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - REALTYAPI_API_KEY
    primaryEnv: REALTYAPI_API_KEY
    homepage: https://www.realtyapi.io
    tags:
      - real-estate
      - agents
      - realtor
      - reviews
      - realtyapi
---

# Agent Finder

## Overview

Find the right real estate agent for an area or property and back the recommendation
with evidence — recent activity, specialization, and reviews — as a ranked shortlist.

Use [`realtyapi-api`](../realtyapi-api/SKILL.md) for auth and endpoint discovery.

## When to Use

- "Find me a top buyer's agent in {area}."
- "Who are the most active listing agents for {neighborhood}?"
- "Who listed this property?"
- "Pull reviews for this agent."

## Workflow

1. **Pick the portal** that has agent data for the market (US portals like `redfin`,
   `realtor`, `zillow` have agent search/details/reviews; check `llms.txt` for
   `agent*` endpoints on the relevant portal).
2. **Search agents** for the area/criteria (`agent/search`, `agentsearch`), or get the
   listing's agent (`owner-agent`, `agentInfo`) when starting from a property.
3. **Enrich** each candidate: profile/details, recent listings & sales, and reviews
   (`agentdetails`, `agentforsale`/`agentsold`, `agentreviews`).
4. **Score for fit** — recent activity/volume in the user's area and price band,
   buyer-vs-seller focus, property-type match, and review signal.
5. **Shortlist** with reasoning and contact/profile links.

## Output Format

```markdown
# Agent Shortlist: {area / property}

Portal: {} · {N} candidates

| # | Agent | Brokerage | Recent sales (12mo) | Area/price focus | Rating | Profile |
|--:|-------|-----------|--------------------:|------------------|-------:|---------|

## Recommendations
1. {agent} — fit because {recent activity in area + price band + reviews}
2. …

## Notes
- Ranked by: {criterion}
- Caveats: activity counts are from public portal data and may be partial.
```

## Common Pitfalls

- Match the agent to the user's **side** (buyer vs. seller) and price band — raw sale
  counts alone don't equal fit.
- Reviews can be sparse or skewed; treat them as one signal, not the verdict.
- Don't expose private contact info beyond what the public profile provides.
- Note that activity figures reflect public portal data and may undercount.
