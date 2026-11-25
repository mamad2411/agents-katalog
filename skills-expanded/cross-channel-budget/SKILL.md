---
name: cross-channel-budget
description: When the user wants to allocate monthly ad budget across TikTok, Meta, ASA, and Google UAC. Use when the user mentions "budget split", "how much per channel", "ad budget allocation", "paid growth budget plan", or "where should I spend my ad budget". For performance data to inform allocation, see cross-channel-performance. For profitability check, see campaign-profitability.
metadata:
  version: 1.0.0
---

# Cross-Channel Budget Allocation

You are a paid growth strategist. Allocate monthly ad budget across channels based on app type, data maturity, and unit economics — then produce a week-by-week execution plan.

## Initial Assessment

1. Read `app-ads-context.md` for total budget, active channels, LTV, CPA targets
2. Check if historical performance exists (from `cross-channel-performance` or context doc)
3. Ask:
   - **Total monthly budget:** $___
   - **App category and geo focus**
   - **Connected channels:** TikTok / Meta / ASA / Google UAC
   - **Data maturity:** New (no data) / Testing (7–14d) / Proven (30d+)
   - **iOS vs Android priority**

## Allocation Philosophy

| Principle | Rule |
|-----------|------|
| ASA first (iOS) | Highest intent, best ROAS for search-driven apps |
| Minimum viable spend | Social/UAC $50/day, ASA $30/day — below floor, don't run that channel |
| Test reserve | Hold 10% for new creative/channel tests |
| Data before scale | No channel > 50% until CPA proven over 50+ conversions |
| Learning budget | First $500/channel is testing — expect negative ROI |

## Default Allocation (No Data Yet)

Use when no performance data exists. **Never split below min viable daily spend.** $1,000/month split 60/20/20 is ~$20 ASA + ~$7 TikTok + ~$7 Meta — none of those learn.

| Monthly budget | Rule | Example |
|----------------|------|---------|
| ≤ $1,500 | **One channel only.** Do not split. | iOS search → 100% ASA (~$30–50/day). Visual/consumer → 100% TikTok or Meta at $50/day. |
| $3,000 | Two channels max, each at floor. | iOS: 40% ASA (~$40/day) + 50% one social (~$50/day) + 10% reserve. Not Meta *and* TikTok. |
| $10,000 | Three channels if each ≥ $50/day. | 30% ASA / 30% TikTok / 30% Meta / 10% reserve. |
| $30,000+ | Add UAC only after social is proven. | 25% ASA / 30% TikTok / 30% Meta / 10% UAC / 5% reserve. |

**Adjust defaults by app type** (only when budget already supports 2+ channels at floor). At ≤ $1.5K, pick the **single** best channel for the type — do not percentage-shift a one-channel plan.

| App type | Shift |
|----------|-------|
| Android-primary | Prefer Google UAC or Meta as the one channel; skip ASA |
| Visual/consumer | Prefer TikTok as the one channel / more TikTok when splitting |
| B2B/productivity | Prefer ASA as the one channel / more ASA when splitting |
| Gaming | Prefer TikTok; add UAC only at $10K+ |

### Why ASA first for iOS

- Users are actively searching — highest conversion intent
- No creative production needed to start
- Reliable attribution (no SKAN delay)
- Typically 30–50% tap-to-install CVR

## Data-Driven Reallocation

After 14+ days of data from `cross-channel-performance`:

### Weight formula

```
Weight(channel) = (1 / CPA_channel) / sum(1 / CPA_all_channels)
```

Apply weights to total budget, then apply caps:

| Cap | Rule |
|-----|------|
| Max single channel | 50% of total until 50+ conversions |
| Min per active channel | Social/UAC $50/day, ASA $30/day — else pause |
| Test reserve | Always hold 5–10% |

### ROAS-adjusted allocation (subscription apps)

When revenue data is available:

```
Weight(channel) = ROAS_channel / sum(ROAS_all_channels)
```

Blend CPA and ROAS weights 50/50 for balanced allocation.

## Budget Tiers by Maturity

### Tier 1 — Launch (Month 1, no data)

| Week | Focus | Budget split |
|------|-------|-------------|
| Week 1 | MMP verification + **one** channel | 100% that channel (ASA if iOS search, else TikTok or Meta) |
| Week 2 | Optimize the first channel | Still 100% — do not add a second channel yet |
| Week 3 | Add a second channel **only if** leftover daily budget still meets the floor | Otherwise keep concentrating |
| Week 4 | First `cross-channel-performance` review if 2 channels are live | Else stay on the winner |

### Tier 2 — Testing (Month 2, 7–14d data)

- Run `cross-channel-performance` weekly
- Reallocate 20% from worst to best channel every 2 weeks
- Maintain test reserve for 1 new creative test/week per social channel

### Tier 3 — Scaling (Month 3+, proven CPAs)

- Scale best channel 20%/week until CPA rises 15%
- Hold test reserve at 5%
- Consider new channel tests (Google UAC, Snapchat) from reserve

## Test Reserve Rules

| Rule | Detail |
|------|--------|
| Hold amount | 10% of monthly budget (5% at $30K+) |
| Minimum test | $50/day for 2 days per new test |
| What to test | New creative angle, new audience, new channel |
| Kill criteria | 2× target CPA with 0 conversions after $100 spend |
| Success criteria | CPA < target → promote to main budget next month |

## Daily Budget Calculation

```
Daily budget per channel = (Monthly allocation × 12) / 365
```

Or simplified: `Monthly allocation / 30`

Present both monthly and daily in output. Flag if any social/UAC channel is under $50/day or ASA is under $30/day — pause that channel instead of starving it.

## Channel Launch Sequence

For a new app with full budget available:

| Order | Channel | Prerequisite | Min daily |
|-------|---------|--------------|-----------|
| 1 | ASA | App live on App Store | $30 |
| 2 | Meta or TikTok | MMP verified | $50 |
| 3 | Second social | 7d data from first social | $50 |
| 4 | Google UAC | Android live + Firebase linked | $30 |

Do not launch social channels before `mmp-setup` is verified.

## Output Template

```markdown
# Budget Plan — [App Name] — $[total]/month

## Assumptions
- Data maturity: New / Testing / Proven
- LTV: $___ | Target CPA: $___
- Geo: [focus] | Platform: iOS / Android / Both

## Allocation
| Channel | % | $/month | $/day | Goal CPA | Min test days |
|---------|---|---------|-------|----------|---------------|
| ASA | | | | | 7 |
| TikTok | | | | | 7 |
| Meta | | | | | 7 |
| Google UAC | | | | | 7 |
| Test reserve | | | | — | — |
| **Total** | 100% | | | | |

## Week 1 focus
- [Channel]: [setup skill] — $/day
- [Channel]: [setup skill] — $/day
- Prerequisite: [mmp-setup / app-ads-context]

## Reallocation triggers
| Signal | Action |
|--------|--------|
| Channel CPA < 0.8× others (14d) | Shift 20% budget to winner |
| Channel CPA > 2× target (7d) | Pause, reallocate to reserve |
| ROAS > 1.5× for 7d | Scale channel 20% |

## Revisit schedule
- Day 7: First `cross-channel-performance` check
- Day 14: First reallocation review
- Day 30: Full `campaign-profitability` review

## Kill criteria (per channel)
- Spend > 2× target CPA with 0 conversions → pause
- ROAS < 0.5× for 14 days → pause and diagnose
```

## Common Mistakes

- Splitting budget evenly across all channels (wastes learning budget)
- Running 4 channels at $10/day each (none gets enough data)
- Splitting a $1K month across ASA + TikTok + Meta (each dies in learning)
- Scaling social before MMP is verified
- Ignoring ASA for iOS apps with search intent
- Not holding test reserve (no room to experiment)
- Reallocating on < 7 days of data

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| Performance data needed | `cross-channel-performance` |
| Profitability check | `campaign-profitability` |
| MMP not set up | `mmp-setup` |
| ASA launch | aso-skills `apple-search-ads` (structure), then `asa-weekly-optimization` |
| Social launch | `tiktok-campaign-setup` or `meta-campaign-setup` |
| Google UAC | `google-uac-campaign` |
| LTV unknown | `subscription-snapshot` |

## Related Skills

- `cross-channel-performance` — data to inform reallocation
- `campaign-profitability` — verify economics before scaling
- `app-ads-context` — store budget plan
- `mmp-setup` — prerequisite for social channels
- aso-skills `apple-search-ads` — ASA campaign structure
- `tiktok-campaign-setup` / `meta-campaign-setup` — social execution
- `google-uac-campaign` — Google App Campaigns
