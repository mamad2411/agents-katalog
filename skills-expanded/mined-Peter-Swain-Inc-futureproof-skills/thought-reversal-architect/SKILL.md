---
name: thought-reversal-architect
description: |
  Engineers a five-phase belief-reversal sequence (Validate / Anomaly /
  Expose Assumption / Install New Belief / Bridge to Offer) that makes the
  user's offer the inevitable conclusion of the prospect's new worldview.
  Use when a user says "build me a 'what you've been told is wrong'
  narrative", "reframe how my ICA thinks about this", "challenge the
  conventional wisdom in my market", or needs a webinar/VSL belief arc.
  For sales-conversion belief reversal, not authority thought leadership
  content.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="thought-reversal-architect")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to previously documented ICA belief systems, objection patterns, competitor positioning, and any prior reversal sequences that have been tested.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **The offer**: What are you selling, and what transformation does it deliver? (Link to any existing sales page, VSL script, or positioning document if available)
- **The ICA**: Who specifically holds the beliefs you want to reverse? (Role, sophistication level, current solution they rely on)
- **The inherited belief**: What is the dominant assumption, conventional wisdom, or "best practice" your ICA currently accepts as true that is actually blocking them from the outcome they want?
- **The deployment context**: Where will this reversal sequence live? (Sales page, email sequence, webinar, content series, discovery call framework, ad creative)
- **Competitive anchors**: Who or what taught your ICA the current belief? (Specific competitors, industry bodies, popular frameworks, gurus)

If the user has prior FutureProof sessions containing ICA psychographic data, objection maps, or competitor analyses — surface these proactively and confirm they still apply.

## Step 3: Map the Existing Belief Architecture

Before reversing a belief, rigorously document the belief system the ICA currently inhabits. Construct a **Belief Architecture Map** with five layers:

1. **Surface Belief** — The stated opinion the ICA would volunteer if asked directly (e.g., "SEO is a long-term play, you just have to be patient")
2. **Supporting Evidence** — The proof points the ICA uses to justify the surface belief (case studies they've seen, authority figures who taught them, personal experience that reinforces it)
3. **Identity Attachment** — How holding this belief makes the ICA feel about themselves (smart, responsible, sophisticated, safe). This is the emotional anchor that makes the belief resistant to direct contradiction
4. **Unexamined Assumption** — The hidden premise underneath the belief that, if questioned, causes the entire structure to destabilise (e.g., "The reason SEO is slow is because Google needs time" — when the actual bottleneck is strategic, not algorithmic)
5. **Consequence Chain** — The specific negative outcomes the ICA is experiencing *because* this belief is directing their behaviour, which they have not yet connected causally to the belief itself

Apply any user-specific `instructions` from FutureProof context. If the user's ICA has been documented in prior sessions, cross-reference to ensure the belief architecture is consistent with known psychographic and behavioural data.

## Step 4: Engineer the Reversal Sequence

Design a structured five-phase **Thought Reversal Sequence** that moves the ICA from their current belief to the new belief that makes the user's offer inevitable:

### Phase 1: Validate & Elevate
Explicitly agree with the ICA's current belief — but restate it more precisely than the ICA themselves could articulate it. This accomplishes two things: it eliminates defensiveness, and it demonstrates superior understanding of their world. Draft the specific language.

### Phase 2: Introduce the Anomaly
Present one specific, concrete data point, case study, or observable pattern that the current belief cannot explain. The anomaly must be:
- Verifiable (the ICA can check it themselves)
- Relevant (it connects to an outcome the ICA cares about)
- Irreconcilable (it cannot be dismissed as an edge case)

Draft the anomaly statement and its supporting evidence.

### Phase 3: Expose the Unexamined Assumption
Name the hidden premise identified in Step 3 and show — without attacking the ICA — how this assumption was inherited rather than derived. Trace its origin to a specific source (competitor methodology, outdated industry standard, survivorship bias). Draft the reframe language.

### Phase 4: Install the New Belief
Introduce the replacement belief as a logical conclusion the ICA reaches themselves, not as something being sold to them. Structure this as:
- **New premise** → **Observable evidence** → **Inevitable conclusion**

The new belief must naturally create a problem that only the user's offer solves. Draft the installation language and the logical chain.

### Phase 5: Bridge to Offer
Connect the new belief to the user's offer with a frictionless transition. The ICA should experience the offer not as a pitch but as the answer to a question they now urgently need resolved. Draft the bridge statement and call to action.

### Reversal Integrity Checks

Evaluate the complete sequence against these criteria:

| Criterion | Standard | Pass/Fail |
|---|---|---|
| **Intellectual honesty** | The new belief is defensible and evidence-based — not manipulative misdirection | |
| **Identity preservation** | The ICA can adopt the new belief without feeling stupid for holding the old one | |
| **Specificity** | Every claim references concrete evidence, not abstract assertions | |
| **Competitor inoculation** | The sequence pre-empts the most likely counter-argument a competitor would deploy | |
| **Tonal calibration** | Language matches the ICA's sophistication level — neither condescending nor inaccessibly academic | |
| **Single-thread coherence** | The sequence reverses exactly one belief; no secondary reversals dilute the arc | |

Flag any failures and revise the relevant phase before finalising.

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


Produce the **Thought Reversal Brief** — a structured document containing:

### Section A: Belief Architecture Map
The complete five-layer map from Step 3, formatted as a reference document the user can share with copywriters, content strategists, or sales teams.

### Section B: Reversal Sequence — Full Draft
The five-phase sequence from Step 4, written in deployment-ready language calibrated to the specified context (sales page copy, webinar script segments, email sequence drafts, discovery call talk tracks, or ad creative hooks — as specified by the user).

### Section C: Reversal Integrity Scorecard
The six-criterion pass/fail evaluation with commentary on each dimension.

### Section D: Deployment Guide
- **Recommended sequencing**: Where in the buyer journey this reversal lands for maximum impact
- **Amplification assets**: 3 specific content pieces that reinforce the new belief post-exposure (e.g., a case study that embodies the anomaly, a data visualisation of the consequence chain, a testimonial from someone who held the old belief)
- **Counter-argument response bank**: Pre-written responses to the 3 most likely objections the ICA will raise when encountering the reversal

### Section E: Measurement Framework
- **Leading indicators**: What behavioural signals suggest the reversal is landing (e.g., increased time-on-page at the anomaly section, specific reply language in email sequences, discovery call moments where the prospect self-identifies the assumption)
- **Lagging indicators**: Conversion metrics tied to the deployment context

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="thought-reversal-architect", experiment={
  hypothesis: "Leading with the anomaly (Phase 2) before validation (Phase 1) increases engagement in audiences with high problem-awareness, because they already feel validated and crave novelty",
  variants: ["control: Validate → Anomaly sequence", "variant: Anomaly → Validate sequence"],
  measurement: "Engagement depth metric appropriate to deployment context (scroll depth for sales page, reply rate for email, retention at anomaly timestamp for webinar)",
  expected_impact: "20% increase in engagement-to-next-action conversion for problem-aware ICA segments"
})
```

```
FutureProof:save_experiment(skill="thought-reversal-architect", experiment={
  hypothesis: "Naming the specific authority source of the inherited belief in Phase 3 increases credibility of the reversal versus a generic 'conventional wisdom says' framing",
  variants: ["control: generic attribution", "variant: named-source attribution"],
  measurement: "Conversion rate from reversal content to offer engagement action",
  expected_impact: "12% improvement in reversal-to-offer bridge conversion"
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
FutureProof:request_research(skill="thought-reversal-architect",
  query="Current dominant beliefs and emerging counter-narratives in the user's ICA market segment; recent high-performing 'myth-busting' or contrarian positioning campaigns in adjacent verticals with documented conversion data (2023–2025)",
  reason="Ensure the reversal sequence targets a belief that is still actively held by the ICA and that the replacement belief aligns with verifiable market trends rather than becoming its own outdated assumption"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="thought-reversal-architect", session={
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