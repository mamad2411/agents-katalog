---
name: profile-converter
description: Audits and optimizes a LinkedIn profile to turn views into booked calls. Use whenever the user wants to audit, review, optimize, or rewrite a LinkedIn profile or any part of it — headline, banner, About section, featured section, profile photo, CTAs, skills, or SSI/engagement metrics. Triggers include "audit my LinkedIn", "optimize my profile", "rewrite my headline", "fix my About section", "what should my banner say", "score my profile", "improve my SSI". Produces a scored audit, rewritten copy in the user's voice, and a 30-60-90 action plan.
---

# Profile Converter

Make a LinkedIn profile a conversion asset, not a résumé. Every time someone sees a post → checks the profile → reads the headline → gets a DM, they should think the same thing: *this person solves my problem.* This is the profile arm of the LinkedIn Operator.

## Step 0 — Load context (always)
Read `CLIENT_CONTEXT.md` at the plugin root first — inherit ICP, offer, proof, named mechanism, and voice. All rewritten copy must use it. If unfilled, ask for the ICP, the offer, and the headline outcome before rewriting.

## Two modes (often used together)
1. **Audit** — score the profile element-by-element, surface quick wins, give a 30-60-90 plan.
2. **Rewrite** — produce ready-to-paste copy for any element in the user's voice.

## Reading the profile
If the user pastes their profile text or screenshots, work from that. If they want a live read and browser tools are available, use the Chrome extension (`mcp__Claude_in_Chrome__*`) to navigate to the `linkedin.com/in/` page and read it; otherwise ask them to paste each section. Sections to cover: photo, banner, headline, About, custom URL, experience, skills/endorsements, recommendations, featured, activity, followers/connections.

## The money formulas (use these for rewrites)

**Headline (the ULTIMATE formula):**
- Hyper-targeted: `I help [ICP] achieve [specific outcome] in [timeframe] with [unique mechanism] ([guarantee — optional])`
- Broad: `Achieve [specific outcome] with [unique mechanism]`
- Append accolades after the promise ("Generated $2M+ for clients", "Forbes 30u30").

**About section (a short-form sales letter):**
1. Pattern interrupt: "[ICP] generating less than [outcome]? Here's why 👇"
2. Credibility: "I've helped X [ICPs] achieve [result] in [timeframe]"
3. Pain recognition: "If you're like most [ICP]: [pain 1] / [pain 2] / [pain 3]"
4. Solution bridge: "Here's what makes us different: [named mechanism in 2–3 sentences]"
5. Proof: "Recent results: Client A [result], B [result], C [result]"
6. CTA: "Ready to [outcome]? DM me '[TRIGGER]' for [next step]"

**Banner (1584×396):** branded, value-prop text, social proof, a CTA. Uncluttered, no tiny text. Build in Canva.
**Featured:** 3–6 magnetic items — lead magnet, case studies, VSL, booking link.
**CTAs (layer them):** custom profile button + banner CTA + About CTA + Featured CTAs, capturing prospects at every level.

Full templates, creator examples, and creator headline patterns are in `references/profile-formulas.md`.

## Audit flow
Score each element with `references/scoring-framework.md`, compute the two mandatory metrics, then write the report.
- **Engagement rate** = (reactions + comments + shares) / impressions × 100. B2B target 3%+.
- **SSI** target 70+ (have them check linkedin.com/sales/ssi, or estimate).
Benchmarks by industry, format, and follower count are in `references/metrics-benchmarks.md`.

## Audit report structure (use `assets/audit-report-template.md`)
1. Executive summary 2. Classification (industry / profile type / audience) 3. Scorecard 4. Calculated metrics 5. Element-by-element analysis 6. Quick wins (high impact, low effort) 7. Strategic recommendations 8. 30-60-90 day action plan.

## Output format
For an **audit**: deliver the full report, lead with the 3 highest-leverage quick wins.
For a **rewrite**: give the ready-to-paste copy, then 1–2 alternatives, then one line on why it converts.
After delivering, offer: "Want me to rewrite the next element, or build the 30-60-90 plan into a tracker?"

## References
- `references/profile-formulas.md` — headline/About/banner/featured/CTA templates + creator examples.
- `references/scoring-framework.md` — element-by-element scoring criteria and weights.
- `references/metrics-benchmarks.md` — SSI, engagement, growth, format, and industry benchmarks.
- `assets/audit-report-template.md` — full audit report + 30-60-90 plan template.
