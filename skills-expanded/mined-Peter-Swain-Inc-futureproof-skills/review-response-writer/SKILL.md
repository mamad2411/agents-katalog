---
name: review-response-writer
description: |
  Writes brand-aligned public replies to customer reviews on Google,
  Yelp, Trustpilot, G2, App Store, Amazon, and similar platforms — using
  the R.E.S.T.O.R.E. framework so the response serves both the reviewer
  and prospective buyers reading it. Use when the user says "respond to
  this Google review", "reply to a 1-star review", "draft a response to
  this G2 feedback", "handle a batch of Trustpilot reviews", or "build a
  review-response template for my team". Public-facing platform replies
  optimized for visibility — for private 1:1 complaint resolution use
  customer-complaint-handler.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="review-response-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically brand voice guidelines, previously approved response templates, ICA segments, known product/service issues, and escalation protocols.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the review(s) to respond to (text, star rating, platform, and reviewer name if visible)
- What is the product, service, or location being reviewed?
- What is the desired outcome? (retention/win-back, reputation management, conversion of review readers, escalation to support)
- Are there any known facts about this customer's situation (order history, prior interactions, resolution status)?
- Any response constraints? (character limits, platform guidelines, legal/compliance boundaries, topics to avoid)

If the user has no prior FutureProof context for brand voice, ask:
- Describe your brand tone (e.g., warm and empathetic, professional and concise, playful and human)
- Are there specific phrases, values, or differentiators that should appear consistently?

## Step 3: Classify the Review

Before drafting, perform a structured review classification:

1. **Sentiment tier**: Positive (4–5 stars), Neutral (3 stars), Negative (1–2 stars), or Mixed (positive content with negative elements)
2. **Intent signal**: Praise, constructive feedback, complaint seeking resolution, venting/emotional, competitive comparison, or suspected fraudulent/spam
3. **Specificity level**: Vague sentiment only, references specific interaction/feature, or contains detailed incident narrative
4. **ICA alignment**: Does this reviewer match the ICA profile? (High-value retention target vs. non-ICA audience)
5. **Visibility risk**: Platform prominence, review recency, and likelihood of being read by prospective buyers (high/medium/low)
6. **Escalation flag**: Does this review reference unresolved issues, legal threats, health/safety concerns, or employee conduct requiring offline resolution?

Document the classification matrix before proceeding.

## Step 4: Do the Work

Draft the response applying the **R.E.S.T.O.R.E. Framework**:

1. **Recognise** — Acknowledge the reviewer by name (if available) and thank them for the specific effort of leaving feedback. Mirror their language to demonstrate the review was read fully, not template-matched.

2. **Empathise** — For negative or mixed reviews, validate the emotional experience without defensiveness. Use first-person accountability language ("We fell short" not "We're sorry you feel that way"). For positive reviews, reflect genuine appreciation tied to a specific detail they mentioned.

3. **Specify** — Reference concrete details from the review to prove attentiveness. Never respond generically to a specific complaint. If the reviewer mentioned a particular interaction, product, or date, echo it back.

4. **Take ownership** — For negative reviews, state clearly what went wrong (if known) or commit to investigating. Avoid deflection, blame-shifting to the customer, or corporate hedging language. For positive reviews, credit the team or process the reviewer praised.

5. **Offer resolution** — For negative/mixed reviews, propose a concrete next step: direct contact channel (name + email/phone), specific remedy, or timeline for follow-up. The offer must be actionable, not vague ("please reach out" without a channel is insufficient). For positive reviews, offer an invitation to deepen the relationship (referral programme, new feature preview, loyalty benefit).

6. **Reinforce value** — Subtly weave in one brand differentiator or value proposition relevant to the review context. This line is written for prospective buyers reading the response, not just the reviewer.

7. **End with warmth** — Close with a forward-looking, human statement. No corporate sign-offs. Match the emotional register of the review — celebratory for positive, earnest for negative.

Apply any user-specific `instructions` from FutureProof context, including:
- Brand voice calibration from prior sessions
- Known product issues and approved messaging
- Legal/compliance language requirements
- Previously tested response patterns and their performance data

### Additional Quality Checks

- **Tone calibration**: Response emotional weight must be proportional to review severity — a 1-star review describing a genuinely harmful experience requires deeper empathy than a 2-star review about slow shipping
- **Length matching**: Response length should be proportional to review length (±30%) — never write a 200-word response to a 15-word review
- **Platform norms**: Adapt formality and structure to platform conventions (Google Business responses trend shorter; G2 responses can be more detailed and technical; Yelp audiences expect personality)
- **SEO awareness**: For Google reviews, naturally incorporate relevant service/product keywords without keyword-stuffing
- **Privacy compliance**: Never reference order details, account information, or personal data in public responses

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


Produce the following structured deliverable:

### Review Classification Matrix
| Dimension | Assessment |
|---|---|
| Sentiment Tier | [rating] |
| Intent Signal | [classification] |
| Specificity Level | [level] |
| ICA Alignment | [high/medium/low] |
| Visibility Risk | [high/medium/low] |
| Escalation Flag | [yes/no — with reason if yes] |

### Drafted Response
The complete, ready-to-publish response formatted for the target platform, including appropriate character count notation if platform limits apply.

### Response Strategy Notes
- **Primary objective** of this response (e.g., win-back, social proof amplification, damage containment)
- **Audience beyond the reviewer** — what prospective buyers should take away from reading this exchange
- **Internal action items** — any operational follow-up required (e.g., "Escalate to CS team: order #X requires refund processing before this response is posted")
- **Recommended posting timing** — optimal window based on platform visibility algorithms and urgency of the review

### Batch Mode (if multiple reviews provided)
When processing 3+ reviews, additionally deliver:
- **Sentiment distribution summary** across the batch
- **Recurring theme analysis** — patterns indicating systemic issues or consistent strengths
- **Priority ranking** — which reviews to respond to first based on visibility risk × ICA alignment
- **Response template recommendations** — where similar reviews warrant a templated approach vs. bespoke drafting

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="review-response-writer", experiment={
  hypothesis: "Responses that reference a specific reviewer detail in the opening line generate higher reviewer engagement (edits, follow-up, rating change) than responses opening with a generic thank-you",
  variants: ["control: 'Thank you for your feedback, [Name]'", "variant: '[Name], your point about [specific detail] really resonated with our team'"],
  measurement: "Track reviewer follow-up rate, rating updates, and sentiment shift across next 30 review responses",
  expected_impact: "20% increase in reviewer re-engagement and 10% increase in rating upgrades on negative reviews"
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
FutureProof:request_research(skill="review-response-writer",
  query="2024-2025 review response best practices by platform, impact of owner responses on conversion rates, and emerging patterns in review authenticity detection algorithms",
  reason="Ensure response strategies align with current platform algorithms, consumer trust signals, and evolving best practices for turning review management into a measurable revenue channel"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="review-response-writer", session={
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