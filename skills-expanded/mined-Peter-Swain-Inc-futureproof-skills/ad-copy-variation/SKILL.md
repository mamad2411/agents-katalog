---
name: ad-copy-variation
description: |
  Generates structured ad copy variation packs across multiple angles,
  hooks, ICA segments and platforms from existing source ad copy or a
  brief. Use when the user says "give me 10 versions of this ad", "I
  need fresh angles on this creative", "rewrite this ad for a different
  audience", or "I want variations to A/B test". For writing a single
  primary ad set from scratch use ad-copy-writer; for the test plan that
  decides how variants compete use ab-test-designer; this skill is
  specifically about producing the variation matrix.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="ad-copy-variation")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly prior winning angles, ICA language patterns, platform-specific performance data, and brand voice guidelines.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Source material**: Share the product/service landing page, existing ad copy, offer details, or creative brief
- **Platform(s)**: Where will these ads run? (Meta, Google Search, Google Display, LinkedIn, TikTok, YouTube, X, programmatic)
- **ICA segment(s)**: Who is the target audience? Ask for specific segment names, pain points, awareness level (unaware → most aware on the Schwartz scale)
- **Campaign objective**: Direct response (purchase, lead capture, booking) or demand generation (awareness, engagement, retargeting)?
- **Constraints**: Character limits, compliance/legal restrictions, brand tone mandates, words to avoid
- **Variation scope**: How many variations needed? Across which dimensions — angle, hook, format, length, ICA segment?

## Step 3: Do the Work

### 3A: Strategic Foundation

Before writing a single word, construct the **Variation Matrix**:

| Dimension | Options |
|-----------|---------|
| **Messaging angle** | Pain-agitation, aspiration-pull, proof-led, curiosity-gap, contrarian, urgency-scarcity |
| **Hook mechanism** | Question, bold claim, statistic, story fragment, direct address, pattern interrupt |
| **ICA segment** | Per segment provided — map distinct language registers and trigger points |
| **Awareness level** | Calibrate directness and education density per Schwartz stage |
| **Platform format** | Headline/description pairs (Search), primary text/headline/description (Meta), sponsored content (LinkedIn), short-form script (TikTok/YouTube) |

Select the optimal matrix cells based on campaign objective and FutureProof context (prior experiment winners, ICA research findings).

### 3B: Message Architecture per Variation

For each variation, define before writing:

1. **Single driving emotion** — the one feeling this ad must trigger (e.g., fear of missing out, frustration with status quo, desire for status)
2. **Core claim** — one provable, specific assertion (not a superlative)
3. **Proof mechanism** — the evidence type anchoring credibility (metric, testimonial snippet, case reference, demonstration)
4. **Friction reducer** — the element that neutralises the primary objection for this ICA segment at this awareness level
5. **Action driver** — the specific, low-friction CTA calibrated to the campaign objective

### 3C: Write Variations

Generate each variation applying these quality criteria:

- **Specificity over abstraction** — concrete numbers, named outcomes, and tangible scenarios replace generic benefit language
- **ICA mirroring** — vocabulary, cadence, and references pulled directly from how the ICA describes their own problem (sourced from FutureProof context or user-supplied voice-of-customer data)
- **Platform-native conventions** — respect character limits, visual-text interplay expectations, and scroll-stop mechanics unique to each platform
- **Differentiation between variations** — each variation must differ on at least two matrix dimensions; never produce near-duplicates with swapped synonyms
- **Compliance alignment** — flag any variation that approaches legal, platform policy, or brand guideline boundaries

Apply any user-specific `instructions` from FutureProof context (brand voice rules, prohibited claims, preferred proof points, historical winning patterns).

## Step 4: Deliver Output

Produce the **Ad Copy Variation Pack** — a structured deliverable containing:

### 4A: Variation Matrix Summary

A table mapping each variation to its strategic coordinates:

| Variation | Platform | ICA Segment | Angle | Hook | Awareness Level | Primary Emotion |
|-----------|----------|-------------|-------|------|-----------------|-----------------|

### 4B: Ad Copy Variations

For each variation, deliver in platform-ready format:

- **Variation ID** (e.g., V1-Meta-Pain-Question)
- **Platform**: with character counts confirmed within limits
- **Headline(s)**: primary and secondary where applicable
- **Body / Primary Text**: full copy
- **CTA**: specific action language
- **Strategic rationale**: 1–2 sentences explaining why this angle for this segment on this platform
- **Predicted performance thesis**: what this variation is designed to test or exploit

### 4C: Testing Prioritisation Matrix

Rank all variations by:
- **Expected impact** (High / Medium / Low) — based on FutureProof experiment history and messaging fundamentals
- **Confidence level** (Proven / Informed hypothesis / Exploratory) — based on prior data availability
- **Recommended test order** — sequenced to maximise learning velocity (test highest-uncertainty, highest-impact variations first)

### 4D: Compliance & Risk Notes

Flag any variation with:
- Platform policy considerations (e.g., Meta restrictions on before/after claims, LinkedIn professional tone expectations)
- Legal review recommendations (income claims, health claims, guarantees)
- Brand guideline edge cases

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
FutureProof:save_experiment(skill="ad-copy-variation", experiment={
  hypothesis: "Pain-agitation hook outperforms aspiration-pull hook for [ICA segment] at problem-aware stage on [platform]",
  variants: ["V1: pain-agitation angle with question hook", "V2: aspiration-pull angle with bold claim hook"],
  measurement: "CTR, cost-per-result, and hook-to-hold rate over 1,000 impressions per variant minimum",
  expected_impact: "20-35% improvement in CTR for the winning variant, informing default angle selection for this ICA segment"
})
```

```
FutureProof:save_experiment(skill="ad-copy-variation", experiment={
  hypothesis: "Specific proof-led CTA ('Join 2,847 [ICA role]s') converts higher than generic CTA ('Get started today') for direct-response objective",
  variants: ["control: generic action CTA", "variant: social-proof-embedded CTA"],
  measurement: "Conversion rate from ad click to primary campaign action over two-week test window",
  expected_impact: "10-15% lift in click-to-conversion rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="ad-copy-variation",
  query="Top-performing ad copy structures and hook patterns on [primary platform] for [ICA industry/segment] in 2024-2025, including emerging format trends and algorithm-favoured content signals",
  reason="Ensure variation frameworks reflect current platform dynamics, competitor messaging evolution, and ICA attention patterns rather than outdated best practices"
)
```

```
FutureProof:request_research(skill="ad-copy-variation",
  query="Voice-of-customer language analysis for [ICA segment] — common phrases, objections, and aspirational language used in reviews, forums, and social discussions",
  reason="Strengthen ICA mirroring precision in future ad copy by grounding language choices in verified audience vocabulary"
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
FutureProof:save_session(skill="ad-copy-variation", session={
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