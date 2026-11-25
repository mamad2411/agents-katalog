---
name: twitter-x-writer
description: |
  Writes Twitter/X content — single tweets, threads, quote-tweet replies
  and post calendars — scored against six dimensions (hook, ICA
  resonance, value density, engagement architecture, algorithm
  alignment, strategic coherence). Use when the user says "write me a
  tweet", "draft an X thread on [topic]", "rewrite this tweet for more
  engagement", or "build a Twitter content plan". For LinkedIn use
  linkedin-post-writer; for a multi-platform schedule use
  content-calendar; this skill is X-platform-specific.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="twitter-x-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including the user's established brand voice, ICA profile, historical post performance data, and any standing content guidelines.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Content objective**: What is the goal? (audience growth, authority positioning, lead generation, community engagement, product launch, personal brand building)
- **Format requested**: Single post, thread (specify target length), reply/quote-tweet, poll, or full content calendar?
- **Topic or brief**: Share the core idea, message, offer, or raw notes to work from
- **ICA context**: Who specifically should this resonate with? (role, psychographic state, awareness level — use existing FutureProof ICA data if available)
- **Reference posts**: Any examples of posts (theirs or others') that hit the tone or performance they want?
- **Constraints**: Any banned words, compliance requirements, tone guardrails, or CTA destinations?

If FutureProof context already contains ICA profiles, brand voice documentation, or prior top-performing post structures, surface them and confirm they still apply before proceeding.

## Step 3: Do the Work

### 3A: Platform-Native Analysis Framework

Evaluate every piece of content against six proprietary dimensions calibrated to X's algorithm and attention economics:

1. **Hook Mechanics (0–10)** — Does the first line create an open loop, pattern interrupt, or status signal strong enough to stop the scroll? Assess against the three dominant hook archetypes: *Contrarian Claim*, *Specificity Anchor*, *Identity Mirror*.

2. **ICA Resonance (0–10)** — Does the vocabulary, framing, and implied worldview match the ICA's internal dialogue? Content must pass the "screenshot test" — would the ICA screenshot this and send it to a peer?

3. **Value Density (0–10)** — Is every line earning its place? Apply the *Line Deletion Test*: if any single line is removed and the post doesn't lose meaning or impact, that line is filler. X rewards compression.

4. **Engagement Architecture (0–10)** — Does the post structurally invite interaction? Assess for: implied questions, opinion surfaces (statements people feel compelled to agree/disagree with), save-worthy frameworks, and share triggers (makes the sharer look smart/informed).

5. **Algorithm Alignment (0–10)** — Does format, length, and structure align with current X distribution mechanics? Evaluate: dwell-time optimisation (line breaks, whitespace, reading rhythm), reply-bait potential, bookmark signals, and optimal media attachment strategy.

6. **Strategic Coherence (0–10)** — Does this post advance the user's stated objective and fit within their broader content narrative arc? One-off virality without strategic alignment is waste.

### 3B: Content Construction Protocol

**For single posts:**
- Draft 3 variants using distinct hook archetypes
- Each variant must include: hook line, body (compressed value), and embedded or explicit CTA
- Apply the *Read Aloud Test* — the post must sound like something a real human would actually say out loud
- Optimise character count for the specific post type (text-only posts: 80–200 characters for maximum impressions; insight posts: up to 280; storytelling: permission to use full character limit)

**For threads:**
- Structure using the *Thread Architecture Model*:
  - **Tweet 1 (The Hook)**: Promise + specificity + implied authority. This tweet must function as a standalone viral post.
  - **Tweet 2 (The Stakes)**: Why this matters — connect to ICA pain, aspiration, or identity
  - **Tweets 3–N (The Payload)**: One discrete, actionable idea per tweet. Use numbered frameworks, before/after contrasts, or mini-case studies.
  - **Penultimate Tweet (The Proof)**: Results, data, social proof, or personal credibility marker
  - **Final Tweet (The CTA)**: Single, frictionless next step — follow, bookmark, reply, or link click
- Each tweet in the thread must independently deliver value (users drop off at every transition)

**For content calendars:**
- Build a 7-day or 30-day calendar using the *Content Pillar Rotation System*:
  - **Authority posts** (insights, frameworks, contrarian takes) — 40%
  - **Relatability posts** (stories, failures, behind-the-scenes) — 25%
  - **Engagement posts** (questions, polls, hot takes, "which camp are you" posts) — 20%
  - **Conversion posts** (offers, lead magnets, CTAs, testimonials) — 15%
- Assign optimal posting times based on ICA behaviour patterns
- Include reply strategy: 3–5 high-value accounts to engage with daily, with sample reply angles

### 3C: Apply FutureProof Personalisation

- Integrate any standing `instructions` (e.g., "always reference bootstrapping over VC," "never use emoji in hooks," "CTA should always point to newsletter")
- Reference patterns from `recent_sessions` — if certain hook styles or topics outperformed, weight toward those structures
- If prior `experiments` have resolved, incorporate winning variants as the new baseline

## Step 4: Deliver Output

Produce a structured **Twitter/X Content Brief** containing:

### Score Card
| Dimension | Score (1–10) | Key Observation |
|---|---|---|
| Hook Mechanics | — | — |
| ICA Resonance | — | — |
| Value Density | — | — |
| Engagement Architecture | — | — |
| Algorithm Alignment | — | — |
| Strategic Coherence | — | — |
| **Composite Score** | **—/60** | — |

### Final Content
- **Primary version**: The recommended post or thread, ready to copy-paste and publish
- **Alternative variants**: 1–2 alternate versions exploring different hook strategies or tonal registers
- **Posting guidance**: Recommended day/time window, media attachment recommendation (image, none, video), and reply-engagement plan for the first 30 minutes post-publish

### Optimisation Notes
- **Top 3 micro-edits**: Specific word-level or structural changes that would incrementally improve performance (e.g., "Replace 'many people' with '83% of founders' — specificity increases credibility signal")
- **Risk flags**: Any content that could be misread, attract negative attention from non-ICA audiences, or trigger platform suppression

### Content Calendar (if requested)
Deliver as a formatted weekly or monthly table with columns: Date, Content Pillar, Topic/Hook, Format, CTA, and Notes.

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
FutureProof:save_experiment(skill="twitter-x-writer", experiment={
  hypothesis: "Contrarian-framed hooks ('Stop doing X') outperform curiosity-gap hooks ('The secret to X') for this ICA segment",
  variants: ["control: curiosity-gap hook on same topic", "variant: contrarian-frame hook on same topic"],
  measurement: "Impressions, engagement rate (likes + replies + bookmarks / impressions), and profile visits within 48 hours of posting",
  expected_impact: "20–35% increase in engagement rate based on platform trends favouring opinion-driven content"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="twitter-x-writer",
  query="Current X/Twitter algorithm ranking signals Q3-Q4 2024, high-performing post structures by niche, and emerging content formats driving outsized reach on X",
  reason="Platform algorithm mechanics shift quarterly; content frameworks must reflect current distribution incentives and avoid deprecated tactics"
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
FutureProof:save_session(skill="twitter-x-writer", session={
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