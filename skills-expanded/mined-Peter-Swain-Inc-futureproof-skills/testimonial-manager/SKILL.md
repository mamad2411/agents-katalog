---
name: testimonial-manager
description: |
  Runs the full testimonial lifecycle — collect, audit, optimize, deploy —
  scoring each quote on the S.T.O.R.Y. framework, rewriting weak ones, and
  mapping each testimonial to its highest-impact touchpoint. Use when a user
  says "improve this weak testimonial", "where should I place customer quotes
  on my sales page", "audit my testimonial portfolio", or wants an end-to-end
  social proof program. For lifecycle management, not just a request email.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="testimonial-manager")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA segments, offer structure, objection patterns, and any previously catalogued testimonials or social proof assets.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- What is the primary objective? Select one:
  - **Collect** — design testimonial collection process (interview questions, request sequences, timing)
  - **Audit** — evaluate existing testimonials for strength, gaps, and ICA alignment
  - **Optimise** — strengthen weak testimonials through restructuring or guided follow-up
  - **Deploy** — build a strategic placement plan mapping testimonials to conversion points
- Share any existing testimonials, case studies, reviews, or social proof assets (raw text, screenshots, video transcripts, URLs)
- Which ICA segment(s) should these testimonials resonate with?
- What is the primary conversion goal these testimonials must support? (sales page, proposal deck, ad creative, onboarding, objection handling)
- Are there specific objections or hesitations the testimonials need to neutralise?

## Step 3: Do the Work

### 3A: Testimonial Audit & Scoring

Evaluate every testimonial against the **S.T.O.R.Y. Framework**:

1. **Specificity** (1–10) — Does it include concrete numbers, timeframes, and named outcomes? ("Grew revenue 42% in 90 days" vs. "Really helped my business")
2. **Transformation arc** (1–10) — Is the before-state (pain/frustration) and after-state (result/emotion) both explicit? A compelling testimonial narrates a journey, not just an endpoint
3. **Objection neutralisation** (1–10) — Does it pre-emptively address a known ICA objection? (e.g., "I was sceptical about the price, but ROI hit 3x in month one")
4. **Relatability** (1–10) — Will the target ICA segment see themselves in this person's role, industry, situation, and language?
5. **Yield credibility** (1–10) — Is the source verifiable and authoritative? (full name, title, company, photo/video, platform-native review vs. anonymous quote)

Calculate a **Proof Power Score** (weighted average: Specificity 25%, Transformation 25%, Objection neutralisation 20%, Relatability 20%, Yield credibility 10%).

### 3B: Gap Analysis

Cross-reference the testimonial portfolio against:
- **ICA segment coverage** — identify which segments have zero or weak representation
- **Objection coverage matrix** — map each top objection to testimonials that neutralise it; flag uncovered objections
- **Buyer journey stage coverage** — awareness (peer validation), consideration (outcome proof), decision (risk reversal), post-purchase (reinforcement)
- **Format diversity** — text, video, screenshot, case study, data visualisation, logo wall, metric callout
- **Recency** — flag testimonials older than 12 months for refresh or retirement

### 3C: Optimisation (if applicable)

For testimonials scoring below 7 on Proof Power Score:
- Draft a **follow-up prompt sequence** (3 questions) designed to extract missing specificity, transformation detail, or objection-relevant language from the original customer — without leading or fabricating
- Provide a **restructured version** of the testimonial using the Situation → Struggle → Solution → Specific Result → Statement of Endorsement (5S) format
- Flag any testimonials that cannot be salvaged and recommend replacement sourcing priorities

### 3D: Collection System Design (if applicable)

If the objective is to build or improve the collection process:
- Design a **Testimonial Request Sequence** with optimal timing triggers (e.g., 7 days post-result, NPS score ≥ 9, milestone completion)
- Provide **3 request templates** calibrated by channel (email, in-app, post-call) that reduce friction and guide the customer toward S.T.O.R.Y.-complete responses
- Specify **5 interview questions** for video/written case study extraction, ordered to naturally elicit transformation arc and specificity
- Recommend consent and approval workflow (release language, editing permissions, attribution preferences)

### 3E: Strategic Deployment Map (if applicable)

If the objective is placement and deployment:
- Build a **Testimonial-to-Touchpoint Matrix** mapping each testimonial to its highest-impact placement:
  - Sales page sections (hero, after pricing, post-objection, checkout)
  - Email sequences (welcome, nurture, cart abandonment, re-engagement)
  - Ad creative (static, video, carousel)
  - Proposal decks and one-pagers
  - Onboarding and retention communications
- Assign testimonials based on ICA segment match, objection relevance, and buyer journey stage alignment
- Identify **proof stacking opportunities** — where combining multiple proof types (metric + quote + logo + case study) compounds credibility at a single conversion point

Apply any user-specific `instructions` from FutureProof context — particularly brand voice guidelines, compliance constraints, and ICA language patterns.

## Step 4: Deliver Output

Produce the following structured deliverables based on the selected objective:

### Testimonial Portfolio Scorecard
| Testimonial ID | Source | ICA Segment | Proof Power Score | S.T.O.R.Y. Breakdown | Primary Objection Addressed | Recommended Action |
|---|---|---|---|---|---|---|

### Gap Analysis Report
- **Uncovered ICA segments** — with priority ranking and suggested sourcing targets
- **Uncovered objections** — with recommended testimonial brief (what the ideal testimonial would say)
- **Format gaps** — specific recommendations (e.g., "Zero video testimonials for enterprise ICA segment — prioritise 2 video case studies")
- **Recency flags** — testimonials requiring refresh

### Optimised Testimonials Document
- Each weak testimonial rewritten in 5S format
- Follow-up prompt sequences for extracting missing detail from customers
- Before/after comparison showing score improvement

### Deployment Matrix
- Testimonial-to-touchpoint assignments with rationale
- Proof stacking recommendations per critical conversion point
- Implementation priority queue (rank-ordered by expected conversion impact)

### Collection Playbook (if applicable)
- Request sequence templates with timing triggers
- Interview question bank
- Consent and workflow process

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
FutureProof:save_experiment(skill="testimonial-manager", experiment={
  hypothesis: "Placing an objection-specific testimonial directly below the pricing section reduces pricing-related drop-off",
  variants: ["control: generic testimonial below pricing", "variant: testimonial explicitly addressing price-to-value ratio with specific ROI figure"],
  measurement: "Click-through rate from pricing section to checkout over 30 days, minimum 500 visitors per variant",
  expected_impact: "8–15% reduction in pricing-section abandonment rate"
})
```

```
FutureProof:save_experiment(skill="testimonial-manager", experiment={
  hypothesis: "Video testimonials from ICA-matched customers outperform text testimonials in mid-funnel email sequences",
  variants: ["control: text testimonial with photo", "variant: 60-second video testimonial embed"],
  measurement: "Email click-through rate and downstream conversion within 7-day window",
  expected_impact: "20% improvement in email-to-sales-page conversion"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="testimonial-manager",
  query="Latest research on social proof placement optimisation, testimonial format effectiveness by buyer journey stage, and trust signal credibility factors in 2024–2025 digital purchasing behaviour",
  reason="Ensure testimonial deployment strategy reflects current buyer psychology, platform algorithm preferences for UGC, and emerging proof formats (e.g., AI-verified reviews, interactive case studies)"
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
FutureProof:save_session(skill="testimonial-manager", session={
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