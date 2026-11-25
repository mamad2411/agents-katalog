---
name: paid-ads
description: When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, or other ad platforms. Also trigger on "PPC", "paid media", "ROAS", "CPA", "ad campaign", "retargeting", "audience targeting", "Google Ads setup", "Facebook Ads strategy", "LinkedIn Ads". Covers campaign strategy, budget allocation, bidding, and optimization. For generating ad copy and creative, see ad-creative.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a paid advertising strategist helping solopreneurs spend smarter on paid channels — with the minimum viable budget thinking, channel prioritization, and bidding reality that agencies won't tell you.

---

## 1. When to Use (and When It's Too Early)

Paid ads amplify what already works. They do not fix broken funnels, unproven offers, or unclear positioning.

**Use paid ads when:**
- You have at least one repeatable, organic conversion path (SEO, referral, direct, cold outreach)
- Your landing page converts at 2%+ for cold traffic (3–5% is the floor for paid to make sense)
- You know your CAC ceiling — meaning you know what you can afford to pay to acquire a customer
- You have a 90-day LTV:CAC ratio of at least 3:1
- You can fund the test phase without pressure to immediately break even

**It is too early when:**
- You have zero organic traction and are using paid to "find out if anyone wants this"
- Your offer is still being validated — paid ads will burn cash proving a broken hypothesis
- You cannot measure conversions properly (no pixel, no GA4, no UTMs)
- Monthly budget is under $500 — this is below the minimum threshold for most platforms to learn
- You are expecting paid to replace a missing content or SEO moat

The hard truth: most solopreneurs start paid ads 6–12 months too early.

---

## 2. Check for Context First

Before giving any paid ads advice, check for:

- `solopreneur-context.md` — business model, audience, product type
- `product-marketing-context.md` — positioning, ICP, offer details

**If those files are missing, ask:**
1. What is your monthly ad budget (actual spend, not aspirational)?
2. Which platform are you considering or already running?
3. What is the product or offer — price point, B2B or B2C, one-time or recurring?
4. Do you have conversion tracking set up (pixel, GA4)?
5. What is your current CAC from organic or other channels, if known?
6. Do you have any existing campaign data, or is this a cold start?

Do not give platform-specific advice without knowing at minimum: budget, product type, and whether tracking exists.

---

## 3. The Pre-Paid Checklist

Run through this before launching any campaign.

- [ ] **Organic proof exists** — at least one channel (SEO, referral, email, cold outreach) is generating customers without paid spend
- [ ] **Landing page converts** — minimum 2% CVR for cold traffic; test with organic first
- [ ] **Tracking is wired up** — Google Tag Manager, GA4, Meta Pixel, LinkedIn Insight Tag all firing correctly
- [ ] **UTM parameters are defined** — consistent utm_source / utm_medium / utm_campaign naming convention
- [ ] **CAC ceiling is known** — calculated from LTV × acceptable payback period
- [ ] **Offer is clear and specific** — vague offers do not convert on paid regardless of targeting
- [ ] **Test budget is funded** — can you spend $1,500–$3,000 on a test without needing it to pay off immediately?
- [ ] **Negative keyword list exists** (Google) or exclusions are built in (Meta)
- [ ] **A/B creative variation exists** — at least 2–3 creative angles to test from day one

If more than 3 boxes are unchecked, paid is premature.

---

## 4. Channel Selection for Solopreneurs

### The Honest Tradeoffs

| Platform | Best For | Minimum Viable Monthly Budget | Avg CPL | ROAS Benchmark |
|---|---|---|---|---|
| Google Search | High-intent buyers already searching | $1,500–$3,000/mo | $40–$100 | 3–5x |
| Meta (Facebook/Instagram) | B2C, DTC, low-ACV B2B, awareness + retargeting | $1,000–$2,500/mo | $20–$60 | 2–4x (blended) |
| LinkedIn | B2B with $5K+ ACV, specific job titles/company sizes | $3,000–$5,000/mo | $80–$200 | Justify on pipeline, not ROAS |
| YouTube | Brand awareness, long-form product demos | $2,000+/mo | Awareness metric | Not ROAS-driven |

### Channel Priority for Most Solopreneurs

1. **Google Search first** — if your buyers are searching for what you sell, demand capture beats demand creation. Cheaper in the long run.
2. **Meta second** — better for demand generation, product discovery, and retargeting audiences built from organic content.
3. **LinkedIn last** — only if your ACV is $5K+ and your ICP is a specific job title at a specific company size. Otherwise it burns cash fast.

---

## 5. Google Ads for Solos

### Search vs Performance Max vs Display

**Search campaigns** are the right starting point for most solopreneurs. You control keywords, match types, and ad copy. You know exactly what triggered your ad and why someone clicked.

**Performance Max (P-Max)** runs across Search, YouTube, Display, Gmail, and Discover simultaneously. It requires strong conversion data to work — at least 30+ conversions per month at the campaign level. Without it, P-Max burns budget experimenting across every placement at your expense. For solos starting out: avoid P-Max until your Search campaigns have 30+ conversions/month.

**Display campaigns** are awareness-only. They have low intent, high impression volume, and poor conversion rates for direct response. Not recommended as a starting point for solopreneurs with limited budgets.

### Keyword Match Types

- **Exact match** — tightest control, lowest volume, highest intent. Start here.
- **Phrase match** — moderate control. Use once exact match data is established.
- **Broad match** — only viable with Smart Bidding and substantial conversion data (50+ conversions/month). Without data, broad match + Smart Bidding is a black hole.

### Smart Bidding Readiness

Smart Bidding works when you have data. It fails when you do not.

| Bidding Strategy | When to Use | Data Requirement |
|---|---|---|
| Manual CPC | Cold start, no conversion data | None |
| Maximize Clicks | Building initial traffic volume | None (risky — watch spend) |
| Target CPA | Have consistent conversion volume | 30+ conversions/month at campaign level |
| Target ROAS | E-commerce with revenue tracking | 50+ conversions/month |

The common trap: switching to Target CPA at week one with 3 conversions. The algorithm optimizes toward what it sees — if it sees almost nothing, it guesses. Start manual CPC, gather 30+ conversions, then switch.

### Google Ads Minimum Budget Reality

- $500–$1,000/month: Too low for most competitive keywords. You will exit the learning phase slowly and gather minimal data.
- $1,500–$2,500/month: Minimum viable for most B2B and SaaS search campaigns.
- $3,000+/month: Where Smart Bidding starts performing reliably.

Build a strong negative keyword list from day one. Common exclusions for B2B/SaaS: "free", "cheap", "DIY", "job", "course", "tutorial", "salary", competitor terms you cannot outbid.

---

## 6. Meta Ads for Solos

### Cold Traffic vs Retargeting

Meta's algorithm is designed for two distinct jobs. Do not mix them in one campaign.

**Cold traffic (prospecting):** Reaching people who do not know you exist. Requires more budget, more creative testing, and more patience. ROAS will be lower (1.5–2.5x) but this builds your retargeting pool.

**Retargeting:** Reaching people who visited your site, watched your video, or engaged with your content. ROAS is higher (4–8x) but the pool shrinks if you stop prospecting. Retargeting only works if cold traffic is feeding it.

Rule of thumb: 70% cold / 30% retargeting when starting. Shift toward 50/50 once you have 1,000+ monthly website visitors.

### Audience Sizing

- Too narrow (under 100K): Algorithm cannot learn, CPMs spike, delivery stalls
- Sweet spot: 500K–5M for prospecting audiences
- Too broad (50M+): Impressions go to the wrong people unless creative does the targeting work

Lookalike audiences work well with 1,000+ seed customers. Do not build lookalikes from 50-person email lists.

### Advantage+ vs Manual

**Advantage+ Shopping/Leads Campaigns:** Meta's automation. Works well for prospecting and top-of-funnel when you have clean conversion data and creative variety. Can lower CPA by 15–30% vs manual — but only when the algorithm has enough data.

**Manual campaigns:** Better for retargeting with specific audiences, niche B2B targeting, or when you need to control placement precisely.

Best approach for solopreneurs: Run Advantage+ for cold prospecting, manual for retargeting. Do not try to run one campaign for both.

### Meta Minimum Budget Reality

- $300–$500/month: Below the threshold for the algorithm to learn properly. You will be in permanent "learning limited" status.
- $1,000–$1,500/month: Minimum viable for one prospecting + one retargeting campaign.
- $2,000–$2,500/month: Where Meta's algorithm exits learning and starts optimizing.

Meta recommends 50 conversions per ad set per week to exit the learning phase. Work backward from your CPA: if your target CPA is $30, you need $1,500/week per ad set for proper learning. That math is brutal for solos — which is why starting with traffic or lead objectives (not conversions) at lower spend makes sense, then scaling with conversion objectives.

---

## 7. LinkedIn Ads

### When to Use LinkedIn

LinkedIn is the right channel only if all of the following are true:
- Your product has an ACV (annual contract value) of $5,000+
- Your ICP is a specific job title (e.g., VP of Engineering, Head of People) at a specific company size
- You need to reach people who would never Google your category
- You can afford $3,000–$5,000/month for at minimum 90 days without expecting ROAS

If your ACV is under $5,000, LinkedIn's CPCs will make your unit economics impossible.

### LinkedIn CPC Reality (2025–2026)

- Average CPC: $5.58–$12.00
- B2B SaaS CPCs (North America): $8–$12 per click
- Cost per lead: $80–$200 for most B2B SaaS verticals
- CPM: $20–$45 (vs $8–$14 on Meta, $4–$8 on TikTok)

At $10 CPC and a 5% landing page CVR, your CPL is $200. At $100 ACV/month ($1,200 ARR), that math does not work. At $500/month ($6,000 ARR) it starts to.

### LinkedIn Ad Formats That Work for Solos

- **Single Image Ads:** Simplest to test, reasonable CPCs, works for lead gen
- **Lead Gen Forms (native):** Removes friction of going to a landing page. Higher lead volume, sometimes lower lead quality. Test both.
- **Message Ads (InMail):** Higher cost, but direct. Use for high-ACV enterprise plays only.
- **Thought Leader Ads:** Boosting organic posts from your personal profile. Lower cost than standard ads, and feels less like an ad.

### LinkedIn Minimum Budget

- $10/day platform minimum: Technically starts here, but this is insufficient for learning
- $50–$100/day per campaign: Minimum for meaningful data
- $3,000–$5,000/month: Minimum to run LinkedIn seriously
- $18,000–$60,000/year: Realistic for a full LinkedIn Ads program

For most solopreneurs: LinkedIn is a money pit unless your ACV and deal volume justify the CPCs. Start with Google or Meta, use LinkedIn organic content to warm ICP, then layer in LinkedIn Ads only after proving the offer works.

---

## 8. Budget Allocation Strategy

### Test Budget Phase (Month 1–3)

Objective: Gather data. Not to be profitable.

| Allocation | Percentage | Purpose |
|---|---|---|
| Primary channel (search or social) | 70% | Main campaign testing |
| Retargeting | 20% | Re-engage site visitors |
| Creative testing | 10% | New angles, formats |

Do not spread across multiple platforms during the test phase. Pick one platform, prove it works, then expand.

### Scale Budget Phase (Month 4+)

Once one channel has a proven CAC:
- Double down on the working channel: 60% of budget
- Add a second channel for reach: 25% of budget
- Retargeting across both: 15% of budget

### Rule of Thumb for Budget Sizing

Work backward from your CAC ceiling, not forward from "what I can afford":

1. Set your target CAC (LTV ÷ 3 is a starting point)
2. Estimate CVR on your landing page (use 2% if unknown)
3. Estimate CPC for your target keywords/audience
4. Calculate: `(CPC ÷ CVR) = CPL` — is that under your CAC ceiling?
5. Budget for at minimum 50–100 conversions in the test phase to get statistically meaningful data

Example: Target CAC $100. Landing page CVR 3%. Google CPC $3. CPL = $100. Budget needed for 50 conversions = $5,000. That is your minimum test budget.

---

## 9. Bidding Strategy

### The Progression for New Campaigns

Do not jump to automated bidding on day one.

**Phase 1 — Manual CPC (weeks 1–4):**
Control your spend. Gather impression, click, and conversion data. Identify which keywords or placements convert. Set bids manually based on keyword performance. Watch for irrelevant clicks and build negative keyword lists.

**Phase 2 — Maximize Conversions (weeks 5–8, 20+ conversions):**
Let the platform optimize for volume of conversions within your budget. A transition step before Target CPA. Watch your average CPA during this phase.

**Phase 3 — Target CPA (month 3+, 30–50 conversions/month):**
Tell the algorithm what you want to pay per conversion and let it work. Requires consistent conversion data. Do not set Target CPA below your actual average CPA — the algorithm will reduce volume chasing an impossible target.

**Phase 4 — Target ROAS (month 6+, e-commerce):**
Only when you have revenue tracking wired to actual transaction values. Requires 50+ conversions/month.

### LinkedIn Bidding

Start with Manual CPC bidding. LinkedIn's automated bidding tends to overbid in competitive auctions early on. Set manual CPCs 10–20% below LinkedIn's suggested bid to test if you still get delivery, then adjust.

---

## 10. Tracking and Attribution

Bad tracking is the #1 reason paid ads "don't work" — the ads were working, but you could not see it.

### Minimum Tracking Stack

- **GA4** with goals/conversions configured for key events (lead, trial signup, purchase)
- **Google Tag Manager** as the tag management layer — never hardcode pixels
- **Meta Pixel** with standard events (Lead, Purchase, CompleteRegistration)
- **LinkedIn Insight Tag** if running LinkedIn campaigns
- **UTM parameters** on every paid link — consistent naming convention matters

### UTM Naming Convention (Suggested)

```
utm_source=google
utm_medium=cpc
utm_campaign=search-brand-exact
utm_content=ad-variant-a
```

Be consistent. Inconsistent UTMs fragment your data and make attribution impossible.

### iOS14+ Reality

Apple's App Tracking Transparency (ATT) broke Meta's pixel tracking. Since 2021, Meta has been running on modeled data for a significant portion of iOS users. What this means in practice:

- Reported conversions in Meta Ads Manager will be lower than actual (Meta under-counts)
- GA4 and Ads Manager numbers will not match — this is expected, not a bug
- Use a 7-day click / 1-day view attribution window for more accurate comparison
- Implement Conversions API (CAPI) server-side to recover some lost signal
- For Google: implement Enhanced Conversions for better accuracy

Do not make optimization decisions based on Meta-reported ROAS alone. Cross-reference with GA4 and your actual revenue data.

### Attribution Windows

- Google Ads default: 30-day click attribution
- Meta default: 7-day click / 1-day view
- LinkedIn default: 30-day click / 7-day view

Shorter windows show lower ROAS but give you faster feedback for optimization.

---

## 11. Optimization Rhythm

### Weekly Checks (every 7 days)

- [ ] Impression share — are you losing to budget or to rank?
- [ ] Search terms report (Google) — add new negatives for irrelevant queries
- [ ] Cost per conversion trend — going up or down?
- [ ] Top-performing vs. bottom-performing ads/creatives — pause the losers
- [ ] Budget pacing — on track for the month or overspending early?

### When to Kill vs Scale

**Kill a campaign/ad set when:**
- CPA is 3x+ your target after 30+ days of data
- CTR is under 0.5% (Google) or under 0.8% (Meta) with no improvement in 2 weeks
- Zero conversions after spending 3x your target CPA

**Scale a campaign when:**
- CPA is at or below target for 14+ consecutive days
- Conversion volume is consistent (not spiking one week, dead the next)
- ROAS is above your minimum threshold for 30+ days

**Never make major changes during the learning phase.** Changing bids, budgets, audiences, or creatives resets the algorithm's learning. Make one change at a time and wait 7–10 days before evaluating.

### Monthly Review

- Compare CAC across all active channels
- Review top-converting keywords / audiences — double down on what works
- Review assisted conversions in GA4 — some channels influence but do not close
- Update creative pool — Meta creative fatigue typically hits at 3–4 weeks with the same audience

---

## 12. Common Mistakes

**Starting paid too early.** No organic proof, no landing page data, no CAC baseline. Paid ads amplify a working funnel — they do not create one.

**Underfunding campaigns.** $200/month on Google is not a test — it is noise. Platforms need minimum conversion volume to learn. Underfunding is worse than not running at all because it produces misleading data.

**Switching to Smart Bidding with no data.** Target CPA with 5 conversions will spend your budget chasing a pattern that does not exist yet. Manual CPC first.

**Running Performance Max before proving Search.** P-Max requires 30+ conversions/month to not be a black box. Without data, it spreads spend across every placement without discrimination.

**Ignoring negative keywords.** For Google Search campaigns, running without a well-pruned negative keyword list burns 20–40% of budget on irrelevant searches. Update weekly from the search terms report.

**No creative variation on Meta.** One ad with one audience will fatigue within 2–3 weeks. Build a creative library before launching — static images, short-form video, founder content.

**Mixing prospecting and retargeting in one campaign.** These are different objectives, different audiences, and different ROAS expectations. They require separate budgets and separate measurement.

**Optimizing for the wrong conversion event.** Optimizing for "page views" or "add to cart" instead of purchases tells the algorithm to find clickers, not buyers. Always optimize for the event closest to revenue that gives you enough volume.

**Trusting vanity metrics.** CTR and impressions do not pay the bills. CAC and ROAS do. Always measure back to revenue.

**Changing too much too fast.** Every change to an ad group resets learning. Make one change, wait 7–10 days, evaluate. Impatient optimization is a budget killer.

---

## 13. Contrarian Takes

**Most solopreneurs start paid ads way too early.** The most common scenario: you have 50 email subscribers, a 1% converting landing page, no organic proof of demand, and you start Google Ads to "test the market." This is expensive market research. Get to consistent organic conversions first.

**Performance Max is a black box for anyone without data.** Google markets P-Max as a set-it-and-forget-it solution. It is not. It consumes budget across Display, YouTube, and Discovery — placements that rarely convert for B2B — while hiding performance by placement. Transparent search campaigns are almost always better for solopreneurs.

**LinkedIn is overpriced for most solopreneurs.** At $8–$12 CPC, you need an ACV of $5,000+ just to make the unit economics survivable. LinkedIn organic content almost always outperforms LinkedIn paid for solopreneurs. Use LinkedIn Ads only when you have proven the offer works and need to scale a specific ICP segment.

**Broad match + Smart Bidding is dangerous without data.** Google will take your broad match keywords as an invitation to match to anything tangentially related, then use Smart Bidding to optimize toward whatever conversion signals exist — even weak ones. This combination, in an account with under 50 monthly conversions, burns budget fast.

**Meta's Advantage+ CPA spike in 2025 is real.** Multiple practitioners reported nCAC (new customer acquisition cost) doubling on Advantage+ campaigns in 2025. Advantage+ is not a universal cost reduction — it depends heavily on your offer, audience, and creative quality. Test it, do not assume it beats manual.

**A 2x ROAS on Meta is often unprofitable.** A 2x ROAS means you are making $2 for every $1 in ad spend. But after product COGS, fulfillment, platform fees, and overhead, 2x ROAS often means losing money. Know your breakeven ROAS before launching: `1 ÷ gross margin`. If your margin is 40%, breakeven ROAS is 2.5x. Anything below that is burning cash.

**Platform-reported ROAS is not your real ROAS.** Google over-counts, Meta under-counts (thanks to iOS14). The truth is somewhere in the middle. Use GA4 + your actual revenue data to triangulate.

---

## 14. Quick Wins

- **Add a remarketing campaign on day one.** Even if cold traffic is not running yet, install the pixel and tag all visitors. When you are ready to retarget, you will have an audience.

- **Use exact match keywords exclusively for the first 30 days.** Control your spend, understand what is actually converting, then expand match types.

- **Steal your best organic content for paid creative.** Your top-performing organic posts are proof of concept. Run them as ads before investing in new creative.

- **Set up a branded search campaign immediately.** Branded keywords (your own name) are cheap, convert at the highest rate, and protect you from competitors bidding on your name.

- **Use lead gen forms on LinkedIn and Meta.** Removing the step of going to your landing page increases lead volume. Lower friction = more leads, even if quality varies.

- **Build your negative keyword list before launch on Google.** Spend 30 minutes adding obvious negatives (free, cheap, DIY, jobs, salary) before your first campaign goes live. This prevents day-one waste.

- **Set up a dashboard.** Pull Google Ads, Meta Ads, and GA4 into a single dashboard (Looker Studio is free). Seeing everything in one place forces better decision-making.

- **Run a $500 Meta test on a warm audience first.** Email list, past customers, video viewers. If you cannot convert a warm audience, you will not convert cold traffic.

---

## 15. Related Skills

- **ad-creative** — Generate and test ad copy, headlines, creative angles, and hooks across Google, Meta, and LinkedIn
- **analytics-tracking** — Set up GA4, UTM parameters, conversion tracking, and attribution models
- **page-cro** — Optimize landing pages to improve conversion rates before scaling paid traffic
- **product-marketing-context** — Define your ICP, positioning, and offer clarity — foundational inputs for any paid campaign

---

*Generated using the paid-ads skill from Solopreneur Skills*
