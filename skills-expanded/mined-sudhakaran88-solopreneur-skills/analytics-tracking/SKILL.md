---
name: analytics-tracking
description: When the user wants to set up, improve, or audit analytics tracking and measurement. Also trigger on "set up tracking", "GA4", "Google Analytics", "conversion tracking", "event tracking", "UTM parameters", "tag manager", "GTM", "analytics implementation", "tracking plan", "what should I track", "analytics stack". For A/B test measurement, see ab-test-setup.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are an analytics expert helping solopreneurs track what actually drives revenue — not set up dashboards they'll never look at.

---

## 1. When to Use This Skill

Trigger this skill when the user wants to:

- Set up Google Analytics 4 or a GA4 alternative from scratch
- Fix broken or missing tracking (UTMs, events, conversions)
- Decide between GA4, Plausible, Fathom, Mixpanel, or PostHog
- Build or audit a tracking plan
- Understand which metrics actually matter for their business model
- Set up ecom analytics (Shopify, WooCommerce)
- Create a weekly reporting rhythm they'll actually stick to

Do NOT trigger for A/B test measurement — see `ab-test-setup`.

---

## 2. Check for Context First

Before giving any recommendations, read:

- `solopreneur-context.md` — business model, stage, team size
- `product-marketing-context.md` — product type, funnel structure, channels

If neither exists, ask these four questions (all at once, not one-by-one):

1. What's your CMS or tech stack? (WordPress, Webflow, Shopify, custom?)
2. What analytics do you currently have installed, if anything?
3. What's your primary business model — SaaS, ecom, content/creator, services?
4. What is your single most important conversion goal? (trial signup, purchase, booking, email subscriber?)

Do not proceed to recommendations until you have at least answers 3 and 4.

---

## 3. The Three Metrics That Actually Matter

Every analytics conversation should start here. Everything else is support data.

### CAC — Customer Acquisition Cost
> What does it cost to acquire one paying customer?

`CAC = Total marketing + sales spend / New customers acquired`

- Track by channel, not just overall
- If you can't calculate CAC, your tracking is broken at the source level
- Healthy benchmark: LTV:CAC ratio should be 3:1 or higher — below that, you have a math problem

### Activation Rate — Are people reaching the "aha moment"?
> What % of signups/visitors complete the one action that predicts retention?

- For SaaS: % of signups who complete a key action within 7 days (e.g., create first project, invite a teammate)
- For ecom: % of sessions that add to cart
- For content: % of visitors who subscribe or return within 30 days
- This is the most undertracked metric for solos. A 1% improvement in activation outperforms most traffic campaigns.

### LTV — Lifetime Value
> How much revenue does a customer generate before they churn?

`LTV = Average revenue per customer / Churn rate`

- For solopreneurs on MRR products: LTV = ARPU / Monthly churn rate
- You cannot make good paid acquisition decisions without this number
- If you don't know your LTV yet, estimate it conservatively and revisit quarterly

**Everything else** — pageviews, sessions, bounce rate, follower counts — is context, not signal. Track it if it helps you diagnose, not because it feels productive.

---

## 4. Marketing Analytics Stack

### Decision Matrix

| Tool | Best For | Privacy | Price/mo | Setup Time |
|---|---|---|---|---|
| **Plausible** | Solos who want clean traffic data fast | Excellent (GDPR-safe by default) | $9–$19 | 5 min |
| **Fathom** | Solos who need better goal funnels + GA importer | Excellent | $14–$74 | 10 min |
| **GA4** | Anyone running Google Ads (required) | Poor (GDPR grey area in EU) | Free | 2–4 hrs |
| **Umami** | Self-hosters who want $0/mo | Excellent | Free (self-host) | 30–60 min |
| **Matomo** | Regulated industries needing full data control | Excellent | Free (self-host) | 1–2 hrs |

### Honest Takes

**Plausible** is the default recommendation for solopreneurs. One script tag, no consent banner needed in most jurisdictions, clean single-page dashboard, custom events via CSS class names (no code). Covers 10K pageviews/month at $9. The 14-day free trial is genuinely useful.

**Fathom** is Plausible's more polished cousin. Better historical data retention (3 years vs 2), smoother goal funnel UI, and a solid GA/UA importer if you're migrating. Costs slightly more but worth it if you're data-sensitive about history.

**GA4** is worth using only if:
- You run Google Ads (the native integration matters for bidding)
- You need demographic or interest data
- You're on a WordPress/Shopify setup where GA4 is already pre-integrated

GA4 is genuinely complex. It samples data on the free tier for large traffic, requires a consent management platform for EU compliance, and the UI punishes people who aren't analytics professionals. If you're spending more than 2 hours/month confused by GA4, switch to Plausible.

**Umami** (self-hosted) is the zero-cost option if you're technical. Runs on a $5/month VPS or free tier on Railway/Vercel. Open-source, no data limits.

---

## 5. GA4 Setup Checklist (Minimum Viable)

If you've committed to GA4, here's the minimum setup that actually works.

### One-Time Configuration
- [ ] Set correct time zone and currency in Admin > Property Settings
- [ ] Extend data retention to 14 months (Admin > Data Settings > Data Retention)
- [ ] Filter internal traffic — add your IP as an internal filter (Admin > Data Filters)
- [ ] Enable Google Signals only if you need cross-device reporting (privacy tradeoff)
- [ ] Connect to Google Search Console for organic keyword data
- [ ] Connect to Google Ads if running paid traffic

### Events to Configure
- [ ] `page_view` — auto-collected, confirm it's firing in DebugView
- [ ] `scroll` — auto-collected (90% scroll depth)
- [ ] `click` (outbound) — auto-collected
- [ ] `form_submit` — custom event on your primary conversion form
- [ ] `sign_up` — mark as a key event (formerly "conversion")
- [ ] `purchase` — if ecom, use the standard ecom schema
- [ ] One "activation event" specific to your product (e.g., `project_created`, `trial_started`)

### Mark as Key Events (Conversions)
Mark only true business outcomes as key events — not micro-actions. A bloated conversion list corrupts attribution.

Recommended key events for most solos:
- `sign_up`
- `purchase`
- `trial_started`
- `contact_form_submitted`

### Verify Before You Trust
Use GA4's DebugView (Admin > DebugView) with `?debug_mode=1` appended to your URL. Confirm events fire, confirm parameters pass correctly. Never trust reports you haven't verified in debug mode.

---

## 6. UTM Parameter Hygiene

UTMs are how you know which traffic actually converts. Without consistent UTMs, your channel attribution is noise.

### Required Parameters
| Parameter | Purpose | Example |
|---|---|---|
| `utm_source` | Where traffic came from | `newsletter`, `google`, `twitter` |
| `utm_medium` | Channel type | `email`, `cpc`, `social`, `referral` |
| `utm_campaign` | Campaign name | `q2-launch`, `black-friday-2026` |

### Optional but Useful
| Parameter | Purpose | Example |
|---|---|---|
| `utm_content` | Which creative/link variant | `hero-cta`, `sidebar-link` |
| `utm_term` | Paid keyword (Google Ads auto-populates) | `project-management-tool` |

### Naming Rules — Follow These or Your Data Is Garbage

1. **Always lowercase.** `Newsletter` and `newsletter` are two separate sources in GA4.
2. **Use hyphens to separate words.** `cold-email` not `cold_email` or `cold email`.
3. **Never use spaces.** A space becomes `%20` and breaks most reports.
4. **Standardize your source list.** Create a locked reference doc with every approved source value. Common approved values: `google`, `facebook`, `instagram`, `linkedin`, `twitter`, `newsletter`, `youtube`, `podcast`.
5. **Standardize your medium list.** `cpc`, `email`, `social`, `referral`, `organic-social`, `affiliate`, `display`.
6. **Date campaigns consistently.** Use `YYYY-MM` format in campaign names when relevant: `product-launch-2026-04`.

### What Breaks Without UTMs

- Email traffic is misattributed to "direct" — makes your best channel invisible
- Social traffic collapses into "referral" or "(direct)" on iOS due to link stripping
- You cannot calculate CAC by channel because you don't know which channel drove which signup

### Build Once, Use Forever
Create a UTM builder spreadsheet (Google Sheets works) with dropdowns for source and medium. Lock the value lists. Make everyone use it. This is the single highest-ROI analytics task you will ever do.

---

## 7. Product Analytics

Marketing analytics tells you who's visiting. Product analytics tells you what they're doing — and whether it leads to activation and retention.

### When You Need Product Analytics

You need a product analytics tool (not GA4) when:
- You have a logged-in product experience (SaaS, app, membership)
- You want funnel analysis from signup → activation → retention
- You need cohort analysis (do users from channel X retain better?)
- You want feature usage data

If you're a content site, ecom store, or pure service business, GA4 or Plausible covers your needs.

### Tool Comparison

**PostHog** — Best default for solopreneurs and indie hackers
- Free tier: 1M events/month (genuinely generous)
- Includes: event analytics, funnels, cohorts, session replay, feature flags, A/B testing, surveys
- Can be self-hosted for $0
- Slightly more technical setup than Mixpanel but much better value
- Best for: engineering-led or developer-comfortable solos

**Mixpanel** — Best out-of-the-box experience
- Free tier: 20M events/month (very generous)
- Clean UI, best-in-class funnel and retention reports
- Added session replay and A/B testing in 2025–2026
- Warning: pricing scales fast past free tier — verify your event volume before committing
- Best for: product-led solos who want polish without engineering overhead

**Amplitude** — Enterprise-grade, not solo-grade
- Pricing is opaque and enterprise-targeted
- Overkill for anything under 10K MAUs
- Skip unless you're post-Series A or have a dedicated data analyst

**Heap** — Auto-capture everything
- Captures all events retroactively — no pre-instrumentation required
- Useful if you're starting late and want historical data
- Privacy concerns; requires consent management
- Best for: solos who missed early tracking and need to backfill analysis

### Recommended Solo Stack for SaaS
- Traffic: Plausible ($9/mo) for marketing site
- Product: PostHog free tier for in-app events
- Total cost: $9/mo and an afternoon of setup

---

## 8. The Tracking Plan

A tracking plan is a document that defines every event you track, what it means, and what properties it carries. Without one, your event names will be chaos within 6 months.

### Event Naming Conventions

Use `snake_case` for all event names. Always `object_action` format.

| Pattern | Example |
|---|---|
| `noun_verb` | `trial_started`, `project_created`, `plan_upgraded` |
| Be specific | `checkout_started` not `button_clicked` |
| No abbreviations | `subscription_cancelled` not `sub_canc` |
| Past tense for completed actions | `payment_completed`, `onboarding_finished` |

### Minimum Tracking Plan for SaaS Solopreneur

| Event | When to Fire | Key Properties |
|---|---|---|
| `page_viewed` | Every page load | `page_name`, `page_url` |
| `sign_up_completed` | Account created | `source`, `plan`, `signup_method` |
| `onboarding_step_completed` | Each onboarding step | `step_name`, `step_number` |
| `activation_event` | Your specific "aha moment" | Product-specific |
| `feature_used` | Core feature engagement | `feature_name` |
| `plan_upgraded` | Upgrade to paid | `from_plan`, `to_plan`, `mrr` |
| `subscription_cancelled` | Churn | `reason`, `plan`, `mrr_lost` |
| `payment_failed` | Payment failure | `amount`, `failure_reason` |

### Document It
Store your tracking plan in Notion, a Google Sheet, or a markdown file alongside your code. Include: event name, description, when it fires, who fires it (frontend/backend), and all properties with their data types.

---

## 9. Ecom Analytics

### Tier 1: Shopify Native (Free — Start Here)
Shopify's built-in analytics covers: revenue by channel, conversion rate by traffic source, top products, geographic breakdown, and returning customer rate. For most solopreneurs under $10K/month in revenue, this is enough.

What Shopify native misses: cross-channel attribution, LTV cohorts, ad spend efficiency.

### Tier 2: GA4 + Shopify (Free — When You Need More)
Google's Shopify channel app installs GA4 enhanced ecom tracking automatically. Gives you: purchase funnels, product performance, cart abandonment, and channel attribution across sessions.

Use this when you're running multiple marketing channels and need to reconcile traffic sources.

### Tier 3: Triple Whale or Polar Analytics ($99+/mo — Only If Ads-Heavy)
For Shopify brands spending $5K+/month on paid ads:

- **Triple Whale**: Best for DTC brands running Meta + Google simultaneously. The Triple Pixel improves post-iOS attribution. Includes cohort LTV, creative analytics, and a unified P&L view.
- **Polar Analytics**: Better for multi-channel data warehousing. 45+ connectors, strong LTV dashboards, AI query interface. Better value if you need cross-platform data in one place.

**Skip both if:** you're spending less than $5K/month on ads. The cost (typically $99–$300/mo) doesn't justify the benefit at lower volumes.

---

## 10. Reporting Rhythm

The best dashboard is one you actually open. Here's a sustainable reporting rhythm for solopreneurs.

### Weekly Check (10 minutes, every Monday)
Focus on leading indicators only:

- Traffic vs. last week (is the trend moving?)
- Signups or leads vs. last week
- Trial-to-paid conversion this week
- Any anomalies? (traffic spike, conversion drop)

Use Plausible or Fathom for this — their single-page dashboards are designed for this review.

### Monthly Review (30 minutes, first Monday of month)
Go deeper:

- CAC by channel this month
- Activation rate: what % of signups hit your key activation event?
- MRR movement: new MRR, expansion MRR, churned MRR
- LTV:CAC ratio — is it holding above 3:1?
- Top-performing content or campaigns

### Quarterly Audit (2 hours, first week of each quarter)
- Are your key events still firing correctly? (run through DebugView)
- Did any UTM naming drift? (audit your source/medium breakdown for garbage values)
- Are your conversion events still mapping to the right business outcomes?
- Review and update your tracking plan

---

## 11. Common Mistakes

**1. Tracking everything, acting on nothing.**
More events do not mean better decisions. Every event you add that you never query is technical debt. Start with 8–10 events. Add more only when you have a specific question that requires them.

**2. Counting pageviews as success.**
Pageviews tell you someone visited. They tell you nothing about whether they converted, activated, retained, or were worth acquiring. Report pageviews as context, never as a north star.

**3. UTM inconsistency destroying channel attribution.**
One team member who uses `Email` instead of `email` as a source splits your data. Build the naming doc. Use a spreadsheet with locked dropdowns. Enforce it.

**4. Setting up GA4 and never verifying events.**
Most GA4 setups have silent errors — events that appear to fire but pass wrong properties or fire on wrong pages. Always verify with DebugView before trusting reports.

**5. Marking too many events as conversions.**
If everything is a conversion, nothing is. Attribution becomes noise. Restrict key events to true business outcomes: signup, purchase, trial start.

**6. Not tracking the activation event.**
Most solopreneurs track signups. Almost none track activation. This means you're measuring the top of your funnel while blind to the part that predicts revenue. Define your activation event in week one.

**7. Ignoring data retention settings in GA4.**
GA4 defaults to 2-month data retention for Explore reports. Set it to 14 months on day one. You cannot retroactively extend it.

**8. Using GA4 for a GDPR-regulated audience without consent management.**
Austrian, French, and Italian authorities have ruled GA4 data transfers non-compliant without proper consent infrastructure. If you have significant EU traffic, either use Plausible/Fathom or implement a properly configured CMP.

---

## 12. Contrarian Takes

**GTM is overkill for most solos.**
Google Tag Manager is powerful but adds complexity, another dependency, and a meaningful learning curve. If you have fewer than 5–7 tags to manage, add scripts directly to your site or use your CMS's built-in integrations. GTM earns its place when you're managing 10+ tags across multiple vendors and need version control. For a solo with one analytics tool and one ad pixel, it's unnecessary.

**More data does not mean better decisions.**
The solopreneur who checks three numbers weekly and acts on them beats the one with a 40-metric dashboard they look at once a month. Restraint in tracking is a competitive advantage. Pick fewer metrics. Look at them more often.

**Plausible at $9/month beats GA4 at $0 for most solos.**
The time you spend learning, debugging, and maintaining GA4 has a cost. If you're not running Google Ads, Plausible's simplicity returns more value than GA4's depth you'll never use.

**Session replay before more event tracking.**
If you want to understand why users aren't converting, 10 session recordings will tell you more than any dashboard. PostHog's free tier includes session replay. Watch people use your product before adding more instrumentation.

**Your analytics are only as good as your definitions.**
"Activation" means nothing until you define it. "Conversion" means nothing until you agree what action it represents. The hardest part of analytics is not the tooling — it's getting ruthlessly clear on what you're measuring and why.

---

## 13. Quick Wins (Set Up in 1 Hour)

These five actions will give you better data than 90% of solopreneurs. Do them in order.

**Hour 1:**
- [ ] Install Plausible or Fathom (15 min) — add the script tag, verify pageviews are coming in
- [ ] Define your top 3 UTM sources and top 3 mediums — write them down in a doc right now
- [ ] Tag every link in your next email send with consistent UTMs using a simple spreadsheet
- [ ] Set up one custom event on your primary CTA (Plausible makes this a CSS class; PostHog/GA4 need one JS call)
- [ ] Open your analytics tool and write down the one number you'll check every Monday morning

**Next Week:**
- Define your activation event — what is the single action that predicts a user will stick around?
- Instrument that event in PostHog or Mixpanel free tier
- Set up a recurring Monday morning calendar block: "10-min analytics check"

---

## 14. Related Skills

- **`ab-test-setup`** — When you want to run controlled experiments to validate copy, pricing, or UX changes. Measurement setup is distinct from analytics instrumentation.
- **`page-cro`** — When conversion rate optimization work precedes tracking decisions. CRO informs which events matter most.
- **`seo-audit`** — When organic traffic analysis and Search Console data are part of the analytics picture.
- **`revops`** — When marketing analytics needs to connect to CRM, sales pipeline, and revenue reporting. Especially relevant when calculating CAC requires merging ad spend data with CRM deal data.

---

*Generated using the analytics-tracking skill from Solopreneur Skills*
