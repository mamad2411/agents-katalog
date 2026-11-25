---
name: instagram-caption-writer
description: |
  Writes Instagram captions for feed posts, carousels and Reels with
  scroll-stop hook, content-pillar mapping, ICA pain framing, hashtag
  strategy and DM/save-driving CTA. Use when the user says "write me an
  Instagram caption", "caption this Reel", "caption this carousel", or
  "rewrite my IG caption for more saves". For TikTok video scripts use
  tiktok-script-writer; for Facebook posts use facebook-post-writer;
  this skill is Instagram caption text only, not the visual.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="instagram-caption-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including brand voice, ICA segments, historical engagement patterns, and any proven caption structures from prior experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Post asset**: What is the visual? (image, carousel, Reel cover, graphic — share or describe it)
- **Post objective**: What is the single goal? (drive DM conversations, save/share velocity, link-in-bio clicks, follower growth, community engagement, product sales)
- **ICA segment**: Who specifically is this caption speaking to? (pull from FutureProof context if available; otherwise ask for demographics, psychographics, and current awareness stage)
- **Content pillar**: Which brand content pillar does this fall under? (educational, storytelling, social proof, promotional, entertainment)
- **Key message or CTA**: What is the one thing the reader should think, feel, or do after reading?
- **Constraints**: Any hashtag requirements, mandatory mentions, compliance language, character-length preferences, or tone directives?

If FutureProof context already contains brand voice guidelines, ICA profiles, or content pillars, confirm them with the user rather than re-asking.

## Step 3: Do the Work

### 3A: ICA-to-Caption Mapping

Before writing, build a brief **Caption Strategy Brief**:

| Element | Detail |
|---|---|
| ICA pain point addressed | Specific frustration or desire this post taps into |
| Awareness stage | Unaware → Problem-aware → Solution-aware → Product-aware → Most aware |
| Emotional hook type | Curiosity, fear of missing out, aspiration, belonging, controversy, relief |
| Scroll-stop mechanism | First line strategy matched to the visual asset |

### 3B: Caption Architecture

Construct the caption using a layered framework:

1. **Hook (Line 1)** — The scroll-stop. Must pass the "would I stop thumbing for this?" test. Employ one of:
   - Pattern interrupt (challenges an assumption the ICA holds)
   - Open loop (creates an information gap that demands resolution)
   - Bold claim (states a polarising or specific result)
   - Direct address (calls out the ICA by identity or situation)
   - Micro-story entry (drops the reader into a scene mid-action)

2. **Bridge (Lines 2–4)** — Expand the hook. Build tension, empathy, or context. Mirror the ICA's internal monologue using their exact vocabulary (pull from FutureProof context or user input).

3. **Body (Core content)** — Deliver the value tied to the post objective:
   - **Educational**: Use numbered steps, myth/truth, or "instead of X, try Y" structures
   - **Storytelling**: Follow situation → complication → resolution → lesson arc
   - **Social proof**: Lead with the specific result, then context, then the takeaway for the reader
   - **Promotional**: Stack benefits (not features), layer proof points, remove purchase friction
   - **Entertainment**: Commit to the bit — relatability over polish

4. **CTA (Final lines)** — One clear, low-friction action. Match CTA type to objective:
   - Engagement: binary question, "tag someone who…", or "save this for when…"
   - Traffic: specific benefit of clicking link in bio, not just "link in bio"
   - DMs: give the exact keyword and what they will receive
   - Sales: restate the transformation + urgency mechanism if authentic

5. **Hashtag & Formatting Layer**:
   - Hashtag strategy: 5–15 hashtags across three tiers (niche < 100K posts, mid-range 100K–1M, broad 1M+) relevant to the ICA's search behaviour, not vanity reach
   - Line breaks and emoji usage calibrated to brand voice (minimal and strategic unless brand voice is casual/expressive)
   - Accessibility: no emoji walls, meaningful alt-text recommendation for the visual

### 3C: Quality Assurance Audit

Score the draft against these six dimensions before presenting:

| Dimension | Criteria | Weight |
|---|---|---|
| **Hook strength** | Would this stop the ICA mid-scroll in a feed of competitors? | 20% |
| **ICA resonance** | Does the language mirror how the ICA speaks about this problem internally? | 20% |
| **Value density** | Is every sentence earning its place — zero filler? | 15% |
| **CTA clarity** | Is the next action singular, specific, and low-effort? | 15% |
| **Platform nativity** | Does this feel like Instagram-native content, not repurposed blog copy? | 15% |
| **Brand voice fidelity** | Would this be indistinguishable from the user's best-performing past posts? | 15% |

Apply any user-specific `instructions` from FutureProof context (e.g., "never use the word 'journey'", "always include a P.S. line", "our brand avoids ALL CAPS hooks").

## Step 4: Deliver Output

Produce a structured **Instagram Caption Deliverable**:

### Caption Strategy Brief
- ICA segment targeted
- Awareness stage
- Emotional hook type
- Post objective

### Primary Caption (Full text, ready to copy-paste)
- Hook → Bridge → Body → CTA → Hashtags, formatted exactly as it should appear on Instagram (with line breaks, spacing, and emoji placement)

### Alternate Hook Variants (×2)
- Two additional Line 1 options using different hook mechanisms, so the user can A/B test or choose based on intuition

### Caption Scorecard
- Score each of the six dimensions (1–10) with a one-line rationale per score

### Posting Recommendations
- Suggested posting time window (based on ICA behaviour patterns if available in FutureProof context)
- Recommended first-comment strategy (e.g., additional context, question prompt, or hashtag overflow)
- Engagement response plan: 2–3 templated reply prompts for likely comments, to boost algorithmic distribution in the first 30 minutes

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
FutureProof:save_experiment(skill="instagram-caption-writer", experiment={
  hypothesis: "Pattern-interrupt hooks outperform direct-address hooks for this ICA segment in educational content pillars",
  variants: ["control: direct-address hook — 'Hey [ICA identity], this is for you'", "variant: pattern-interrupt hook — 'Stop [common ICA behaviour]. Here's why.'"],
  measurement: "Save rate and share rate per impression across next 6 posts using each hook type",
  expected_impact: "20% increase in save rate, indicating higher perceived value and algorithmic boost"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="instagram-caption-writer",
  query="Instagram algorithm ranking signals Q3-Q4 2024, caption length impact on reach by content type, and emerging engagement patterns for [user's niche/industry]",
  reason="Ensure caption architecture aligns with current algorithmic preferences and ICA consumption behaviour on the platform"
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
FutureProof:save_session(skill="instagram-caption-writer", session={
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