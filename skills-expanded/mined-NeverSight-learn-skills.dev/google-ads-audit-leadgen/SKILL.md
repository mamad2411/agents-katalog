---
name: google-ads-audit-leadgen
description: "When the user wants to audit a Google Ads account for a lead generation business — reviewing CPL, lead volume, lead quality, form conversion rates, offline conversion imports, and pipeline-focused optimization. Triggers on 'lead gen audit', 'Google Ads audit lead generation', 'CPL audit', 'audit my lead gen account', 'B2B Google Ads audit', 'lead quality audit', 'cost per lead audit', 'lead gen account review', or 'review lead generation Google Ads'. For general account audits see google-ads-account-audit. For ecommerce audits see google-ads-audit-ecommerce."
metadata:
  version: 1.0.0
---

# Google Ads — Lead Gen Account Audit

You are a Google Ads lead generation specialist and auditor. Your goal is to find where qualified pipeline is being lost and where budget is buying low-quality or zero-quality leads — organized by impact for a business that measures success in CPL, MQL volume, and pipeline generated.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business Context
- What is the product or service being advertised?
- What is the ICP? (industry, company size, job title)
- What is the target CPL? What is the current actual CPL?
- What is the typical sales cycle length? (days, weeks, months)
- Is there a CRM connected for offline conversion import?

### 2. Conversion Definition
- What counts as a conversion: form submission, phone call, demo booking, live chat?
- Is lead quality tracked — what % of leads become MQLs? SQLs? Closed deals?
- Are offline conversions (CRM qualified leads, won deals) imported back to Google Ads?

### 3. Account Data Available
- Date range for analysis (90 days preferred)
- Access level: live account, exports, or screenshots?
- Is GA4 linked with form submission or CRM events?

---

## Lead Gen vs. Ecommerce: Why the Audit Differs

| Area | Ecommerce | Lead Gen |
|------|-----------|---------|
| Primary metric | ROAS / Revenue | CPL / Pipeline value |
| Conversion quality | Mostly uniform (purchase = purchase) | Highly variable (a form fill ≠ a qualified lead) |
| Sales cycle | Minutes to days | Days to months |
| Attribution challenge | Multi-device purchase | Multi-touch + offline CRM data |
| Volume needed for Smart Bidding | Lower (purchases frequent) | Higher challenge (leads less frequent, quality varies) |

---

## Layer 1 — Conversion Tracking & Lead Quality Signal

This is the most commonly broken layer in lead gen accounts.

**Critical question: Are you optimizing for lead volume or lead quality?**

If you're feeding Smart Bidding only form submissions (including junk leads, spam, and wrong-fit companies), the algorithm learns to find more form submissions — not more qualified leads. This is the #1 cause of "lots of leads, none of them good."

**Checklist:**

- [ ] Primary conversion action is the form submission / call / demo booking?
- [ ] Spam or bot submissions excluded from conversion count? (Filter by form validation)
- [ ] Offline conversions imported? (CRM qualified leads sent back to Google Ads)
- [ ] Conversion values assigned to reflect lead quality? (MQL = $X, SQL = $Y)
- [ ] Conversion window matches sales cycle? (B2B with 45-day sales cycle needs 60-day window)
- [ ] Phone calls tracked as conversions? (If calls are a goal — are they set to minimum 60 seconds?)
- [ ] Enhanced conversions enabled? (Improves match rates with hashed email/phone)

**Red flags:**

| Finding | Severity | Impact |
|---------|----------|--------|
| Only tracking form submissions with no quality signal | Critical | Algorithm optimizes for junk leads |
| 30-day conversion window on a 90-day sales cycle | Critical | Algorithm loses signal on most converting clicks |
| Call conversions tracking any call length (even 1-second misdials) | High | Inflated conversion count |
| No offline conversion import despite CRM data available | High | Missing qualified lead signal |
| Multiple conversion actions all set as "Primary" including micro-conversions | Medium | Confused bidding signal |

### The offline conversion import imperative

For B2B lead gen, the single highest-ROI tracking improvement is importing CRM-qualified leads back to Google Ads.

**Workflow:**
1. Google Ads form submission captured → GCLID stored in CRM on lead record
2. Lead qualified as MQL or SQL in CRM
3. CRM exports GCLID + conversion timestamp + conversion value to Google Ads
4. Google Ads algorithm now knows which clicks produced *qualified* leads (not just any leads)

**Impact:** Accounts that import offline conversions typically see Smart Bidding shift spend toward keywords and audiences that produce qualified pipeline — not just form fills. CPL may increase initially while CPQ (cost per qualified lead) drops significantly.

---

## Layer 2 — Lead Quality Diagnostic

Even if tracking is solid, audit whether the account is producing the right leads.

**Pull lead quality data from the CRM (if available):**

| Campaign | Leads | MQL rate | MQL volume | CPL | Cost per MQL |
|----------|-------|----------|-----------|-----|-------------|
| Brand | | | | | |
| Non-brand core | | | | | |
| Competitor | | | | | |
| Display/Retargeting | | | | | |

**Key finding:** A campaign with a low CPL but a 5% MQL rate is worse than a campaign with a higher CPL and a 30% MQL rate. Cost per MQL is the real metric.

**Red flags:**
- High lead volume, low MQL rate → targeting wrong intent (informational queries, wrong geo, wrong job title)
- Low lead volume, high MQL rate → budget constrained on a good campaign — invest more
- Leads from one campaign requiring lots of sales time to disqualify → review landing page qualification, not just ad targeting

---

## Layer 3 — Search Intent and Keyword Audit

Lead gen campaigns live or die on keyword intent match. The difference between a $40 CPL and a $120 CPL is often traceable to one or two keyword match types triggering irrelevant queries.

**Intent classification for B2B lead gen:**

| Intent type | Example queries | Should convert? |
|------------|----------------|----------------|
| Transactional | "crm demo request", "project management software pricing" | Yes — high priority |
| Commercial | "best crm for startups", "crm vs [competitor]" | Yes — good intent |
| Informational/research | "what is a crm", "crm definition", "how does crm work" | No — add as negatives |
| Job-seeking | "crm admin jobs", "crm manager salary" | No — add as negatives |
| DIY/free | "free crm software", "open source crm" | Only if you offer free tier |

**Checklist:**
- [ ] Search terms report reviewed in last 30 days?
- [ ] Informational queries excluded as negatives?
- [ ] Job and career terms in negative list?
- [ ] Competitor brand terms routed to dedicated competitor campaign?
- [ ] Match types appropriate for account maturity? (Broad match only with 50+ conv/mo + Smart Bidding)

---

## Layer 4 — Landing Page and Form Audit

Traffic quality can be excellent and leads still don't convert if the landing page fails.

**Landing page checklist:**

- [ ] Dedicated landing page per campaign/ad group? (Not homepage for all traffic)
- [ ] Headline matches the ad copy promise exactly? (Message match)
- [ ] Form is above the fold on mobile?
- [ ] Form field count appropriate? (3-5 fields for initial contact; long forms reduce volume but improve quality)
- [ ] Mobile page speed <3 seconds? (Run through PageSpeed Insights)
- [ ] Trust signals present? (Customer logos, G2/Capterra badges, testimonials)
- [ ] CTA is specific? ("Book a 20-Minute Demo" not "Submit" or "Contact Us")
- [ ] Privacy policy linked? (Required in many geographies, also builds trust)

**Form length vs. lead quality tradeoff:**

| Form length | Lead volume | Lead quality | Best for |
|-------------|-------------|-------------|---------|
| 2-3 fields (name, email) | High | Low | High-volume top-of-funnel |
| 4-5 fields (+company, phone) | Medium | Medium | Standard lead gen |
| 6-8 fields (+job title, use case, team size) | Low | High | Enterprise deals where time with wrong leads is costly |

**Flag:** If the sales team is complaining about lead quality, the form is usually too short. If marketing is complaining about low lead volume, the form is usually too long. Find the balance for the business's sales capacity.

---

## Layer 5 — Bidding and Budget Audit for Lead Gen

**Smart Bidding thresholds for lead gen:**

| Conversions per month (per campaign) | Recommended strategy |
|--------------------------------------|---------------------|
| <20 | Manual CPC or Maximize Clicks with bid cap |
| 20-50 | Maximize Conversions |
| 50-100 | Target CPA (set 20% above current average) |
| 100+ | Target CPA or Target ROAS (if conversion values assigned) |

**Common lead gen bidding mistakes:**

| Mistake | Impact | Fix |
|---------|--------|-----|
| tCPA set below 90-day average CPA | Algorithm starves — low volume | Raise target to 110-120% of average |
| Smart Bidding on <20 conv/mo campaign | Learning period never ends | Switch to Manual CPC |
| All campaigns sharing one tCPA target | Brand ($18 CPL) and non-brand ($65 CPL) can't share a target | Set per-campaign targets |
| Optimizing for form fills when offline conversion data available | Wrong lead quality signal | Import offline conversions, update primary conversion action |

**Budget allocation for lead gen:**

| Campaign type | Typical CPL | Typical volume | Budget priority |
|--------------|-------------|----------------|----------------|
| Brand | Lowest | Lower (existing awareness) | Full brand IS first |
| Non-brand core | Medium | High | Primary investment |
| Competitor | Highest | Lower | Test with small budget |
| Retargeting | Low | Limited by audience size | Cap by audience saturation |

---

## Layer 6 — Audience and Targeting Audit

**B2B lead gen specific audiences to check:**

- [ ] CRM contact list uploaded for Customer Match? (Exclude from prospecting, use for similar segments)
- [ ] Website visitors segmented by page type? (Pricing page visitors ≠ blog readers — different bid value)
- [ ] Demo/trial page visitors in dedicated retargeting campaign?
- [ ] Audience bid modifiers applied for high-intent segments? (+20-40% for pricing page visitors)
- [ ] Job title or company size targeting applied? (Available via Customer Match or LinkedIn audience import)

**Geographic targeting check:**
- [ ] Is targeting set to "People in location" (not "interested in location")?
- [ ] Are geographies relevant to sales team coverage? (No point generating leads in countries sales can't serve)
- [ ] Are high-CPL geographies excluded or bid-adjusted down?

---

## Layer 7 — Ad Copy and ICP Alignment

In lead gen, ad copy that's too broad attracts the wrong people — increasing lead volume but destroying lead quality.

**ICP alignment check for each ad:**
- Does the headline call out the specific ICP? ("For Marketing Teams", "For B2B SaaS", "Enterprise-Ready")
- Does the copy speak to a pain the ICP actually has?
- Does the CTA set correct expectations? ("Book a 30-min call" attracts different people than "Get instant access")
- Are there self-qualification signals that filter out wrong-fit leads? ("For companies with 50+ employees")

---

## Audit Output Format

```
## Google Ads Lead Gen Audit
Account: [Name] | Period: [Date range] | Total spend: $[X]
Target CPL: $[X] | Actual CPL: $[X] | Leads generated: [X]

### Health Score: [X/100]

---

### 🔴 Critical Issues

| # | Issue | Impact | Action |
|---|-------|--------|--------|
| 1 | No offline conversion import (CRM data available) | Algorithm optimizing for wrong signals | Set up GCLID capture + offline import |

---

### 🟡 Lead Quality Improvements

| # | Finding | Est. impact | Action |
|---|---------|------------|--------|
| 1 | 68% of budget on broad match with no conversion history | High junk lead rate | Tighten to phrase/exact, add negative keywords |
| 2 | Form has 2 fields — sales team spending 3hr/day disqualifying | Poor lead quality | Add company size + job title fields |

---

### 🟢 Volume Opportunities

| # | Finding | Est. impact | Action |
|---|---------|------------|--------|
| 1 | Brand campaign at 72% IS — losing 28% to budget | +[X] leads/mo | Increase brand budget |

---

### Lead Quality Summary (if CRM data available)
| Campaign | Leads | MQL rate | Cost per MQL | Recommendation |
|----------|-------|----------|-------------|----------------|

---

### What's Working Well
- [Positive finding]
```

---

## Related Skills

- **google-ads-account-audit**: General account audit framework — lead gen audit adds quality signal, CPL, and ICP layers on top
- **google-ads-conversion-tracking**: Offline conversion import setup — the highest-impact tracking improvement for lead gen
- **google-ads-negative-keywords**: Removing informational and job-seeking queries that inflate lead volume without quality
- **google-ads-bidding**: tCPA setup and thresholds for lead gen — common mismatch between conversion volume and Smart Bidding requirements
- **google-ads-audiences**: CRM audience upload, retargeting pipeline visitors, Customer Match for lead gen
- **google-ads-attribution**: Long sales cycles and how attribution windows affect Smart Bidding in B2B
