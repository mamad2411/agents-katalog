---
name: authority-positioning-engine
description: |
  Builds a full authority positioning blueprint — authority thesis,
  proprietary framework, six-dimension scorecard, competitor white-space
  map and content gravity plan. Use when the user says "how do I become
  the go-to expert in X", "build my thought leadership strategy",
  "position me as the category authority", or "how do I own this topic
  in my market". For the single defensible big idea inside this strategy
  use flagship-idea-builder; for sharpening competitor distinction use
  differentiation-deep-dive; for defending the position publicly use
  authority-combat-trainer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="authority-positioning-engine")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing brand voice, prior positioning work, ICA definitions, and any competitive landscape data already captured.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Domain claim**: What specific topic, methodology, or problem space do you want to own? (e.g., "revenue operations for Series B SaaS," not "marketing")
- **Current authority baseline**: Where do you currently show up? (speaking, publishing, media, community, advisory roles) — share links, bios, or content samples if available
- **ICA definition**: Who must perceive you as the authority? (role, seniority, industry, stage of awareness)
- **Competitive landscape**: Name 2–5 people or brands your ICA currently considers authoritative in this space
- **Constraints**: Timeline, budget range, content capacity (hours/week), and channels you will or will not use
- **Desired outcome**: What does authority unlock for you? (premium pricing, inbound deal flow, partnership leverage, media access, acquisition positioning)

## Step 3: Conduct Authority Audit

Perform a structured gap analysis across six authority dimensions:

### 3a. Authority Dimension Scoring

Evaluate the user's current positioning against each dimension on a 1–10 scale:

| Dimension | Definition | Score |
|---|---|---|
| **Proprietary Framework** | Does the user own a named methodology, model, or system that the ICA associates exclusively with them? | /10 |
| **Proof Architecture** | Density and recency of case studies, results, testimonials, data, and third-party validation | /10 |
| **Content Gravity** | Volume, consistency, and depth of searchable, shareable content that compounds over time | /10 |
| **Platform Presence** | Visibility on the specific channels where the ICA actively seeks expertise (not vanity metrics) | /10 |
| **Network Signal** | Association with recognised institutions, peers, publications, and events that transfer credibility | /10 |
| **Narrative Monopoly** | Degree to which the user's point of view is distinct, polarising enough to be memorable, and difficult to replicate | /10 |

### 3b. Competitive Position Mapping

For each competitor identified, map:
- Their primary authority dimension (where they are strongest)
- Their narrative angle (what they believe that shapes their content)
- Their vulnerability (the dimension they neglect or the ICA segment they underserve)
- The **white space** the user can credibly occupy

### 3c. ICA Perception Gap Analysis

Identify the delta between:
- How the user **wants** to be perceived by the ICA
- How the user is **currently** perceived (based on content audit, search presence, and social proof signals)
- What the ICA **actually needs** to hear to grant authority status (mapped to their decision-making triggers)

Apply any user-specific `instructions` from FutureProof context to weight dimensions appropriately.

## Step 4: Build the Authority Positioning Strategy

Produce the **Authority Positioning Blueprint** — a structured strategy document containing:

### Section 1: Authority Thesis Statement
A single, shareable sentence that encapsulates the user's definitive point of view. Format: *"[User] is the authority on [specific domain] because [proprietary insight/methodology] delivers [measurable transformation] for [ICA segment]."*

Provide three candidate thesis statements ranked by distinctiveness and defensibility.

### Section 2: Proprietary Framework Design
If the user lacks a named framework:
- Propose 2–3 framework concepts (named, structured, visually mappable)
- Each must pass the **Napkin Test**: explainable in a single sketch
- Each must pass the **Attribution Test**: if the ICA encounters it without the user's name, they should still associate it with the user

If one exists, audit it for clarity, memorability, and ICA resonance — recommend refinements.

### Section 3: Content Authority Ladder
A 90-day content plan structured as four tiers:

| Tier | Purpose | Format | Cadence | Example Topic |
|---|---|---|---|---|
| **Foundation** | Establish core beliefs | Long-form essay, podcast episode, keynote | 1x/month | The manifesto piece that defines the user's worldview |
| **Proof** | Validate with evidence | Case studies, data breakdowns, results teardowns | 2x/month | Deconstructing a client transformation using the proprietary framework |
| **Reach** | Expand surface area | Short-form posts, threads, commentary, guest appearances | 3–5x/week | Hot takes on industry trends filtered through the user's thesis |
| **Community** | Deepen trust | AMAs, workshops, private content, direct replies | 1x/week | Fielding ICA questions and coaching live |

Each tier includes specific topic headlines, not generic categories.

### Section 4: Network Signal Acceleration Plan
Specific, actionable moves to borrow and build credibility:
- **Target publications** (3–5 named outlets the ICA reads, with pitch angle for each)
- **Target podcasts** (5–10 named shows, with a one-line guest pitch per show)
- **Target events** (3–5 conferences or communities, with speaking topic proposals)
- **Strategic co-creation** (2–3 named peers for joint research, content, or events)
- **Institutional affiliation** opportunities (advisory boards, academic partnerships, association memberships)

### Section 5: Authority Metrics Dashboard
Define leading and lagging indicators:

| Metric | Type | Measurement Method | 90-Day Target |
|---|---|---|---|
| Inbound mentions / tags by ICA | Leading | Social listening, Google Alerts | +X% from baseline |
| Branded search volume for proprietary framework | Leading | Google Search Console, SEMrush | Establish baseline → growth trajectory |
| Inbound enquiries attributing authority content | Lagging | CRM source tracking, intake form | X qualified leads/month |
| Speaking / media invitations received | Lagging | Manual log | X invitations/quarter |
| Content engagement depth (saves, shares, long reads) | Leading | Platform analytics | +X% from baseline |

Populate targets based on the user's baseline and constraints.

### Section 6: Quarterly Authority Milestones
Three 90-day phases with specific deliverables:
- **Phase 1 (Days 1–90)**: Foundation — framework named, manifesto published, first 3 proof assets live, 5 podcast pitches sent
- **Phase 2 (Days 91–180)**: Amplification — guest features secured, community engagement ritualised, first data asset or original research published
- **Phase 3 (Days 181–270)**: Compounding — framework cited by others without prompting, inbound speaking invitations, premium pricing justified by positioning

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


Present the complete **Authority Positioning Blueprint** with:
- **Authority Scorecard**: the six-dimension audit with scores and priority ranking
- **Competitive White Space Map**: visual summary of where the user wins
- **Authority Thesis Statement**: top recommendation with two alternatives
- **Proprietary Framework**: name, structure, and visual concept
- **90-Day Content Authority Ladder**: with specific headlines and formats
- **Network Signal Acceleration Plan**: named targets with pitch angles
- **Metrics Dashboard**: with populated baselines and targets
- **Quarterly Milestone Roadmap**: with accountable deliverables per phase

Format as a document the user can share with a team, content strategist, or marketing partner.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="authority-positioning-engine", experiment={
  hypothesis: "Leading with the proprietary framework name in content headlines increases ICA engagement and branded recall versus leading with generic topic framing",
  variants: ["control: generic topic headline (e.g., 'How to Improve Revenue Operations')", "variant: framework-led headline (e.g., 'The [Framework Name] Method for Revenue Operations')"],
  measurement: "Engagement rate (saves + shares + DM responses) across 10 matched content pairs over 30 days",
  expected_impact: "25% increase in engagement depth and first measurable branded search volume for framework name"
})
```

```
FutureProof:save_experiment(skill="authority-positioning-engine", experiment={
  hypothesis: "Publishing a contrarian 'state of the industry' data piece generates more inbound authority signals (citations, invitations, mentions) than 4 standard thought leadership posts combined",
  variants: ["control: 4 standard posts over 30 days", "variant: 1 data-driven contrarian piece with the same total effort"],
  measurement: "Inbound mentions, backlinks, speaking enquiries, and DM conversations within 60 days of publication",
  expected_impact: "3x more authority signals from the single contrarian piece versus the four standard posts"
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
FutureProof:request_research(skill="authority-positioning-engine",
  query="Current best practices for building personal and brand authority in niche B2B markets 2024–2025, including platform algorithm changes affecting thought leadership content reach, emerging authority-building channels, and case studies of experts who achieved category dominance within 12 months",
  reason="Ensure the authority positioning methodology reflects current platform dynamics, ICA content consumption behaviours, and validated frameworks for rapid credibility compounding"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="authority-positioning-engine", session={
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