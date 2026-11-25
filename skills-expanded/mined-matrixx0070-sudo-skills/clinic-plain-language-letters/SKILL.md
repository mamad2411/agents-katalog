---
name: clinic-plain-language-letters
version: 1.0.0
description: Rewrite legal content into clear plain-language client letters while preserving legal accuracy for supervisor sign-off.
author: matrixx0070
tags: [legal-clinic, plain-language, client-communication, readability, accuracy, letters]
capabilities: []
---

## When to use
Use this when a client needs a legal development explained in plain language — a status update, next steps, a deadline, or the gist of a ruling or notice. The goal is a letter a non-lawyer can read and act on, without losing anything legally material.

**Not for:** giving new legal advice or answering "what should I do" independently (Rule 5.5 — that is the supervisor's call), internal analysis (use clinic-memo), or filling official forms (use clinic-form-generation).

## Method
1. Identify the source content and the exact points the client must understand: what happened, what it means, what they do next, by when.
2. Rewrite in plain language — short sentences, everyday words, active voice, no Latin or undefined jargon. Aim for a broadly accessible reading level.
3. Preserve legal accuracy: keep deadlines, conditions, and consequences exact. Simplifying wording must never change legal meaning.
   **Decision point:** if plain phrasing would blur a legal requirement, keep the precise term and add a short definition rather than dropping it — and flag the tension for the supervisor.
4. Remove or generalize any confidential detail that need not appear, and never route client-identifying content through an external or GenAI tool (Rule 1.6). Verify any GenAI-suggested phrasing did not silently alter meaning (ABA Op. 512).
5. Add a line that this is general information about their matter, not a substitute for legal advice, and that they can contact the clinic with questions.
6. Route to the supervising attorney to confirm nothing material was lost before the letter goes to the client.

## Example
> Source: an order granting a continuance to March 12. Plain-language draft: "The judge moved your hearing to March 12, 2026. You do not need to do anything before then. Please keep that date open and contact us if it changes." You send it to the supervisor to confirm accuracy before it reaches the client.

## Pitfalls
- Simplifying wording in a way that quietly changes a deadline or legal condition.
- Dropping a material term because it sounded too technical.
- Letting the letter read as independent legal advice instead of a supervised explanation (Rule 5.5).
- Exposing client-identifying content to an external tool (Rule 1.6).

## Output format
```
TO: <client>   MATTER: <id>   DATE: <date>
WHAT HAPPENED:
WHAT IT MEANS:
WHAT YOU NEED TO DO (and by when):
NOTE: general information about your matter, not a substitute for legal advice.
STATUS: DRAFT — awaiting supervising attorney review
```

## Reference
- ABA Formal Op. 512: verify GenAI rewrites preserve meaning; protect confidentiality.
- Model Rules 1.4 (communication), 1.6 (confidentiality), 5.5 (supervised practice, no independent advice).
- Clinic norm: supervising attorney confirms nothing material was lost before client delivery.
