---
name: eqr-sector-overview
version: 1.0.0
description: Map a sector — structure, drivers, competitive dynamics, key debates, and relative positioning of names — into a framework note that grounds single-stock work.
author: matrixx0070
tags: [equity-research, sector, industry, framework, relative-value]
capabilities: []
---

## When to use

Use this when you're picking up a new sector, orienting before single-stock work, or need a shared framework for comparing names within an industry. A sector overview establishes the drivers, the structure, the debates, and where each name sits — the top-down context that keeps single-stock theses honest.

**Not for:** a full call on one name (use `eqr-initiating-coverage`), finding a specific idea (use `eqr-idea-generation`), or a daily update (use `eqr-morning-note`). This is the map, not the destination. Outputs are research and education, not personalized investment advice.

## Method

1. **Define the sector and its boundaries.** What's in, what's out, and the sub-segments that behave differently.
2. **Identify the demand and supply drivers.** What makes the sector grow or shrink — end markets, cycle, regulation, technology. *Decision point:* secular vs. cyclical drivers change how you weight the current point in the cycle.
3. **Assess structure and profit pools.** Concentration, barriers to entry, bargaining power (Porter-style), and where the profit actually accrues in the value chain.
4. **Frame the key debates.** The two or three questions the market argues about (e.g., pricing durability, capacity discipline, disruption risk) — where views differ and money is made or lost.
5. **Position the names.** A relative table: growth, margin, valuation, and exposure of each covered name to the drivers and debates.
6. **Rank relative attractiveness.** Best-to-worst within the sector on risk/reward, with the reason — not absolute calls, but who wins if the debate resolves each way.
7. **State the sector view and what changes it.** Overweight/neutral/underweight framing and the observable that would flip it.

## Example

Map the memory-semiconductor sector. Sub-segments: DRAM, NAND — different cycles. Drivers: AI-server demand (secular) layered on a supply-driven pricing cycle (cyclical). Structure: DRAM oligopoly (three players, disciplined capex) vs. more fragmented NAND. Key debates: (1) is capacity discipline durable, (2) how much AI demand is pull-forward. Names table: pure-play A (high beta to DRAM price), diversified B (steadier), equipment C (early-cycle). Ranking: A best risk/reward if discipline holds; B the hedge. Sector view: overweight into the up-cycle; flips if inventory days re-expand two months running.

## Pitfalls

- **Bottom-up in disguise.** Stacking single-stock views without the structural frame that reconciles them.
- **Ignoring the cycle position.** Treating cyclical drivers as secular (or vice versa) mistimes the whole sector.
- **No profit-pool view.** Growth without asking who captures it leads to owning the wrong link in the value chain.
- **Debates without positioning.** Naming the debate but not showing which names win under each resolution.
- **Static map.** Sector dynamics shift; state the observable that changes the view or the note goes stale.

## Output format

```
SECTOR OVERVIEW: <sector> | as of <date>
SCOPE: sub-segments in/out
DRIVERS: demand | supply | secular vs cyclical
STRUCTURE: concentration | barriers | bargaining power | profit pools
KEY DEBATES: 1) … 2) … 3) …
NAMES TABLE: ticker | growth | margin | valuation | driver/debate exposure
RANKING (risk-reward): best -> worst + reason
SECTOR VIEW: OW/N/UW | flips if: <observable>
Note: research/education, not personalized investment advice.
```

## Reference

Research process: establish the top-down frame first — scope, demand/supply drivers separated into secular versus cyclical, industry structure and profit pools, and the two or three debates where views diverge — then position covered names against that frame in a relative table. Modeling: the overview sets shared assumptions and relative rankings that single-stock work in `eqr-initiating-coverage` and `eqr-model-update` inherits, keeping bottom-up theses consistent with the sector picture. Disclosure: a sector overview is research and education, its rankings are relative and cycle-dependent opinions rather than absolute calls, and it is not personalized investment advice or a recommendation to transact.
