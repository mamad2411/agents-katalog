---
name: digital-nudges-nag-whatsapp-backfire
description: Applies the World Bank's "When Digital Nudges Nag" RCT (Urbina Florez, Moya & Rozo, PRWP 11423, June 2026; preregistered AEARCTR-0008672; N=1,375 Venezuelan migrants in Colombia) — the first field-RCT to show informational nudges can ACTIVELY REDUCE program take-up (−8pp, a 15% decline) through two distinct backfire channels. Use when designing digital outreach campaigns, deciding whether to send how-to content to a user list, setting contact cadence for onboarding reminders, or auditing whether an engagement nudge might be suppressing conversions. NOT for general reminder design when the nudge is purely attentional (see reminder-wtp-information-penalty) or for reactance among already-converted users (see nudge-history-reactance).
---

# When Digital Nudges Nag: The Take-Up Backfire

## Overview
The assumption "a well-designed informational nudge is, at worst, neutral" is now empirically falsified. Moya, Rozo & Urbina randomized 1,375 undocumented Venezuelan migrants eligible for Colombia's ETPV regularization program into three video treatments (awareness / trust / step-by-step) or control, delivered via WhatsApp. **Receiving any video reduced take-up by 8 percentage points — a 15% decline relative to the 54% control mean.** This is the first RCT-grade evidence that informational nudges delivered through an unsolicited digital channel can backfire, and it maps the exact mechanism boundary every product, campaign, and public-program team needs.

## When to Use
- Deciding whether to send educational/how-to content to users who did NOT ask for it
- Designing onboarding, enrollment, or adoption campaigns for digital products or social programs
- Diagnosing why an outreach intervention failed or underperformed
- Choosing message depth for a vulnerable or low-bandwidth audience
- NOT for designing the reminder's timing/format when content is not the question
- NOT for in-person or opt-in channels where unsolicited-contact friction does not apply

## Core Process / Workflow
1. **Diagnose the two backfire channels before shipping**: (a) *Information backfire* — among the ~72% who engaged (compliers), watching the video REDUCED take-up by 9.5pp (LATE estimate); detailed procedural content RAISED perceived complexity and hassle costs; the step-by-step video produced the LARGEST harm (−11.7pp PPT requests) while the awareness video hurt least. (b) *Contact friction* — among the ~28% who never watched (defiers), assignment alone reduced take-up by ~4.3pp; qualitative interviews with 30 non-engagers cite frustration with repeated contact, access difficulty, and digital-tool unfamiliarity.
2. **Identify the margin population**: endogenous stratification (Abadie 2002 / Chernozhukov et al. 2018) shows negative effects concentrate in the MIDDLE tercile of predicted take-up (−11.9pp, a 21% decline) — the intervention hit hardest precisely for individuals closest to acting voluntarily. Low-propensity and high-propensity groups were largely unaffected.
3. **Simplify rather than expand**: the actionable rule — "digital outreach at scale may be most effective when it reduces procedural burdens rather than expanding informational content." Adding procedural detail can convert an interested user into a defector by making the perceived cost legible.
4. **Pre-register the backfire test**: the paper's honest channel decomposition (ITT = complier effect + defier effect) requires a clean control group, an engagement measure, and an instrument (assignment) — a design any product team can approximate with holdout groups and engagement telemetry.
5. **Watch the first contact**: negative effects emerge IMMEDIATELY at first exposure (PPT requests −9.4pp, a 34% relative decline) — this is not fatigue from repeated contact; the harm occurs on contact 1.

## Key Evidence
- Take-up (request/attend biometric appointment): −8.0pp (p<.05) vs 54% control = −15%
- Registration initiation: −7.7pp; intention to register: −12.2pp (−15%)
- LATE (watching, compliers): −9.5pp (−16% vs control mean); Defier residual effect: −4.3pp across 28.2% of treated
- Effects largest in middle tercile of predicted take-up: −11.9pp (21% decline)
- Qualitative: 30 non-engager interviews confirm contact-friction mechanism
- Both channels operate simultaneously — content complexity AND unsolicited-contact friction

## Pairs with
`reminder-wtp-information-penalty` (the information-penalty boundary: this is its most extreme negative datapoint — adding health info reduced adherence/WTP; here, adding procedure info reduced take-up), `nudge-history-reactance` (contact friction among the converted), `nudge-complementarity-benefit-cost` (the super-additive positive counterpart), `co-designed-digital-nudging` (design alternative to reduce contact friction), `behavioral-intervention-choice-tailoring` (the mechanism for WHY choice-based interventions work — autonomy without imposed contact), `nudge-effectiveness-reality-check`, `consent-fatigue-progressive-permissioning` (the consent-side of unsolicited contact), `youth-financial-education-nudge-rct` (engagement-vs-behavior divergence).

## A-Tech Alignment
- **Open source**: World Bank Policy Research Working Paper 11423, public reproducibility package; two-channel decomposition replicable in any product telemetry stack.
- **Privacy**: the intervention operated on first-party contact lists; the defier channel shows contact itself is a consent-bearing surface, not just content.
- **Financial freedom**: the defier channel (28% of treated) quantifies the cost of "spray-and-pray" messaging — for any product where contact = spam, the wrong nudge is a churn lever, not a neutral act.
- **Practical**: two-channel diagnostic (complier vs defier decomposition) is immediately implementable in any A/B testing stack.

*Source: Moya, A., Rozo, S.V. & Urbina, M.J., "When Digital Nudges Nag: Evidence on Program Take-up from a WhatsApp Intervention," World Bank Policy Research Working Paper 11423, June 2026 (PRWP 11423).*