---
name: popup-cro
description: 'When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also trigger on "exit intent popup", "popup conversions", "modal optimization", "lead capture popup", "email popup", "announcement banner", "overlay", "lightbox", "sticky bar". For forms not in popups, see form-cro. For general page CRO, see page-cro. Note: intrusive mobile popups risk Google penalties — this skill covers compliant approaches.'
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a popup conversion expert helping solopreneurs capture more emails and leads with overlays that don't annoy visitors, tank SEO, or trigger Google's intrusive interstitial penalty.

---

## 1. When to Use This Skill

Use this skill when you need to:

- Build or fix an email capture popup (lead magnet, newsletter, discount)
- Set up exit intent popups to recover abandoning visitors
- Add a slide-in, sticky bar, or announcement banner
- Audit a popup that gets dismissed too fast or has low conversion
- Make sure your popups won't get you penalized by Google on mobile
- Choose the right popup tool for your stack and budget

**Not this skill:** Forms embedded in landing pages → use `form-cro`. Onboarding flows after signup → use `onboarding-cro`. Full page conversion audit → use `page-cro`.

---

## 2. Check for Context First

Before giving recommendations, ask or check `solopreneur-context.md` for:

- **Goal:** Email capture / lead gen / announcement / discount / offer?
- **Traffic type:** Cold (SEO/ads) or warm (returning visitors, social)?
- **Mobile traffic %:** Critical — changes what you can safely show
- **Current tool:** What popup builder are you using?
- **Current conversion rate:** What are you seeing now?
- **Trigger preference:** Do you have a trigger set up (exit, scroll, time)?

Without this context, recommendations will be generic. The difference between 2% and 8% conversion is almost always in the targeting + offer combination, not the design.

---

## 3. Google's Intrusive Interstitial Penalty

**This is real, still active, and solopreneurs get burned by it constantly.**

### What the penalty is

Google launched the mobile intrusive interstitials penalty in January 2017. It is still enforced in 2025. The 2024 Google Content Warehouse leak confirmed it is a primary ranking signal, with a named attribute `violatesMobileInterstitialPolicy` and a scaled violation strength from 0 to 1000.

The penalty applies specifically when a visitor arrives from a **Google mobile search result** and is immediately shown an interstitial that blocks the main content.

### What triggers the penalty

- Full-screen popup shown immediately on page load (from search)
- Popup that covers the main content and requires dismissal before the visitor can read anything
- Fake "above the fold" layouts where the actual content is hidden below a large interstitial
- Any popup that makes the page look unusable before the user can engage

### What is safe on mobile

| Approach | Safe? |
|---|---|
| Cookie consent / legal banners | Yes (legally required) |
| Age verification dialogs | Yes |
| Login dialogs for gated content | Yes |
| Small sticky footer bar (not full-screen) | Yes |
| Slide-in after scroll or time delay | Yes (not on first load from search) |
| Exit intent (only fires on exit, not load) | Yes |
| Full-screen popup — cold traffic, immediate | No |
| Full-screen popup — timed 5s+ after load | Gray area; avoid on mobile |

### The safe rule for solopreneurs

On mobile, **never show a full-screen popup to first-time visitors arriving from search**. Use a sticky footer bar or a slide-in with at least a 5–8 second delay instead. Save full-screen modals for returning visitors, email traffic, or desktop users.

---

## 4. Popup Types + Benchmarks

| Type | Avg. Conversion | Top 10% | Best For |
|---|---|---|---|
| Exit intent | 2–5% | 10–17% | Cold traffic, cart abandon |
| Scroll trigger (70%+) | 3–6% | 8–12% | Blog readers, engaged visitors |
| Time delay (30–60s) | 2–4% | 6–10% | Warm traffic, content sites |
| Click trigger (2-step) | 20–31% | 40%+ | Buttons, links (intent-qualified) |
| Entry popup (0–5s) | 1–2% | 3–5% | Discount/offer sites only |
| Sticky bar / hello bar | 0.5–1.5% | 2–3% | Low-friction, always-visible |
| Slide-in (corner) | 2–4% | 5–8% | Less intrusive, mobile-friendly |
| Gamified (spin wheel) | 3.5–8% | 12%+ | Ecom discounts |

Source: Popupsmart 2025 benchmark (10,000+ campaigns), Wisepops 1.24B display study, Sumo/BDOW opt-in data.

**Key insight:** Click triggers convert 10x more because the visitor has already self-selected by clicking. Use 2-step opt-ins ("Yes, I want the guide" → form appears) for cold traffic popups.

---

## 5. Trigger Timing Rules

**Exit intent** — Best for cold traffic and visitors who haven't opted in. Only fires once per session. Does not trigger the Google penalty (it fires on exit, not on load). Works best when the offer directly addresses the reason they're leaving (e.g., hesitating on price → discount; leaving blog → content upgrade).

**Scroll trigger (50–70% depth)** — Best for blog and content traffic. The visitor has already read enough to be interested. 70% scroll is the sweet spot — they've consumed the content and are receptive to a related offer.

**Time delay (30–60 seconds)** — Use for warm or returning traffic. 6–10 seconds outperforms immediate by up to 25% in benchmark data. 30 seconds filters for genuinely engaged visitors. Never use sub-5-second delays on cold traffic.

**Entry popup (0–3 seconds)** — Only appropriate for high-discount ecom or when the whole page IS the offer (dedicated landing pages). On a blog or home page, it kills trust with cold visitors.

**Click trigger** — Always use for high-intent moments (pricing page, download button, "Get access" CTAs). Conversion rates are 10–30x higher because intent is confirmed before the form appears.

**Never combine triggers.** One popup per page. Multiple overlapping triggers create popup fatigue and confuse analytics.

---

## 6. Copy Patterns That Convert

### The offer (most important)

Your offer needs to be specific and immediately understood. Vague kills conversions.

- Weak: "Join our newsletter"
- Weak: "Get updates"
- Strong: "Get the 5-day content calendar template (free)"
- Strong: "Save 15% on your first order — expires tonight"
- Strong: "Download the SaaS pricing teardown (17 examples)"

### Headline formula

Pick one frame and use it cleanly:

- **Curiosity:** "The one email tactic most solopreneurs never try"
- **Direct offer:** "Get the free [X] — no fluff, just the template"
- **Pain relief:** "Still guessing what to post? This fixes it."
- **Social proof:** "11,000 solopreneurs use this content calendar"
- **Fear of missing out:** "Offer closes when you leave this page"

### Dismiss CTA (the "no" copy)

Do not use a blank X button. Write a specific dismiss link that frames the cost of leaving:

- "No thanks, I'll figure it out myself"
- "I don't need more leads right now"
- "Skip — I'm already happy with my conversion rate"

This is called negative opt-out copy. Use it carefully — manipulative versions annoy visitors. Factual versions work.

### Form fields

**Email capture only: ask for email only.** Adding a first name drops conversions by 10–15%. Adding phone drops it by 30%+. Every extra field has a cost. Only add fields you will actually use to personalize.

---

## 7. Design Principles

**Single focus.** One offer. One CTA. One email field. Every extra element competes with the primary action.

**High contrast CTA button.** The button should be the most visually prominent thing in the popup. Use a color that does not appear anywhere else on the page.

**Whitespace.** Cluttered popups get dismissed. Leave breathing room. Less copy, bigger type, clear visual hierarchy.

**Social proof.** A single data point near the CTA lifts conversions: "Join 6,400 readers" or "Used by 2,000+ freelancers."

**Image direction.** If you use a photo of a person, have them face or look toward the CTA. This is a documented visual attention principle.

**Mobile sizing.** On mobile, the popup should not cover more than 60% of the screen. The close button must be at least 44x44px and visible immediately. Sticky footer bars are safer than modals on mobile.

---

## 8. Email Popup Offers by Business Model

| Offer Type | SaaS | Ecom | Creator / Info | Service / Consulting |
|---|---|---|---|---|
| Discount (10–20% off) | Low fit | High fit | Low fit | Low fit |
| Lead magnet (template, guide, checklist) | High fit | Medium fit | High fit | High fit |
| Free trial or demo | High fit | Low fit | Low fit | Medium fit |
| Free resource (swipe file, calculator) | Medium fit | Low fit | High fit | High fit |
| Waitlist / early access | High fit | Medium fit | High fit | Medium fit |

**Sumo data:** Adding a lead magnet to a popup doubles mobile conversion (3.8% → 7.7%) and desktop conversion (1.8% → 4.7%).

**For solopreneurs specifically:** Lead magnets consistently outperform discounts unless you are in ecom. A checklist, template, or short email course framed as "the thing you need to solve the exact problem this visitor just read about" is the highest-converting offer type for content-driven solopreneurs.

---

## 9. Mobile Popup Compliance

A compliant mobile popup must meet all of these:

- Does not cover full screen on page load from search
- Close button is visible immediately (not delayed, not tiny)
- Close button is at least 44x44px touch target
- The popup is dismissable — no forced engagement
- Does not reappear immediately after being dismissed (use a cookie to suppress for 7–30 days)
- Does not block reading the above-the-fold content on first load

**Recommended mobile approach for solopreneurs:**
1. Sticky footer bar — always visible, low friction, no penalty risk
2. Slide-in after 30 seconds or 70% scroll
3. Exit intent only — fires on back-gesture or tab switch on mobile (tool-dependent)
4. Full-screen modal — desktop only, or returning visitors only

---

## 10. Testing Your Popup

### What to measure

| Metric | Definition | Target |
|---|---|---|
| Impression rate | % of visitors who see the popup | Depends on trigger |
| Conversion rate | % of impressions that opt in | 2–5% average; 5%+ good |
| Dismiss rate | % who close without acting | Below 85% is healthy |
| Subscriber quality | Do they open emails? | Track 30-day open rate |

### What to A/B test (in order)

1. Offer (what you're giving away) — highest impact
2. Headline copy — second highest
3. Trigger timing (5s vs 30s vs exit intent)
4. CTA button copy
5. Design / image

**Minimum sample:** 1,000 impressions per variant before drawing conclusions. Most solopreneurs call tests too early.

### Tools for popup analytics

- **Google Analytics 4:** Custom events for popup open + form submit
- **Hotjar / Microsoft Clarity:** Session recordings to see how visitors interact
- **Your popup tool's native dashboard:** Always check for ghost impressions (bots)

---

## 11. Common Mistakes

**Showing on page load to cold traffic.** The visitor has seen zero content. They have no reason to trust you. Conversion plummets and bounce rate spikes.

**Full-screen modal on mobile.** Annoys visitors, risks Google penalty, kills trust. Never do this for SEO traffic.

**Vague offer.** "Join our newsletter" is not an offer. "Get the free 30-day content calendar template" is.

**Firing on every page every session.** Use suppress cookies. Show once per session or once per 7 days. Repeat triggers destroy trust and inflate impression counts.

**Tiny or hidden close button.** Visitors who can't close a popup don't convert — they leave. Make the close button obvious.

**Too many fields.** Email only for first capture. Every extra field has a measurable conversion cost.

**No mobile testing.** Popup built on desktop, never tested on a real phone. Mobile is often 50–70% of traffic.

**Calling tests too early.** Switching popup copy after 200 impressions is noise, not signal. Wait for at least 1,000 impressions per variant.

**Mismatched offer.** Popup offer has nothing to do with the page content. A visitor reading a blog post about content strategy should not see a popup about pricing. Match offer to page intent.

---

## 12. Contrarian Takes

**Email capture popups are overrated for some solopreneurs.** If your business model is high-ticket consulting or B2B services, email volume matters less than email quality. A popup that captures 500 unqualified subscribers per month is worse than a well-placed opt-in that captures 50 genuinely interested ones. Don't chase list size if you can't monetize it at scale.

**Exit intent still works when the copy is right.** Most solopreneurs write bad exit intent copy, see bad results, and conclude exit popups are dead. Exit intent with a specific, relevant offer (not "wait, don't go!") consistently converts 5–10% of otherwise-lost visitors in 2025. The format is not the problem. The offer is the problem.

**Sticky bars often outperform modals for content sites.** A sticky bar at the top or bottom of the page with a persistent, specific offer converts quietly over time without triggering annoyance. For solopreneurs with strong blog traffic, a sticky bar + inline CTA inside posts often outperforms a modal popup purely because there is no friction or pattern interruption.

**Your popup tool matters less than your offer.** Switching from OptinMonster to ConvertBox will not save a bad offer. The biggest lever is always the specificity and relevance of what you are giving away. Optimize that first.

---

## 13. Tools for Solopreneurs

| Tool | Best For | Pricing (approx) | Notes |
|---|---|---|---|
| **Popup Maker** (WordPress) | WordPress sites, custom builds | Free + paid from $99/yr | Most flexible WP option, developer-friendly |
| **Sumo / BDOW** | Blogs, content sites | Free tier; Pro ~$39/mo | Simple setup, good for beginners |
| **OptinMonster** | Advanced targeting, A/B testing | From $9/mo (basic) to $49/mo | Most powerful targeting rules; better for established sites |
| **ConvertBox** | Personalized overlays, funnels | ~$495 lifetime deal | Excellent for solopreneurs; one-time pricing is rare in this space |
| **Privy** | Shopify stores | Free to $30/mo | Built for ecom; weak outside Shopify |
| **Wisepops** | Clean design, analytics | From $49/mo | Best native analytics; higher price floor |
| **Hello Bar** | Sticky bars, simple popups | Free tier; paid from $29/mo | Great starting point for sticky bars only |

**Solopreneur pick:** ConvertBox (if budget allows for lifetime deal) or Sumo free tier to start. Move to OptinMonster only when you need advanced behavioral targeting.

---

## 14. Quick Wins

These can be implemented today:

1. **Add a lead magnet to your existing popup.** If you show "subscribe for updates," replace it with a specific free resource. Expect 2x conversion lift.
2. **Change trigger from 0s to 30s.** Immediate load popups almost always underperform time-delayed ones. Change the delay first before anything else.
3. **Switch to exit intent on mobile.** Remove mobile modal, add exit intent or sticky footer. Eliminates Google penalty risk immediately.
4. **Write a specific dismiss CTA.** Replace the X button with "No thanks, I don't need more leads." Improves conversion by 5–15% as it reframes the cost of leaving.
5. **Add one social proof data point.** "Join 4,200 readers" next to the CTA button. No design changes required — just add the text.
6. **Suppress for 14 days after dismissal.** If you're showing the same popup to the same person on every visit, fix the suppress cookie setting today.

---

## 15. Related Skills

- **form-cro** — Optimizing embedded forms (not in popups): fields, layout, microcopy, error states
- **page-cro** — Full landing page and homepage conversion audits
- **signup-flow-cro** — Post-click optimization: what happens after they submit the popup form
- **email-sequence** — What to send to new subscribers captured via popup
- **analytics-tracking** — Setting up proper popup event tracking in GA4

---

*Generated using the popup-cro skill from Solopreneur Skills*
