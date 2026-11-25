---
name: beta-testing-plan-creator
description: |
  Designs phased beta testing programs with recruitment tiers, instrumentation,
  a weighted Beta Scorecard, and a go/no-go decision framework. Use when users
  say "plan a beta for our new feature", "design a closed beta program", "how
  do I structure a private beta", or "set up beta tester recruitment and
  success metrics". For pre-launch validation programs, not roadmap planning
  or feature prioritization.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="beta-testing-plan-creator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing ICA definitions, product positioning, prior launch data, or feature roadmap artefacts.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Product or feature under test** — what is being beta tested? Share any PRDs, feature briefs, prototypes, or screenshots.
- **Beta objectives** — what must this beta prove or disprove? (e.g., usability validation, willingness-to-pay signal, retention hypothesis, technical stability under load)
- **ICA definition** — who is the ideal beta tester? What segments, behaviours, or firmographics matter most?
- **Constraints** — timeline, budget ceiling, engineering bandwidth for instrumentation, legal/compliance considerations (e.g., NDA requirements, GDPR, HIPAA)
- **Prior beta experience** — has the team run betas before? What worked or failed?
- **Success threshold** — what quantitative or qualitative result would greenlight a full launch?

## Step 3: Do the Work — Beta Testing Plan Development

### 3A: Beta Programme Architecture

Define the programme structure using a phased gating model:

| Phase | Name | Duration | Cohort Size | Gate Criteria |
|-------|------|----------|-------------|---------------|
| 0 | Internal Dogfood | 3–5 days | Core team only | Zero P0/P1 defects; core workflow completable end-to-end |
| 1 | Closed Alpha | 1–2 weeks | 5–15 hand-picked ICA testers | Task completion rate ≥ 80%; no data-loss bugs |
| 2 | Private Beta | 2–4 weeks | 50–200 recruited ICA testers | NPS ≥ 30; activation rate ≥ 60%; P0 defect rate < 0.5% |
| 3 | Open Beta (optional) | 2–4 weeks | Uncapped / waitlist-controlled | Retention D7 ≥ target; infrastructure stable at 10× Phase 2 load |

Adjust phase count, duration, and cohort sizing based on the user's constraints and objectives. Flag any phases that can be collapsed or skipped with explicit risk trade-offs.

### 3B: Tester Recruitment & Segmentation Strategy

Design a recruitment plan across three tester tiers:

1. **Power ICA testers** — existing users or prospects who match the ICA profile with high engagement history. Source: CRM segments, community champions, sales-nominated accounts.
2. **Edge-case testers** — users who represent boundary conditions (low technical literacy, atypical use cases, accessibility needs, high-volume usage). Source: support ticket analysis, product analytics outlier detection.
3. **Fresh-eyes testers** — users with zero prior exposure to the product. Source: referral incentives, beta communities (e.g., BetaList, Product Hunt Ship), targeted social outreach.

Define for each tier:
- Recruitment channel and messaging template
- Screening criteria (survey or form with 5–7 qualifying questions)
- Cohort allocation ratio (recommended: 50% Power / 30% Edge-case / 20% Fresh-eyes)
- Incentive structure (early access, extended trial, branded swag, influence on roadmap, monetary compensation if applicable)

### 3C: Instrumentation & Data Collection Framework

Specify the four data streams to instrument before beta launch:

1. **Behavioural analytics** — define 10–15 key events to track (activation, core feature usage, feature discovery, error encounters, drop-off points). Map each event to a hypothesis. Recommend tooling (e.g., Amplitude, Mixpanel, PostHog) based on user's stack.
2. **Structured feedback** — design three survey touchpoints:
   - **Onboarding survey** (Day 0): expectations, use case intent, baseline satisfaction with current solution
   - **Mid-beta pulse** (midpoint): SUS score, feature-specific satisfaction (1–7 Likert), open-ended friction capture
   - **Exit survey** (final day): NPS, willingness-to-pay question (Van Westendorp or Gabor-Granger format), likelihood to recommend, unmet needs
3. **Qualitative depth** — schedule 5–8 moderated user interviews (30 min each) stratified across tester tiers. Provide a semi-structured interview guide with 10 questions covering: first impressions, workflow integration, perceived value, comparison to alternatives, and dealbreakers.
4. **Bug & issue reporting** — define the reporting mechanism (in-app widget, dedicated Slack channel, structured form), severity taxonomy (P0–P3 with definitions), and SLA for acknowledgement (P0: 2 hours; P1: 24 hours; P2: 72 hours; P3: batched weekly).

### 3D: Success Metrics & Decision Framework

Build a **Beta Scorecard** with weighted metrics tied to the user's stated objectives:

| Metric | Target | Weight | Source |
|--------|--------|--------|--------|
| Task completion rate | ≥ 85% | 20% | Behavioural analytics |
| Activation rate (defined action within first session) | ≥ 60% | 15% | Behavioural analytics |
| Net Promoter Score | ≥ 30 | 15% | Exit survey |
| System Usability Scale score | ≥ 68 (above average) | 10% | Mid-beta survey |
| P0/P1 defect density | < 0.5 per 100 sessions | 15% | Bug reports |
| Feature adoption breadth (% of beta features used) | ≥ 50% | 10% | Behavioural analytics |
| Willingness-to-pay signal | ≥ 40% at target price point | 10% | Exit survey |
| Qualitative sentiment (coded positive/negative ratio) | ≥ 3:1 | 5% | Interviews + open-ended responses |

Define three decision outcomes:
- **Green (weighted score ≥ 75%)**: proceed to general availability with minor refinements
- **Amber (50–74%)**: extend beta with targeted fixes; re-evaluate in 2 weeks
- **Red (< 50%)**: halt launch; return to discovery/development with specific remediation backlog

### 3E: Operational Runbook

Produce a week-by-week operational plan:

- **Pre-launch (T-2 weeks)**: finalise instrumentation QA, recruit and screen testers, prepare welcome kit (onboarding guide, feedback channels, expectations document, NDA if required), brief support team
- **Launch week**: deploy to Phase 1 cohort, send welcome sequence, monitor dashboards for anomalies, conduct daily 15-min beta stand-up (PM + Eng + Design)
- **Mid-beta**: deploy mid-beta survey, conduct first wave of interviews, publish internal beta health report, triage and prioritise bug backlog, decide Phase 2 gate
- **Final week**: deploy exit survey, conduct remaining interviews, compile raw data export, begin analysis
- **Post-beta (T+1 week)**: synthesise findings, present Beta Scorecard to stakeholders, make go/no-go recommendation, publish tester thank-you and results summary

### 3F: Risk Register

Identify and mitigate the top risks:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Low tester engagement / survey fatigue | High | High | Keep surveys under 5 min; gamify participation; weekly engagement nudges |
| Selection bias (only enthusiasts participate) | Medium | High | Recruit edge-case and fresh-eyes tiers; weight analysis by tier |
| Scope creep from beta feedback | High | Medium | Pre-commit to "fix only P0/P1 in-beta" policy; log all else to post-beta backlog |
| Data integrity gaps | Medium | High | Run instrumentation dry-run in Phase 0; validate event firing before Phase 1 |
| Negative word-of-mouth from buggy experience | Medium | High | NDA for Phases 0–1; set expectations in welcome kit; fast P0 SLA |
| Regulatory / compliance exposure | Low | Critical | Legal review of beta terms, data handling, and consent flows pre-launch |

Apply any user-specific `instructions` from FutureProof context to adjust methodology, terminology, tooling recommendations, or compliance requirements.

## Step 4: Deliver Output

Produce a **Beta Testing Plan Document** with the following structure:

1. **Executive Summary** — one-page overview of beta objectives, timeline, cohort strategy, and success criteria
2. **Programme Architecture** — phased model with gate criteria (Section 3A)
3. **Recruitment Plan** — tester tiers, channels, screening criteria, incentives (Section 3B)
4. **Instrumentation Specification** — event taxonomy, survey instruments, interview guide, bug reporting protocol (Section 3C)
5. **Beta Scorecard** — metrics table with targets, weights, and decision thresholds (Section 3D)
6. **Operational Runbook** — week-by-week timeline with owners and deliverables (Section 3E)
7. **Risk Register** — risk matrix with mitigations (Section 3F)
8. **Appendices** — tester screening form template, survey question banks, interview guide, welcome kit draft, NDA template outline

Format: structured Markdown document suitable for export to Google Docs, Notion, or Confluence. All tables render cleanly. All templates are copy-paste ready.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="beta-testing-plan-creator", experiment={
  hypothesis: "Segmenting beta testers into three tiers (Power ICA / Edge-case / Fresh-eyes) at a 50/30/20 ratio produces higher-signal feedback than unsegmented open recruitment",
  variants: ["control: open recruitment with no tier stratification", "variant: tiered recruitment with stratified analysis"],
  measurement: "Actionability score of beta findings (rated by PM on 1-10 scale) and defect discovery rate per tester across next 3 beta programmes",
  expected_impact: "30% increase in actionable insights per beta tester; 2× improvement in edge-case defect detection"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="beta-testing-plan-creator",
  query="Best practices for beta programme design in SaaS and digital products 2024: optimal cohort sizing models, survey instruments with highest signal-to-noise ratio, engagement retention tactics for multi-week betas, and emerging approaches to willingness-to-pay validation during beta",
  reason="Ensure beta plan frameworks reflect current industry benchmarks and incorporate proven engagement and measurement techniques beyond traditional approaches"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="beta-testing-plan-creator", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```