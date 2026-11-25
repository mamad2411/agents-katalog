---
name: one-person-business-idea
description: Find a profitable one-person business idea at the intersection of what someone knows, what they enjoy, and what the market will pay for — without hiring anyone. Use when someone wants to start a solo business/side hustle, doesn't know what to build a one-person business around, or asks to validate a business idea against "can one person actually run this."
---

# One-Person Business Idea

Source: a 5-prompt "Dan Koe-style one-person business system" carousel from a
social account (@yourgptguide / "Your GPT Guide"), reviewed from an uploaded
photo batch — no GitHub repo to vendor, so this is written up as a skill from
the prompt itself. The carousel's framing ("BREAKING: Claude can now help
you...", "like Dan Koe's $5M solo operation") is marketing hype from an
account that also pitches a separate paid "Art of AI 2.0" prompt bundle in
the same post — the $5M figure is an unverified claim about a third party,
not something this skill asserts as fact. The prompt itself is a reasonable,
well-structured piece of prompt engineering independent of that framing, so
it's kept and adapted.

This is stage 1 of a 5-stage system (idea → offer → content system → sales
system → scaling). Run it first — every later stage assumes a validated
idea exists.

## What this does

Finds the intersection of three things: what the person knows, what they
enjoy, and what the market already pays for — then generates and validates
candidate one-person business models (operable solo, no hires, clear path
to revenue), rather than accepting the first idea that comes to mind.

## How to run it

1. Ask for skills, interests, current income, and lifestyle goals before
   generating anything — don't guess these.
2. Identify the intersection of what they know, what they enjoy, and what
   people demonstrably pay for (not just "could" pay for — look for existing
   evidence: competitors, communities, search demand).
3. Generate 3 distinct one-person business models that scale without
   employees.
4. Validate each candidate: is someone *already* paying for this outcome
   today? Reject or flag models with no evidence of existing demand rather
   than dressing them up.
5. Select the strongest model and write a one-sentence positioning statement
   that names the customer, the outcome, and the mechanism.

## Rules

- The business model must be operable by one person — no team required.
- Every idea needs a clear monetization path within 90 days, not a vague
  "eventually."
- The positioning statement must name customer + outcome + mechanism, not
  just a vibe.
- Flag the weakest ideas honestly — not every idea generated deserves to
  become a business. This is a validation exercise, not a hype exercise.

## Output

Skill Intersection → 3 Business Models → Validation Check → Strongest Model
→ Positioning Statement

## Prompt (copy-paste)

The following is the original prompt as sourced, unedited, for use directly
in Claude or another assistant outside this skill:

```text
<role>Act as a one-person business strategist who applies Dan Koe's philosophy of monetizing a single skill, interest, and personality into a scalable solo operation.</role>

<task>Identify my most profitable one-person business idea based on what I know, what I enjoy, and what the market will pay for — without hiring a single person.</task>

<steps>
1. Ask for my skills, interests, current income, and lifestyle goals before starting
2. Identify the intersection of what I know, what I enjoy, and what people pay for
3. Generate 3 one-person business models that scale without employees
4. Validate each model — is someone already paying for this outcome
5. Select the strongest model and write a one-sentence business positioning statement
</steps>

<rules>
- Business model must be operated by one person — no team required
- Every idea must have a clear monetization path within 90 days
- Positioning statement must name the customer, the outcome, and the mechanism
- Weakest ideas flagged honestly — not every idea deserves a business
</rules>

<output>Skill Intersection → 3 Business Models → Validation Check → Strongest Model → Positioning Statement</output>
```

## Related skills in this repo

- **the-specific-knowledge-excavator** / **the-productize-yourself-blueprint**: cover the same "find and package your own expertise" territory in far more depth — run those first if the person hasn't already identified their specific knowledge; this skill's Step 2 is a faster, lighter version of that same intersection.
- **saas-idea-validator**: a much harder validation pass for software/product ideas specifically — use it instead of (or after) this skill's lighter Step 4 validation if the idea is a software product rather than a service/content business.
- **one-person-offer-architect**: stage 2 — takes the positioning statement this skill outputs and turns it into a sellable offer.
- **product-marketing-context**: once an idea is validated here, capture it there as the durable positioning doc the rest of this repo's marketing/design skills pull from.
