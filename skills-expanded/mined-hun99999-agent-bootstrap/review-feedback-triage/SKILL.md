---
name: review-feedback-triage
description: Use only when the user explicitly asks to evaluate or apply concrete code-review feedback.
---

# Review Feedback Triage

## Result

Classify each review item as accepted, rejected, deferred, or needing a material decision; implement accepted items when the request includes changes.

## Route

1. Map each item to the affected file, behavior, requirement, and available evidence.
2. Accept feedback that is correct, in scope, and useful for the current codebase.
3. Reject feedback that conflicts with current evidence, approved architecture, compatibility needs, or YAGNI; state the technical reason.
4. Defer valid items outside the requested scope and identify the appropriate follow-up boundary.
5. Request one concise decision only when ambiguity materially changes correctness, scope, safety, or architecture.
6. Apply accepted changes in dependency order and run the narrow evidence invalidated by those changes.
7. Report the classification, resulting edits, and evidence without performative agreement.

## Stop

Pause before external replies, architecture changes, destructive actions, or scope expansion that the user has not authorized. Return the exact unresolved item and decision needed.
