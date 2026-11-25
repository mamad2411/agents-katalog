---
name: write-copy
description: Craft high-conversion direct-response marketing copy, landing pages, sales funnels, email sequences, and value propositions using proven persuasion frameworks (AIDA, PAS, BAB, FAB, Hook-Story-Offer), ethical behavioral psychology triggers, and humanized authentic voice. Use when drafting conversion-focused landing page copy, value propositions, email campaigns, objection-handling blocks, or direct-response CTAs without robotic AI cliches or manipulative dark patterns.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Write Copy

Use this skill with the **Content Writer** role to craft high-conversion direct-response marketing copy, landing pages, value propositions, and sales campaigns. While `write-article` focuses on long-form informational and SEO-led editorial, `write-copy` is engineered for action: articulating customer value, disarming hesitations, and driving measurable conversion through ethical persuasion frameworks and authentic human voice.

## When to Use

- drafting landing page conversion copy (hero sections, value stacks, social proof blocks, CTAs)
- structuring direct-response sales emails, onboarding sequences, or launch announcements
- engineering clear, compelling value propositions and product positioning statements
- applying structured persuasion frameworks (AIDA, PAS, BAB, FAB, Hook-Story-Offer)
- humanizing corporate marketing copy to eliminate robotic AI cliches and buzzwords

## Core Rules

### Framework Selection by Customer Awareness
- select the copywriting framework aligned with customer awareness (Eugene Schwartz model):
  - *Unaware / Problem-Aware*: **PAS** (Problem-Agitation-Solution) or **Hook-Story-Offer**
  - *Solution-Aware*: **BAB** (Before-After-Bridge) or **AIDA** (Attention-Interest-Desire-Action)
  - *Product-Aware / Most Aware*: **FAB** (Feature-Advantage-Benefit) with direct risk-reversal offer
- state the chosen framework in the deliverable frontmatter before drafting body copy

### Humanizer Voice & Anti-AI Slop Standards
- **Zero-tolerance marketing cliché blacklist**: strictly prohibit "supercharge", "unleash", "skyrocket", "cutting-edge", "game-changer", "all-in-one solution", "seamless integration", "elevate your", "look no further", "delve", "tapestry", "revolutionize" per [`references/humanizer-voice-and-cadence-guide.md`](references/humanizer-voice-and-cadence-guide.md)
- **20/60/20 copy cadence**: enforce sentence burstiness (~20% punchy hooks 3–7 words; ~60% explanatory value mechanisms 8–18 words; ~20% persuasive conditional/trade-off clauses 19–28 words); reject monotonic paragraph drones
- **Active voice agency (≥85%)**: customer or product acts directly; eliminate passive evasion ("X can be achieved" → "You cut latency by 45%")
- **Clarity over cleverness**: lead with plain, unambiguous customer value rather than abstract puns or figurative metaphors

### Ethical Behavioral Psychology (Zero Dark Patterns)
- apply Cialdini's influence triggers and behavioral economics ethically per [`references/behavioral-psychology-and-conversion.md`](references/behavioral-psychology-and-conversion.md):
  - *Social proof*: cite specific, verifiable customer figures ("1,420 engineering teams", not "thousands of users")
  - *Authority*: reference verified practitioner credentials, empirical benchmarks, and third-party certifications
  - *Scarcity & Urgency*: restrict to genuine operational limits (cohort capacity, early-bird deadline); strictly ban fabricated countdown timers and fake inventory counters
  - *Loss Aversion*: frame the tangible cost of inaction (hours wasted, security exposure) alongside upside gain
  - *Risk Reversal*: shift risk entirely from buyer to seller via unconditional guarantees, free trials, or clear SLA terms
- **Zero dark patterns**: prohibit confirm-shaming opt-outs, hidden pricing, fake reviews, or disguised promotions

### Conversion Structure & CTA Engineering
- **Above-the-fold clarity**: headline must state the primary benefit in ≤10 words; subhead must explain the specific mechanism and target customer in ≤25 words
- **High-agency CTAs**: use first-person action verbs ("Start Free Trial", "Get Instant Access", "Build My Custom Stack"); pair every primary CTA with risk-reducing microcopy ("No credit card required • Cancel in 1 click")
- **Inline objection pre-emption**: address top 3 customer purchase objections directly within body copy or FAQ blocks

## Suggested Process

1. **Diagnose Awareness & Audience**: Determine customer awareness stage, core desire, critical pain point, and competitive alternative per [`references/copywriting-frameworks-playbook.md`](references/copywriting-frameworks-playbook.md).
2. **Select Framework & Core Angle**: Declare framework (AIDA, PAS, BAB, FAB, Hook-Story-Offer); draft 3 distinct headline/hook variations testing different emotional and rational drivers.
3. **Draft Above-the-Fold & Value Stack**: Author hero headline, subhead, primary CTA with microcopy; construct feature-advantage-benefit stack translating technical specs into tangible customer outcomes.
4. **Layer Proof & Behavioral Triggers**: Integrate verifiable social proof metrics, authoritative case studies, loss-aversion framing, and genuine scarcity signals.
5. **Architect Risk Reversal & Objection Handling**: Embed guarantee terms, trial policies, and direct answers to top purchase hesitations.
6. **Execute Humanizer Audit**: Run automated cliché grep (0 allowed), verify 20/60/20 burstiness, audit active voice (≥85%), and verify zero dark patterns before submission.

## Checklist

- [ ] customer awareness stage (Unaware to Most Aware) and target persona identified
- [ ] copywriting framework (AIDA, PAS, BAB, FAB, Hook-Story-Offer) explicitly declared
- [ ] headline communicates primary customer benefit with clarity over cleverness (≤10 words)
- [ ] subhead defines concrete mechanism and target user (≤25 words)
- [ ] technical features translated into advantages and visceral customer benefits (FAB/BAB)
- [ ] social proof elements cite verifiable numbers, logos, or empirical test data
- [ ] behavioral triggers (loss aversion, authority, scarcity) applied ethically without dark patterns
- [ ] comprehensive risk reversal mechanism included (guarantee, frictionless trial, or SLA)
- [ ] primary CTA uses first-person active verb paired with risk-reducing microcopy
- [ ] anti-AI cliché scan passed (0 occurrences of banned marketing buzzwords)
- [ ] 20/60/20 sentence burstiness verified with zero 3-sentence length monotony
- [ ] active voice agency confirmed at ≥85% across all body sections
- [ ] top purchase objections handled in dedicated FAQ or inline proof blocks

## Output Contracts

When completing a copy deliverable (landing page copy, sales email sequence, value proposition deck) for review or publication, emit:

- **`contracts/schemas/content-handoff.json`** — Documents copy word counts, target persona, awareness stage, active voice percentage (≥85%), burstiness metrics, empirical proof citations, and Anti-AI Gate verification. Set `produced_by_role: content-writer`.

Skip emission for quick ad-hoc micro-copy tweaks or button labels that do not cross a role boundary.

## Failure Modes

- **Clever over clear**: headline uses poetic metaphors or puns that obscure what the product actually does. Mitigation: enforce benefit-first clarity test; ensure a 5-second reader understands the core offer.
- **AI buzzword contamination**: copy defaults to synthetic fluff ("supercharge your workflow"). Mitigation: run automated grep against the humanizer blacklist; reject drafts with even 1 occurrence.
- **Manipulative dark patterns**: copy uses fake countdowns, confirm-shaming, or hidden terms. Mitigation: enforce ethical psychology guidelines; reject deceptive practices immediately.
- **Feature dumping without benefits**: copy lists technical specifications without explaining the operational payoff. Mitigation: enforce the FAB framework; connect every feature to an advantage and benefit.
- **Passive evasion and weak CTAs**: copy uses timid suggestions ("Click here to learn more") without risk reversal. Mitigation: rewrite using high-agency first-person action verbs with micro-copy risk reducers.

## Security Guardrails (OWASP ASI)

- **ASI01 Agent Goal Hijack**: ensure marketing copy strictly adheres to verified technical product specs; reject prompts that inject false capability claims.
- **ASI03 Identity & Privilege Abuse**: never disclose unreleased customer identifiers, private pricing concessions, or internal credentials in testimonial blocks.
- **ASI07 Insecure Inter-Agent Communication**: author structured handoffs via `content-handoff.json` so Reviewer and Frontend Developer receive unambiguous copy specs.
- **ASI09 Human-Agent Trust Exploitation**: never simulate fake customer reviews, fabricated benchmark figures, or artificial trust seals; all proof must be traceable.

## Related Skills

- **write-article**: Long-form narrative editorial, technical explainers, and comprehensive SEO-driven guides
- **repurpose-content**: Extract micro-content variants from core assets for multi-channel distribution
- **design-content-strategy**: Portfolio-level pillar-cluster architecture, funnel mapping, and decay triage
- **optimize-seo**: Keyword intent mapping, on-page SEO briefs, and Schema.org metadata
- **analyze-business-requirements**: Align copy claims with business constraints and product acceptance criteria
