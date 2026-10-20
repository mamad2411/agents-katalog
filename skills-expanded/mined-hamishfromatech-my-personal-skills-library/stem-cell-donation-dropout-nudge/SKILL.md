---
name: stem-cell-donation-dropout-nudge
description: Applies the Japan Marrow Donor Program field experiment (Kato, Ohtake, Kurosawa, Yoshiuchi & Fukuda, JEBO vol. 248, 2026, DOI 10.1016/j.jebo.2026.107666) on reducing donor dropout at the moment of match — where a message emphasizing the limited number of compatible donors per patient increased donor completion of the confirmatory typing stage by 7.3% and increased donor availability for transplantation. Use when [designing retention interventions for high-stakes signup-then-commit funnels (donors, volunteers, mentors, beta testers, open-source contributors), diagnosing why users who already said yes fail to complete the next step, or deciding when an informational message outperforms no message]. NOT for [initial recruitment (the intervention operates on the already-registered), health/donation compliance policy per se, or low-commitment engagement nudges where the marginal cost of one more user is trivial].
---

# Stem-Cell Donation Dropout Nudge: Framing Scarcity at the Matching Moment

## Overview
Registered potential donors in stem-cell transplantation sometimes refuse to donate when matched with patients, causing supply shortages. Kato, Ohtake, Kurosawa, Yoshiuchi & Fukuda ran a field experiment with the Japan Marrow Donor Program: when a donor is matched with a patient, the program sends a letter; the experiment varied which behavioral message was added. The winning message emphasized that each patient has a *limited number of compatible donors* — a scarcity/expected-value frame, not a moral appeal — and raised the probability of donors completing the confirmatory typing stage by 7.3%. This is the rare mechanism family where an *informational* nudge outperforms both moral appeals and no message, precisely because the commitment is high-cost and the decision is made once.

## The Evidence Base
- **Kato, Hiroki; Ohtake, Fumio; Kurosawa, Saiko; Yoshiuchi, Kazuhiro; Fukuda, Takahiro** — "Exploring information provision to promote stem cell donation: Evidence from a field experiment of the Japan Marrow Donor Program," *Journal of Economic Behavior & Organization* vol. 248 (2026), DOI 10.1016/j.jebo.2026.107666.
- **Setting:** Registered donors already in the system — the marginal decision happens at the matching letter, not at signup.
- **Headline result:** the scarcity message ("limited number of compatible donors per patient") increased the probability of completing confirmatory typing by **7.3%**, which in turn increases donor availability for transplantation (physicians choose the best donor among those who complete confirmatory typing).
- **Contrast with the information penalty:** the library's `reminder-wtp-information-penalty` skill (Barron/Damgaard/Gravert) showed that *adding health information to a reminder reduced both adherence and WTP*. This study shows the boundary case: informational framing that communicates **decision-relevant consequences** (your choice uniquely matters) works where informational framing that adds *cognitive processing burden* (instructions, education) destroys value.
- **JEL codes:** D64 (altruism/philanthropy), D90, H41 (public goods), I11 (health).

## Core Findings (the three rules)
1. **Intervene at the commitment moment, not the signup moment.** The binding constraint was not recruiting registrants — it was the small fraction who refuse when actually matched. Put the nudge where the expensive decision is made.
2. **Scarcity framing beats moral framing for high-stakes, one-shot commitments.** "You are one of few compatible donors" supplies a concrete reason the decision matters; "please help save a life" asks for the same sacrifice with no new information.
3. **Information is not always a penalty — clarify when the information changes the perceived payoff.** The library's information-penalty rule applies to reminders where information adds processing cost; scarcity information here changes the *benefit* side of the decision. Diagnose which: does the added content make the choice feel larger (helps) or heavier (hurts)?

## When to Use
- Retention of already-committed contributors in open-source projects (sustaining a library you depend on; "you are one of three maintainers capable of this fix").
- High-cost volunteer programs (mentors, moderators, on-call rotation, peer reviewers).
- Donor/volunteer products where the signup→action gap is the bottleneck.
- Any funnel with a low-cost opt-in followed by a high-cost fulfillment step.

## NOT For
- Initial recruitment (the mechanism is dropout, not acquisition).
- Cheap, repeatable actions where moral appeals or reminders work fine.
- Scarcity framing used manipulatively for commercial products (this is a public-health / public-good intervention pattern).

## Core Process / Workflow
1. **Map the commitment funnel.** Identify the exact step where cost spikes (matching → confirmatory typing; contributor onboarding → first real PR; signup → payment).
2. **Diagnose dropout cause at that step.** Is it perceived cost, perceived non-uniqueness ("someone else will do it"), or ambiguity about what happens next? The nudge works only if the binding constraint is the last two.
3. **Choose the message class.** Scarcity/unique-role framing for high-stakes one-shot commitments; keep content minimal (the informational-penalty rule still applies to instructions bundled into the same message).
4. **Deliver through the existing channel.** This study's intervention was a message added to a letter the program already sends — zero additional contact, minimal cost.
5. **Measure the completion stage, not the intermediate metric.** Adoption of confirmatory typing is the proximate outcome; donor *availability for transplantation* is the real outcome.
6. **Pre-commit the ethics check.** Scarcity framing must be factually accurate — "limited number of compatible donors" is a medical truth, not manufactured urgency.

## A-Tech Alignment
- **Open source:** the "you are one of few compatible maintainers" framing is the donor-scarcity mechanism applied to the bus-factor-1 problem; complements `oss-endowment-and-coop-funding-2026` (structural) with a behavioral layer.
- **Privacy:** N/A — flagged honestly; the intervention is a letter, not a data product.
- **Financial freedom:** the same scarcity framing maps to time-bank and mentorship economics (per-hour value of expertise rises with scarcity of that expertise).
- **Practical:** one-page message template + funnel-mapping worksheet.

## References
- Pairs with: `reminder-wtp-information-penalty` (when does information help vs hurt), `nudge-complementarity-benefit-cost` (pairing benefit and cost nudges), `nudge-history-reactance` (do not nudge the already-converted), `belief-profile-targeting-rct` (friction-type → intervention-type map), `nudge-effectiveness-reality-check` (small-effects calibration).