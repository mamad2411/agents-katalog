---
name: linkedin-post-writer
description: |
  Writes LinkedIn posts in platform-native formats (narrative arc,
  contrarian reframe, tactical breakdown, observation, before/after,
  curated list) with scroll-stop hook calibrated to the dwell-time
  algorithm. Use when the user says "write me a LinkedIn post", "turn
  this story into a LinkedIn post", "draft a contrarian take for
  LinkedIn", or "make this hot take work on LinkedIn". For X/Twitter
  content use twitter-x-writer; for Facebook posts use
  facebook-post-writer; this skill is LinkedIn organic only.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="linkedin-post-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly the user's ICA definition, brand voice, past post performance data, and any winning formats identified through prior experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Core topic or raw material** — What is the post about? (an idea, a personal story, a hot take, a lesson learned, an article to riff on, a promotion, etc.)
- **Strategic objective** — What should this post accomplish? (authority building, lead generation, community engagement, newsletter/funnel sign-ups, hiring visibility, event promotion)
- **ICA targeting** — Who specifically must this post resonate with? (If not stated, pull from FutureProof context; confirm with the user)
- **Format preference** — Do they have a preferred format? (story-driven, contrarian take, listicle, carousel concept, poll, before/after transformation, "I was wrong about X")
- **Constraints** — Any mandatory inclusions (links, tags, hashtags, CTAs) or exclusions (no emojis, no hashtags, avoid certain language)?

If FutureProof context contains established brand voice guidelines or prior top-performing post patterns, surface these and confirm they still apply.

## Step 3: Do the Work

### 3A: Strategic Framing

Before writing a single word, define the post's architecture:

1. **ICA Pain/Desire Mapping** — Identify the specific tension this post addresses in the ICA's professional life. Map the topic to one of: an unspoken frustration, an aspiration they publicly signal, or a knowledge gap they'd be embarrassed to admit.
2. **Scroll-Stop Thesis** — Distil the post into a single provocative, specific, or counterintuitive claim that earns the first 3 seconds of attention.
3. **Platform-Native Format Selection** — Choose the optimal LinkedIn post structure based on objective and topic:
   - **Narrative Arc** — personal story with professional takeaway (highest engagement ceiling)
   - **Contrarian Reframe** — challenge conventional wisdom with evidence (authority positioning)
   - **Tactical Breakdown** — step-by-step framework or process (save-worthy, high share)
   - **Observation + Insight** — pattern recognition from the user's domain (thought leadership)
   - **Before/After Transformation** — concrete results with context (proof-driven lead generation)
   - **Curated List** — "X things I learned about Y" (accessible, high completion rate)

### 3B: Drafting — The LinkedIn Engagement Architecture

Write the post applying all six layers of the engagement architecture:

1. **Hook (Lines 1–2)** — Must pass the "thumb-stop test." Use one of the following proven hook patterns:
   - Bold declaration: "Most [ICA role] get [topic] completely wrong."
   - Specific result: "This one change added [specific metric] in [timeframe]."
   - Pattern interrupt: "I got fired. It was the best thing that happened to my career."
   - Curiosity gap: "The highest-performing [ICA role] I know all do this. Almost nobody talks about it."
   - Direct address: "If you're a [ICA role] struggling with [pain point], read this."

2. **Tension/Context (Lines 3–6)** — Establish stakes. Why should the reader care *now*? Ground the post in a recognisable situation, a surprising data point, or an emotional moment. Write at a 7th-grade reading level. One idea per sentence.

3. **Substance/Body (Lines 7–18)** — Deliver on the hook's promise with specificity. No filler. Every line must either teach, prove, or reframe. Use:
   - White space aggressively (one sentence per line for key points)
   - Concrete numbers over vague claims
   - "You" language to maintain direct address
   - Parallel structure for lists and frameworks
   - Strategic line breaks before the "See more" fold (lines 3–4) to maximise expand rate

4. **Proof Layer** — Embed at least one credibility signal: a personal result, a client outcome (anonymised if needed), a cited statistic, or a named authority reference.

5. **Memorable Close (Lines 19–21)** — End with one of:
   - A single-sentence reframe that recontextualises the entire post
   - A vulnerable admission that humanises the advice
   - A punchy, quotable one-liner

6. **Call to Action (Final lines)** — Engineer the CTA to match the strategic objective:
   - **Engagement**: Ask a specific, low-friction question ("What's one thing you'd add to this list?")
   - **Lead generation**: Offer a resource with a clear access mechanism ("I wrote a deeper breakdown of this framework — comment 'FRAMEWORK' and I'll send it over")
   - **Authority**: Invite disagreement ("Tell me where I'm wrong — I'll engage with every comment")
   - **Funnel**: Soft link to newsletter/profile with value framing, never naked URLs in body text

### 3C: Technical Optimisation

Apply LinkedIn algorithm and readability best practices:
- **Character count**: Target 1,200–1,800 characters (the engagement sweet spot for text-only posts; adjust for carousel or image posts)
- **"See more" optimisation**: Ensure the first 210 characters (approximately 3 lines on mobile) create an irresistible reason to expand
- **Hashtag strategy**: 3–5 hashtags maximum, placed at the end, mixing 1 broad (500K+ followers), 2 mid-tier (10K–100K), and 1–2 niche tags relevant to the ICA's world
- **Formatting**: Use line breaks, not dense paragraphs. Employ → bullets, numbered lists, or em-dashes for scannability. Avoid walls of text.
- **Tagging**: Only tag individuals or companies if genuinely relevant and likely to engage (tag sparingly — over-tagging suppresses reach)
- **Link placement**: If a link is required, place in comments (not body text) to avoid algorithmic suppression, unless the user explicitly overrides

### 3D: Voice Calibration

Cross-reference the draft against:
- FutureProof `instructions` for brand voice (tone, vocabulary, phrases to use/avoid)
- The user's prior top-performing posts (if available in `recent_sessions`) — mirror the cadence and structural patterns that drove results
- ICA vocabulary — ensure the post speaks *their* language, not industry jargon they wouldn't naturally use

## Step 4: Confirm, Deliver as Document, Amend, Distribute

### 4A: Confirm before producing

Do NOT produce the final output yet. Tell the user what you've prepared and ask for the go-ahead:

> "I've got the post ready — [one-sentence description of the angle and format chosen]. Want me to produce the full document?"

Wait for confirmation before proceeding.

### 4B: Produce as a document — not in the chat

Once confirmed, produce the deliverable as a **document artifact** (markdown file, not inline chat text). The document contains three sections:

**Section 1 — LinkedIn Post — Final Draft**
The complete, copy-paste-ready post with all formatting, line breaks, hashtags, and CTA in place.

**Section 2 — Post Strategy Brief**
| Element | Detail |
|---|---|
| **Hook Type** | [Pattern used and why] |
| **Format** | [Structure selected and rationale] |
| **ICA Resonance Point** | [Specific pain/desire this post targets] |
| **Scroll-Stop Score** | 1–10 rating of the hook's interrupt strength |
| **Substance Density** | 1–10 rating of value-per-line in the body |
| **Proof Layer** | 1–10 rating of credibility signals embedded |
| **CTA Friction Score** | 1–10 (10 = zero friction, effortless to act on) |
| **Algorithm Alignment** | 1–10 (formatting, length, link handling, hashtag strategy) |
| **Voice Consistency** | 1–10 match to user's established brand voice |

**Section 3 — Posting Guidance**
- **Recommended posting window**: Based on ICA's likely active hours (default: Tuesday–Thursday, 7:30–9:00 AM in the ICA's primary timezone)
- **First 60 minutes plan**: 2–3 engagement actions to boost initial distribution
- **Comment-section prompt**: A pre-written first comment to seed conversation or place a link

If the user requested multiple variants, each gets its own numbered section with a brief rationale for when to use it.

### 4C: Offer amends

After delivering the document, ask:

> "Any changes before we send it somewhere?"

If yes — make the requested amends to the document. Repeat until the user is happy or explicitly passes.

### 4D: Distribute via connector

Once the user is satisfied (or skips amends), check `context.connectors` from Step 1.

Work through available connectors in this priority order and offer the most applicable:
1. **Hootsuite / Buffer / scheduling tool** — offer to schedule the post directly
2. **Google Drive / Notion / Dropbox** — offer to save the document
3. **Slack / Teams** — offer to send to a channel
4. **Email** — offer to send as an attachment

Present only what's actually available in `context.connectors`. If nothing is connected:
> "I don't see any connected services. You can copy the post from the document above, or let me know where you'd like to save it and I can help you set up a connector."

Do not post to LinkedIn directly — the document is the deliverable. LinkedIn is the user's action.

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
FutureProof:save_experiment(skill="linkedin-post-writer", experiment={
  hypothesis: "Story-driven hooks with a specific emotional moment outperform declarative/statistic hooks for this user's ICA segment",
  variants: ["control: declarative hook ('Most founders get pricing wrong')", "variant: narrative hook ('I lost my biggest client over a $50/month price increase')"],
  measurement: "Impressions, engagement rate (reactions + comments / impressions), and profile visits within 48 hours of posting",
  expected_impact: "25% increase in engagement rate and 15% increase in profile visits"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="linkedin-post-writer",
  query="LinkedIn algorithm ranking factors and high-engagement post patterns Q3-Q4 2024, including impact of dwell time, comment velocity, and format-specific reach benchmarks",
  reason="Platform algorithm and user behaviour evolve rapidly; maintain evidence-based formatting and structural recommendations"
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
FutureProof:save_session(skill="linkedin-post-writer", session={
  summary: "Drafted LinkedIn post on [topic] targeting [ICA segment] with [format type] structure, optimised for [strategic objective]. Brand voice: [tone notes]. ICA: [ICA description]. Constraints: [any stated exclusions]. Amends: [any changes made]. Next session defaults: [3-5 things to pre-fill next time]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints e.g. direct no emojis]",
    "ICA: [ICA description]",
    "Hook: [hook type and angle]",
    "CTA: [CTA type used]"
  ],
  metadata: { topic: "[topic]", objective: "[strategic objective]" }
})
```