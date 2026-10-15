---
name: google-ads-audiences
description: "When the user wants help with Google Ads audience targeting, remarketing lists, RLSA (Remarketing Lists for Search Ads), Customer Match, lookalike audiences, in-market audiences, custom intent audiences, affinity audiences, audience segmentation, or audience bid layering. Triggers on 'audience targeting', 'remarketing', 'RLSA', 'Customer Match', 'lookalike', 'in-market audience', 'custom intent', 'audience list', 'audience signal', or 'retargeting list'. For audience signals in PMax see google-ads-pmax."
metadata:
  version: 1.0.0
---

# Google Ads — Audience Targeting & Remarketing

You are a Google Ads audience specialist. Your goal is to build audience strategies that let you bid more on high-value users, re-engage prospects at the right funnel stage, and feed the algorithm with signals that improve automated bidding decisions.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Data Assets
- Is the Google tag (gtag.js) installed sitewide?
- Google Analytics 4 linked to Google Ads?
- Customer email/phone list available?
- CRM data exportable?

### 2. Website Traffic
- Monthly website visitors?
- Key pages by funnel stage (pricing, demo, checkout)?
- Average session duration and pages per session?

### 3. Campaign Goals
- Remarketing to convert known visitors, or prospecting new audiences?
- Which campaigns will audiences be applied to?
- Using Smart Bidding? (Audiences are critical signals for tCPA/tROAS)

---

## Audience Types Overview

| Audience Type | Source | Best For |
|---------------|--------|---------|
| Website Visitors (Remarketing) | Google tag on your site | Re-engaging visitors |
| App Users | Firebase / app tag | Mobile app remarketing |
| Customer Match | Email/phone upload | Re-engage known customers |
| YouTube Viewers | YouTube channel | Re-engage video watchers |
| In-Market | Google data | Finding purchase-intent prospects |
| Custom Intent | Keywords + URLs you define | High-intent prospecting |
| Affinity | Google data | Broad interest targeting |
| Life Events | Google data | Major life transition moments |
| Similar Segments | Google-generated | Lookalike prospecting |

---

## Website Remarketing (RLSA)

### Tag Setup Requirements
- Google tag (`gtag.js`) or Google Tag Manager on all pages
- Tag must fire on page load, not just on click events
- Verify via Tag Assistant or Ads Conversion page

### Audience Segments to Create

**Funnel-based segmentation:**

| Segment | Definition | Membership Duration | Use |
|---------|-----------|---------------------|-----|
| All visitors | All pages | 30 days | Top-funnel baseline |
| High-intent visitors | Pricing page OR demo page | 30 days | Warm prospecting bid-up |
| Cart abandoners | Added to cart, no purchase | 7 days | Highest priority retargeting |
| Checkout abandoners | Started checkout, no purchase | 7 days | Critical — near-converters |
| Past purchasers | Thank you / confirmation page | 180 days | Upsell, cross-sell, exclude |
| Trial users | Trial signup confirmation | 30 days | Convert to paid |
| Lead form submitters | Lead confirmation page | 90 days | Nurture → close |
| Blog readers | /blog/* URL rule | 60 days | Top-of-funnel content |

**Time-window segmentation:**
- Recent visitors (0-7 days): Highest intent → highest bid modifier
- Mid-window (8-30 days): Still warm → moderate modifier
- Cold window (31-90 days): Lower intent → baseline or slight reduction

### Audience Combination Logic
Create combined lists for precision:

```
"Pricing page visitors, NOT purchasers" =
  Included: Pricing page visitors (30 days)
  Excluded: Purchasers (180 days)

"High-value prospects" =
  Included: Demo request page visitors (30 days)
  Excluded: Existing customers (Customer Match)
```

### RLSA (Remarketing for Search Ads)
Layer remarketing audiences onto search campaigns in two modes:

| Mode | Behavior | Use When |
|------|----------|---------|
| Observation | Track performance by audience; bid adjustments applied | Always — no downside |
| Targeting | Only show ads to this audience | Bidding exclusively to known visitors |

**Standard RLSA setup:**
1. Add all remarketing lists to search campaigns in "Observation" mode
2. Set bid modifiers based on audience value
3. After 30 days, review performance by audience
4. Shift high-value audiences to "Targeting" mode if volume allows

**Bid modifier recommendations:**
| Audience | Bid Modifier |
|----------|-------------|
| Cart/checkout abandoners | +50-100% |
| Pricing/demo page visitors | +30-50% |
| All visitors (recent) | +15-25% |
| Past purchasers (upsell) | +20-40% |
| Past purchasers (exclude) | -100% (exclude) |

---

## Customer Match

### What It Is
Upload first-party data (emails, phone numbers, addresses) to match against Google's signed-in users.

### Data Requirements
- Minimum 1,000 matched users (list must reach this threshold to be usable)
- SHA-256 hashed or plaintext (Google hashes automatically)
- Format: CSV with header (Email, Phone, First Name, Last Name, Country, Zip)

### List Types to Create

| List | Source Data | Use Case |
|------|------------|---------|
| All customers | Full customer list | Exclude from acquisition campaigns |
| High-LTV customers | Top 20% by revenue | Bid-up signal for lookalikes |
| Churned customers | Customers who haven't purchased in X months | Win-back campaigns |
| Trial users (free) | Free trial signups | Convert to paid |
| Leads (not converted) | CRM contacts, not customers | Nurture via display/YouTube |
| Lost deals | CRM stage: closed-lost | Re-engagement after 90 days |

### Match Rates
Typical match rates:
- Email: 40-60%
- Phone: 30-50%
- Address: 20-40%
- Combined (email + phone + address): 60-70%

**Improving match rate:**
- Include multiple identifiers per record
- Ensure email domain variety (not just @gmail.com)
- Include physical address for better household matching

### Customer Match in Smart Bidding
Customer Match lists used as signals dramatically improve Smart Bidding accuracy:
- Add to all campaigns in "Observation" mode
- The algorithm learns what these users have in common and finds similar users

---

## Similar Segments (Lookalikes)

Google auto-generates similar segments based on your remarketing and Customer Match lists.

### Key Properties
- Generated automatically when source list has 1,000+ users
- Shows users with similar online behavior to your source list
- Not available on Search (only Display, YouTube, Discovery, Gmail)
- Availability depends on list size and Google's data

### Best Practices
- Seed with highest-quality list (high-LTV customers, converted leads — not all visitors)
- Use for prospecting campaigns only
- Pair with content or topic targeting for precision
- Monitor performance separately from other prospecting audiences

---

## Google-Provided Audiences

### In-Market Audiences
Users actively researching or comparing products in a category.

**How they work:**
- Google scores users based on recent search, YouTube, and browsing behavior
- Refreshed continuously — users leave the audience when behavior changes
- High-intent but not specific to your brand

**Best in-market segments for common industries:**
| Industry | Segments to Try |
|----------|----------------|
| B2B SaaS | Business & Industrial > Business Services > Business Software |
| E-commerce (apparel) | Apparel & Accessories > relevant subcategories |
| Finance | Financial Services > [relevant product type] |
| Real estate | Real Estate > Home Buyers |
| Auto | Autos & Vehicles > [vehicle type] |

**Use in:**
- Display prospecting (Targeting mode)
- Search campaigns (Observation + bid modifier)
- YouTube prospecting
- PMax audience signals

### Custom Intent Audiences
Build your own intent audience from:
- Keywords (people searching these terms on Google)
- URLs (people who visited these websites)
- Apps (people who use these apps)

**High-value custom intent strategies:**

**Competitor URL targeting:**
```
Add competitor websites as URL signals:
- competitor1.com
- competitor2.com
→ Reaches users actively browsing competitors
```

**Category keyword targeting:**
```
Add keywords reflecting purchase intent:
- "project management software pricing"
- "best project management tool"
- "trello vs asana"
→ Reaches users in active evaluation mode
```

**Combining keywords + URLs:**
```
Keywords: [intent signals]
URLs: [competitor + category sites]
= Highly qualified prospecting audience
```

### Affinity Audiences
Broad, long-term interest categories (not actively purchasing — just interested).

**Use cases:**
- Top-of-funnel brand awareness only
- YouTube reach campaigns
- Very low-CPM awareness display

**Do NOT use for:**
- Lead gen or direct response campaigns
- Any campaign with a CPA target

### Life Events
Users experiencing major life milestones.

| Life Event | Relevant Industries |
|------------|-------------------|
| Getting married | Financial services, travel, home goods |
| Having a baby | Insurance, retail, baby products |
| Buying a home | Mortgage, insurance, home improvement |
| Starting a business | B2B SaaS, financial services |
| Graduating | Education, first jobs, financial products |

---

## Audience Strategy by Campaign Type

### Search Campaigns (RLSA)
```
All keywords → Observation mode for all lists
High-intent audiences → +30-100% bid modifiers
Existing customers → Exclude (or separate upsell campaign)
```

### Display Remarketing
```
Segment by funnel stage and recency
Different creative per segment
Frequency caps per tier (hot: 5-7/day, cold: 1-2/day)
```

### Display Prospecting
```
Custom Intent (competitors + category keywords)
  + In-Market audience
  + Exclude existing customers (Customer Match)
```

### YouTube
```
Prospecting: Custom Intent + In-Market
Remarketing: Website visitors + Video viewers sequence
```

### PMax Audience Signals
```
Tier 1: Customer Match (high-LTV) + website converters
Tier 2: Custom Intent (competitor URLs + category keywords)
Tier 3: In-Market audiences
```

---

## Audience Management

### List Membership Duration
Set duration based on decision cycle length:

| Product Type | Decision Cycle | List Duration |
|-------------|---------------|---------------|
| Impulse purchase | Days | 7-14 days |
| Considered purchase (SaaS, consumer) | Weeks | 30-60 days |
| Complex B2B deal | Months | 90-180 days |
| High-value (enterprise, real estate) | Months-year | 180-540 days |

### Exclusions — Critical
Always exclude in acquisition campaigns:
- Existing customers (Customer Match + past purchaser URL list)
- Recent converters (7-14 day window)
- Irrelevant audiences (bounced visitors <10 sec, career page visitors)

### Audience Insights
In Google Ads: Audiences → Audience Manager → Insights
- See demographics, interests, in-market segments of your remarketing lists
- Use to refine prospecting targeting

---

## Audience Performance Analysis

### Observation Mode Report (Weekly)
In any campaign → Audiences tab → filter by "Observation"
- Compare conversion rate, CPA, ROAS by audience segment
- Audiences converting well → add bid modifier or shift to Targeting
- Audiences with high spend / 0 conversions → exclude or reduce modifier

### Audience Overlap
Check if audiences are too similar:
- Audience Manager → select audiences → check overlap
- Overlapping audiences in same campaign can cause inefficiency

---

## Optimization Checklist

### Setup (One-Time)
- [ ] Google tag firing on all pages
- [ ] All funnel-stage URL audiences created
- [ ] Customer Match lists uploaded (customers, high-LTV, trials)
- [ ] Audiences added in Observation mode to all campaigns
- [ ] Existing customers excluded from acquisition campaigns

### Weekly
- [ ] Audience performance in search campaigns — adjust bid modifiers
- [ ] Remarketing campaign performance by segment
- [ ] Customer Match list refresh (upload new customers)

### Monthly
- [ ] Similar segment availability — add new ones to prospecting
- [ ] Audience overlap check
- [ ] New funnel segments based on new pages/products
- [ ] Custom intent audience refresh (new competitor URLs, new keywords)

---

## Common Mistakes

### Setup
- Not excluding existing customers from acquisition campaigns
- Audience lists with too-short duration (misses consideration cycle)
- Customer Match list with low match rate (missing identifiers)

### Strategy
- Using affinity audiences for direct response (too broad)
- Not using RLSA on search campaigns (missed bid signal)
- Same bid modifier for all visitors regardless of funnel stage

### Smart Bidding
- Not adding audience signals to PMax (misses most important signal)
- Not adding Customer Match to campaigns (cheapest lookalike improvement)
- Over-excluding with Targeting mode (limiting algorithm's reach)

---

## Related Skills

- **google-ads-search**: RLSA implementation on search campaigns
- **google-ads-display**: Remarketing audiences for display campaigns
- **google-ads-video**: YouTube audience targeting and video remarketing lists
- **google-ads-pmax**: Audience signals for PMax learning
- **google-ads-bidding**: Audience bid modifiers and Smart Bidding signals
- **google-ads-conversion-tracking**: Required for building website visitor audiences
- **analytics-tracking**: GA4 audience import to Google Ads
