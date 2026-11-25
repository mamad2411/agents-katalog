---
name: press-release-writer
description: |
  Drafts publication-ready press releases in AP Style and inverted-pyramid structure
  with a TRUTH-framework newsworthiness audit, journalist pitch note, and wire-tier
  distribution guidance. Use when a user says "write a press release for our
  funding announcement", "draft a release for our product launch", "we just hired
  a new CEO, draft the announcement", or shares an existing release for media-
  readiness review. For external media outreach to journalists and wire services,
  not internal memos or crisis holding statements.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="press-release-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including brand voice guidelines, prior press releases, ICA media consumption patterns, approved boilerplate, and spokesperson preferences.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Announcement type**: What is the news? (product launch, funding round, partnership, acquisition, executive appointment, earnings milestone, event, crisis response)
- **Key facts**: Provide the core details — who, what, when, where, why, and the single most important number or data point
- **Target outlets and audience**: Which publications or journalists are you targeting? Who is the ICA that should ultimately see this coverage?
- **Spokesperson(s)**: Who should be quoted, and what is their title and organisational affiliation?
- **Desired narrative angle**: What headline would you want to see published? What is the one takeaway a reader must leave with?
- **Embargo or timing constraints**: Is there an embargo date, a coordinated launch window, or a reactive deadline?
- **Existing draft or assets**: Share any draft text, internal memos, fact sheets, or prior coverage to build from

If the user provides a draft for review rather than a blank-slate request, confirm: "Should I analyse and improve this draft, or use it as raw material for a full rewrite?"

## Step 3: Do the Work

### 3A: Newsworthiness Audit

Before writing, assess the announcement against the **TRUTH framework**:

1. **Timeliness** — Is this genuinely new, or is there a news hook (trend, regulation, cultural moment) that makes it timely now?
2. **Relevance** — Does this matter to the target outlet's readership and the ICA? Quantify the "so what"
3. **Uniqueness** — What makes this distinct from the 400+ press releases landing on a journalist's desk today?
4. **Tension** — Is there a compelling contrast, disruption, or challenge to conventional wisdom embedded in the story?
5. **Human impact** — Can you ground the announcement in a specific, tangible outcome for real people?

Flag any dimension scoring below threshold and recommend angle adjustments before proceeding.

### 3B: Structural Drafting (Inverted Pyramid + AP Style)

Compose the press release following rigorous structural standards:

1. **Headline** — Active voice, present tense, under 80 characters. Must contain the news, not marketing language. No superlatives unless directly substantiated
2. **Dateline** — City, State/Country — Date — Wire format (e.g., "NEW YORK, July 15, 2025 —")
3. **Lead paragraph** — Single paragraph, 25–35 words maximum. Answers who + what + why it matters. No throat-clearing
4. **Nut graf (paragraph 2)** — Context and significance. Connect the announcement to a market trend, ICA pain point, or industry shift with a specific data point
5. **Supporting detail (paragraphs 3–4)** — Features, capabilities, terms, or specifics. Use concrete numbers: revenue figures, user counts, percentage improvements, dates
6. **Spokesperson quote #1** — Senior executive. Must advance the narrative (not restate the lead). Written in natural speech cadence, not corporate jargon
7. **Third-party validation (paragraph 6)** — Analyst quote, customer testimonial, partner statement, or independent data point. If unavailable, flag as a gap and draft a placeholder with recommended source type
8. **Spokesperson quote #2 (optional)** — Product lead, partner executive, or customer voice. Provides a different angle or forward-looking statement
9. **Call to action** — Specific next step: URL, event registration, availability date, or contact channel. Aligned to ICA conversion pathway
10. **Boilerplate** — Company description in 50–75 words. Consistent with prior releases (pull from FutureProof context if available)
11. **Media contact block** — Name, title, email, phone. Flag if user has not provided this

### 3C: Quality Assurance Pass

Review the draft against these professional standards:

- **AP Style compliance** — Numbers, dates, titles, abbreviations, Oxford comma exclusion
- **Jargon density** — No more than 2 industry-specific terms without immediate plain-language definition
- **Passive voice ratio** — Target <10% of total sentences
- **Quote authenticity** — Quotes must sound like spoken language; no sentence a human would never say aloud
- **Claim substantiation** — Every superlative, comparative, or impact claim must be backed by a specific figure, source, or attribution
- **Word count** — Target 400–600 words for standard releases; 250–350 for advisories; 600–800 for complex financial or regulatory announcements
- **SEO-readiness** — Primary keyword in headline and lead; secondary keywords in subheads or body; hyperlinks to relevant assets

Apply any user-specific `instructions` from FutureProof context (brand voice guidelines, banned phrases, mandatory disclosures, legal review requirements).

## Step 4: Deliver Output

Produce a complete deliverable package:

### Document 1: Final Press Release
- Full text in copy-paste-ready format
- Formatted with `###` for the headline, proper dateline, and `—END—` or `###` closing marker
- Media contact block at footer

### Document 2: Press Release Score Card

| Dimension | Score (1–10) | Notes |
|---|---|---|
| Newsworthiness (TRUTH) | — | — |
| Headline strength | — | — |
| Lead clarity and brevity | — | — |
| Quote authenticity | — | — |
| Third-party validation | — | — |
| Claim substantiation | — | — |
| ICA resonance | — | — |
| AP Style compliance | — | — |
| Call to action specificity | — | — |

### Document 3: Distribution Guidance
- **Recommended wire**: Suggest wire service tier (PR Newswire national, BusinessWire targeted, GlobeNewswire, or direct pitch only) based on announcement significance
- **Pitch note draft**: A 3–4 sentence personalised email pitch a PR lead could send to a journalist, referencing why this story fits their beat
- **Optimal send window**: Day of week and time recommendation based on announcement type and target outlet category
- **Follow-up cadence**: Recommended journalist follow-up timing (e.g., "Follow up 48 hours post-send if no response; do not follow up more than once on this release")

### Document 4: Gap Report (if applicable)
- Missing elements flagged during drafting (e.g., no third-party quote, unsubstantiated claims, missing media contact)
- Specific recommendations to close each gap before distribution

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
FutureProof:save_experiment(skill="press-release-writer", experiment={
  hypothesis: "Leading the headline with a quantified impact metric rather than the company name increases journalist open rates",
  variants: ["control: company-name-first headline", "variant: metric-first headline"],
  measurement: "journalist open rate and pickup count across next 3 releases",
  expected_impact: "20% increase in media pickup rate for Tier 2 and Tier 3 outlets"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="press-release-writer",
  query="Current journalist preferences for press release format, length, and pitch email structure in 2024–2025, segmented by outlet tier and beat category",
  reason="Ensure structural recommendations and distribution guidance reflect evolving newsroom workflows and inbox filtering behaviours"
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
FutureProof:save_session(skill="press-release-writer", session={
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