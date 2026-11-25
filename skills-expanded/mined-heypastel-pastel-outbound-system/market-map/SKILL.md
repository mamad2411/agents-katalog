---
name: market-map
description: Cartographer — chooses which slice of the market to work, writes down how to recognise a buyer in it, and turns that into Pastel ICP definitions and agents. Use for "who should we target", a new market or segment, a brief made only of a website, an empty lead list, or when what-works says the aim is off.
---

# Market map — Cartographer

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Pastel's agents only bring back what they're told to watch. A market map is that instruction: which accounts, which people, which moments, which sources.

## Steps

1. **See what exists.** `outbound-brief.md`, `pastel_get_workspace_context`, `pastel_list_icp_definitions`, `pastel_list_agents(include_stats=true)`, plus `pastel_aggregate_leads` by `industry` and by `company_size` to see where leads already cluster. Read the latest `what-works` report if there is one.
2. **Draw up to three segments**, each written as one sentence a salesperson could repeat: _"Series A–B SaaS in France, 20–150 people, selling to mid-market."_ Name the most promising one first and say why.
3. **For each segment, three recognisers:**
   - **the account** — sector, headcount, country, how they make money;
   - **the person** — the role that feels the pain, and whether they can sign;
   - **the moment** — what they do in public right before they buy (ask their network for a tool, react to a competitor's launch, post about the problem, open a role in the team we'd equip).
4. **Exclusions:** the off-limits list from the brief, plus any segment `what-works` shows produced no hot replies over at least 50 people.
5. **Compare with Pastel:** which segments already have an agent, which agents produce leads (stats), which drift outside the map.
6. **Write the Pastel changes** — `create_icp_definition`, `update_icp_definition`, `create_agent`, `update_agent` — each with its exact params and a one-line reason. After approval, request them and confirm with `pastel_list_agents`.

## Output

```
# Market map — [date]

Segment 1 (start here): [one sentence]
  Account:
  Person:
  Moment:
Segment 2 / 3: …

Exclusions:
Pastel changes: action · params · reason
First batch: how many leads, which segment, which moment
Open questions:
```

