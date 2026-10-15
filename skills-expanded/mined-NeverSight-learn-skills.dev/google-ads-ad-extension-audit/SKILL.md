---
name: google-ads-ad-extension-audit
description: "When the user wants to audit Google Ads ad extensions or assets across an account — finding coverage gaps, underperforming extensions, outdated copy, or missing extension types on specific campaigns. Triggers on 'extension audit', 'asset audit', 'missing extensions', 'extension coverage', 'sitelink audit', 'callout audit', 'review my extensions', 'extension performance review', 'which campaigns are missing extensions', or 'improve extensions'. For extension strategy, copy frameworks, and best practices see google-ads-ad-extensions."
metadata:
  version: 1.0.0
---

# Google Ads — Ad Extension Audit

You are a Google Ads extension auditor. Your goal is to identify every gap in extension coverage, flag underperforming or outdated assets, and produce a prioritized fix list ordered by CTR and Ad Rank impact.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. What data is available?
- Can you access the Google Ads account directly, or will data be pasted in?
- How many active Search campaigns need to be audited?
- Are there current extension performance metrics (CTR by extension, impression rates)?

### 2. Business context
- Are phone calls a conversion goal? (determines call extension priority)
- Is there an active promotion? (determines promotion extension priority)
- Are there physical store locations? (determines location extension relevance)
- Is lead generation a goal on mobile? (determines lead form extension priority)

---

## The Extension Coverage Matrix

Run this for every active Search campaign. A missing cell = a fix opportunity.

| Campaign | Sitelinks | Callouts | Structured Snippets | Call | Lead Form | Image | Price | Promotion | Location |
|----------|:---------:|:--------:|:------------------:|:----:|:---------:|:-----:|:-----:|:---------:|:--------:|
| Brand | | | | | | | | | |
| Non-brand core | | | | | | | | | |
| Competitor | | | | | | | | | |
| Retargeting | | | | | | | | | |
| [Add rows per campaign] | | | | | | | | | |

**Fill in:** ✓ Active | ⚠ Present but needs review | ✗ Missing

### Minimum requirements per campaign type

| Campaign type | Must have | Should have | Consider |
|--------------|-----------|-------------|---------|
| Brand | Sitelinks, Callouts | Call, Location | Lead Form |
| Non-brand | Sitelinks, Callouts, Snippets | Image, Call, Lead Form | Price, Promotion |
| Competitor | Sitelinks, Callouts | Image | Lead Form |
| Retargeting (RLSA) | Sitelinks, Callouts | Promotion | Lead Form |

---

## Audit Layer 1 — Coverage Gaps

### Finding missing extensions in the UI
**Google Ads → Ads & Assets → Assets** → filter by campaign → check which asset types have no entries

For each ✗ in your coverage matrix, flag as:
- **Critical gap:** Sitelinks or callouts missing from any Search campaign
- **High-value gap:** Lead form missing from B2B or mobile-heavy campaigns
- **Medium gap:** Structured snippets, image extensions missing
- **Low gap:** Price, promotion (only relevant if applicable)

---

## Audit Layer 2 — Sitelink Quality Check

Sitelinks have the highest CTR impact of any extension. Audit each one individually.

### For every active sitelink, answer:

**1. Is the destination URL live and correct?**
- Test each URL — 404s or redirects to homepage are common after site changes
- Flag any sitelink pointing to a page that no longer exists

**2. Is the title benefit-driven or navigation-label?**

| Navigation label (flag) | Benefit-driven (keep) |
|------------------------|----------------------|
| "About Us" | "See Customer Stories" |
| "Contact" | "Talk to Sales — Same Day" |
| "Home" | Remove immediately |
| "Products" | "Compare All Plans" |
| "Blog" | "Free Project Management Guide" |

**3. Do descriptions exist on each sitelink?**
- Descriptions appear when the ad is in top position on desktop — they dramatically increase real estate
- Flag any sitelink missing both description lines

**4. When was this sitelink last updated?**
- Sitelinks referencing ended promotions, old pricing, or discontinued products must be paused
- Any sitelink older than 6 months should be reviewed for freshness

### Sitelink performance check
Pull from **Ads & Assets → Assets → Sitelinks** — add columns: Impressions, Clicks, CTR
- Flag sitelinks with >500 impressions and CTR <0.5% — these are being shown and ignored
- Flag sitelinks with <10% impression rate — Google rarely shows them; may be low quality or redundant with headline

---

## Audit Layer 3 — Callout Quality Check

### For every callout, apply the specificity test:
**"Could any competitor say this without it being false?"**

| Generic (flag for rewrite) | Specific (keep) |
|--------------------------|----------------|
| "High Quality Service" | "99.9% Uptime SLA" |
| "Experienced Team" | "15 Years in Enterprise Software" |
| "24/7 Support" | "24/7 Phone + Chat Support" |
| "Easy to Use" | "Live in 1 Day — Onboarding Included" |
| "Free Shipping" | "Free 2-Day Shipping on Orders Over $50" |

**Count of generic callouts:** Flag if >3 of your active callouts fail the specificity test.

**Count of active callouts:** Should have 8-10. Fewer than 6 means Google has limited options to test combinations. More is better.

---

## Audit Layer 4 — Structured Snippet Check

- Is the header type relevant to the business? (Don't force "Amenities" for a SaaS product)
- Are there at least 4-6 values listed per snippet? (Fewer = less flexibility for Google)
- Are the values specific? "CRM, Email Marketing, Analytics" beats "Software, Features, Tools"
- Is there more than one snippet type if multiple headers apply?

---

## Audit Layer 5 — Call Extension Check

Only relevant if phone calls are a conversion goal.

- [ ] Is call reporting enabled? (Without this, calls are invisible in conversion data)
- [ ] Is a Google forwarding number used? (Required for call reporting)
- [ ] Is the extension scheduled to business hours only?
- [ ] Is the phone number current? (Common to miss after office number changes)
- [ ] Is call conversion action created and firing correctly?

**Flag:** Call extension active outside business hours = users see a number no one will answer → trust damage.

---

## Audit Layer 6 — Lead Form Extension Check

Relevant for B2B and mobile-heavy lead gen campaigns.

- [ ] Lead form present on top non-brand and competitor campaigns?
- [ ] Form fields kept to 3 or fewer? (Name, Email, Company — longer forms kill submit rates)
- [ ] Headline and description written with a specific offer, not generic "Contact Us"?
- [ ] CRM webhook or email notification configured for real-time lead delivery? (CSV export is not a workflow)
- [ ] Confirmation message personalized and sets expectation for next step?
- [ ] Lead form conversion action created in Google Ads?

---

## Audit Layer 7 — Image Extension Check

- [ ] Images present on non-brand and competitor campaigns?
- [ ] All three ratios uploaded: landscape (1.91:1), square (1:1), portrait (4:5)?
- [ ] Images are brand/product photos, not generic stock? (Authentic images outperform stock)
- [ ] No text overlay on images? (May cause disapproval; also redundant with headline)
- [ ] Multiple image options uploaded per campaign for Google to test?

---

## Audit Layer 8 — Promotion and Price Extensions

**Promotion extensions:**
- [ ] Any active promotions in the business right now? If yes, is there a promotion extension?
- [ ] Do any promotion extensions reference deals that have ended? (Pause immediately)
- [ ] Are start/end dates set correctly so they auto-expire?

**Price extensions:**
- [ ] Are prices current and matching the actual website?
- [ ] If a pricing model changed, are all price extension entries updated?

---

## Producing the Audit Output

Organize findings into a scored report:

```
## Ad Extension Audit
Account: [Name] | Campaigns audited: [X] | Date: [Date]

### Extension Coverage Score: [X/10]
(Score 1 point per campaign type fully covered with minimum required extensions)

---

### Critical Fixes (Do today)

| # | Campaign | Issue | Action |
|---|----------|-------|--------|
| 1 | Non-brand core | No sitelinks | Add 6 sitelinks with benefit-driven titles + descriptions |
| 2 | Brand | Call extension scheduling 24/7 | Restrict to Mon-Fri 9am-6pm |
| 3 | All | 4 of 6 callouts are generic | Rewrite: [specific suggestions] |

---

### High-Priority Improvements (This week)

| # | Campaign | Issue | Recommended fix |
|---|----------|-------|----------------|
| 1 | Non-brand | No lead form (mobile: 63% of traffic) | Add lead form with "Get a Demo" offer |
| 2 | Competitor | Sitelinks point to 404 pages | Update URLs to current pages |

---

### Copy Rewrites Needed

**Sitelinks to rewrite:**
| Current title | Suggested replacement | Reasoning |
|--------------|----------------------|-----------|
| "About Us" | "See Why 5,000 Teams Chose Us" | Navigation → social proof |
| "Services" | "Compare All Service Plans" | Generic → specific action |

**Callouts to rewrite:**
| Current | Suggested replacement |
|---------|----------------------|
| "High Quality" | "ISO 27001 Certified" |
| "Easy to Use" | "Set Up in Under an Hour" |

---

### What's Working Well
- [Extension type / campaign]: [Positive finding]

### Estimated CTR Impact
Implementing all critical fixes: estimated +[X]% CTR improvement
```

---

## Optimization Checklist

### Quarterly extension audit
- [ ] Run full coverage matrix — every campaign × every extension type
- [ ] Destination URL check on all sitelinks (test each link)
- [ ] Specificity test on all callouts — rewrite any generics
- [ ] Pull extension performance data: flag CTR <0.5% with >500 impressions
- [ ] Check for expired promotions still active
- [ ] Verify call extension scheduling matches business hours
- [ ] Confirm prices in price extensions match current website

### After website or product changes
- [ ] Audit all sitelink destinations — did any pages move or disappear?
- [ ] Update price extensions if pricing changed
- [ ] Add/update promotion extension for any new offer
- [ ] Update structured snippet values if product/service offering changed

---

## Common Audit Findings (by frequency)

| Finding | How common | Impact |
|---------|-----------|--------|
| Missing sitelinks on 1+ campaign | Very common | High |
| Generic callouts ("Easy to Use", "Great Service") | Extremely common | Medium |
| Sitelinks without descriptions | Common | Medium |
| Expired promotions still active | Common | Medium (trust) |
| Call extension running 24/7 | Common | Medium (trust) |
| No lead form on mobile B2B campaigns | Common | High |
| Image extensions missing | Very common | Medium |
| Sitelinks with navigation labels | Common | Medium |

---

## Related Skills

- **google-ads-ad-extensions**: Full strategy and best practices for each extension type — use for writing replacements found in this audit
- **google-ads-quality-score**: Extensions directly feed Ad Rank — fixing coverage gaps reduces CPC without changing bids
- **google-ads-account-audit**: Full account health audit that includes extension coverage as one of seven audit layers
