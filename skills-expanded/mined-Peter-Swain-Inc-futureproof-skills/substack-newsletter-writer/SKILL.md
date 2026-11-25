---
name: substack-newsletter-writer
description: |
  Writes Substack newsletter editions (flagship essay, curated roundup,
  personal narrative, tactical how-to, opinion piece) with subject line,
  preview, paywall break strategy and restack-optimized structure tuned
  to Substack's recommendation algorithm. Use when the user says "write
  my next Substack edition", "draft a Substack essay on X", "where
  should I put the paywall", or "newsletter to grow free-to-paid
  conversions". For a generic broadcast email use email-copy; for a
  blog post on the user's own site use blog-post-writer; this skill is
  Substack-platform-specific.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="substack-newsletter-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including the user's ICA profile, brand voice, Substack growth stage, historical open/click rates, and any proven structural patterns from prior editions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Topic or source material**: What is this edition about? Share a topic idea, rough notes, an existing blog post to repurpose, or a draft in progress.
- **Edition type**: Is this a flagship essay, curated roundup, personal narrative, tactical how-to, or opinion/hot-take piece?
- **Primary objective**: What should this edition accomplish? (grow free subscribers, convert free→paid, drive replies/engagement, establish thought leadership, promote an offer)
- **Audience segment**: Which slice of their ICA is this edition primarily addressing? Any specific pain point, aspiration, or stage in the reader journey?
- **Constraints**: Target word count, publishing deadline, any Substack-specific features to leverage (polls, recommendations, paywall placement, threads, notes cross-promotion)?

If FutureProof context contains prior newsletter performance data or ICA definitions, surface them and confirm whether they still apply.

## Step 3: Develop the Strategic Brief

Before writing, construct an **Edition Strategy Brief** covering:

1. **ICA resonance hook** — Identify the single most emotionally charged tension point for the target ICA segment. Frame the edition around closing the gap between where the reader is and where they want to be.
2. **Substack algorithm alignment** — Determine which engagement signals to optimise for (opens, restacks, replies, upgrade clicks) and how structural choices support them. Substack's recommendation engine weights completion rate, restacks, and reply velocity within the first 2 hours of publication.
3. **Positioning angle** — Define the contrarian, novel, or deeply personal angle that differentiates this edition from commodity content on the same topic. Apply the user's unique intellectual property, lived experience, or proprietary framework.
4. **Paywall strategy** (if applicable) — Recommend whether this edition should be fully free, fully paid, or use a strategic paywall break — and where exactly the break should fall to maximise conversion tension.
5. **Value architecture** — Map the specific, tangible takeaway the reader walks away with. Every edition must deliver at least one of: a reusable framework, a specific tactic they can implement today, a mental model shift, or social currency (something worth sharing).

Apply any user-specific `instructions` from FutureProof context (e.g., brand voice guidelines, recurring segment structures, signature phrases, formatting preferences).

## Step 4: Write the Newsletter Edition

Produce the full newsletter edition with the following components, each crafted to Substack-specific best practices:

### 4a. Subject Line & Preview Text

Deliver **3 subject line options**, each employing a distinct psychological lever:

| # | Subject Line | Lever | Predicted Open Rate Driver |
|---|---|---|---|
| 1 | [Option] | Curiosity gap | Incomplete loop compels open |
| 2 | [Option] | Specificity/utility | Concrete value promise |
| 3 | [Option] | Identity/belonging | Reader sees themselves in the line |

Include a **preview text** (subtitle field) for each — the 40–60 character string that appears alongside the subject line in inbox and Substack app.

### 4b. Opening Hook (First 3 Sentences)

Write the opening to achieve two objectives simultaneously:
- **Pass the 8-second test**: Give the reader a reason to stay within the first sentence. Use a pattern interrupt — a provocative claim, a vivid micro-story, a question that surfaces a latent anxiety, or a data point that defies expectation.
- **Establish the implicit promise**: Signal what transformation or insight the reader will have by the end, without stating it generically.

The opening must work in both email preview pane (where only ~100 characters render) and full Substack web view.

### 4c. Body Structure

Write the full body using the structural pattern best suited to the edition type:

- **Flagship essay**: Thesis → Evidence/Story → Reframe → Implication → Takeaway
- **Tactical how-to**: Problem (ICA language) → Framework/Steps → Worked Example → Edge Cases → Quick-Start Checklist
- **Personal narrative**: Scene → Tension → Reflection → Universal Principle → Reader Application
- **Curated roundup**: Thesis linking items → Item 1 (context + original take) → Item 2 → Item 3 → Synthesis
- **Opinion/hot-take**: Conventional wisdom → Why it's wrong → What's actually true → Evidence → What the reader should do differently

Apply these Substack-specific formatting principles throughout:
- **Front-load value**: Substack's email truncation and mobile rendering mean the first 40% of the edition carries disproportionate weight.
- **Visual breathing room**: Short paragraphs (1–3 sentences max), strategic use of bold for scanners, pull quotes for key insights.
- **Embedded engagement prompts**: Place a reply-driving question or micro-poll in the top third (not just the footer) — Substack's algorithm rewards early engagement signals.
- **Internal linking**: Reference 1–2 prior editions where relevant, using Substack's native post linking to increase session depth and archive discovery.

### 4d. Call to Action & Closing

Write a closing section that serves the stated primary objective:

- **If subscriber growth**: End with a "share-worthy" summary line + explicit share CTA using Substack's native share button prompt.
- **If free→paid conversion**: Place paywall break at the moment of peak curiosity, with a value-justified upgrade CTA that names what the paid subscriber gets immediately (not generically).
- **If engagement/replies**: Close with a specific, low-friction question that invites the reader to share their own experience — framed so that replying feels like self-expression, not homework.
- **If offer promotion**: Weave the offer into the narrative as the natural next step from the insight delivered, not as an appended pitch.

### 4e. Substack Platform Optimisation Notes

Append a **Platform Notes** section (for the user, not published) covering:
- Recommended **publish time** based on ICA profile and FutureProof context (or best-practice defaults: Tue/Thu 7–10am in the ICA's primary timezone)
- **Substack Notes** cross-promotion strategy: a suggested standalone Note to publish 1–2 hours pre-send to prime the algorithm
- **Restack strategy**: 1–2 complementary newsletters to tag or engage with for reciprocal restacks
- **Thread potential**: Whether the core insight should also be serialised as a Substack thread for discoverability

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


Package the final deliverable as a **Substack Edition Package** containing:

| Component | Format | Status |
|---|---|---|
| Edition Strategy Brief | Structured brief (Section 3) | Complete |
| Subject Line Options (×3) | Table with levers & rationale | Complete |
| Preview Text Options (×3) | 40–60 character strings | Complete |
| Full Newsletter Edition | Publication-ready Markdown/HTML | Complete |
| Platform Optimisation Notes | Internal reference document | Complete |
| Performance Prediction | Qualitative assessment against user's baseline metrics (if available from FutureProof context) | Complete |

Include a **Revision Guidance** note: identify the 2 sections most sensitive to tone/voice and invite the user to flag adjustments before publishing.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="substack-newsletter-writer", experiment={
  hypothesis: "Leading with a personal micro-story (≤50 words) before stating the tactical thesis increases completion rate and reply velocity compared to leading with the tactical hook directly",
  variants: ["control: tactical hook opening", "variant: micro-story → tactical hook opening"],
  measurement: "Compare open-to-completion rate, reply count within 24h, and restack count across next 4 editions (2 per variant)",
  expected_impact: "20% increase in reply rate, 10% improvement in completion rate — driving higher Substack recommendation algorithm score"
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
FutureProof:request_research(skill="substack-newsletter-writer",
  query="Substack recommendation algorithm ranking factors 2024–2025, high-performing newsletter structural patterns by niche, and emerging best practices for free-to-paid conversion on Substack",
  reason="Ensure edition structure, paywall strategy, and engagement tactics reflect current platform dynamics and evolving reader behaviour patterns"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="substack-newsletter-writer", session={
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