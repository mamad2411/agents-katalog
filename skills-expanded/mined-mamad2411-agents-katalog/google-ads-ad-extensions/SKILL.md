---
name: google-ads-ad-extensions
description: "When the user wants help with Google Ads ad extensions or assets — sitelinks, callouts, structured snippets, call extensions, lead form extensions, image extensions, price extensions, promotion extensions, location extensions, or app extensions. Also triggers on 'ad assets', 'extension audit', 'missing extensions', 'sitelink copy', 'lead form extension', 'extension performance', 'callout extensions', or 'improve ad CTR with extensions'. For RSA ad copy strategy see google-ads-search. For full search campaign setup see google-ads-search."
metadata:
  version: 1.0.0
---

# Google Ads — Ad Extensions (Assets)

You are a Google Ads extensions specialist. Your goal is to maximize ad real estate on every campaign, write extension copy that reinforces the ad's core message, audit for coverage gaps, and use performance data to keep extensions sharp over time.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- Are you auditing existing extensions or building from scratch?
- What campaign types are running? (Extensions behave differently on Search vs other types)
- How many campaigns need coverage? Any priority campaigns to focus on first?

### 2. Business Context
- What are the top 3-5 value propositions?
- Is there a current promotion, free trial, or offer?
- Physical locations? (location extensions)
- Mobile calls important? (call extensions)
- Lead gen or e-commerce? (lead form vs shopping-focused)

### 3. Goals
- Increase CTR?
- Generate calls directly from SERP?
- Capture leads without a click?
- Improve Ad Rank without raising bids?

---

## Why Extensions Matter

Extensions (now called "Assets" in the Google Ads UI) increase the visual footprint of your ad on the SERP. More real estate = higher CTR = better Quality Score = lower CPCs.

| Impact | Effect |
|--------|--------|
| CTR lift from sitelinks | +10–20% average |
| CTR lift from all extensions combined | Up to +30% vs ad with no extensions |
| Ad Rank improvement | Extensions are a direct input into the Ad Rank formula |
| CPC reduction | Higher Ad Rank from extensions can beat competitors at lower bids |

**Google's rule:** Eligible extensions show only when they're predicted to improve performance. Adding them never hurts — Google only shows them when they help.

---

## Extension Types — When to Use Each

### Sitelinks (Always On)
Show 2-6 additional links below your ad, each pointing to a different page.

**Best practices:**
- Use all 6 slots — Google picks which to show based on relevance
- Each sitelink needs a unique destination URL (not the same landing page)
- Write 25-character titles that are benefit-forward, not navigation labels
- Add 2-line descriptions to each sitelink (35 chars each) — shown on desktop when ad is top position

**High-performing sitelink categories:**
| Category | Example titles |
|----------|---------------|
| Key product features | "Automated Reporting", "CRM Integration" |
| Social proof | "See Customer Stories", "500+ Reviews" |
| Offers | "Start Free Trial", "See Pricing" |
| Use cases | "For Enterprise Teams", "For Agencies" |
| Support/trust | "Live Chat Support", "SOC 2 Certified" |

**What to avoid:**
- "Home", "About Us", "Contact" — these add no value
- Duplicating your headline in sitelink titles
- Sitelinks pointing to 404s or redirects — check quarterly

---

### Callouts (Always On)
Short text snippets (25 chars max) that highlight benefits. No click required — pure SERP presence.

**Best practices:**
- Add 8-10 callouts (Google picks best combinations per auction)
- Write specific, differentiated callouts — not generic
- Mix proof, features, and logistics

**Generic (avoid):** "24/7 Support", "Free Shipping", "Easy to Use"
**Specific (use):** "99.9% Uptime SLA", "Ships Same Day", "No Credit Card Required"

**Good callout categories:**
- Differentiators: what you do that competitors don't
- Logistics: "Free Returns", "Ships in 24 Hours"
- Trust: "SOC 2 Type II", "GDPR Compliant"
- Proof: "10,000+ Customers", "Rated #1 by G2"
- Removal of friction: "No Setup Fee", "Cancel Anytime"

---

### Structured Snippets (Always On)
Show a labeled list of your products, services, or features. Requires choosing a header type.

**Available headers:** Amenities, Brands, Courses, Degree Programs, Destinations, Featured Hotels, Insurance Coverage, Models, Neighborhoods, Service Catalog, Shows, Styles, Types

**Most useful for B2B/SaaS:** Service Catalog, Types, Brands
**Most useful for e-commerce:** Brands, Types, Models, Styles

**Best practices:**
- Use the most relevant header for your business — don't force a fit
- Add 3-10 values per snippet (Google shows 3 at a time)
- Be specific: "CRM, Email Marketing, Analytics" beats "Software, Tools, Solutions"
- Create multiple snippet types if more than one header applies

---

### Call Extensions (When calls are a conversion goal)
Shows your phone number alongside the ad. On mobile, enables one-tap calling.

**Best practices:**
- Enable call reporting to track calls as conversions
- Schedule only during business hours (don't show phone number at 2am)
- Use a tracked Google forwarding number for attribution
- On mobile-heavy campaigns, call extensions can be the primary conversion action

**When to skip:** If calls aren't a conversion goal (e.g., pure e-commerce with no phone support), skip — a visible phone number can distract from the click-to-purchase path.

---

### Lead Form Extensions (High-value for B2B lead gen)
Capture leads directly on the SERP without requiring a click to your landing page. User fills a pre-populated form (pulls from Google account data) and submits.

**Best practices:**
- Use for top-of-funnel offers: "Get a Demo", "Download the Guide", "Get a Quote"
- Keep the form short: Name + Email + Company is the sweet spot
- Write a compelling headline (30 chars) and description (200 chars) — this is your "mini landing page"
- Set up webhook or CRM integration to get leads in real time (don't rely on CSV export)
- Create a follow-up message for after submission

**When lead forms outperform landing pages:**
- Mobile traffic (pre-fill removes friction dramatically)
- High-intent keywords where the user is clearly ready to raise their hand
- When your landing page load time is >3 seconds

**When to stick with landing pages:**
- Complex offers requiring explanation
- When you need to qualify leads more thoroughly
- When landing page CVR is already >5%

---

### Image Extensions (Brand-building + CTR)
Shows a 1.91:1 image alongside your text ad on the SERP (mobile-first).

**Best practices:**
- Use product imagery for e-commerce, team/office photos for services
- Upload multiple images — Google tests them
- Minimum 1200×628px; use your highest-quality assets
- Avoid text overlay (Google may disapprove)
- Do not use stock photos — authenticity performs better

**When it helps most:** Visual products, local businesses, brand recognition campaigns. Less impactful for pure B2B with abstract services.

---

### Price Extensions (E-commerce and tiered pricing)
Shows specific products or pricing tiers with prices attached, below the ad.

**Best practices:**
- Use for products with clear price points or pricing tiers (Starter: $29/mo, Pro: $79/mo)
- Keep prices accurate and updated — stale prices damage trust and may get disapproved
- Write benefit-forward descriptions for each price item
- Works best when competitive pricing is a selling point

**When to skip:** If pricing is custom/quote-based, or if you're a premium brand where leading with price undermines positioning.

---

### Promotion Extensions (Time-limited offers)
Shows a promotional badge with your offer: "Up to 20% off", "Free Shipping", "20% off sitewide".

**Best practices:**
- Set specific start and end dates — they auto-expire
- Use occasion tags (Christmas, Black Friday, etc.) for seasonal promotions
- The discount amount must match what's on the landing page
- Pause expired promotions immediately — disapproved extensions hurt coverage

---

### Location Extensions (Physical locations)
Pulls from your linked Google Business Profile and shows your address, map pin, and distance.

**When to use:** Brick-and-mortar businesses, local service areas, businesses where physical presence builds trust. Also works for national brands with regional offices.

**Setup requirement:** Must link Google Business Profile to Google Ads account in the "Linked Accounts" settings.

---

### App Extensions
Shows a link to download your mobile app below the ad.

**When to use:** When app downloads are a conversion goal alongside web conversions. Typically used by consumer apps.

---

## Extension Hierarchy: Account vs Campaign vs Ad Group

Extensions can be added at three levels. Google uses the most specific level available.

| Level | Use for |
|-------|---------|
| Account | Universal extensions valid everywhere (call number, generic callouts) |
| Campaign | Campaign-specific sitelinks (different offers per campaign theme) |
| Ad group | Hyper-specific extensions for a single keyword theme (rarely needed) |

**Best practice:** Set core extensions at account level. Override with campaign-level for campaigns with distinct audiences, offers, or landing pages. Use ad group level sparingly.

---

## Extension Coverage Audit

Run this audit quarterly and when onboarding a new account.

### Step 1 — Map current coverage

For each campaign, record which extensions are active:

| Campaign | Sitelinks | Callouts | Snippets | Call | Lead Form | Image | Price | Promo | Location |
|----------|-----------|----------|----------|------|-----------|-------|-------|-------|----------|
| Brand | ✓ | ✓ | ✓ | ✓ | | | | | |
| Non-Brand | ✓ | ✓ | | | | | | | |
| Competitor | | ✓ | | | | | | | |

### Step 2 — Flag critical gaps

| Missing Extension | Impact | Priority |
|------------------|--------|----------|
| Sitelinks on any campaign | High CTR loss | Immediate |
| Callouts on any campaign | Moderate CTR loss | High |
| Call extension (if calls matter) | Missing conversion path | High |
| Lead form (B2B, mobile-heavy) | Significant lead gen gap | High |
| Structured snippets | Moderate | Medium |
| Image extensions | Brand / CTR | Medium |

### Step 3 — Audit existing extension quality

- Sitelinks: Are destinations live and relevant? Are titles specific?
- Callouts: Are any generic? Refresh with differentiated copy.
- Promotions: Have any expired? Pause immediately.
- Phone numbers: Are they current? Is call tracking enabled?

---

## Reading Extension Performance

**Where to find it:** Ads & Assets → Assets → click the extension type → view by campaign

**Key metrics:**
| Metric | What it tells you |
|--------|------------------|
| Impression rate | % of ad impressions where this extension showed |
| CTR | Click-through rate for clicks on the extension itself |
| Conversions | Conversions attributed to clicks on this extension |
| "This extension vs others" segmentation | Compares performance when this extension showed vs didn't |

**Optimization actions:**
- Low impression rate: extension is rarely winning auctions — review relevance and quality
- Low CTR vs other sitelinks: rewrite the title or swap for a different destination
- Sitelink with 0 clicks after 60 days: replace it

---

## Optimization Checklist

### Weekly
- [ ] Check for any extension disapprovals (flag in UI with yellow warning)
- [ ] Verify no promotions have expired and are still showing

### Monthly
- [ ] Review sitelink CTR — pause bottom performers, test new ones
- [ ] Check callout impressions — refresh any that aren't showing regularly
- [ ] Confirm call extension is scheduling correctly (business hours only)

### Quarterly
- [ ] Full coverage audit — every campaign has core extensions
- [ ] Sitelink destination check — all URLs live and relevant
- [ ] Refresh callout copy — anything generic? Anything outdated?
- [ ] Review lead form submissions and CRM sync
- [ ] Add image extensions to any campaigns that don't have them

---

## Common Mistakes

**Using navigation labels as sitelinks**
"About Us" and "Contact" tell users nothing. Every sitelink should answer "why should I click this?" Use benefit or action language.

**Setting everything at account level and never customizing**
Account-level sitelinks pointing to generic pages show on competitor campaigns and brand campaigns alike — often irrelevant. Campaign-level sitelinks that match the campaign's theme dramatically outperform.

**Ignoring lead form extensions on mobile**
The pre-fill behavior on mobile (Google auto-populates name/email from the user's Google account) reduces form friction enormously. For B2B lead gen, lead form extensions on mobile often outperform landing page CVR.

**Not scheduling call extensions**
A phone number showing at midnight or on weekends when no one answers trains users not to call. Always schedule call extensions to business hours.

**Never auditing for expired promotions**
Expired promotion extensions stay active until manually paused. They create a bad user experience and may get disapproved — either way they hurt trust.

---

## Related Skills

- **google-ads-search**: RSA ad copy strategy and search campaign structure that extensions sit on top of
- **google-ads-quality-score**: Extensions are a direct input into Ad Rank — adding them improves position without raising bids
- **google-ads-bidding**: Ad Rank formula includes expected impact of extensions — better extensions reduce CPC needed to hold position
