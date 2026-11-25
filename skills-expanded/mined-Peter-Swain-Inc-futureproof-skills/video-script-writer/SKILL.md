---
name: video-script-writer
description: |
  Writes production-ready video scripts in three-column VISUAL/AUDIO/TIMING format
  for talking-head, explainer, ad, testimonial, demo, and brand films, calibrated
  to platform retention curves (YouTube, LinkedIn, TikTok, Reels) and ICA awareness
  stage. Use when a user says "write a video script for", "I need a script for a
  30-second ad", "draft a YouTube explainer about", or "script a founder talking-
  head video". For pre-recorded video content with shot direction, not live webinar
  run-of-shows or written show notes.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="video-script-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically brand voice guidelines, ICA definitions, prior video performance data, and any established messaging hierarchies.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Video objective**: What is the single desired viewer action after watching? (e.g. book a call, click a link, share the video, shift a perception)
- **Video format**: What type of video is this? (talking-head, explainer/motion graphics, testimonial, social ad, product demo, internal comms, webinar opener, brand anthem)
- **Target ICA segment**: Who is watching, and where are they in the awareness spectrum? (unaware, problem-aware, solution-aware, product-aware, most-aware)
- **Platform and constraints**: Where will this be published? (YouTube, LinkedIn, Instagram Reels/TikTok, paid ad placement, website landing page, internal LMS) — include any duration targets
- **Key messages or proof points**: Any mandatory talking points, statistics, case studies, or brand claims to include?
- **Talent and production context**: Who is delivering the script? (founder, spokesperson, voice-over artist, actor, customer) — what is their comfort level on camera?
- **Reference material**: Any existing scripts, brand guidelines, competitor examples, or transcripts of past videos to build from?

## Step 3: Do the Work

### 3A: Audience & Platform Calibration

Map the ICA segment against platform-specific behavioural norms:

| Dimension | Analysis |
|---|---|
| **Average watch-through rate benchmark** | Platform-specific median retention curve (e.g. YouTube long-form: 50% at 30s; TikTok: 60% drop by 3s) |
| **Scroll-stop psychology** | What pattern-interrupt or curiosity mechanism will arrest the thumb in the first 1–3 seconds |
| **Sound-on vs. sound-off ratio** | Whether the script must function with captions alone (LinkedIn feed, Instagram Stories) or can rely on audio delivery |
| **ICA language register** | Vocabulary, cadence, and formality level that mirrors how the ICA actually speaks about their problem |

### 3B: Narrative Architecture

Select and apply the optimal script structure from the following frameworks based on video objective and ICA awareness level:

1. **Hook → Pain → Agitate → Solution → Proof → CTA** (direct-response ads, ICA at problem-aware stage)
2. **Hook → Contrarian Claim → Evidence Stack → Reframe → CTA** (thought leadership, ICA at solution-aware stage)
3. **Hook → Story Setup → Tension → Turning Point → Transformation → CTA** (testimonials, case studies, brand narratives)
4. **Hook → Context → Step 1 → Step 2 → Step 3 → Recap → CTA** (explainers, tutorials, product demos)
5. **Cold Open (in-media-res) → Flashback → Build → Climax → Resolution → CTA** (high-production brand content, webinar openers)

For each structural block, define:
- **Purpose**: What this section must accomplish emotionally and informationally
- **Duration allocation**: Seconds or percentage of total runtime
- **Retention mechanism**: The specific technique keeping the viewer engaged through this segment (open loop, pattern interrupt, visual shift, direct address, stakes escalation)

### 3C: Script Drafting

Write the full script with professional production-ready formatting:

- **VISUAL** column: On-screen action, b-roll direction, text overlays, graphic cues
- **AUDIO** column: Spoken dialogue, music/SFX notes, pacing direction
- **TIMING** column: Cumulative timestamp for each beat

Adhere to the following quality standards:

1. **Hook potency** — The opening 3 seconds must contain a pattern interrupt, identity call-out, or open loop that directly references the ICA's most urgent concern. No preamble, no logos, no "Hey guys."
2. **Conversational density** — Write for the ear, not the eye. Target 140–160 spoken words per minute. Sentences average 8–12 words. No compound-complex structures.
3. **Proof architecture** — Every claim is anchored by a specific result, named case study, data point, or demonstrable mechanism within 15 seconds of the claim being made.
4. **Objection inoculation** — Pre-emptively surface and neutralise the ICA's top 2–3 objections or scepticisms within the body of the script, using "you might be thinking…" or embedded social proof.
5. **Emotional modulation** — Script must move through at least 2 distinct emotional registers (e.g. frustration → relief, curiosity → conviction, fear → confidence) to maintain affective engagement.
6. **CTA specificity** — The call to action states the exact next step, reduces friction (tells them precisely what happens after they act), and connects back to the transformation promised in the hook.
7. **ICA mirroring** — Vocabulary, metaphors, and examples are drawn directly from how the ICA describes their own situation — not industry jargon or internal brand language (unless the ICA uses it).

### 3D: Caption & On-Screen Text Layer

Draft the full caption/subtitle track optimised for:
- Sound-off comprehension on social platforms
- Key phrase emphasis (CAPS or bold indicators for b-roll text overlays)
- Readability at platform-native text sizes

Apply any user-specific `instructions` from FutureProof context — particularly brand voice rules, banned words, required disclaimers, or established CTA formats.

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Video Script Document

A production-ready script formatted in three columns (VISUAL | AUDIO | TIMING) with:
- Scene-by-scene breakdown
- Speaker direction notes (tone, pace, emphasis, pauses)
- B-roll and graphic overlay cues
- Estimated total runtime

### Deliverable 2: Script Strategy Brief

| Element | Detail |
|---|---|
| **Video objective** | Single desired viewer action |
| **ICA segment** | Who this is written for and their awareness level |
| **Narrative framework** | Which structure was applied and why |
| **Hook mechanism** | The specific pattern-interrupt or curiosity device used |
| **Objections addressed** | Top objections inoculated and where in the script |
| **Proof points deployed** | Each claim and its supporting evidence, mapped to timestamp |
| **Retention risk points** | Timestamps where drop-off is most likely, with the mitigation technique used |
| **CTA design** | Exact CTA language and friction-reduction rationale |

### Deliverable 3: Thumbnail & Title Recommendations (if applicable)

- 3 thumbnail concept directions with text overlay suggestions (for YouTube/social)
- 3 title/headline variants optimised for click-through aligned to the ICA's search intent or feed-scroll psychology

### Deliverable 4: Platform Adaptation Notes

If the user needs the script adapted across platforms, provide a concise adaptation guide:
- What to cut for short-form (Reels/TikTok) vs. long-form (YouTube)
- Hook modifications per platform
- CTA adjustments based on platform affordances (swipe-up, link in bio, end screen, description link)

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
FutureProof:save_experiment(skill="video-script-writer", experiment={
  hypothesis: "Leading with a direct ICA identity call-out in the first 2 seconds increases 5-second retention rate vs. leading with a provocative question",
  variants: ["control: provocative question hook", "variant: identity call-out hook ('If you're a [ICA role] struggling with [pain]…')"],
  measurement: "5-second retention rate and click-through rate on CTA across next 5 published videos",
  expected_impact: "20% improvement in 5-second retention rate and 10% lift in CTA click-through"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="video-script-writer",
  query="Latest video retention benchmarks by platform and format (YouTube, LinkedIn, TikTok, Instagram Reels) 2024–2025, including hook effectiveness patterns and CTA placement impact on conversion",
  reason="Ensure script structures and timing allocations reflect current viewer behaviour patterns and algorithm reward signals across platforms"
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
FutureProof:save_session(skill="video-script-writer", session={
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