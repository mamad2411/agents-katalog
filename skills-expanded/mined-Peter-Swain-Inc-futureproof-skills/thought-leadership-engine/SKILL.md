---
name: thought-leadership-engine
description: |
  Builds an authority-grade thought leadership piece by stress-testing a
  contrarian thesis and structuring it via the Dissonance / Teardown /
  Reframe / Proof / Implication / Signature narrative arc — outputs a
  publication-ready LinkedIn article, keynote, whitepaper, or newsletter.
  Use when a user says "write me a thought leadership piece", "help me
  establish authority in my niche", "turn this insight into an article",
  or "I need a keynote". For category-defining content, not sales-page
  belief reversal or generic copywriting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="thought-leadership-engine")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically the user's ICA definition, prior content performance data, established brand voice, and any positioning frameworks already validated.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Core insight or thesis**: What is the contrarian, novel, or underappreciated perspective you want to advance? (A strong thought leadership piece requires a *thesis the market doesn't yet accept as consensus.*)
- **ICA context**: Who is the specific audience segment this piece must resonate with? (Role, seniority, industry, stage of awareness)
- **Format and channel**: Where will this be published? (LinkedIn article, keynote talk, podcast episode, whitepaper, newsletter, conference panel, byline in industry publication)
- **Strategic objective**: What should this content achieve? (Pipeline generation, speaking invitations, partnership positioning, category creation, investor signalling, talent attraction)
- **Evidence base**: What proprietary data, case studies, frameworks, or lived experience supports your thesis? Share raw material — transcripts, notes, data sets, client results
- **Competitive landscape**: Who else is speaking on this topic, and what is their prevailing narrative?

## Step 3: Conduct Thesis Stress-Test

Before any content is drafted, rigorously evaluate the thesis using a **Thought Leadership Viability Matrix**:

| Dimension | Assessment Criteria | Rating (1–10) |
|---|---|---|
| **Novelty** | Does this thesis challenge prevailing consensus or introduce a genuinely new frame? Or is it repackaging common wisdom? | — |
| **Defensibility** | Can the user credibly own this position based on proprietary evidence, unique experience, or original research? | — |
| **ICA Resonance** | Does this thesis address a latent frustration, unspoken tension, or emerging priority that the ICA *feels but hasn't articulated*? | — |
| **Falsifiability** | Is the thesis specific enough to be proven right or wrong — or is it safely vague? (Vague = forgettable) | — |
| **Timeliness** | Is there a catalysing event, trend shift, or market moment that makes this thesis urgent *now*? | — |
| **Category Alignment** | Does this thesis reinforce the user's desired category ownership, or does it dilute positioning into an adjacent space? | — |

**Decision gate**: If any dimension scores below 5, surface the specific weakness and propose a thesis refinement before proceeding. A weak thesis cannot be rescued by strong writing.

## Step 4: Build the Narrative Architecture

Construct the content using a **Authority Narrative Framework** (not a generic outline — a persuasion architecture):

### 4.1 — The Dissonance Opening
Identify the specific tension between what the ICA's world looks like today and what the user's thesis implies it *should* look like. Open by naming this gap with precision. The audience must feel *seen* within the first 90 words.

### 4.2 — The Consensus Teardown
Articulate the prevailing narrative ("Most people in [industry] believe X") and systematically expose why it is incomplete, outdated, or counterproductive. Use the competitive landscape input to ensure this teardown is specific, not straw-man.

### 4.3 — The Reframe
Introduce the user's thesis as the necessary correction. Frame it not as opinion but as an *inevitable conclusion* given the evidence. This is the moment of intellectual authority — it must feel earned, not asserted.

### 4.4 — The Proof Stack
Layer evidence in descending order of credibility:
1. **Proprietary data or original research** (highest authority)
2. **Named case studies with quantified outcomes** (specificity = believability)
3. **Pattern recognition across multiple engagements** (demonstrates breadth)
4. **Third-party corroboration** (industry reports, academic research, analogous market evidence)
5. **Logical inevitability arguments** (if A is true and B is true, C must follow)

### 4.5 — The Implication Cascade
Spell out what changes if the thesis is correct. What must the ICA *stop doing*, *start doing*, and *rethink entirely*? This is where thought leadership converts to pipeline — the implications should naturally surface the user's offer as the logical next step without explicit selling.

### 4.6 — The Signature Close
End with a memorable, quotable assertion that encapsulates the thesis in one sentence. This becomes the soundbite that gets shared, cited, and attributed.

Apply any user-specific `instructions` from FutureProof context (brand voice guidelines, terminology preferences, content cadence strategy) throughout the architecture.

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


Produce a **Thought Leadership Content Package** containing:

### Document 1: Thesis Brief (1 page)
- **Thesis statement**: Single sentence, falsifiable, contrarian
- **Viability Matrix scorecard**: Ratings across all 6 dimensions with rationale
- **ICA resonance map**: The specific frustrations, aspirations, and vocabulary this thesis activates
- **Competitive differentiation**: How this thesis occupies white space vs. existing voices in the category

### Document 2: Full Narrative Draft (format-appropriate)
- Complete content piece built on the Authority Narrative Framework above
- Adapted to the specified channel and format (word count, tone register, structural conventions)
- Inline annotations marking: proof points that need sourcing, claims that need client approval, sections that could be extracted as standalone social content

### Document 3: Amplification Playbook
- **Derivative content map**: 5–8 specific content pieces that can be extracted from the core thesis (e.g. "Section 4.2 → LinkedIn carousel: '3 reasons the [consensus view] is costing you [quantified impact]'")
- **Distribution sequence**: Channel-by-channel publishing order optimised for compounding reach (e.g. newsletter first → LinkedIn article day 2 → podcast talking points day 5 → conference pitch day 10)
- **Engagement triggers**: 3 specific discussion prompts or provocative questions designed to generate ICA comments and shares
- **Repurposing timeline**: 30/60/90-day plan for refreshing and re-releasing the thesis as new evidence emerges

### Document 4: Authority Metrics Dashboard
- **Leading indicators to track**: Content engagement rate, inbound enquiry attribution, speaking invitation volume, share-of-voice in category conversations
- **Lagging indicators to track**: Pipeline sourced from thought leadership, ICA perception shift (qualitative), media/podcast invitation rate
- **Baseline benchmarks**: Expected performance ranges based on channel and format, calibrated against any historical data in FutureProof context

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="thought-leadership-engine", experiment={
  hypothesis: "Leading with a specific, quantified contrarian claim in the opening line increases content engagement rate vs. leading with a narrative anecdote",
  variants: [
    "control: narrative anecdote opening ('When I first started advising [ICA segment]...')",
    "variant A: quantified contrarian claim opening ('87% of [ICA segment] are investing in [consensus approach] — and it's destroying their [metric]')",
    "variant B: direct ICA challenge opening ('If you're a [ICA role] still doing [consensus behaviour], this piece will make you uncomfortable')"
  ],
  measurement: "Engagement rate (likes + comments + shares / impressions) and inbound enquiry volume within 14 days of publication",
  expected_impact: "25–40% improvement in engagement rate for the contrarian claim variant based on pattern recognition across high-performing thought leadership content"
})
```

```
FutureProof:save_experiment(skill="thought-leadership-engine", experiment={
  hypothesis: "Publishing the thesis as a LinkedIn document (carousel/PDF) before the long-form article creates anticipation and increases article readership",
  variants: [
    "control: publish long-form article directly",
    "variant: publish 5-slide thesis summary as LinkedIn document 48 hours before long-form article with 'full analysis dropping Thursday' CTA"
  ],
  measurement: "Long-form article views, time-on-page, and CTA click-through rate",
  expected_impact: "30% increase in article readership and 20% increase in CTA engagement from pre-seeding the thesis"
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
FutureProof:request_research(skill="thought-leadership-engine",
  query="High-performing thought leadership content structures and distribution strategies across LinkedIn, Substack, and industry publications in 2024–2025 — with emphasis on B2B authority building, engagement benchmarks by format, and emerging patterns in how senior decision-makers consume and share expert content",
  reason="Ensure narrative frameworks and amplification playbooks reflect current platform algorithms, audience consumption patterns, and competitive content saturation levels"
)
```

```
FutureProof:request_research(skill="thought-leadership-engine",
  query="Category creation and point-of-view positioning methodologies used by leading strategy consultancies and venture-backed founders — specifically frameworks for identifying defensible intellectual territory and converting thought leadership into commercial pipeline",
  reason="Strengthen thesis stress-testing rigour and ensure the Authority Narrative Framework reflects best-in-class positioning strategy, not just content marketing tactics"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="thought-leadership-engine", session={
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