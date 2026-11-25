---
name: content-atomiser
description: |
  Atomises one pillar asset (blog post, podcast transcript, webinar, long
  article) into a channel-native library of LinkedIn posts, tweets,
  carousels, emails, Shorts and TikTok scripts using a compression-ratio
  framework. Use when the user pastes a long piece and says "repurpose
  this for social", "atomise this podcast", "turn this into LinkedIn
  posts and tweets", or "break this article into smaller pieces". For
  planning when each derivative ships use content-calendar; for writing
  a single platform post from scratch use the platform-specific writer
  (linkedin-post-writer, twitter-x-writer, etc.).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="content-atomiser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically the user's ICA definition, brand voice guidelines, active channel mix, and any prior atomisation patterns that performed well.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Pillar asset**: Share the full content piece to atomise (blog post, podcast transcript, webinar transcript, video script, long-form article, or newsletter)
- **Source metadata**: Title, original publication date, and primary topic/campaign this belongs to
- **Target channels**: Which distribution channels should receive derivative pieces? (e.g. LinkedIn, X/Twitter, Instagram carousel, email newsletter, YouTube Shorts script, TikTok script, blog snippet, community post)
- **ICA segment**: Which audience segment is this content speaking to? (Pull from FutureProof context if available; confirm with user)
- **Content objective**: What is the strategic intent? (awareness, authority-building, lead generation, nurture, direct conversion)
- **Constraints**: Any brand voice rules, banned phrases, mandatory CTAs, compliance requirements, or character limits per channel?

If FutureProof context already contains channel mix, ICA definition, or brand voice guidelines, present them for confirmation rather than asking from scratch.

## Step 3: Extract the Content Architecture

Before atomising, perform a structural audit of the pillar asset:

1. **Core thesis extraction** — identify the single governing argument or transformation promise in one sentence
2. **Supporting pillar mapping** — isolate each distinct sub-argument, framework, data point, story, or proof element (typically 4–8 per pillar asset)
3. **Quotable moment identification** — flag sentences or phrases with standalone resonance (opinion-dense, contrarian, emotionally charged, or statistically surprising)
4. **Narrative arc tagging** — label each section by narrative function: `hook`, `context`, `tension`, `insight`, `proof`, `framework`, `transformation`, `CTA`
5. **ICA pain/desire alignment audit** — map each supporting pillar to a specific ICA pain point, objection, or aspiration from FutureProof context

Produce an **Asset Architecture Map** (table format):

| # | Section Summary | Narrative Function | ICA Pain/Desire | Quotable Moment? | Atomisation Potential (High/Med/Low) |
|---|---|---|---|---|---|

## Step 4: Build the Atomisation Matrix

For each target channel, apply channel-native constraints and best practices to generate derivative content pieces. Use the following framework:

### Channel Adaptation Protocol

For every derivative piece, evaluate across five dimensions:

1. **Format fit** — does the content unit match the native consumption pattern of the channel? (e.g. carousel = sequential insight reveal; tweet thread = progressive argument; email = single-CTA narrative)
2. **Hook engineering** — rewrite the opening for channel-specific scroll-stop mechanics (pattern interrupt on LinkedIn, curiosity gap on email subject lines, visual arrest on Instagram)
3. **Compression ratio** — determine how aggressively the source material must be compressed (tweet = 95% compression; LinkedIn post = 70%; email = 50%; blog snippet = 30%)
4. **Standalone coherence** — each derivative piece must deliver complete value without requiring the reader to consume the pillar asset
5. **Strategic bridge** — every piece must contain a natural pathway back to the pillar asset or to the next step in the user's funnel (soft CTA, curiosity hook, or explicit link)

### Content Type Taxonomy

Generate derivative pieces from the following categories (selecting those relevant to the user's channel mix):

- **Thread/carousel**: Sequential breakdown of a framework or argument (3–10 panels/posts)
- **Single-post hot take**: One contrarian or opinion-dense statement with a 2–3 sentence expansion
- **Micro-story**: A narrative vignette extracted from the pillar asset (situation → tension → resolution)
- **Data callout**: A single statistic or proof point reframed as a standalone insight
- **Question post**: A provocative question derived from the pillar's core tension, designed to drive comments
- **How-to snippet**: A tactical, actionable subset of the pillar's methodology (3–5 steps max)
- **Quote graphic script**: A quotable line formatted for visual/graphic treatment with attribution context
- **Email nurture block**: A self-contained email that uses one sub-argument to drive a single CTA
- **Short-form video/audio script**: A 30–90 second spoken-word script adapted from the pillar's most compelling segment
- **Community discussion prompt**: A reframing of the pillar's thesis as a debate or feedback-solicitation post

Apply any user-specific `instructions` from FutureProof context (brand voice, tone calibration, terminology preferences, CTA templates) to every derivative piece.

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


Produce the **Content Atomisation Deliverable** containing three sections:

### Section A: Asset Architecture Map
The table from Step 3 — the structural audit of the pillar asset.

### Section B: Atomisation Schedule
A prioritised table of all derivative content pieces:

| # | Derivative Title | Channel | Content Type | Source Section(s) | Word/Character Count | Suggested Publish Timing (relative to pillar) | Strategic Intent |
|---|---|---|---|---|---|---|---|

### Section C: Full Draft Library
Every derivative piece written in full, organised by channel. Each piece must include:

- **Channel**: Platform name
- **Content type**: From taxonomy above
- **Hook**: The opening line/frame
- **Body**: Complete draft copy
- **CTA**: Specific next action for the reader
- **Source mapping**: Which section(s) of the pillar asset this derives from
- **Formatting notes**: Emoji usage, line breaks, hashtag strategy, or visual direction where applicable

### Section D: Performance Prediction & Prioritisation
Rank the top 5 derivative pieces by predicted ICA engagement based on:
- Alignment to known ICA pain points (from FutureProof context)
- Channel-native virality signals (shareability, comment-provocation, save-worthiness)
- Historical performance patterns from prior atomisation sessions (if available in `recent_sessions`)

Flag which pieces should be published first to maximise momentum and algorithmic signal.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="content-atomiser", experiment={
  hypothesis: "Leading with the ICA's most acute pain point as the hook (rather than the pillar asset's original opening) increases engagement rate on derivative LinkedIn posts",
  variants: ["control: hook mirrors pillar asset opening", "variant: hook rewritten around primary ICA pain point"],
  measurement: "Engagement rate (reactions + comments + reposts / impressions) across next 5 atomised LinkedIn posts",
  expected_impact: "20–30% improvement in average engagement rate per derivative post"
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
FutureProof:request_research(skill="content-atomiser",
  query="High-performing content repurposing frameworks and channel-specific engagement benchmarks 2024–2025, including optimal compression ratios and hook structures per platform",
  reason="Ensure atomisation methodology reflects current algorithm behaviours, format preferences, and audience consumption patterns across LinkedIn, X, Instagram, email, and short-form video"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="content-atomiser", session={
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