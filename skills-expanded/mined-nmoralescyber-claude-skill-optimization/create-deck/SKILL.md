---
name: create-deck
description: Generates tailored sales, investor, or customer presentation decks from your deal/audience context. Make sure to use this skill whenever the user says build a deck for [prospect/audience], create a sales deck, make an investor deck, draft a presentation for [meeting], pitch deck for [scenario], demo deck for [customer], or describes wanting a multi-slide presentation tied to a specific business context. Adapts depth and structure to audience (technical vs. business, prospect vs. investor vs. existing customer). For cybersecurity products, includes trust-signal slides, threat-landscape framing, technical architecture without over-explaining, and ROI/risk-reduction quantification. Do NOT use for: single-page sales collateral (use create-one-pager), prospect landing pages (use create-landing-page), screencast/walkthrough scripts (use create-workflow-demo), or content marketing decks like webinars (use marketing:draft-content). Defining characteristic: "multi-slide presentation, given live or async, anchored to a specific audience and meeting."
---

# Create Deck

Tailored multi-slide presentations for sales, investor, and customer meetings.

## When to use vs. adjacent asset skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Building a multi-slide presentation | Single-page handout → `create-one-pager` |
| Anchored to a specific meeting/audience | Self-serve prospect landing page → `create-landing-page` |
| Will be presented live or shared async | Screencast / walkthrough script → `create-workflow-demo` |
| Sales / investor / customer context | Webinar or content marketing → `marketing:draft-content` |

## Deck types this skill handles

### Sales deck (prospect-facing, mid-funnel)
Audience: a named prospect or ICP segment evaluating purchase.

Standard structure (10-15 slides):
1. Cover — prospect logo + your logo + meeting context
2. Their world — research-grounded statement of their context (proves you did homework)
3. The problem — specific to their context, not generic
4. The cost of inaction — quantified if possible
5. Your category position — what space you play in (sentence, not paragraph)
6. How you solve it — 3 capabilities maximum, each with proof
7. Customer evidence — 2-3 customers like them with quantified outcomes
8. Differentiation — vs. their likely alternatives (NOT a feature matrix, a positioning summary)
9. Pricing model overview — be transparent about how pricing works
10. ROI / value framing — payback period or cost-of-issue avoided
11. Implementation overview — week-by-week so they see it's not 6 months
12. Next steps — specific calendar action

### Investor deck (fundraising)
Audience: VCs/angels evaluating an investment.

Standard structure (10-15 slides for seed/Series A; less for pre-seed, more for later rounds):
1. Cover — company + tagline + ask amount + round
2. The problem — large, specific, growing
3. Why now — what's changed in the world that makes this winnable
4. Your solution — 1 sentence + visual
5. How it works — 1 slide, 3-step max
6. Market — TAM/SAM/SOM if requested, but better: "here's our beachhead and adjacent markets"
7. Traction — revenue, customers, growth rate, retention (or for pre-revenue: design partners, LOIs, technical milestones)
8. Business model — how you make money + unit economics
9. Competition — honest map, where you win, where you don't
10. Team — why this team for this problem
11. Roadmap / use of funds — what 18 months of runway buys
12. The ask — amount, structure, what you want from investors beyond capital

### Customer / strategic-account deck (existing customer, expansion or QBR)
Audience: existing customer in an expansion or quarterly business review.

Standard structure (8-12 slides):
1. Cover — both logos + period + meeting purpose
2. Outcomes delivered last quarter (quantified, owned by you)
3. Their KPIs / how you contributed
4. Roadmap from your side — what's coming that benefits them
5. Their roadmap — what they shared, how you align
6. Expansion opportunities — modules, seats, adjacent use cases
7. Health check — utilization, satisfaction, risks
8. Asks (if any) — referrals, case study permission, intros
9. Next steps + commitments

### Cybersecurity-specific overlay (apply to any of the above)

For security/cybersec products, layer in these slide patterns:

- **Threat-landscape framing slide** — establishes "why this matters now" with current attack data (citing real incidents in their industry, e.g., "3 healthcare networks breached this quarter via [vector]")
- **Trust-signals row** — SOC 2, ISO 27001, customer logos in regulated industries, named security advisors, known investors
- **Architecture slide** — technical depth without overwhelming; for technical buyers (CISO/security eng) include data flow, encryption layers, deployment options. For business buyers (CFO, CIO) keep abstract.
- **ROI framing for security** — translate to one of: cost of breach avoided ($4.45M average per IBM/Ponemon), regulatory penalty avoided, audit cost reduction, cyber-insurance premium reduction
- **Compliance mapping** — which framework controls your product satisfies (SOC 2 CC6.1, HIPAA §164.312(a)(2)(i), PCI 8.3, etc.)
- **Pen test / vuln disclosure** — show your security posture matches what you're selling
- **Customer story** — case study from a customer with similar threat profile and similar regulatory burden

## Anti-patterns (especially for security products)

- **Fear-only selling** — pure FUD turns off sophisticated buyers; lead with specificity, not panic
- **Feature catalogs** — 8 capabilities each with 6 sub-bullets; nobody reads it
- **Architecture slides for non-technical audiences** — kills momentum
- **Overpromising compliance** — saying "HIPAA compliant" when you mean "supports HIPAA workflows"
- **Logo soup** — 24 customer logos arranged on a slide. Pick 3-5 in the prospect's industry instead
- **Demo as deck** — if it can be shown live, show it; don't put 6 slides of UI screenshots
- **Burying the ask** — sales meeting? Specific next-step calendar action on a final slide. Investor meeting? Round size and structure on slide 1 or 2

## Research before drafting

Before generating a deck, gather:
1. Audience identity (named individuals if possible, role descriptions if not)
2. Meeting context (length, format, what they expect)
3. Prior interactions / what they already know
4. Their language — pull from their site, recent posts, earnings calls if public
5. The one decision you want them to make at the end

If any of these is unknown, ASK before drafting. A deck without a target decision is a brochure.

## Output

Produces:
1. The deck content in markdown (one section per slide with title, key points, speaker notes)
2. Slide-by-slide design intent (which slides need data viz, which need imagery, which are text-heavy)
3. Optional: HTML or .pptx-ready version (chains to anthropic-skills:pptx)
4. Speaker notes appropriate to the meeting format
5. Suggested follow-up artifact (often a one-pager — chains to `create-one-pager`)
