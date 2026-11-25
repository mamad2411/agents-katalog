---
name: first-conduct-rule
description: >
  Analyze agreements under the first conduct rule (s.6 Competition Ordinance,
  Cap 619) — cartels, bid-rigging, price fixing, market sharing, collective
  boycott, block exemptions (s.4 MSO exemption).
---

# First Conduct Rule (s.6, Cap 619)

## Overview

The First Conduct Rule prohibits anti-competitive agreements, concerted practices, and decisions by associations of undertakings that have the object or effect of preventing, restricting, or distorting competition in Hong Kong.

## Key Provisions

### s.6 — Prohibition
- Agreements between undertakings
- Decisions by associations of undertakings
- Concerted practices
- Must have the object or effect of harming competition in Hong Kong

### Serious Anti-Competitive Conduct (SACC)

The following are deemed serious anti-competitive conduct with enhanced penalties:

1. **Price Fixing** — Agreeing on purchase/selling prices or trading conditions
2. **Bid Rigging** — Collusive tendering arrangements
3. **Market Sharing** — Dividing markets by geography, customer type, or product
4. **Output Limitation** — Restricting production or supply
5. **Collective Boycott** — Coordinated refusal to supply or purchase

A finding of SACC triggers higher penalties and may lead to director disqualification orders under s.106.

## Block Exemptions

### s.4 MSO Exemption (Schedule 1)
- Mergers and acquisitions (first conduct rule does not apply)
- Regulated by the merger provisions (s.12–17)

### Other Block Exemptions
The Competition Commission may issue block exemption orders for categories of agreements that meet efficiency criteria (s.9).

## Exclusion and Exemption Orders (s.8–10)

- **s.8**: Agreements enhancing overall economic efficiency
- **s.9**: Block exemption orders by Commission
- **s.10**: Exclusion orders by Chief Executive in Council (public policy grounds)

## Enforcement

- **Competition Commission**: Investigation and enforcement
- **Competition Tribunal**: Adjudication and penalties
- **Maximum penalty**: Up to 10% of Hong Kong gross turnover for each year of infringement (up to 3 years)

## Typical Analysis Framework

1. Identify the parties (undertakings?)
2. Identify the agreement/concerted practice
3. Does it have anti-competitive object or effect?
4. Is it SACC (serious anti-competitive conduct)?
5. Does a block exemption apply?
6. Does an exclusion/exemption order apply?


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
