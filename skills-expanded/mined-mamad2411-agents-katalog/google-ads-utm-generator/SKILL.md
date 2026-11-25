---
name: google-ads-utm-generator
description: "When the user wants to build, audit, or standardize UTM parameters for Google Ads campaigns — generating UTM URLs, setting up naming conventions, using dynamic value insertion, choosing between auto-tagging and manual UTMs, or ensuring GA4 channel grouping works correctly. Triggers on 'UTM', 'UTM parameters', 'UTM generator', 'UTM builder', 'tracking URL', 'campaign tracking', 'auto-tagging', 'GCLID', 'UTM naming convention', 'GA4 source medium', 'utm_source utm_medium utm_campaign', 'build UTM links', or 'Google Ads tracking links'. For conversion action setup in Google Ads see google-ads-conversion-tracking."
metadata:
  version: 1.0.0
---

# Google Ads — UTM Parameter Generator & Tracking Setup

You are a Google Ads tracking specialist. Your goal is to build a UTM system that gives GA4 (and any other analytics tool) clean, consistent, parseable data — so every click can be attributed to the right campaign, ad group, keyword, and match type without ambiguity or manual effort.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Setup Context
- Are you building UTMs from scratch or auditing an inconsistent existing setup?
- What analytics tool is the destination: GA4, UA (legacy), third-party (Northbeam, Triple Whale, etc.)?
- Is Google Ads auto-tagging currently enabled? (If yes, basic attribution already works — UTMs add custom dimensions)
- How many campaigns need UTMs? (Informs whether dynamic insertion is essential)

### 2. Naming Standards
- Are there existing UTM conventions elsewhere in the business (Meta, email, LinkedIn)?
- Any requirements from the data/analytics team on dimension naming?
- Is the team using GA4 Channel Groups that need specific source/medium values?

---

## Auto-Tagging vs. Manual UTMs — Decide First

This is the most important decision before building any UTM.

### Auto-tagging (Google's default)
When auto-tagging is enabled, Google appends a `gclid` parameter to every ad click URL automatically. GA4 and Google Analytics use this to import campaign data directly from Google Ads.

**What auto-tagging gives you automatically:**
- Campaign name
- Ad group name
- Keyword
- Match type
- Network (Search, Display, etc.)
- Device
- Ad format

**When auto-tagging is sufficient:** Most Google Ads accounts that use GA4 and don't need custom dimensions.

### Manual UTMs
You manually append `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, and `utm_term` to every destination URL.

**When manual UTMs are needed:**
- Third-party analytics tools (Northbeam, Triple Whale, Hyros) that don't read gclid
- You need custom campaign labels beyond what auto-tagging provides (e.g., funnel stage, product line)
- You want consistent UTM data across all paid channels (Google + Meta + LinkedIn) in one analytics view
- Auto-tagging is breaking because of URL redirects or UTM stripping on the landing page

**Can you use both?** Yes. Auto-tagging + manual UTMs work simultaneously. Auto-tagging handles Google Ads native attribution; UTMs handle cross-channel analytics.

---

## The 5 UTM Parameters

| Parameter | What it tracks | Google Ads standard value |
|-----------|---------------|--------------------------|
| `utm_source` | The platform sending traffic | `google` |
| `utm_medium` | The type of channel | `cpc` |
| `utm_campaign` | The campaign name | Campaign name or ID |
| `utm_content` | The specific ad or creative | Ad name, ad group, or variation |
| `utm_term` | The keyword or audience | Keyword triggered |

---

## Dynamic Value Insertion — Use This, Always

Manually hardcoding keyword and campaign values is error-prone and doesn't scale. Google Ads supports dynamic UTM parameters — `{ValueTrack}` tags — that automatically insert the actual values at click time.

### Essential ValueTrack parameters for Google Ads

| Parameter | What it inserts | Example output |
|-----------|----------------|----------------|
| `{campaignid}` | Campaign ID (number) | `12345678` |
| `{campaign}` | Campaign name | `NB_Search_Core_US` |
| `{adgroupid}` | Ad group ID | `87654321` |
| `{adgroup}` | Ad group name | `Project_Management_Software` |
| `{keyword}` | The keyword that triggered the ad | `project+management+software` |
| `{matchtype}` | Match type of the triggered keyword | `e` (exact), `p` (phrase), `b` (broad) |
| `{network}` | Network the ad served on | `g` (Search), `d` (Display), `x` (Shopping) |
| `{device}` | Device type | `m` (mobile), `t` (tablet), `c` (computer) |
| `{creative}` | Ad ID | `111222333` |
| `{placement}` | Domain where display ad showed | `example.com` |
| `{loc_physical_ms}` | Physical location ID of the user | Location criteria ID |

---

## UTM Templates by Account Type

### Standard Search Campaign Template

```
utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content={adgroup}&utm_term={keyword}_{matchtype}
```

**Full URL example:**
```
https://yoursite.com/landing-page?utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content={adgroup}&utm_term={keyword}_{matchtype}
```

**What you see in GA4:**
- Source: `google`
- Medium: `cpc`
- Campaign: `NB_Search_Core_US` (actual campaign name)
- Ad content: `Project_Management_Software` (ad group name)
- Term: `project+management+software_e` (keyword + match type)

---

### Brand Campaign Template

```
utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content=brand&utm_term={keyword}
```

Adding `utm_content=brand` lets you filter brand vs. non-brand traffic easily in GA4 without relying on campaign naming.

---

### Shopping / PMax Template

Shopping and PMax don't support keyword-level UTMs (no keyword targeting). Use product-level identifiers instead:

```
utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content=shopping&utm_term={adgroup}
```

For PMax, use the campaign-level template — ad group granularity is limited.

---

### Display / Demand Gen Template

```
utm_source=google&utm_medium=display&utm_campaign={campaign}&utm_content={creative}&utm_term={placement}
```

Using `utm_medium=display` (not `cpc`) keeps Display traffic in its own channel grouping in GA4, separate from paid search.

---

### Retargeting Campaign Template

Add a funnel stage signal so you can separate retargeting performance from prospecting in analytics:

```
utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content=retargeting_{adgroup}&utm_term={keyword}_{matchtype}
```

---

## UTM Naming Convention

Consistent naming is what makes UTM data useful. Establish these rules before building:

### Rules
1. **Lowercase only** — `google` not `Google`. GA4 is case-sensitive; `Google` and `google` are two different sources.
2. **Hyphens not spaces** — `non-brand-search` not `non brand search`. Spaces become `%20` in URLs and break readability.
3. **Consistent separators** — pick one: hyphens (`-`) or underscores (`_`). Don't mix.
4. **No special characters** — avoid `&`, `=`, `#`, `?` in values (they break URL parsing)
5. **Mirror your campaign naming convention** — if campaigns are named `NB_Search_Core_US`, `utm_campaign` should match exactly

### Recommended campaign naming structure for UTM consistency

```
[Channel]_[Type]_[Theme]_[Geo]

Examples:
google_search_brand_us
google_search_nonbrand-core_us
google_search_competitor_us
google_display_prospecting_us
google_shopping_all-products_uk
google_pmax_retargeting_global
```

If you use `{campaign}` dynamic insertion, the UTM inherits whatever the campaign is named — so naming the campaign correctly is the same as naming the UTM correctly.

---

## UTM Builder — Step by Step

When building a UTM URL manually:

### Step 1 — Start with the destination URL
```
https://yoursite.com/free-trial
```

### Step 2 — Add the UTM string
```
https://yoursite.com/free-trial?utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content={adgroup}&utm_term={keyword}_{matchtype}
```

### Step 3 — Check for existing parameters
If the URL already has a `?` (e.g., `https://yoursite.com/page?ref=homepage`), use `&` instead of `?` to start UTMs:
```
https://yoursite.com/page?ref=homepage&utm_source=google&utm_medium=cpc&...
```

### Step 4 — Test with a preview
Replace `{keyword}` with an example keyword before saving. Does the URL render correctly? Does it land on the right page?

### Step 5 — Apply at the right level
In Google Ads, tracking templates can be set at:
- **Account level:** Applies to all campaigns automatically (most efficient — set this first)
- **Campaign level:** Overrides account level for specific campaigns
- **Ad group level:** Overrides campaign level
- **Keyword level:** Most granular; use for specific keyword tracking

**Best practice:** Set a tracking template at account level using dynamic insertion. Only override at campaign level when a specific campaign needs different UTM values (e.g., a brand campaign that needs `utm_content=brand`).

**In Google Ads:** Settings → Account settings → Tracking → Tracking template
```
{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_content={adgroup}&utm_term={keyword}_{matchtype}
```
`{lpurl}` is replaced by the ad's final URL at click time.

---

## UTM Audit: Fixing Inconsistent Tracking

For accounts with messy existing UTM setups:

### Common problems and fixes

| Problem | Symptom in GA4 | Fix |
|---------|---------------|-----|
| Mixed case values (`Google` vs `google`) | Duplicate source rows in reports | Standardize to lowercase in all UTMs |
| Missing `utm_medium` | Traffic classified as "Direct" or "Other" | Add medium to all UTMs |
| Wrong medium (`utm_medium=paid` instead of `cpc`) | Not appearing in "Paid Search" channel group | Use `cpc` for paid search |
| Hardcoded campaign names | Stale campaign names in reports after rename | Switch to `{campaign}` dynamic insertion |
| UTMs stripped by landing page redirects | All traffic shows as direct after redirect | Configure redirect to preserve UTM parameters |
| Auto-tagging disabled | No Google Ads data in GA4 | Enable auto-tagging in Google Ads settings |
| Spaces in UTM values | Broken URLs, `%20` in reports | Replace spaces with hyphens |

### GA4 Channel Grouping — Ensure UTMs Route Correctly

GA4's default channel grouping uses source/medium to categorize traffic. Your UTMs must align:

| GA4 Channel | Required source/medium |
|-------------|----------------------|
| Paid Search | source: `google`, medium: `cpc` |
| Display | source: `google`, medium: `display` |
| Paid Social | source: `facebook/instagram/linkedin`, medium: `paid-social` or `cpc` |
| Organic Search | source: `google`, medium: `organic` (auto from GA4) |
| Email | medium: `email` |
| Direct | No UTM (or `(direct)/(none)`) |

**If your GA4 shows Google Ads traffic in "Unassigned" or "Direct":** Usually caused by wrong medium value, UTMs being stripped, or auto-tagging disabled.

---

## UTM Checklist

### When setting up a new Google Ads account
- [ ] Auto-tagging enabled in account settings?
- [ ] Account-level tracking template set with dynamic UTMs?
- [ ] UTM naming convention documented and shared with team?
- [ ] GA4 channel groups verified — does paid traffic land in "Paid Search"?
- [ ] Test a click: do UTMs appear correctly in GA4 Real-time?

### When launching new campaigns
- [ ] Campaign name follows naming convention? (UTM inherits campaign name)
- [ ] Any campaign-level UTM override needed? (e.g., brand campaign)
- [ ] Final URL verified — no existing parameters that conflict?

### Quarterly UTM audit
- [ ] Pull source/medium report in GA4 — any unexpected values?
- [ ] Any "(not set)" or "(none)" in campaign dimension for paid traffic?
- [ ] Any sessions appearing as "Direct" that should be paid? (UTM stripping issue)
- [ ] All active campaigns using dynamic insertion — no hardcoded values?

---

## Common Mistakes

**Mixing lowercase and uppercase**
`utm_source=Google` and `utm_source=google` create two separate rows in GA4. Always lowercase.

**Using the wrong medium for non-search campaigns**
Display campaigns with `utm_medium=cpc` show up in GA4's Paid Search channel instead of Display — inflating paid search metrics. Use `utm_medium=display` for Display and Demand Gen.

**Hardcoding campaign names instead of using `{campaign}`**
When you rename a campaign in Google Ads, hardcoded UTMs still show the old name in GA4. Always use `{campaign}` for the campaign dimension.

**Not testing before launch**
Preview the URL with actual values substituted. A broken `?` or `&` means every click loses its tracking data permanently.

**Forgetting that UTMs don't work on phone calls**
UTMs track web sessions. For call tracking, you need Google Ads call extensions with call reporting enabled, or a call tracking platform like CallRail.

---

## Related Skills

- **google-ads-conversion-tracking**: How Google Ads native conversion tracking (gclid / auto-tagging) works alongside UTMs
- **google-ads-attribution**: How UTM data feeds into GA4 attribution models and differs from Google Ads native attribution
- **google-ads-anomaly-detection**: Sudden drops in UTM-tracked traffic can signal UTM stripping or tracking template errors
