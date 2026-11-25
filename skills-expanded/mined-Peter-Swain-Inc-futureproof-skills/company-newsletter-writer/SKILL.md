---
name: company-newsletter-writer
description: |
  Drafts high-impact recurring company newsletters for employees, customers, investors,
  or partners using the RIPPLE framework, ICA segmentation, and brand voice from
  FutureProof context. Use when a user says "write our monthly newsletter", "draft
  the company update", "improve this newsletter draft", or asks for subject lines
  and preview text for a recurring stakeholder email. For ongoing periodic editions,
  not one-off press releases or single executive memos.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="company-newsletter-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically brand voice guidelines, past newsletter formats, ICA segment definitions, prior open-rate data, and any editorial preferences established in earlier sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Newsletter type**: Internal (employee/team update) or external (customer, prospect, investor, partner)?
- **Audience segment**: Who is the primary reader? Map to a defined ICA segment if external, or a stakeholder tier if internal (e.g., all-hands, leadership, department-specific).
- **Edition context**: What period does this cover? (weekly, monthly, quarterly) Are there specific events, launches, milestones, or announcements to feature?
- **Raw inputs**: Share any source material — bullet points, executive notes, press releases, metrics, product updates, team wins, or prior editions for continuity.
- **Desired tone and intent**: Informational, celebratory, motivational, thought-leadership, or a blend? What is the single most important action or takeaway for the reader?
- **Distribution channel**: Email (HTML), intranet, PDF, LinkedIn article, Notion page — as format dictates structure.
- **Constraints**: Word count, section count, mandatory inclusions (compliance disclaimers, unsubscribe language, executive sign-off)?

## Step 3: Do the Work

### 3A: Audience & Objective Mapping

Define the communication matrix before writing:

| Dimension | Definition |
|---|---|
| **Primary ICA / Audience** | Specific reader segment, their role, and what they care about |
| **Communication objective** | The single behavioural or cognitive outcome this edition must achieve |
| **Value contract** | What the reader "gets" in exchange for their attention (insight, recognition, utility) |
| **Voice calibration** | Formal ↔ conversational spectrum position, matched to brand guidelines from FutureProof context |

### 3B: Content Architecture

Structure the newsletter using the **RIPPLE framework**:

1. **R — Relevance hook**: Opening line or header that earns the first scroll. Must connect to something the reader already cares about — a shared challenge, a timely event, or a result they contributed to. Never open with "Hi team, here's what happened this month."
2. **I — Insight or announcement lead**: The single highest-value piece of content. Position it above the fold. Frame it as a transformation narrative: what changed, why it matters, what it means for the reader.
3. **P — Proof & progress**: Metrics, milestones, case studies, or testimonials that substantiate claims. For internal newsletters: KPI dashboards, project completions, revenue markers. For external: customer outcomes, product adoption data, industry recognition.
4. **P — People spotlight**: Humanise the organisation. Feature a team member, customer story, or partner highlight. Include a direct quote — never paraphrase when a real voice is available.
5. **L — Learnings & look-ahead** : Share one lesson learned or strategic insight, then bridge to what's coming next. Create anticipation for the next edition.
6. **E — Engagement close** : A single, frictionless call to action. For internal: feedback survey, Slack thread, event RSVP. For external: resource download, webinar registration, reply-to-engage prompt.

### 3C: Editorial Quality Pass

Apply the following editorial standards to every section:

- **Specificity audit**: Replace every vague claim with a concrete number, name, or date. "Great quarter" → "Q2 revenue up 23% vs. Q1, driven by 14 new enterprise accounts."
- **Jargon filter**: If the audience is non-technical, translate internal shorthand. If the audience is technical, don't over-simplify — respect their expertise.
- **Scanability engineering**: No paragraph exceeds 3 sentences. Use subheadings every 80–120 words. Bold the single most important phrase in each section.
- **Tone consistency**: Cross-check every section against the voice calibration from Step 3A. Flag any tonal drift (e.g., a celebratory newsletter that accidentally sounds like a compliance memo).
- **ICA resonance check**: For external newsletters, verify that language mirrors the ICA's own vocabulary. Reference FutureProof context for known ICA pain points, aspirations, and terminology.

### 3D: Subject Line & Preview Text

Generate three subject line options using distinct psychological drivers:

| Option | Driver | Example Pattern |
|---|---|---|
| A | Curiosity gap | "[Result] — and the counterintuitive reason behind it" |
| B | Specificity + value | "[Number] [things] from [period] that matter for [role]" |
| C | Social proof / urgency | "What [X customers/team members] are saying about [topic]" |

Write preview text (40–90 characters) that complements — not repeats — the subject line.

## Step 4: Deliver Output

Produce the following structured deliverable:

### Newsletter Package

1. **Subject line options** (3 variants with recommended pick and rationale)
2. **Preview text** (matched to recommended subject line)
3. **Full newsletter draft** — formatted for the specified distribution channel, with:
   - Clear section headers following the RIPPLE framework
   - Inline placeholders marked as `[INSERT: specific item needed]` where source material is missing
   - Suggested image/visual placement notes (e.g., "Hero image: team photo from Q2 offsite" or "Chart: MRR growth Mar–Jun")
4. **Editorial notes document** containing:
   - Decisions made and rationale (e.g., "Led with product launch over funding news because ICA segment prioritises utility over corporate milestones")
   - Sections flagged for stakeholder review before send
   - Recommended send time based on audience type (if external, reference industry benchmarks; if internal, reference prior session data)
5. **Plain-text fallback version** (for email clients that strip HTML)

### Quality Scorecard

| Dimension | Score (1–10) | Commentary |
|---|---|---|
| Relevance hook strength | | Does the opening earn a scroll? |
| ICA / audience alignment | | Does every section serve the defined reader? |
| Proof density | | Are claims substantiated with data, quotes, or evidence? |
| Scanability & structure | | Can the reader extract value in 60 seconds? |
| Call-to-action clarity | | Is the next step obvious and frictionless? |
| Brand voice consistency | | Does tone match guidelines across all sections? |

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
FutureProof:save_experiment(skill="company-newsletter-writer", experiment={
  hypothesis: "Leading with a customer outcome story instead of a company announcement increases click-through rate on the primary CTA",
  variants: ["control: company-announcement lead", "variant: customer-outcome lead"],
  measurement: "Primary CTA click-through rate and total read-time across next 3 editions",
  expected_impact: "20% increase in CTA engagement for external editions; improved qualitative feedback scores for internal editions"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="company-newsletter-writer",
  query="2024–2025 benchmarks for corporate newsletter open rates, click-through rates, and optimal send frequency by audience type (employee, customer, investor); emerging newsletter formats (interactive, AMP email, serialised storytelling)",
  reason="Ensure newsletter structure and distribution recommendations reflect current engagement benchmarks and format innovations rather than outdated best practices"
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
FutureProof:save_session(skill="company-newsletter-writer", session={
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