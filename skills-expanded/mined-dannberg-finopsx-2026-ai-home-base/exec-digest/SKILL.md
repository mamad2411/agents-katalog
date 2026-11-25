---
name: exec-digest
description: Produce a one-paragraph executive summary on a FinOps topic, in house style. Triggers on phrases like "exec digest", "CFO summary", "one-paragraph summary for leadership", "write this up for the exec readout". Lead with dollars, no jargon, action-oriented close.
---

# Executive Digest

When invoked, produce a single tight paragraph suitable for an executive readout, weekly digest, or the top of a longer doc that a busy executive will only skim. Always one paragraph. Always under 100 words. Always in house style.

## Inputs to confirm before starting

- The topic (e.g., "Q3 GCP commitment renewal", "Datadog overage", "savings from rightsizing initiative")
- The relevant numbers (current spend, projected spend, savings, deltas)
- The decision being supported (if any) or the action the practitioner wants the reader to take
- The audience: CFO / CTO / CEO / general exec / FP&A — affects framing

## House rules — non-negotiable

These are what makes a paragraph feel like *ours* and not a generic AI blob. Apply all of them, every time.

1. **Lead with the dollar.** First sentence is always the dollar impact, the dollar trend, or the dollar decision.
2. **No service names** unless the audience is technical. "Our cloud analytics platform" beats "BigQuery" for a CFO.
3. **No FinOps jargon.** No "rightsizing," "commitment portfolio," "rate optimization," or "tagging hygiene." Translate every term to the action it represents.
4. **One number, one comparison.** Don't stack metrics. Pick the one that frames the decision and stick with it.
5. **Action-oriented close.** Last sentence is what's happening next or what the reader needs to do. Never end with a recap.

## Steps

1. Read the inputs and identify the single most important dollar figure.
2. Identify the action the reader needs to take (or the decision they need to be aware of).
3. Draft the paragraph in 4–6 sentences:
   - Sentence 1: dollar impact + headline
   - Sentences 2–4: what's driving it / what's been done / what we know
   - Final sentence: action / decision / what's next
4. Cut. The first draft is always too long. Aim for under 100 words.
5. Read it aloud. If it sounds like a press release, rewrite.

## Length budget

- Target: 60–90 words
- Hard ceiling: 100 words
- If you can't fit it, the topic is too big for a digest — recommend a one-pager instead.

## Output format

```
[paragraph]

---
Word count: N
Audience tested for: [CFO / CTO / general exec]
Action implied: [one line — what the reader is being asked to do or notice]
```

The metadata footer is for the practitioner's eyes, not the digest. They'll strip it before sending.

## Examples of the close

Good action-oriented closes:
- *"We'll have the renewal proposal in your hands by Friday."*
- *"No action needed; flagging in case it comes up in board prep."*
- *"Recommend approving the $40K commitment to lock in the rate before Oct 1."*

Bad closes:
- *"In summary, we should optimize our spend." (recap, no action)*
- *"This represents a meaningful improvement in our cost posture." (no number, no decision)*
- *"Let me know if you have questions." (always assumed, wastes the close)*

## Skeptic check

Before delivering, run yourself through:
- Is the first sentence a dollar?
- Did I use any FinOps or service-specific jargon?
- Is the last sentence an action or decision?
- Is it under 100 words?

If any answer is no, rewrite.
