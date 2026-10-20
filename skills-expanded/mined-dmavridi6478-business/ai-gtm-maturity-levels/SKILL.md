---
name: ai-gtm-maturity-levels
description: Places a go-to-market team on the 5 Levels of AI in GTM (AI is a Tab → Feature → Layer → Engine → Brain), names the tools typical of each level, and defines the single next-level move. Use when someone asks how "AI-native" their sales/marketing is, what to automate next, or how to sequence a GTM AI roadmap. Run via /gtm-ai-level.
---

# The 5 Levels of AI in GTM

Source: Matteo Fois / Kinetyca infographic. It is a practitioner's maturity ladder, not a benchmarked standard — use it to structure a conversation, not to score against industry data.

| Level | Name | Team shape | Defining sentence | Typical tools shown |
|---|---|---|---|---|
| 1 | AI is a Tab | Solo founder | "Copy gets faster. Nothing changes." | Claude, ChatGPT |
| 2 | AI is a Feature | Small team | "Built in. Not connected." | HubSpot, Apollo, LinkedIn |
| 3 | AI is a Layer | GTM operator | "AI runs before humans decide." | Smartlead, Clay, Claude |
| 4 | AI is an Engine | GTM engineer | "Signals trigger execution automatically." | Clay, Supabase, n8n |
| 5 | AI is the Brain | AI-native team | "System reasons, remembers, improves." | Claude, Supabase, n8n, GitHub |

## Diagnostic questions (ask in one batch)

1. Where does AI output go after it is generated — into a doc a human pastes, or into a system? (L1 vs L2+)
2. Are AI features inside each tool connected to each other, or does a human move data between them? (L2 vs L3)
3. Does AI run *before* a human decision (enrich, score, draft) or only *on request*? (L3)
4. Does a buying signal (job change, funding, site visit) trigger an action with no human starting it? (L4)
5. Does the system store what worked, and change its own prompts/rules based on results? (L5)

Placement = the highest level where the answer is a clear yes AND evidence exists. Do not credit aspirations.

## Rules

- **Never recommend skipping a level.** A Level-4 signal engine on top of an unconnected Level-2 stack automates noise. The next move is always exactly one level up.
- The next-level move must name one concrete integration, one owner, and one metric (e.g. "connect enrichment to CRM; owner RevOps; metric = % of leads enriched before first touch").
- Send actions (email, LinkedIn, ads) stay behind a human approval gate until Level 4 has run cleanly for a full cycle — see `gtm-outbound-engine` and `outbound-campaign-brief`.
- Map to connectors only if they are actually connected in this account (Clay, HubSpot, Zapier, Notion, Slack are); say "not connected" for the rest (Smartlead, Apollo, Supabase need authorisation).

## Output format

```
Current level: <n — name> (evidence: …)
Why not higher: <the failing diagnostic question>
Next-level move: <one integration + owner + metric>
30-day plan: week 1 … week 4
Risks: <data quality, GDPR consent, over-automation>
```

Pair with: `gtm-strategy`, `gtm-outbound-engine`, `gtm-stack-20person-b2b`, `n8n-agent-builder`, `revops`.
