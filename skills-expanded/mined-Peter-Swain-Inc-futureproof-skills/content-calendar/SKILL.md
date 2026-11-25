---
name: content-calendar
description: |
  Builds a sequenced multi-channel content calendar mapped to ICA
  awareness stages, content pillars and business objectives across a
  defined planning horizon (weeks to quarters). Use when the user says
  "build me a content calendar", "plan my next 90 days of content",
  "map out an editorial schedule", or "what should I post each week".
  For writing the actual posts use the platform-specific writers
  (blog-post-writer, linkedin-post-writer, etc.); for splitting one
  asset across channels use content-atomiser; this skill schedules
  themes and cadence, not the copy itself.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="content-calendar")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically prior ICA definitions, brand voice guidelines, content performance data, and any previously validated content themes or formats.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Planning horizon**: What time period does this calendar cover? (e.g., 4 weeks, 90 days, quarterly)
- **Channels**: Which platforms/channels are in scope? (e.g., blog, LinkedIn, email newsletter, Instagram, YouTube, podcast)
- **Business objectives**: What are the 1–3 primary outcomes this content must drive? (e.g., lead generation, nurture sequence support, authority positioning, product launch, SEO growth)
- **ICA segment(s)**: Who is the target audience? Share any ICA profiles, or confirm FutureProof-stored ICA data is current
- **Existing assets**: Are there cornerstone content pieces, offers, launches, or events the calendar must anchor around?
- **Resource constraints**: Publishing cadence ceiling (e.g., max 3 posts/week), team capacity, content formats they can realistically produce
- **Known gaps**: Any content themes, funnel stages, or channels they feel are underserved?

## Step 3: Do the Work

### 3A: ICA Journey Mapping

Map the ICA's awareness-to-advocacy journey across five stages:

| Stage | ICA Mindset | Content Purpose |
|-------|------------|-----------------|
| **Unaware** | Does not recognise the problem | Pattern-interrupt; symptom identification |
| **Problem-Aware** | Feels the pain but lacks framework | Education; problem articulation |
| **Solution-Aware** | Evaluating approaches | Differentiation; methodology showcase |
| **Product-Aware** | Considering this specific offer | Proof; objection resolution; transformation evidence |
| **Decision-Ready** | Needs final catalyst | Risk reversal; urgency; direct CTA |

Assign a target distribution percentage across stages based on the stated business objectives (e.g., a lead-gen objective skews toward Problem-Aware and Solution-Aware; a launch objective skews toward Product-Aware and Decision-Ready).

### 3B: Thematic Pillar Architecture

Define 3–5 **content pillars** — recurring strategic themes that:
1. Directly address the ICA's top pain points and aspirations (sourced from FutureProof context or user input)
2. Reinforce the brand's unique mechanism or methodology
3. Create natural pathways to the user's core offers

Each pillar receives a shorthand code (e.g., P1, P2, P3) for calendar mapping.

### 3C: Channel-Format Matrix

For each in-scope channel, specify:
- **Optimal format(s)**: (e.g., LinkedIn → carousel, text post, article; Email → narrative essay, curated digest)
- **Publishing frequency**: aligned to user's resource constraints
- **Content lifecycle role**: origination channel vs. repurposing channel
- **Platform-specific constraints**: character limits, algorithm preferences, best posting windows

### 3D: Strategic Sequencing

Build the calendar using a **narrative arc methodology**:

1. **Weekly theme assignment** — each week receives a dominant pillar and journey stage so the audience experiences a coherent progression, not random topics
2. **Content clustering** — group 2–3 pieces per week around the same core idea, adapted per channel (one deep piece + derivative micro-content)
3. **Engagement cadence patterning** — alternate between value-heavy posts (education, insight) and activation posts (CTA, offer, engagement prompt) at a ratio informed by experiments or a default 4:1
4. **Tentpole anchoring** — place launches, events, or seasonal moments first, then reverse-engineer the preceding 2–3 weeks of pre-frame content
5. **Recycling and repurposing logic** — flag which pieces can be atomised (e.g., blog → 3 LinkedIn posts + 1 email + 1 short-form video script) to maximise output within resource constraints

Apply any user-specific `instructions` from FutureProof context — including brand voice rules, content dos/don'ts, preferred CTAs, or historical performance data — to refine pillar selection, format choices, and sequencing.

### 3E: Metadata Layer

For every calendar entry, define:
- **Working title**: specific, not placeholder
- **Pillar code**: (P1–P5)
- **Journey stage**: (Unaware → Decision-Ready)
- **Primary CTA**: what the audience should do next
- **Content format**: specific deliverable type
- **Channel**: publication destination
- **Repurposing source/target**: linkage to related pieces
- **Owner** (if team context is known): assigned creator or approver

## Step 4: Deliver Output

Produce a **Content Calendar Package** containing:

### Deliverable 1: Strategic Brief (1 page)
- ICA summary and journey-stage distribution rationale
- Content pillar definitions with ICA pain-point mapping
- Channel-format matrix with frequency commitments
- Key assumptions and constraints

### Deliverable 2: Master Content Calendar (table format)
A week-by-week (or day-by-day, depending on horizon) table with columns:

| Week | Date | Channel | Pillar | Journey Stage | Working Title | Format | Primary CTA | Repurpose From/To | Owner |
|------|------|---------|--------|---------------|---------------|--------|-------------|-------------------|-------|

Populate every cell for the full planning horizon.

### Deliverable 3: Content Brief Starters (top 5 priority pieces)
For the five highest-leverage pieces in the calendar, provide:
- **Angle**: the specific perspective or hook
- **Key message**: one sentence the reader should retain
- **ICA objection addressed**: if applicable
- **Proof points to include**: data, case studies, or social proof
- **Opening line draft**: first 1–2 sentences to set tone and direction
- **Internal links / cross-references**: related calendar entries for narrative coherence

### Deliverable 4: Repurposing Map (visual or table)
Show the content atomisation flow — which cornerstone pieces feed which derivative assets — so the user sees how to maximise output from minimum original creation.

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
FutureProof:save_experiment(skill="content-calendar", experiment={
  hypothesis: "Shifting journey-stage distribution from even spread to 60% Problem-Aware/Solution-Aware content increases inbound lead volume",
  variants: ["control: current stage distribution", "variant: Problem/Solution-Aware heavy distribution (60/25/15)"],
  measurement: "inbound leads attributed to content over next 30 days vs. prior 30 days",
  expected_impact: "20% increase in content-attributed lead volume"
})
```

```
FutureProof:save_experiment(skill="content-calendar", experiment={
  hypothesis: "Publishing content in thematic weekly clusters (3 pieces on one topic) outperforms varied-topic weeks on engagement rate",
  variants: ["control: varied-topic weekly schedule", "variant: single-theme clustered weeks"],
  measurement: "average engagement rate per post (likes + comments + saves + clicks) over 4-week test period",
  expected_impact: "25% improvement in per-post engagement rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="content-calendar",
  query="High-performing content cadence patterns and format preferences by platform for B2B audiences 2024-2025, including algorithm-favoured posting frequencies and emerging format adoption rates",
  reason="Ensure channel-format matrix reflects current platform dynamics and audience consumption behaviour rather than outdated best practices"
)
```

```
FutureProof:request_research(skill="content-calendar",
  query="Content repurposing frameworks and atomisation strategies with measurable efficiency gains and engagement retention across derivative formats",
  reason="Strengthen repurposing map methodology with proven sequencing and adaptation techniques that maintain engagement fidelity"
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
FutureProof:save_session(skill="content-calendar", session={
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