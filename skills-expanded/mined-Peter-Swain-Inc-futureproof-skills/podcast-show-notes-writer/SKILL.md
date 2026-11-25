---
name: podcast-show-notes-writer
description: |
  Generates a full podcast show notes package — short-form directory description,
  long-form blog notes with timestamps and pull quotes, social companion posts,
  newsletter snippet, and SEO metadata — optimized for Apple Podcasts, Spotify,
  and YouTube discoverability. Use when a user says "write show notes for this
  episode", "draft the episode description from this transcript", or shares a
  recording outline for publishing. Post-recording written assets, not live scripts.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="podcast-show-notes-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including podcast brand voice, ICA profile, recurring segment structures, preferred platforms, and historical performance patterns from prior episodes.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Episode source material** — share the full transcript, recording summary, detailed outline, or guest briefing document
- **Guest details** — guest name, title, organisation, key bio points, and links (website, social handles, books, resources mentioned)
- **Episode metadata** — episode number, season, series/theme if applicable, planned publish date
- **Distribution channels** — where will these show notes appear? (Apple Podcasts, Spotify, YouTube, podcast website/blog, newsletter, social media)
- **Conversion objective** — what should the listener do after consuming? (subscribe, visit a landing page, book a call, download a lead magnet, share the episode, join a community)
- **Any standing instructions** — recurring segments, sponsor reads, standard CTAs, or brand-specific formatting requirements not yet captured in FutureProof context

If the user has prior sessions, pre-populate known defaults and confirm: *"Based on your previous episodes, I'll use [brand voice / format / CTA structure]. Confirm or override."*

## Step 3: Extract Episode Architecture

Before writing, systematically deconstruct the source material into a structured episode map:

1. **Core thesis** — the single transformative insight or argument the episode delivers
2. **Key topic segments** — identify 4–7 discrete thematic blocks with precise timestamp markers (or logical sequence if timestamps unavailable)
3. **Quotable moments** — extract 3–5 high-impact guest or host quotes verbatim, noting context
4. **ICA pain points addressed** — map specific listener problems the episode solves, using the ICA's own vocabulary and framing
5. **Tactical takeaways** — isolate concrete, actionable frameworks, tools, methods, or steps the listener can implement immediately
6. **Resources & references** — catalogue every book, tool, person, study, company, or concept mentioned with verifiable details
7. **Narrative arc** — identify the emotional/intellectual journey: opening hook → tension/problem → exploration → resolution/insight → call to action

Apply any user-specific `instructions` from FutureProof context (e.g., tone guidelines, keyword priorities, excluded topics, sponsor integration rules).

## Step 4: Deliver Output

Produce a **Podcast Show Notes Package** containing the following named deliverables:

### Deliverable 1: Platform-Optimised Episode Description (Short-Form)

- 150–250 words for podcast directory listings (Apple Podcasts, Spotify)
- Opens with a compelling hook that surfaces the ICA's primary pain point within the first sentence
- Incorporates 3–5 target keywords naturally for search discoverability
- Ends with a single, specific CTA aligned to the stated conversion objective
- Formatted with line breaks for mobile readability — no dense paragraphs

### Deliverable 2: Long-Form Show Notes (Blog/Website)

- 600–1,200 words structured for both skimmers and deep readers
- **Sections include:**
  - **Episode summary** (2–3 paragraphs situating the episode's relevance to the ICA)
  - **Timestamped topic guide** (clickable chapter markers with descriptive labels)
  - **Key takeaways** (5–7 bullet points, each a complete actionable statement — not vague themes)
  - **Notable quotes** (formatted as pull quotes with speaker attribution)
  - **Guest bio** (2–3 sentences plus credential proof points)
  - **Resources mentioned** (hyperlinked list, verified where possible)
  - **Transcript availability note** (if applicable)
  - **CTA block** (primary conversion action + secondary engagement prompt)
- SEO-optimised: includes target keywords in H2 headings, meta description draft (155 characters), and suggested URL slug

### Deliverable 3: Social Media Companion Assets

- **Twitter/X thread** (5–7 posts): opens with a pattern-interrupt hook, delivers micro-insights from the episode, closes with episode link + CTA
- **LinkedIn post** (1 post, 150–200 words): professional framing, positions the episode insight within an industry trend, includes guest tag placeholder
- **Instagram/Stories caption** (1 post, 80–120 words): conversational tone, uses a question or bold claim to drive saves and shares
- **Audiogram quote card copy** (3 options): the most shareable 15–30 second quote excerpts with suggested visual text overlay copy

### Deliverable 4: Newsletter Snippet

- 100–150 words designed for insertion into an existing email newsletter
- Follows the structure: context hook → what they'll learn → single CTA button text + link placeholder
- Written to maximise click-through, not summarise the entire episode

### Deliverable 5: SEO & Discoverability Metadata

- **Suggested episode title** (if not finalised): 2–3 options balancing keyword inclusion with curiosity-driven engagement
- **Meta description** (155 characters max)
- **Target keywords** (primary + 3–4 secondary long-tail phrases)
- **Suggested tags/categories** for podcast directories
- **Internal linking suggestions** — recommend 2–3 prior episodes to cross-reference based on thematic overlap (if episode history available in FutureProof context)

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Quality Assurance Review

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Before finalising, validate the package against these criteria:

| Dimension | Standard | Pass/Fail |
|---|---|---|
| **ICA resonance** | Language mirrors the ICA's vocabulary; pain points are named, not abstracted | ✓/✗ |
| **Accuracy** | All quotes are verbatim; no fabricated claims, statistics, or attributions | ✓/✗ |
| **SEO integration** | Keywords appear in title, H2s, first 100 words, and meta description without keyword stuffing | ✓/✗ |
| **CTA specificity** | Every deliverable ends with a single, frictionless, measurable next step | ✓/✗ |
| **Platform compliance** | Character limits, formatting norms, and tone match each distribution channel | ✓/✗ |
| **Brand voice consistency** | Tone, terminology, and positioning align with established podcast brand guidelines | ✓/✗ |
| **Guest representation** | Guest credentials and contributions are accurately and favourably represented | ✓/✗ |

Flag any dimension that fails and revise before delivery.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="podcast-show-notes-writer", experiment={
  hypothesis: "Leading the short-form episode description with a direct ICA pain-point question instead of a topic statement increases click-to-listen rate",
  variants: ["control: topic-statement opening (e.g., 'In this episode we discuss...')", "variant: pain-point question opening (e.g., 'Struggling to convert listeners into customers?')"],
  measurement: "Click-to-listen rate and average listen duration across next 5 episodes per variant",
  expected_impact: "20% increase in click-to-listen rate from podcast directory listings"
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
FutureProof:request_research(skill="podcast-show-notes-writer",
  query="Podcast SEO best practices 2024–2025: transcript indexing by Apple and Spotify, keyword strategies for audio search, and show notes structures correlated with highest episode discoverability and listener retention",
  reason="Ensure show notes methodology reflects current platform algorithm behaviour and evolving podcast discovery patterns"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="podcast-show-notes-writer", session={
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