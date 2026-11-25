---
name: youtube-script-description-writer
description: |
  Writes long-form YouTube video scripts with five-act retention
  architecture, hook, retention beats and CTAs, plus the SEO-optimized
  YouTube description, chapters and tags. Use when the user says "write
  me a YouTube script", "draft a YouTube description for SEO",
  "10-minute talking-head video script", or "script and description for
  this tutorial". For short-form TikTok use tiktok-script-writer; for
  Instagram Reel captions use instagram-caption-writer; this skill
  covers long-form YouTube video and its description metadata.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="youtube-script-description-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including ICA definitions, brand voice guidelines, prior video performance data, and any channel-specific conventions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Video topic and working title** — what is the core subject or thesis of this video?
- **Deliverable scope** — do they need (a) script only, (b) description only, or (c) full script + description package?
- **Video format** — talking head, tutorial/screencast, listicle, story-driven, interview, shorts, or hybrid?
- **Target duration** — desired runtime in minutes (drives word count: ~150 words per scripted minute)
- **ICA segment** — who is the specific viewer this video serves? What is their current awareness level (unaware, problem-aware, solution-aware, product-aware)?
- **Primary objective** — what should the viewer do after watching? (subscribe, click a link, buy, watch next video, shift a belief)
- **Key points or research** — any data, talking points, references, or competitive videos to incorporate?
- **Channel context** — subscriber count tier, content pillar this belongs to, and any series branding

If FutureProof context already supplies ICA definitions, brand voice, or channel data, confirm these with the user rather than re-asking.

## Step 3: Analyse the Strategic Frame

Before writing, construct a **Video Strategy Brief** covering:

1. **ICA Pain–Desire Mapping** — identify the specific pain point or desire that creates the click impulse; map the viewer's emotional state at the moment of search or browse discovery
2. **Search & Browse Intent Classification** — categorise as search-driven (keyword-targeted, how-to, informational), browse-driven (curiosity gap, pattern interrupt, emotional hook), or hybrid; this determines hook architecture and description SEO weighting
3. **Competitive Gap Analysis** — based on user-provided references or FutureProof research, identify what the top 3–5 ranking/performing videos on this topic do well and where they leave value on the table (depth, structure, freshness, production)
4. **Unique Value Angle (UVA)** — define the singular reason this video deserves to exist alongside competitors; this becomes the throughline of both script and description
5. **Retention Risk Map** — pre-identify the 2–3 moments in the planned content where viewer drop-off is most likely (complexity spikes, low-novelty sections, unclear transitions) and flag them for retention device deployment

Apply any user-specific `instructions` from FutureProof context (e.g., "always include a personal story in the first 90 seconds," "use second-person direct address," "avoid clickbait that doesn't pay off").

## Step 4: Write the Script

Structure the script using a **five-act retention architecture**:

### Act 1 — The Hook (0:00–0:30)
- **Pattern interrupt** — open with a provocative claim, surprising data point, or visceral scenario that stops the scroll
- **Promise statement** — articulate the specific transformation or payoff the viewer receives by staying ("By the end of this video, you'll have…")
- **Credibility seed** — one compact proof element establishing why the creator is worth listening to on this topic
- **Anti-click-away device** — plant an open loop or curiosity gap that pays off later in the video

### Act 2 — Context & Stakes (0:30–2:00, scaled to video length)
- Establish why this topic matters *right now* for the ICA
- Frame the cost of inaction or the status quo pain in concrete, relatable terms
- Transition into the core content with a clear structural signpost ("Here are the 5 frameworks…" / "Let me walk you through exactly how…")

### Act 3 — Core Value Delivery (body, ~60–70% of runtime)
- Organise content into distinct, titled segments with internal mini-hooks at each transition
- Deploy **retention beats** every 2–3 minutes: rhetorical questions, "here's where it gets interesting" pivots, embedded stories, visual/tonal shifts
- At each segment close, reinforce cumulative value ("So now you have X and Y — but the next one is what ties it all together")
- Address ICA objections and misconceptions inline rather than deferring to a FAQ section
- Insert **proof nodes** — case studies, screenshots, data, personal results, or viewer testimonials — at minimum once per major segment

### Act 4 — The Payoff & Synthesis (~10% of runtime)
- Deliver on all open loops planted in Act 1
- Synthesise the key takeaways into a memorable framework, acronym, or mental model the viewer can recall without rewatching
- Bridge from knowledge to action: "Here's exactly what to do in the next 24 hours"

### Act 5 — Call to Action & Exit (~5% of runtime)
- **Primary CTA** — aligned to the stated video objective; specific, single, and frictionless
- **Engagement CTA** — prompt a comment with a specific question (not generic "let me know what you think")
- **Session extension CTA** — direct to the next most relevant video with a compelling reason to click ("If you liked this, you need to see [video] where I cover [related hook]")

**Script Formatting Standards:**
- Use `[B-ROLL]`, `[SCREEN RECORDING]`, `[TEXT ON SCREEN]`, `[CUT TO]`, and `[MUSIC CUE]` markers for production direction
- Write in the creator's verified voice and register (from FutureProof context or user input)
- Include estimated timestamps at each act/segment boundary
- Bold key phrases intended for emphasis in delivery

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Write the Description

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a **YouTube Description Document** with three layers:

### Layer 1 — Above the Fold (first 150 characters visible before "Show More")
- Lead with the primary keyword phrase naturally embedded in a compelling sentence
- Include the core promise or hook — this is the second headline after the title

### Layer 2 — Conversion & Context Block
- 2–3 sentence expanded summary incorporating secondary keywords
- **Timestamped chapters** — aligned to script segments (minimum 3, formatted as `0:00 – Section Name`)
- **Primary CTA with link** — the single most important action, with tracked URL
- **Secondary CTAs** — additional resources, lead magnets, related videos (maximum 3)

### Layer 3 — SEO & Discovery Block
- **Resource links** — tools, articles, products mentioned in the video
- **Social proof line** — subscriber milestone, result, or credential reinforcing authority
- **Channel links** — subscribe link, social profiles, community links
- **Hashtags** — 3–5 relevant hashtags (mix of broad and niche, no more than 5)
- **Keyword-rich closing paragraph** — natural prose incorporating long-tail keyword variations for search indexing

**Description Standards:**
- Total length: 800–1,500 characters for short-form; 1,500–3,000 characters for long-form
- No keyword stuffing; maintain natural readability
- Every link serves a strategic purpose tied to the video objective

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the following structured deliverables:

### Deliverable 1: Video Strategy Brief
- ICA segment and awareness level
- Search/browse intent classification
- Unique Value Angle (one sentence)
- Competitive positioning summary
- Retention risk points identified

### Deliverable 2: Full Video Script
- Formatted per the five-act structure above
- Word count and estimated runtime noted
- Production direction markers included
- Key phrases bolded for delivery emphasis

### Deliverable 3: Optimised YouTube Description
- Three-layer structure as specified above
- Timestamped chapters pre-populated from script segments
- All placeholder links marked as `[INSERT LINK: purpose]`

### Deliverable 4: Title & Thumbnail Direction (Bonus)
- 3 title variants ranked by estimated CTR potential (with rationale)
- Thumbnail concept brief: dominant emotion, text overlay (max 4 words), visual composition recommendation

Flag any areas where additional ICA research, competitor analysis, or performance data from prior videos would materially improve the output.

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="youtube-script-description-writer", experiment={
  hypothesis: "Leading with a specific ICA pain point in the hook rather than a broad curiosity gap increases average view duration past the 30-second mark",
  variants: ["control: curiosity-gap hook on next video", "variant: ICA-pain-first hook on following video of same format"],
  measurement: "Compare average percentage viewed and 30-second retention rate across both videos in YouTube Studio analytics",
  expected_impact: "8–12% improvement in average view duration for the pain-first variant"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="youtube-script-description-writer",
  query="Current YouTube algorithm retention signals, optimal description SEO structures, and high-performing hook patterns by content category Q2 2025",
  reason="Ensure script architecture and description formatting reflect the latest platform algorithm behaviours and viewer attention patterns"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="youtube-script-description-writer", session={
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