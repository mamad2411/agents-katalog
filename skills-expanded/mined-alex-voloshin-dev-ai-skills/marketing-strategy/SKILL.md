---
name: marketing-strategy
description: Use this skill when the agent is defining or revising marketing positioning, messaging, channel mix, content pillars, a tactical/calendar plan, or success metrics — for marketing strategy frameworks covering hierarchy (mission → positioning → messaging → channels → pillars → tactical → calendar), channel-selection (audience/resource/content fit), content-pillar model, and measurement framework (vanity / engagement / pipeline / revenue). The reusable knowledge layer behind /marketing-init (one-time setup) and /marketing (recurring ops) — both reference these frameworks instead of inlining them.
disable-model-invocation: true
---

# Marketing Strategy Frameworks

Reusable strategy frameworks shared by `/marketing-init` (one-time strategy setup) and `/marketing` (recurring operations). Knowledge-only — never invoked directly.

## Marketing Strategy Hierarchy

```
Mission (why we exist)
  └── Positioning (who we serve, what we offer, why us)
        └── Messaging Framework (value prop, pillars, proof points)
              └── Channel Strategy (where we show up)
                    └── Content Pillars (what we talk about)
                          └── Tactical Plan (daily/weekly/monthly)
                                └── Content Calendar (specific tasks + dates)
```

Decisions flow top-down: positioning constrains messaging, messaging constrains channels, channels constrain pillars, pillars feed the tactical plan, the plan populates the calendar. When a lower layer feels off, audit the layer above before patching the symptom.

## Channel Selection Framework

Evaluate each candidate channel on three dimensions before committing:

| Dimension | Question |
|---|---|
| **Audience fit** | Is our ICP active here? Can we reach them? |
| **Resource fit** | Can we sustain the required publishing cadence? |
| **Content fit** | Does our content type work on this platform? |

**Rule:** better to do 2 channels well than 5 channels poorly. Start with 1–2 high-fit channels and expand only after consistent execution proves cadence is sustainable.

## Content Pillar Model

Define 3–5 content pillars aligned with:

1. **ICP pain points** — problems the audience actively searches for
2. **Product strengths** — areas where the product genuinely excels
3. **Industry expertise** — topics with unique knowledge or data
4. **Trending intersections** — emerging topics that connect to the product

Each piece of content maps to exactly one pillar. Track pillar distribution to avoid over-indexing on a single topic. Re-balance pillars during the monthly `strategy-review` operation if any pillar exceeds ~50 % of output for two months in a row.

## Measurement Framework

| Level | Metrics | Review cadence |
|---|---|---|
| **Vanity** (awareness) | Impressions, followers, page views | Weekly (track, don't optimize for) |
| **Engagement** | Likes, comments, shares, click-through | Weekly |
| **Pipeline** | Signups, leads, demo requests, email subs | Weekly |
| **Revenue** | Conversions, MRR impact, CAC, LTV | Monthly |

**Rule:** optimize for pipeline + revenue. Use vanity metrics only as leading indicators — when vanity rises but pipeline does not, the channel is delivering reach but not relevance, and the messaging or audience fit is off.

## ICP and Positioning References

- **JTBD framing** — Clayton Christensen "Jobs to Be Done"; users hire products to make progress on a specific job in a specific context
- **April Dunford positioning** — define competitive alternatives, unique attributes, value the attributes deliver, market category, the ICP that cares most
- **ICP tiering for B2B** — tier-1 (named accounts, hand-crafted), tier-2 (account list, programmatic), tier-3 (broader segment, automated). See ABM playbook in `/marketing` for B2B specifics.

## When each framework applies

| Phase | Framework |
|---|---|
| `/marketing-init` Step 3 — Define Strategy | Hierarchy, Channel Selection, Content Pillar |
| `/marketing-init` Step 5 — Create Content Calendar | Content Pillar, Measurement |
| `/marketing analytics` (weekly) | Measurement |
| `/marketing strategy-review` (monthly) | All four — full re-audit top-down |
| `/marketing trend-research` (weekly) | Content Pillar (map new opportunities to pillars) |

## Integration

- **Used by**: `/marketing-init` (one-time setup), `/marketing` (recurring operations)
- **Companion to**: `marketing-strategist` agent (applies these frameworks when spawned by either workflow)
- **External references**: Clayton Christensen JTBD, April Dunford "Obviously Awesome" positioning model
