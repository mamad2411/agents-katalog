---
name: aigov-use-case-triage
version: 1.0.0
description: Rapidly triage a proposed AI use case into a risk tier and a route (approve / conditions / assess further / prohibit) so teams know how much scrutiny it needs.
author: matrixx0070
tags: [ai-governance, risk-triage, eu-ai-act, nist-ai-rmf, compliance, intake]
capabilities: []
---

## When to use

Use this at first contact with a proposed or in-flight AI use case — an intake form, a new vendor pilot, an internal build request — when you need a fast, defensible sort before committing deeper effort. It answers one question: how much scrutiny does this deserve? The output routes the case to approve, approve-with-conditions, assess-further, or prohibit, and decides whether a full impact assessment is warranted.

**Not for:** the deep assessment itself once triage says "assess further" (use aigov-aia-generation), reviewing a vendor's contract and DPA (use aigov-vendor-ai-review), building the register of what you already run (use aigov-ai-inventory), mapping regulatory obligations to controls (use aigov-reg-gap-analysis), first-time scoping interviews (use aigov-cold-start-interview), or standing up policy (use aigov-policy-starter).

This skill is decision-support, not legal advice. Triage is a screening judgment; any high-stakes or rights-affecting use case, any "prohibited?" call, and anything to be relied on or filed must be reviewed by a qualified attorney before you act on it.

## Method

1. Capture the case in one line: what the system does, who/what it acts on, the decision or output it produces, and whether a human is meaningfully in the loop.
2. Screen for prohibited practices first (EU AI Act Article 5 — social scoring, subliminal/manipulative techniques, exploitation of vulnerabilities, untargeted facial-image scraping, most real-time remote biometric ID in public, emotion recognition in workplace/education, certain predictive policing/biometric categorization). A hit stops triage.
3. Screen for high-risk categories: Annex III domains plus safety-component/regulated-product uses. **Decision:** any match, or any decision that materially affects a person's rights, safety, access, or livelihood → route to assess-further and trigger aigov-aia-generation.
4. If not high-risk, screen for limited-risk transparency duties (chatbots, AI-generated or manipulated content / deepfakes, emotion/biometric categorization outside prohibited contexts).
5. Otherwise classify minimal-risk. **Decision:** minimal-risk with no sensitive data and no automated adverse decision → approve or approve-with-conditions.
6. Map the case to NIST AI RMF MAP (context, purpose, affected people, benefits/harms) to record why the tier fits.
7. Emit tier + route + rationale + the one condition or next step that unblocks it, and flag every uncertainty for attorney review.

## Example

Intake: "HR wants a tool that screens résumés and ranks candidates for recruiters."

Step 2: not a prohibited practice. Step 3: employment/recruitment is Annex III high-risk, and it affects access to livelihood. **Route: assess-further → high-risk.** MAP note: affected people = applicants (including protected classes); primary harm = discriminatory filtering; human-in-loop = recruiter reviews shortlist but relies on the ranking. Trigger aigov-aia-generation; require bias testing and a vendor conformity/role check; escalate the "is the recruiter review meaningful oversight?" question to attorney.

## Pitfalls

- **Skipping the prohibited screen.** A limited-risk-looking chatbot that does emotion recognition on employees is a prohibited use — always run Article 5 first.
- **"Human in the loop" as a free pass.** Rubber-stamp review does not downgrade a high-risk decision; oversight must be able to override in practice.
- **Triaging the vendor's marketing, not the actual use.** Tier the concrete decision the system drives in your context, not the product category.
- **Treating triage as the assessment.** This is the fast sort; a "high-risk" or "prohibited?" result is the start of real work and attorney review, not the end.

## Output format

```
AI USE-CASE TRIAGE (decision-support, not legal advice) — <case> — <date>
ONE-LINER: does <what> to <whom>, produces <decision/output>, human-in-loop=<yes/no/rubber-stamp>

TIER: prohibited | high-risk | limited-risk | minimal-risk
BASIS: <EU AI Act Art.5 / Annex III domain / transparency Art.50 / none>
NIST MAP: context=<> affected=<> primary-harm=<>

ROUTE: approve | approve-with-conditions | assess-further | prohibit
CONDITION / NEXT STEP: <the one thing that unblocks or the AIA trigger>
FULL AIA REQUIRED: yes/no  ->  aigov-aia-generation

ATTORNEY ESCALATION: <rights-affecting / prohibited-call / uncertain items>
UNVERIFIED: <assumptions to confirm>
```

## Reference

Triage rests on the EU AI Act's risk-tier architecture, cross-checked with NIST AI RMF MAP. Tiers below are the current framework as commonly summarized; article numbers and Annex contents change, so confirm the operative text with counsel before relying on a tier.

### EU AI Act risk tiers (the triage backbone)

| Tier | What it covers | Consequence |
|------|----------------|-------------|
| **Prohibited** (Art. 5) | Unacceptable-risk practices — banned outright | Do not deploy; escalate immediately |
| **High-risk** (Art. 6 + Annex III / safety components) | Systems posing significant risk to health, safety, or fundamental rights | Conformity assessment, risk mgmt, data governance, logging, human oversight, transparency, accuracy/robustness |
| **Limited-risk** (Art. 50) | Interaction/content systems | Transparency/disclosure obligations only |
| **Minimal-risk** | Everything else | No mandated obligations; voluntary codes |

### Prohibited practices (Article 5) — a hit stops triage

- Subliminal, manipulative, or deceptive techniques that distort behavior and cause harm.
- Exploiting vulnerabilities (age, disability, socio-economic situation).
- Social scoring by public or private actors leading to detrimental/unjustified treatment.
- Untargeted scraping of facial images to build recognition databases.
- Emotion recognition in the workplace and education (narrow exceptions for safety/medical).
- Biometric categorization inferring sensitive attributes (race, political/religious/union status, sexual orientation).
- Real-time remote biometric identification in public spaces for law enforcement (narrow, authorized exceptions).
- Certain individual predictive policing based solely on profiling.

### High-risk categories (Annex III domains)

| # | Domain | Typical use |
|---|--------|-------------|
| 1 | Biometrics | Remote/post biometric ID, categorization, emotion recognition (where not prohibited) |
| 2 | Critical infrastructure | Safety of traffic, water, gas, electricity, digital infrastructure |
| 3 | Education & vocational training | Admissions, scoring, proctoring, assessment |
| 4 | Employment & worker management | Recruitment, screening, promotion, termination, task allocation |
| 5 | Essential services | Credit scoring, insurance risk/pricing, access to public benefits, emergency dispatch |
| 6 | Law enforcement | Risk assessment, evidence reliability, profiling |
| 7 | Migration, asylum, border control | Risk assessment, visa/application examination |
| 8 | Justice & democratic processes | Assisting judicial decisions, influencing elections |

Also high-risk: AI that is a safety component of, or is itself, a product under EU harmonization law requiring third-party conformity assessment.

### Limited-risk transparency (Article 50)

Disclose when a person interacts with an AI system (chatbots), and label AI-generated or manipulated content (deepfakes, synthetic media). Emotion-recognition and biometric-categorization subjects must be informed. These are disclosure duties, not full-conformity obligations.

### Triage decision rubric

```
Art. 5 prohibited practice?          -> PROHIBIT (attorney)
  else Annex III / safety component
       OR rights/safety/livelihood-affecting decision?  -> ASSESS-FURTHER (high-risk, AIA + attorney)
  else interaction/synthetic content? -> LIMITED-RISK (transparency conditions)
  else                                -> MINIMAL-RISK (approve / conditions)
```

### Mapping to NIST AI RMF MAP

MAP is the RMF function that establishes context before you measure or manage. In triage, record: (1) intended purpose and deployment context, (2) affected individuals/groups and their vulnerability, (3) categorized benefits and potential harms, (4) whether human oversight can meaningfully intervene. A well-populated MAP is the evidence trail that justifies the assigned tier and feeds directly into a full aigov-aia-generation if the route is assess-further.

### Escalation rule

High-stakes or rights-affecting decisions — anything touching employment, credit, benefits, health, safety, law enforcement, or a prohibited-practice question — escalate to a qualified attorney and route to a full algorithmic-impact assessment. Triage narrows scrutiny; it never substitutes for legal review on the cases that carry legal stakes.
