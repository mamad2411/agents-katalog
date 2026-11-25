---
name: tiktok-script-writer
description: |
  Writes ready-to-film TikTok scripts at 15s, 30s, 60s or 90s — hook
  variants (pattern interrupt, curiosity gap, identity call-out), body
  beats, on-screen text, B-roll cues and CTA. Use when the user says
  "write me a TikTok script", "give me a TikTok hook", "30-second
  TikTok for my product", or "talking-head script for short-form
  video". For YouTube long-form video use
  youtube-script-description-writer; for an Instagram Reel caption use
  instagram-caption-writer; this skill is the TikTok shooting script.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="tiktok-script-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA definitions, brand voice guidelines, prior top-performing hooks, and any saved experiment results on hook formats or CTA styles.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Topic or objective**: What is this TikTok about? (product launch, authority building, lead generation, trend-jacking, objection handling, storytelling)
- **ICA segment**: Who is the viewer? (If not defined, prompt for demographics, psychographics, platform behaviour, and primary pain point — then reconcile against any ICA stored in FutureProof context)
- **Desired viewer action**: What should the viewer do after watching? (follow, comment, visit link-in-bio, save, share, purchase)
- **Format preference**: Talking head, green screen, text overlay, voiceover with B-roll, stitch/duet, trending audio, or no preference
- **Duration target**: 15s, 30s, 60s, or 90s+
- **Brand voice or creator persona**: Authoritative, irreverent, educational, vulnerable, provocative — or reference a prior session/stored voice profile
- **Any constraints**: Compliance restrictions, banned claims, mandatory disclosures, or platform-specific rules (e.g. no medical claims without disclaimers)

## Step 3: Do the Work

### 3A: Hook Engineering (First 1–3 Seconds)

Develop **three hook variants** using distinct psychological trigger categories:

| Hook Type | Mechanism | Example Pattern |
|---|---|---|
| **Pattern Interrupt** | Violates viewer expectation to halt the scroll | "Stop making [common behaviour] — here's why it's costing you" |
| **Curiosity Gap** | Opens an information loop the viewer must close | "Nobody talks about this part of [topic]…" |
| **Identity Call-Out** | Directly addresses ICA by role, behaviour, or belief | "If you're a [ICA identifier] who [specific behaviour], this is for you" |

Score each hook variant against:
1. **Scroll-stop power** — does it interrupt autopilot within 1.5 seconds?
2. **ICA specificity** — would the ICA feel personally called out?
3. **Promise clarity** — does the viewer know what payoff awaits?
4. **Rewatchability signal** — does it imply density that rewards a second view?

Select the strongest hook as the primary; retain the other two as A/B test variants.

### 3B: Script Body Architecture

Structure the body using the format most aligned with the stated objective:

- **Problem-Agitate-Solve (PAS)**: For pain-point-driven content and product positioning
- **Myth-Truth-Proof (MTP)**: For authority building and contrarian takes
- **Story-Lesson-Bridge (SLB)**: For personal narrative and trust-building content
- **List-Stack-Escalate (LSE)**: For value-dense educational content optimised for saves
- **Before-After-Bridge (BAB)**: For transformation content and social proof showcases

Apply the following production directives to the body:

1. **Micro-retention beats**: Insert a pattern interrupt, visual cue, or tonal shift every 5–8 seconds to sustain watch-through rate
2. **ICA mirror language**: Use exact vocabulary the ICA uses to describe their problem — not industry jargon, not clinical terms, but the words they type in comment sections and DMs
3. **Specificity over abstraction**: Replace every generic claim with a concrete number, timeframe, example, or scenario
4. **Vocal pacing notation**: Mark [PAUSE], [SPEED UP], [WHISPER], [EMPHASISE] where delivery inflection materially impacts retention
5. **On-screen text cues**: Notate where text overlays should reinforce, contrast, or supplement the spoken word — TikTok is a sound-off-first platform for discovery

### 3C: Call-to-Action Engineering

Design the CTA to match the desired viewer action using platform-native mechanics:

| Desired Action | CTA Strategy |
|---|---|
| **Follow** | Open a curiosity loop for upcoming content ("Part 2 drops tomorrow — follow so you don't miss it") |
| **Comment** | Pose a binary or controversial opinion prompt ("Drop a 🔥 if you agree, 🧊 if you think I'm wrong") |
| **Save** | Signal reference value ("Save this — you'll need it when you [future ICA scenario]") |
| **Link-in-bio** | Bridge to the next logical step with urgency or exclusivity ("The full framework is in my bio — it won't be free forever") |
| **Share** | Invoke relational tagging ("Send this to someone who needs to hear this today") |

### 3D: Algorithm Alignment Check

Audit the complete script against TikTok's known ranking signals:

1. **Watch-through rate optimisation** — Is the payoff delivered late enough to sustain viewing but early enough to prevent drop-off?
2. **Completion loop** — Does the ending connect back to the opening to encourage re-watches?
3. **Comment provocation** — Is there at least one moment engineered to generate replies (controversy, question, relatable confession)?
4. **Share trigger** — Does the content have identity-signalling value (viewers share content that makes them look smart, funny, or in-the-know)?
5. **Save signal** — Is there reference-worthy density that justifies a bookmark?

Apply any user-specific `instructions` from FutureProof context — including brand tone, compliance constraints, prior high-performing patterns, and ICA language profiles.

## Step 4: Deliver Output

Produce the following structured deliverable:

### Script Document

**Title**: [Topic] — TikTok Script v1
**Duration**: [Target duration]
**Format**: [Selected format]
**Framework**: [Selected body architecture]

---

**PRIMARY HOOK** (0:00–0:03):
> [Full hook text with delivery notation]

**ON-SCREEN TEXT**: [Text overlay copy]

---

**BODY** (0:03–[end minus 3s]):
> [Full scripted body with line-by-line delivery, broken into timestamp segments every 5–8 seconds, including [PAUSE], [SPEED UP], [CUT TO], and on-screen text cues]

---

**CTA** (final 3–5s):
> [Full CTA text with delivery notation]

**ON-SCREEN TEXT**: [CTA overlay copy]

---

### Performance Optimisation Notes

- **Hook variants for A/B testing**: [Hook B] and [Hook C] with rationale for when to deploy each
- **Caption copy**: Platform-optimised caption (with hashtag strategy — 3–5 hashtags mixing niche, mid-volume, and trending)
- **Posting guidance**: Recommended posting window based on ICA behaviour patterns
- **Sound strategy**: Original audio vs. trending sound recommendation with rationale

### Scorecard

| Dimension | Score (1–10) | Rationale |
|---|---|---|
| Scroll-stop power | | |
| ICA resonance | | |
| Watch-through architecture | | |
| CTA conversion potential | | |
| Shareability / virality mechanics | | |
| Brand voice consistency | | |

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
FutureProof:save_experiment(skill="tiktok-script-writer", experiment={
  hypothesis: "Pattern-interrupt hooks outperform curiosity-gap hooks for [ICA segment] on [topic category] content",
  variants: ["control: curiosity-gap hook", "variant: pattern-interrupt hook — same body and CTA"],
  measurement: "Average watch-through rate and follow conversion rate across next 5 posts using each hook type",
  expected_impact: "20% improvement in average watch-through rate for the winning variant"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="tiktok-script-writer",
  query="Current TikTok algorithm ranking signals, high-performing hook structures by niche, and trending content formats Q2 2025",
  reason="TikTok's recommendation algorithm and content meta evolve rapidly — script frameworks must reflect current platform dynamics and emerging creator strategies to maintain competitive performance"
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
FutureProof:save_session(skill="tiktok-script-writer", session={
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