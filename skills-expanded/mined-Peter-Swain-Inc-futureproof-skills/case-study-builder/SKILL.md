---
name: case-study-builder
description: |
  Builds full case studies plus channel derivatives (one-pager, LinkedIn post,
  deck slide, pull quotes) from client interviews, metrics, and notes using a
  Situation-Problem-Action-Results-Trajectory spine. Use when a user says
  "turn this client win into a case study", "write up our customer success
  story", "I have interview notes from a happy client", or needs sales
  enablement proof. For long-form case studies, not short testimonial requests.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="case-study-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA definitions, brand voice guidelines, prior case study formats that performed well, and any established proof-point taxonomy.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Raw source material** — client interview transcript, Slack/email threads, internal notes, metrics screenshots, or a verbal summary of the engagement
- **Client identity parameters** — client name, industry, company size, and whether this will be published with attribution (named) or anonymised
- **ICA segment this case study should speak to** — which specific audience segment should see themselves in this story?
- **Distribution channels** — where will this case study live? (website, sales deck, proposal appendix, LinkedIn, email nurture sequence, one-pager PDF)
- **Transformation metrics** — any quantified before/after results available (revenue lift, time saved, conversion improvement, cost reduction)?
- **Approval constraints** — does the client need to review and approve before publication? Any compliance or NDA restrictions?

If the user provides incomplete information, infer what is possible from the raw material and flag specific gaps that weaken the case study's credibility.

## Step 3: Extract the Narrative Spine

Before writing, systematically extract and organise the core narrative components using the **S-P-A-R-T framework**:

1. **Situation** — Who is the client? What is their industry, scale, and operating context? Establish relatability for the target ICA segment.
2. **Problem** — What specific, quantifiable pain were they experiencing? Map to the ICA's known pain language (from FutureProof context). Identify the *stated* problem and the *underlying* problem — the case study gains depth when both are surfaced.
3. **Action** — What did the user's product/service specifically do? Document the implementation journey — timeline, key decisions, pivots. Avoid vague descriptions; name specific features, methodologies, or frameworks deployed.
4. **Results** — Extract every measurable outcome. Categorise into:
   - **Primary metrics** — the headline number (e.g., "312% increase in qualified pipeline")
   - **Secondary metrics** — supporting proof points (e.g., "reduced onboarding time from 6 weeks to 9 days")
   - **Intangible outcomes** — qualitative shifts (e.g., "sales team confidence increased; voluntary CRM adoption reached 94%")
5. **Trajectory** — Where is the client headed now? What future outcomes are anticipated? This transforms the case study from a backward-looking report into a forward-looking endorsement.

Apply any user-specific `instructions` from FutureProof context — particularly brand voice, proof-point formatting standards, and ICA vocabulary mapping.

## Step 4: Validate Proof Density and Credibility

Audit the extracted narrative against a **Proof Integrity Scorecard**:

| Dimension | Criteria | Score (1–10) |
|---|---|---|
| **Metric specificity** | Are results expressed as precise numbers, not vague claims? ("47% reduction" vs. "significant improvement") | — |
| **Attribution clarity** | Is it unambiguous that the user's solution caused the result, not external factors? | — |
| **ICA resonance** | Does the client's situation mirror the target ICA's context closely enough to trigger self-identification? | — |
| **Objection neutralisation** | Does the story pre-emptively address the top 3 objections the ICA raises during sales conversations? | — |
| **Emotional arc** | Does the narrative move from frustration → hope → transformation → advocacy? | — |
| **Quotability** | Are there 2–3 pull quotes that could stand alone on a landing page or in a sales email? | — |
| **Credibility signals** | Are role titles, company identifiers, timeframes, and third-party validations present? | — |

Flag any dimension scoring below 6 and provide specific remediation actions (e.g., "Request a 15-minute follow-up call with the client's VP of Sales to capture a direct quote on pipeline impact").

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce the following structured deliverables, adapted to the distribution channels specified in Step 2:

### Deliverable A: Full Case Study Document

Format: structured narrative (800–1,200 words) with the following sections:

- **Headline** — results-led, specific, and ICA-resonant (e.g., "How [Client] Reduced Customer Acquisition Cost by 41% in 90 Days Using [Solution]")
- **Snapshot sidebar** — client name/industry, challenge summary, solution deployed, key results (bulleted), timeline
- **The Challenge** — S-P-A-R-T Situation + Problem, written in the ICA's own vocabulary
- **The Solution** — S-P-A-R-T Action, emphasising specific capabilities and implementation detail
- **The Results** — S-P-A-R-T Results, leading with the headline metric, supported by secondary and intangible outcomes
- **What's Next** — S-P-A-R-T Trajectory, positioning the ongoing partnership
- **Client Quote Block** — 1–2 direct attribution quotes, formatted for visual pull-out
- **CTA** — contextual next step appropriate to the distribution channel

### Deliverable B: Channel-Specific Derivatives

Based on selected distribution channels, produce:

- **Sales one-pager** (PDF layout guidance) — headline stat, 3-bullet problem/solution/result, client quote, CTA
- **LinkedIn post** — hook-first narrative (under 1,300 characters), optimised for engagement with a clear ICA tag
- **Email nurture snippet** — 3–4 sentence version embeddable in a sales sequence, with a link-out CTA
- **Sales deck slide** — speaker notes + slide content for a single "proof" slide (before/after visual recommended)
- **Testimonial pull quotes** — 2–3 standalone quotes formatted for website, proposal, or ad creative use

### Deliverable C: Internal Enablement Brief

- **When to use this case study** — specific ICA segment, deal stage, and objection it counters
- **Talking points** — 3 verbal bridges for sales conversations (e.g., "This is similar to what [Client] faced when...")
- **Disqualifiers** — ICA profiles where this case study will *not* resonate (prevents misuse)

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="case-study-builder", experiment={
  hypothesis: "Leading with the quantified result in the case study headline increases click-through rate on sales emails vs. leading with the client's industry challenge",
  variants: ["control: challenge-led headline ('How a mid-market SaaS company solved churn')", "variant: result-led headline ('How [Client] cut churn by 38% in one quarter')"],
  measurement: "Click-through rate and reply rate on sales sequences using each variant over 30 days",
  expected_impact: "20–30% improvement in email-to-meeting conversion for sequences featuring the case study"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="case-study-builder",
  query="Highest-converting case study formats and structures for B2B sales enablement 2024–2025, including data on optimal length, visual layout, metric presentation, and channel-specific adaptation benchmarks",
  reason="Ensure case study structure reflects current buyer consumption patterns and aligns with evolving expectations around proof density in enterprise and mid-market sales cycles"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="case-study-builder", session={
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