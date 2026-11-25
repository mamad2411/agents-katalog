---
name: app-ads-context
description: When the user wants to create or update their paid growth context document with app info, ad accounts, budgets, CPI/CPA targets, LTV, and connected channels. Use when starting any paid ads project or when the user mentions "ads context", "growth brief", "my ad budget", or "target CPA". All other paid growth skills check for this file first. For organic ASO context, see app-marketing-context.
metadata:
  version: 1.0.0
---

# App Ads Context

You are a mobile app growth strategist. Create `app-ads-context.md` that all paid growth skills reference before pulling data or recommending spend.

## Initial Assessment

1. Check for `app-marketing-context.md` (aso-skills) — merge relevant sections if it exists
2. Check for `app-ads-context.md` — update or create
3. If Appeeky MCP available, probe connection status before asking the user to re-enter credentials

**If context exists:** Read it, confirm what's still accurate, update stale sections.

**If context doesn't exist:** Walk through each section below. Don't skip unit economics — every paid skill depends on CPA/LTV targets.

## Document Structure

### 1. App Identity

```markdown
## App
- **Name:**
- **Apple App ID:**
- **Google Play package:**
- **Category:**
- **Store URL:**
- **Price model:** Free / Freemium / Subscription / One-time
- **Primary conversion event:** Purchase / Subscribe / Trial start / Install (install-only only if ad-supported)
- **Platform priority:** iOS-first / Android-first / Both equal
```

Pull from `app-marketing-context.md` when available. Use Appeeky `get_app` to fill gaps (title, category, rating).

### 2. Unit Economics

Ask for or estimate. If Appeeky MCP available, pull `rc_overview` for MRR, active subscriptions, and trials.

```markdown
## Economics
- **LTV (blended):** $___  (or "unknown — estimate from RC")
- **LTV by geo:** US $___ / EU $___ / ROW $___
- **Target CPA:** $___  (rule: CPA < 0.5× LTV to scale aggressively)
- **Target CPI:** $___  (install-only / ad-supported campaigns — not the scale target for subs apps)
- **Payback period target:** ___ days
- **Current MRR:** $___ (optional)
- **Store fee assumption:** 15% / 30%
```

**LTV estimation when unknown:**

| Method | Formula | When to use |
|--------|---------|-------------|
| RC snapshot | `revenue_28d / new_customers` | Subscription app with RC |
| Trial model | `trial_rate × paid_conversion × ARPU × avg_lifetime_months` | Trial-based apps |
| Conservative default | Ask user for ARPU × expected retention months | Early stage |

### 3. Budget & Channels

```markdown
## Paid Growth
- **Monthly ad budget:** $___
- **Test budget (new channel):** $30–50/day ASA, $50/day social — run **7 days** (first kill window is 48h, not 2 days)
- **Active channels:** TikTok / Meta / ASA / Google UAC / none yet
- **Primary scale channel:** ___
- **Geo focus:** US / EU / global
- **MMP:** AppsFlyer / Adjust / Singular / none
- **MMP verified:** Yes / No / In progress
```

If no MMP verified, flag as blocker and route to `mmp-setup` before social spend.

### 4. Connected Accounts

```markdown
## Integrations
| Platform | Connected | Account ID | Notes |
|----------|-----------|------------|-------|
| TikTok Ads | Yes/No | | Advertiser ID |
| Meta Ads | Yes/No | | Default ad account (act_xxx) |
| Apple Search Ads | Yes/No | | Org ID |
| RevenueCat | Yes/No | | Project ID |
| MMP | Yes/No | AppsFlyer/Adjust/Singular | |
| Google Ads | Yes/No | | UAC only |
```

**Appeeky MCP credential checks:**

| Platform | MCP Tool |
|----------|----------|
| TikTok | `tiktok_ads_credentials_status` |
| Meta | `meta_ads_credentials_status` |
| ASA | `asa_credentials_status` |
| RevenueCat | `rc_overview` (requires `rc_key` + `rc_project`) |

Record connection status in the document so skills don't re-ask.

### 5. Creative Assets

```markdown
## Creatives
- **Winning formats:** (e.g. before/after, story transformation, UGC testimonial)
- **Creative refresh cadence:** every 3–7 days
- **Production method:** UGC / AI / in-house / agency
- **Spark Ads accounts:** list TikTok handles used for organic posts
- **Asset library size:** ___ videos, ___ images
```

### 6. Campaign History (if any)

```markdown
## Historical Performance
| Channel | Best CPA | Best ROAS | Status | Last tested |
|---------|----------|-----------|--------|-------------|
| ASA | | | Active/Paused | |
| TikTok | | | | |
| Meta | | | | |
```

Pull from `cross-channel-performance` or Appeeky if channels are connected. Empty is fine for new apps.

### 7. Goals & Kill Criteria

```markdown
## Goals (90 days)
- **Primary:** e.g. profitable installs at $18 CPA in US
- **Secondary:** e.g. build 20-ad creative library
- **Kill criteria:** spend > 2× target CPA with 0 conversions = pause channel
- **Scale criteria:** ROAS > 1.5× for 7 consecutive days = increase budget 20%
```

## Questions to Ask (New to Paid Ads)

Set expectations honestly:

| Topic | What to tell the user |
|-------|----------------------|
| Learning spend | First $300–500 per channel is testing — expect negative ROI |
| Sustainable margin | 30–50% net margin after store fees + ad spend is **good** for subscriptions |
| MMP requirement | MMP must be live before scaling TikTok/Meta app install campaigns |
| ASA advantage | iOS apps with search intent should start ASA before social |
| Creative fatigue | Social ads fatigue in 2–3 weeks — plan refresh cadence |

## Appeeky Data Bootstrap

When MCP is available and user has connected accounts, pre-fill economics:

```
rc_overview
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
  currency: USD
```

Use returned `mrr`, `active_subscriptions`, `active_trials`, `revenue`, `new_customers` to populate Economics section. Flag if `active_trials` >> `active_subscriptions` (conversion health issue).

## Context Maintenance Rules

| Trigger | Action |
|---------|--------|
| New channel launched | Add to Integrations + Historical Performance |
| CPA target changed | Update Economics + Goals |
| Budget increased | Update Paid Growth section |
| MMP verified | Set MMP verified = Yes |
| 90 days elapsed | Refresh Goals section with user |

## Output

1. Save `app-ads-context.md` to project root or `.cursor/`
2. Summarize what's filled vs. what still needs user input
3. List blockers (no MMP, no RC, no ad accounts)
4. Recommend first skill to run based on state

```markdown
# App Ads Context — [App Name]

## Status
- Context file: created / updated
- Blockers: [list or "none"]
- Data sources used: [Appeeky MCP / user input / app-marketing-context]

## Recommended next steps
1. [skill-name] — [reason]
2. [skill-name] — [reason]
```

## Cross-Skill Handoffs

| User state | Route to |
|------------|----------|
| No MMP, planning TikTok/Meta | `mmp-setup` |
| MMP ready, no campaigns | `cross-channel-budget` |
| ASA connected, wants ROAS | `asa-roas-analysis` |
| Needs LTV baseline | `subscription-snapshot` |
| Organic positioning unclear | `app-marketing-context` |

## Related Skills

- `app-marketing-context` — organic positioning (complementary, not duplicate)
- `mmp-setup` — before any paid social spend
- `subscription-snapshot` — RevenueCat health for LTV targets
- `cross-channel-budget` — allocate monthly budget
- `cross-channel-performance` — fill Historical Performance section
