---
name: cross-channel-performance
description: When the user wants a unified view of TikTok, Meta, and Apple Search Ads performance in one report. Use when the user mentions "all channels performance", "compare TikTok vs Meta", "paid channel dashboard", "where should I spend", or "channel comparison". For budget allocation, see cross-channel-budget. For profitability verdict, see campaign-profitability.
metadata:
  version: 1.0.0
---

# Cross-Channel Performance Dashboard

You are a paid growth analyst. Produce a unified performance report across all connected ad channels — spend, installs, conversions, CPA, and ROAS — in one executive view.

## Initial Assessment

1. Read `app-ads-context.md` for active channels, budget, and CPA targets
2. Check credential status for each platform
3. Ask for date range: default **last 7 days** (operational) or **last 14 days** (strategic)
4. Identify which channels are connected vs. planned

## Credential Check

| Platform | MCP Tool |
|----------|----------|
| TikTok | `tiktok_ads_credentials_status` |
| Meta | `meta_ads_credentials_status` |
| ASA | `asa_credentials_status` |
| RevenueCat | `rc_overview` (test with keys) |

Report which channels have data vs. which need connection. Don't skip disconnected channels — note them as "not connected" in the dashboard.

## Data Collection

Pull last 7d (or user-specified) from each connected channel:

### TikTok

```
tiktok_ads_performance
  level: advertiser
  days: 7
```

For campaign-level drill-down:

```
tiktok_ads_performance
  level: campaign
  days: 7
```

### Meta

```
meta_ads_insights
  target_type: ad_account
  date_preset: last_7d
  level: campaign
```

If user has a specific ad account:

```
meta_ads_insights
  target_type: ad_account
  ad_account_id: "act_xxx"
  date_preset: last_7d
  level: campaign
```

### Apple Search Ads

```
asa_profitability
  rc_key: "<sk_xxx>"
  level: campaign
  days: 7
  min_spend: 5
```

### Revenue context

```
rc_overview
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"

rc_attribution_summary
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
```

## Unified Metrics Table

Build this table for every connected channel:

| Channel | Spend | Impressions | Clicks | Installs | Conv | CPI | CPA | Revenue* | ROAS | Trend |
|---------|-------|-------------|--------|----------|------|-----|-----|----------|------|-------|
| TikTok | | | | | | | | | | ↑/↓/→ |
| Meta | | | | | | | | | | |
| ASA | | | | | | | | | | |
| Google UAC | | | | | | | | | | manual |
| **Total** | | | | | | | | | | |

*Revenue from RC attribution or `asa_profitability` join where available. Mark estimated revenue with ~ prefix.

### Derived metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| CPI | Spend / Installs | Top-of-funnel efficiency |
| CPA | Spend / Conversions | Bottom-of-funnel efficiency |
| ROAS | Revenue / Spend | Profitability signal |
| CTR | Clicks / Impressions | Creative relevance (social) |
| CVR | Installs / Clicks | Store listing quality |
| Share of spend | Channel spend / Total spend | Budget allocation check |

## Channel Fit Guide

Help the user interpret which channels suit their app:

| App type | Usually best channel | Why |
|----------|---------------------|-----|
| High-intent utility | ASA first | User is searching for solution |
| Visual consumer / B2C | TikTok | Demo-friendly, young audience |
| Broad demographic | Meta | Scale + lookalike targeting |
| Subscription beauty/lifestyle | TikTok + Meta test | UGC creative performs well |
| Productivity / B2B | ASA + Meta | Intent + professional targeting |
| Gaming | TikTok + Google UAC | Visual gameplay hooks |
| Niche community | Meta (interest) + Reddit | Precise interest targeting |

Cross-reference with user's category from `app-ads-context.md`.

## Trend Analysis

Compare current period to prior period (pull `days: 14` and split, or use two date ranges):

| Signal | Diagnosis | Action |
|--------|-----------|--------|
| Spend up, CPA up | Audience saturation or creative fatigue | Refresh creatives |
| Spend up, CPA stable | Healthy scaling | Continue |
| Spend down, CPA up | Budget cut on best ad sets | Check pacing |
| Installs up, conversions flat | Low-quality traffic | Tighten targeting or event optimization |
| ASA CPI low, social CPA high | Normal — ASA is highest intent | Don't compare CPI directly |

## Reallocation Recommendation

If one channel CPA < 0.8× others with meaningful volume (50+ conversions):

1. Shift 20% budget from worst-performing channel to best
2. Document in output with specific dollar amounts
3. Route to `cross-channel-budget` for formal reallocation plan

**Minimum volume rule:** Don't reallocate based on < 20 conversions or < 7 days of data.

## Per-Channel Drill-Down

For each channel, include a brief section:

### TikTok highlights
- Top campaign by CPA
- Worst campaign (pause candidate)
- Creative fatigue signal (CTR declining 3+ days)

### Meta highlights
- Top ad set by CPA
- Audience breakdown if available
- Event optimization status (install vs. purchase)

### ASA highlights
- Top campaign by ROAS
- Bleeder campaign (ROAS < 1.0)
- Link to `asa-roas-analysis` for keyword detail

## Output Template

```markdown
# Cross-Channel Performance — [App Name] — [Period]

## Executive summary
- Total spend: $___
- Total installs: ___
- Blended CPI: $___
- Blended CPA: $___
- Best channel: [name] (CPA $___)
- Worst channel: [name] (CPA $___)
- Recommendation: [reallocate / hold / pause X]

## Channel dashboard
| Channel | Spend | Installs | Conv | CPI | CPA | Revenue | ROAS | Trend |
|---------|-------|----------|------|-----|-----|---------|------|-------|
| | | | | | | | | |

## Channel details

### TikTok
- Connected: Yes/No
- Top campaign: [name] — CPA $___
- Issue: [if any]

### Meta
- Connected: Yes/No
- Top ad set: [name] — CPA $___
- Issue: [if any]

### Apple Search Ads
- Connected: Yes/No
- Top campaign: [name] — ROAS ___×
- Issue: [if any]

## Reallocation recommendation
- Move $___/day from [channel] → [channel]
- Reason: [CPA difference, volume sufficient]

## Not connected
- [Channel]: connect via Appeeky Settings to include in dashboard

## Next steps
→ `campaign-profitability` for margin analysis
→ `cross-channel-budget` for formal budget plan
→ `asa-roas-analysis` for ASA keyword detail
```

## Update app-ads-context.md

Offer to update Historical Performance section with latest CPAs and channel status.

## Cadence

| Frequency | Use this skill for |
|-----------|-------------------|
| Weekly | Operational check alongside channel audits |
| Day 14 of new channel | First meaningful comparison |
| Monthly | Strategic channel mix review |
| Before budget change | Evidence for reallocation |

## Cross-Skill Handoffs

| Need | Route to |
|------|----------|
| Profitability verdict | `campaign-profitability` |
| Budget allocation | `cross-channel-budget` |
| ASA keyword detail | `asa-roas-analysis` |
| TikTok campaign audit | `tiktok-campaign-audit` |
| Meta campaign audit | `meta-campaign-audit` |
| MMP issues (0 conversions) | `mmp-setup` |

## Related Skills

- `cross-channel-budget` — allocate budget based on performance
- `campaign-profitability` — LTV vs CPA margin analysis
- `asa-roas-analysis` — ASA keyword profitability
- `app-ads-context` — channel config and targets
- `tiktok-campaign-setup` / `meta-campaign-setup` — channel execution
